from OpenGL.GL import *
import glm

from entities.entity import Entity

class Missile(Entity):
  def __init__(self, x: int, y: int, texture: Entity) -> None:
    super().__init__(x, y)

    self.owner = None
    self.texture = texture
    self.direction_velocity = 0.2

    self.damage = 1

  def move(self):
    self.position += self.direction * self.direction_velocity
    self.recalculate_matrix()
  
  def is_out_of_bounds(self, world_width: int, world_height: int):
    return (self.position.x > world_width / 2 or self.position.x < -world_width / 2 or self.position.y > world_height / 2 or self.position.y < -world_height / 2)

  def recalculate_matrix(self):
    right = glm.normalize(glm.cross(self.direction, glm.vec3(0, 0, 1)))
    up = glm.normalize(glm.cross(right, self.direction))

    self.modelMatrix[0] = glm.vec4(right, 0)
    self.modelMatrix[1] = glm.vec4(self.direction, 0)
    self.modelMatrix[2] = glm.vec4(up, 0)
    self.modelMatrix[3] = glm.vec4(self.position, 1)