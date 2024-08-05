from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glm

class Entity:
  def __init__(self, x: int, y: int) -> None:
    self.position = glm.vec3(x, y, 0)
    self.direction = glm.vec3(0,1,0)
    self.lateral = glm.vec3(1,0,0)
    self.modelMatrix = glm.mat4(1)
    self.direction_velocity = self.angular_velocity = 0.1 
    self.front = self.back = self.left = self.right = False
    self.texture = None

  def distance(self, other: 'Entity'):
    return glm.distance(self.position, other.position)

  def draw(self):
    glBindTexture(GL_TEXTURE_2D, self.texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(-1,-1)
    glTexCoord2f(1, 0)
    glVertex2f( 1,-1)
    glTexCoord2f(1, 1)
    glVertex2f( 1, 1)
    glTexCoord2f(0, 1)
    glVertex2f(-1, 1)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

  def recalculate_matrix(self):
    self.modelMatrix[0] = glm.vec4(self.lateral, 0)
    self.modelMatrix[1] = glm.vec4(self.direction, 0)
    self.modelMatrix[2] = glm.vec4(0, 0, 1, 0)
    self.modelMatrix[3] = glm.vec4(self.position, 1)
