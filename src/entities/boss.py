from OpenGL.GL import *

import random
import time

from entities.ship import Ship
from entities.enemy import Enemy
from utils.constants import SHIPS

class Boss(Ship):
  def __init__(self, x: int, y: int, type: dict) -> None:
    super().__init__(x, y, type)
    self.last_shot_time = 0
    self.shoot_cooldown = 3.0

  def draw(self):
    super().draw()
    self.draw_health_bar()

  def shoot(self):
    current_time = time.time()
    if current_time - self.last_shot_time >= self.shoot_cooldown:
      x, y = self.position.x, self.position.y
      enemy = Enemy(x, y, random.choice(SHIPS['enemy']))
      self.last_shot_time = current_time

      return enemy

  def move(self, world_width: float):
    velocity = self.direction_velocity if self.right else -self.direction_velocity
    self.position.x += velocity

    if self.position.x > world_width / 2:
      self.position.x = world_width / 2
      self.right = False
    elif self.position.x < -world_width / 2:
      self.position.x = -world_width / 2
      self.right = True

    self.recalculate_matrix()