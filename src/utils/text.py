from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Text:
  def __init__(self, text, x, y, window_width, window_height, callback = None) -> None:
    self.text = text
    self.x = x
    self.y = y
    self.screen_x = self.screen_y = 0
    self.window_width = window_width
    self.window_height = window_height
    self.callback = callback
    self.calculate_dimensions()

  def draw(self):
    current_text = self.text() if callable(self.text) else self.text

    glColor3f(1, 1, 1)
    glWindowPos2i(self.screen_x, self.screen_y)
    for char in current_text:
      glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char)) # type: ignore
  
  def calculate_dimensions(self):
    current_text = self.text() if callable(self.text) else self.text

    self.screen_x = int((self.x + 1) * self.window_width / 2)
    self.screen_y = int((1 - self.y) * self.window_height / 2)
    self.width = sum([glutBitmapWidth(GLUT_BITMAP_TIMES_ROMAN_24, ord(char)) for char in current_text]) # type: ignore
    self.height = 24 

  def check_click(self, mouse_x, mouse_y):
    if self.screen_x <= mouse_x <= self.screen_x + self.width and self.screen_y <= mouse_y <= self.screen_y + self.height:
      if self.callback:
        self.callback()
        return True
    return False
