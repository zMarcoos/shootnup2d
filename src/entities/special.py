from OpenGL.GL import *
import glm

from entities.entity import Entity
from utils.utility import load_texture_with_sprites
from utils.constants import SHIPS

class Special(Entity):
  def __init__(self, x: int, y: int) -> None:
    super().__init__(x, y)

    self.textures = load_texture_with_sprites(SHIPS['player']['special_shoot_texture'], SHIPS['player']['special_sprites_size'])
    self.current_texture_index = 0
    self.texture = self.textures[self.current_texture_index]

    self.direction_velocity = 0.2
    self.damage = 1
    self.animation_timer = 0
    self.animation_interval = 0.1
    self.active = True
    self.scale_increment = 0.05
    self.collision_scale_factor = 0.05

  def draw(self):
    if not self.active: return

    scale_factor = 1.0 + self.collision_scale_factor
    glPushMatrix()
    glScalef(scale_factor, scale_factor, 1)
    super().draw()
    glPopMatrix()

  def update_sprite(self, delta_time):
    self.animation_timer += delta_time
    if self.animation_timer >= self.animation_interval:
      self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)
      self.texture = self.textures[self.current_texture_index]
      self.animation_timer = 0
      self.collision_scale_factor = 0.05 + 0.05 * self.current_texture_index

      if self.current_texture_index == 0:
        self.active = False

  def distance(self, other):
    base_distance = glm.distance(self.position, other.position)
    return base_distance - self.collision_scale_factor

  def recalculate_matrix(self):
    right = glm.normalize(glm.cross(self.direction, glm.vec3(0, 0, 1)))
    up = glm.normalize(glm.cross(right, self.direction))
    self.modelMatrix[0] = glm.vec4(right, 0)
    self.modelMatrix[1] = glm.vec4(self.direction, 0)
    self.modelMatrix[2] = glm.vec4(up, 0)
    self.modelMatrix[3] = glm.vec4(self.position, 1)
