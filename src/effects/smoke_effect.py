from OpenGL.GL import *

from utils.utility import load_texture_with_sprites
from utils.constants import EFFECTS

class SmokeEffect:
  def __init__(self, position):
    self.position = position
    self.textures = load_texture_with_sprites(EFFECTS['smoke']['texture'], EFFECTS['smoke']['sprites_size'])
    self.current_sprite_index = 0
    self.texture = self.textures[self.current_sprite_index]

    self.animation_timer = 0
    self.animation_interval = 1000 / 12
    self.active = True

  def update_sprite(self, delta_time: float):
    self.animation_timer += delta_time
    if self.animation_timer >= self.animation_interval:
      self.current_sprite_index = (self.current_sprite_index + 1) % len(self.textures)
      self.texture = self.textures[self.current_sprite_index]
      self.animation_timer = 0
      
      if self.current_sprite_index == 0:
        self.active = False

  def draw(self):
    if self.active:
      glPushMatrix()  # Save the current matrix
      glTranslatef(self.position[0], self.position[1], 0)  # Move to the correct position
      glBindTexture(GL_TEXTURE_2D, self.texture)
      glBegin(GL_QUADS)
      glTexCoord2f(0, 0); glVertex2f(-1, -1)  # Bottom Left
      glTexCoord2f(1, 0); glVertex2f(1, -1)   # Bottom Right
      glTexCoord2f(1, 1); glVertex2f(1, 1)    # Top Right
      glTexCoord2f(0, 1); glVertex2f(-1, 1)   # Top Left
      glEnd()
      glBindTexture(GL_TEXTURE_2D, 0)
      glPopMatrix()  # Restore the original matrix