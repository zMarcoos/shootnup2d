from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glm
import time

from entities.entity import Entity
from entities.missile import Missile
from utils.utility import load_texture, load_texture_with_sprites

class Ship(Entity):
  def __init__(self, x: int, y: int, type: dict) -> None:
    super().__init__(x, y)

    self.type = type
    self.health = type['health']
    self.direction_velocity = self.angular_velocity = type['velocity']

    self.sprites = load_texture_with_sprites(type['texture'], type['sprites_size'])
    self.current_sprite_index = 0
    self.texture = self.sprites[self.current_sprite_index]

    self.missile_texture = load_texture(type['shoot_texture'])
    self.animation_timer = 0
    self.animation_interval = 1000 / 12

    self.shoot_cooldown = 1.0
    self.last_shot_time = time.time()

    self.health_bar_width = 0.6
    self.health_bar_height = 0.1
    self.health_bar_offset_y = -1.5
  
  def move(self, world_width: float, world_height: float):
    if self.front or self.back:
      self.position += (self.direction * self.direction_velocity) * (1 if self.front else -1)

    if self.left or self.right:
      rotation_angle = self.angular_velocity if self.left else -self.angular_velocity
      rotation = glm.rotate(glm.mat4(1.0), rotation_angle, glm.vec3(0, 0, 1))
      self.direction = glm.vec3(rotation * glm.vec4(self.direction, 0))
      self.lateral = glm.vec3(rotation * glm.vec4(self.lateral, 0))

    self.position.x = (self.position.x + world_width / 2) % world_width - world_width / 2
    self.position.y = (self.position.y + world_height / 2) % world_height - world_height / 2

    self.recalculate_matrix()

  def can_shoot(self, current_time):
    return current_time - self.last_shot_time >= self.shoot_cooldown

  def shoot(self):
    current_time = time.time()

    if self.can_shoot(current_time):
      missile = Missile(self.position.x, self.position.y, self.missile_texture)
      missile.owner = self
      missile.direction = glm.vec3(self.direction)
      missile.texture = self.missile_texture

      self.last_shot_time = current_time

      return missile

  def update_sprite(self, delta_time: float):
    self.animation_timer += delta_time
    if self.animation_timer >= self.animation_interval:
      self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)
      self.texture = self.sprites[self.current_sprite_index]
      self.animation_timer = 0
  
  def is_dead(self):
    return self.health <= 0

  def damage(self, amount: int):
    self.health -= amount

  def draw_health_bar(self):
    health_percentage = self.health / self.type['health']

    bar_start_x = -self.health_bar_width / 2
    bar_end_x = bar_start_x + self.health_bar_width * health_percentage
    bar_top_y = self.health_bar_offset_y
    bar_bottom_y = bar_top_y - self.health_bar_height

    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(bar_start_x, bar_top_y)
    glVertex2f(bar_start_x + self.health_bar_width, bar_top_y)
    glVertex2f(bar_start_x + self.health_bar_width, bar_bottom_y)
    glVertex2f(bar_start_x, bar_bottom_y)
    glEnd()

    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex2f(bar_start_x, bar_top_y)
    glVertex2f(bar_end_x, bar_top_y)
    glVertex2f(bar_end_x, bar_bottom_y)
    glVertex2f(bar_start_x, bar_bottom_y)
    glEnd()