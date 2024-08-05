import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import glm
import time
import random

from utils.constants import *

from utils.text import Text
from entities.player import Player
from entities.enemy import Enemy
from entities.boss import Boss
from entities.special import Special
from items.item import Item

from effects.smoke_effect import SmokeEffect
from utils.utility import load_texture_with_sprites

from utils.timer import Timer


def load_high_scores():
    try:
        with open("./resources/settings/high_scores.txt", "r") as file:
            scores = {}

            for line in file.readlines():
                player_name, score = line.strip().split(': ')
                scores[player_name] = int(score)

            return scores
    except FileNotFoundError:
        return {}


def save_high_scores(scores):
    with open("./resources/settings/high_scores.txt", "w") as file:
        for player_name, score in scores.items():
            file.write(f"{player_name}: {score}\n")


def update_high_score(scores, player_name, new_score):
    if player_name in scores:
        if new_score > scores[player_name]:
            scores[player_name] = new_score
    else:
        scores[player_name] = new_score

    save_high_scores(scores)


class Game:
    def __init__(self) -> None:
        self.missiles = None
        self.smoke_effects = None
        self.special = None
        self.powers = None
        self.state_map_resources = None
        self.player = None
        self.enemies_needed_to_spawn = None
        self.last_frame_time = None
        self.last_enemy_spawn_time = None
        self.enemy_spawn_interval = None
        self.boss = None
        self.enemies = None
        self.wave_length = None
        self.level = None
        self.timer_manager = None

        pygame.init()
        pygame.mixer.init()

        self.background_sound = pygame.mixer.Sound(SOUNDS['background'])

        self.state = 'START_SCREEN'
        self.fps = 60
        self.world_height = self.world_width = 20
        self.window_height = self.window_width = 700
        self.stars = []
        self.high_scores = load_high_scores()

    def build(self):
        self.timer_manager = Timer()
        self.level = 0
        self.wave_length = 5
        self.player = self.boss = None
        self.enemies = []
        self.enemy_spawn_interval = 5
        self.last_enemy_spawn_time = self.last_frame_time = time.time()
        self.enemies_needed_to_spawn = 5
        self.player = Player(0, 0, SHIPS['player'])
        self.state_map_resources = {
            'START_SCREEN': {
                'methods': [self.build],
                'texts': [
                    Text("Novo Jogo", -0.1, 0, self.window_width, self.window_height,
                         callback=lambda: self.set_state('PLAYING')),
                    Text("Ajuda", -0.1, 0.3, self.window_width, self.window_height,
                         callback=lambda: self.set_state('HELP_SCREEN')),
                    Text("Recordes", -0.1, -0.3, self.window_width, self.window_height,
                         callback=lambda: self.set_state('RECORDS_SCREEN')),
                ],
            },
            'HELP_SCREEN': {
                'methods': [],
                'texts': [
                    Text("Jogo criado por:", -0.1, 0.3, self.window_width, self.window_height),
                    Text("Marcos Grégory", -0.2, 0, self.window_width, self.window_height),
                    Text("Isis Lavor", -0.2, -0.1, self.window_width, self.window_height),
                    Text("Voltar", -0.1, -0.3, self.window_width, self.window_height,
                         callback=lambda: self.set_state('START_SCREEN'))
                ],
            },
            'PLAYING': {
                'methods': [self.draw_game],
                'texts': [
                    Text(lambda: f'Level {self.level}', -0.9, 0.9, self.window_width, self.window_height),
                    Text(
                        lambda: f'Vida: {self.player.health} ({max(0, self.player.damage_cooldown - (time.time() - self.player.last_damage_time)):.1f}s)' if self.player.is_invulnerable(
                            time.time()) else f'Vida: {self.player.health}', -0.9, 0.8, self.window_width,
                        self.window_height)
                ],
            },
            'ENTER_NAME': {
                'methods': [],
                'texts': [
                    Text("Digite seu nome:", -0.1, 0.3, self.window_width, self.window_height),
                    Text(lambda: self.player.name, -0.1, -0.3, self.window_width, self.window_height)
                ],
            },
            'RECORDS_SCREEN': {
                'methods': [],
                'texts': [
                    Text("Voltar", -0.1, -0.3, self.window_width, self.window_height,
                         callback=lambda: self.set_state('START_SCREEN'))
                ]
            }
        }

        self.special = None
        self.powers = []
        self.smoke_effects = []
        self.missiles = []

    def timer(self, v):
        self.update_game_state()
        glutTimerFunc(int(1000 / self.fps), self.timer, 0)
        glutPostRedisplay()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.call_methods_by_state()
        self.draw_informations_by_state()

        glutSwapBuffers()

    def update_game_state(self):
        if self.state == 'PLAYING':
            current_time = time.time()
            delta_time = current_time - self.last_frame_time
            self.last_frame_time = current_time

            self.handle_enemy_spawning(current_time)
            self.update_entities(current_time, delta_time)

    def handle_enemy_spawning(self, current_time):
        if not self.boss:
            if self.enemies_needed_to_spawn > 0:
                if (current_time - self.last_enemy_spawn_time >= self.enemy_spawn_interval):
                    self.spawn_enemy()
                    self.last_enemy_spawn_time = current_time
            elif self.enemies_needed_to_spawn == 0 and len(self.enemies) == 0:
                self.advance_level()
                self.check_for_boss_spawn()

    def spawn_enemy(self):
        x, y = self.generate_random_world_position()
        enemy = Enemy(x, y, random.choice(SHIPS['enemy']))
        self.enemies.append(enemy)
        self.enemies_needed_to_spawn -= 1

    def check_for_boss_spawn(self):
        if self.level % 2 == 0 and self.level != 0:
            self.boss = Boss(0, 8, SHIPS['boss'])

    def generate_item(self):
        self.powers.append(Item(0, 8))

    def generate_random_world_position(self):
        positions = {
            0: ("x", self.world_height / 2 + 1),  # Superior
            1: ("x", -self.world_height / 2 - 1),  # Inferior
            2: ("y", -self.world_width / 2 - 1),  # Esquerda
            3: ("y", self.world_width / 2 + 1)  # Direita
        }

        edge = np.random.randint(4)
        axis, offset = positions[edge]

        if axis == "x":
            x = np.random.uniform(-self.world_width / 2, self.world_width / 2)
            y = offset
        else:
            y = np.random.uniform(-self.world_height / 2, self.world_height / 2)
            x = offset

        return x, y

    def advance_level(self):
        self.timer_manager.add_timer(3,
                                     lambda: Text('Level up!', -0.1, 0, self.window_width, self.window_height).draw())
        self.player.clear_all_habilities()

        self.level += 1
        self.wave_length += 2
        self.enemies_needed_to_spawn = self.wave_length
        self.enemy_spawn_interval = max(2, self.enemy_spawn_interval * np.log(self.level + 1) / np.log(self.level + 2))

        if self.level % 2 == 0 and self.level != 0:
            self.generate_item()

    def update_entities(self, current_time, delta_time):
        self.player.move(self.world_width, self.world_height)
        self.player.update_sprite(delta_time * 1000)

        if self.special:
            self.special.position = self.player.position + self.player.direction * 2.5
            self.special.direction = self.player.direction
            self.special.recalculate_matrix()
            self.special.update_sprite(delta_time)

            if not self.special.active:
                self.special = None

        for power in self.powers[:]:
            power.move()
            power.update_sprite(delta_time * 1000)

            if power.is_out_of_bounds(self.world_width, self.world_height):
                self.powers.remove(power)

            if self.player.distance(power) < 1:
                self.player.active_hability(power.name)
                self.powers.remove(power)

        for effect in self.smoke_effects:
            effect.update_sprite(delta_time * 1000)

            if not effect.active:
                self.smoke_effects.remove(effect)

        if self.boss:
            self.boss.move(self.world_width)
            self.boss.update_sprite(delta_time * 1000)

            if self.player.distance(self.boss) < 1:
                if self.player.take_damage(1, current_time):
                    if self.player.is_dead():
                        self.set_state('ENTER_NAME')

            self.shoot_missile(self.boss)

        for enemy in self.enemies[:]:
            enemy.follow(self.player)
            enemy.move(self.world_width, self.world_height)
            enemy.update_sprite(delta_time * 1000)
            self.shoot_missile(enemy)

            if enemy.distance(self.player) < 1:
                if self.player.take_damage(1, current_time):
                    self.smoke_effects.append(SmokeEffect(enemy.position))
                    self.enemies.remove(enemy)

                    if self.player.is_dead():
                        self.set_state('ENTER_NAME')

                    break

        self.update_missiles()

    def update_missiles(self):
        if self.special:
            if self.boss:
                if self.special.distance(self.boss) < 1:
                    self.boss.damage(3)
                    self.special.active = False

                    if self.boss.is_dead():
                        self.boss = None
                        self.advance_level()

                    return

            for enemy in self.enemies:
                if self.special.distance(enemy) < 1:
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)

                    self.smoke_effects.append(SmokeEffect(enemy.position))
                    continue

        for missile in self.missiles[:]:
            missile.move()

            if missile.is_out_of_bounds(self.world_width, self.world_height):
                self.missiles.remove(missile)
                continue

            entity = missile.owner

            if entity == self.player:
                if self.boss:
                    if missile.distance(self.boss) < 1:
                        self.missiles.remove(missile)
                        self.boss.damage(1)

                        if self.boss.is_dead():
                            self.smoke_effects.append(SmokeEffect(self.boss.position))
                            self.boss = None

                            self.advance_level()

                        break

                for enemy in self.enemies[:]:
                    if missile.distance(enemy) < 1:
                        if enemy.health >= 1:
                            enemy.health -= 1

                        self.missiles.remove(missile)

                        if enemy.health == 0:
                            self.smoke_effects.append(SmokeEffect(enemy.position))
                            self.enemies.remove(enemy)

                        break
            elif entity == self.boss:
                pass
            else:
                if missile.distance(self.player) < 1:
                    self.missiles.remove(missile)

                    if self.player.take_damage(1, time.time()):
                        if self.player.is_dead():
                            self.set_state('ENTER_NAME')

    def call_methods_by_state(self):
        for method in self.state_map_resources[self.state]['methods']:
            method()

    def draw_informations_by_state(self):
        texts = self.state_map_resources[self.state]['texts']
        for text in texts:
            text.draw()

    def draw_game(self):
        self.clear_screen()
        self.draw_stars()
        self.draw_entities()
        self.sound_effects()
        self.timer_manager.update_timers()

    def sound_effects(self):
        if not pygame.mixer.get_busy():
            self.background_sound.play(-1)

    def clear_screen(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.world_width / 2, self.world_width / 2, -self.world_height / 2, self.world_height / 2, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_entities(self):
        self.draw_entity(self.player)

        for enemy in self.enemies:
            self.draw_entity(enemy)

        if self.boss:
            self.draw_entity(self.boss)

        for missile in self.missiles:
            self.draw_entity(missile)

        if self.special:
            self.draw_entity(self.special)

        for power in self.powers:
            power.draw()

        for effect in self.smoke_effects:
            effect.draw()

    def draw_entity(self, entity):
        glPushMatrix()
        glMultMatrixf(np.asarray(glm.transpose(entity.modelMatrix)))
        entity.draw()
        glPopMatrix()

    def shoot_missile(self, entity):
        shoot = entity.shoot()
        if not shoot:
            return

        if entity == self.boss:
            self.enemies.append(shoot)
        else:
            self.missiles.append(shoot)

    def draw_stars(self):
        if len(self.stars) == 0:
            self.stars = [(np.random.uniform(-self.world_width / 2, self.world_width / 2),
                           np.random.uniform(-self.world_height / 2, self.world_height / 2)) for _ in range(100)]

        glPointSize(2)
        glColor3f(1, 1, 1)
        glBegin(GL_POINTS)
        for x, y in self.stars:
            glVertex2f(x, y)
        glEnd()

    def set_state(self, state):
        self.state = state

        if state == 'RECORDS_SCREEN':
            if len(self.high_scores) == 0:
                self.state_map_resources[state]['texts'].extend(
                    [Text("Nenhum recorde", -0.1, 0, self.window_width, self.window_height)]
                )
            else:
                self.state_map_resources[state]['texts'].extend(
                    [Text(f"{player_name}: {score}", -0.1, 0.2 - i * 0.1, self.window_width, self.window_height) for i, (player_name, score) in enumerate(self.high_scores.items())]
                )

    def mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            texts = self.state_map_resources[self.state]['texts']

            for text in texts:
                if text.check_click(x, self.window_height - y):
                    break

    def keyboard(self, key, x, y):
        if self.state == 'ENTER_NAME':
            if key == b'\x08':  # Backspace
                self.player.name = self.player.name[:-1]
            elif key == b'\r':  # Enter
                update_high_score(self.high_scores, self.player.name, self.level)
                self.set_state('START_SCREEN')
            elif len(self.player.name) < 10 and key.isalnum():
                self.player.name += key.decode('utf-8')

            glutPostRedisplay()
            return

        if key == b'w':
            self.player.front = True
        elif key == b's':
            self.player.back = True
        elif key == b'a':
            self.player.left = True
        elif key == b'd':
            self.player.right = True
        elif key == b'q':
            quit()
        elif key == b' ':
            self.shoot_missile(self.player)
        elif key == b'c':
            if not self.player.is_charging:
                self.player.is_charging = True
                self.player.charge_time = time.time()

                self.player.sprites = load_texture_with_sprites(SHIPS['player_special']['texture'],
                                                                SHIPS['player_special']['sprites_size'])

    def keyboard_up(self, key, x, y):
        if key == b'w':
            self.player.front = False
        elif key == b's':
            self.player.back = False
        elif key == b'a':
            self.player.left = False
        elif key == b'd':
            self.player.right = False
        elif key == b'c':
            if self.player.is_charging:
                self.player.is_charging = False

                self.player.sprites = load_texture_with_sprites(SHIPS['player']['texture'],
                                                                SHIPS['player']['sprites_size'])

                charge_time = time.time() - self.player.charge_time
                self.player.charge_time = 0

                if charge_time < 1.5:
                    print('Poder não carregado!')
                    return

                if not self.special:
                    self.special = Special(self.player.position.x, self.player.position.y)
                    self.special.direction = self.player.direction
                    self.special.recalculate_matrix()

    def reshape(self, width, height):
        self.window_width = width
        self.window_height = height
        self.world_width = self.world_height * width / height
        self.world_height = self.world_width * height / width

        self.stars = []

        glViewport(0, 0, width, height)

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB | GLUT_RGBA)
        glutInitWindowSize(self.window_height, self.window_height)
        glutInitWindowPosition(int((glutGet(GLUT_SCREEN_WIDTH) - self.window_width) / 2),
                               int((glutGet(GLUT_SCREEN_HEIGHT) - self.window_height) / 2))
        glutCreateWindow('Space Invaders')

        glClearColor(0, 0, 0, 1)
        glLineWidth(3)
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.build()

        glutTimerFunc(int(1000 / self.fps), self.timer, 0)
        glutKeyboardFunc(self.keyboard)
        glutKeyboardUpFunc(self.keyboard_up)
        glutMouseFunc(self.mouse)
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.draw)
        glutMainLoop()
