from OpenGL.GL import *

from utils.utility import load_texture_with_sprites
from utils.constants import ITEMS

from entities.entity import Entity

class Item(Entity):

  STATE = {
    0: '',
    1: 'health',
    2: 'shoot'
  }

  def __init__(self, x: int, y: int) -> None:
    super().__init__(x, y)

    self.direction_velocity = 0.03

    self.name = self.STATE[0]
    self.sprites = load_texture_with_sprites(ITEMS['habilities']['texture'], ITEMS['habilities']['sprites_size'])
    self.current_sprite_index = 0
    self.texture = self.sprites[self.current_sprite_index]

    self.animation_timer = 0
    self.animation_interval = 1000 / 12

  def is_out_of_bounds(self, world_width: int, world_height: int):
    return (self.position.x > world_width / 2 or self.position.x < -world_width / 2 or self.position.y > world_height / 2 or self.position.y < -world_height / 2)
  
  def move(self):
    self.position += (self.direction * self.direction_velocity) * -1

    self.recalculate_matrix()

  def update_sprite(self, delta_time: float):
    self.animation_timer += delta_time
    if self.animation_timer >= self.animation_interval:
      self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)
      self.texture = self.sprites[self.current_sprite_index]
      self.animation_timer = 0

    self.name = self.STATE[self.current_sprite_index]

  def draw(self):
    glPushMatrix()
    glTranslatef(self.position.x, self.position.y, 0)
    glScalef(0.7, 0.7, 1)
    glBindTexture(GL_TEXTURE_2D, self.texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(-1, -1)
    glTexCoord2f(1, 0)
    glVertex2f(1, -1)
    glTexCoord2f(1, 1)
    glVertex2f(1, 1)
    glTexCoord2f(0, 1)
    glVertex2f(-1, 1)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)
    glPopMatrix() 