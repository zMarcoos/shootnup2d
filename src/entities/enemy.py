import glm
import math

from entities.ship import Ship

class Enemy(Ship):
  def __init__(self, x: float, y: float, type: dict) -> None:
    super().__init__(x, y, type)

    self.shoot_cooldown = 5.0
  
  def follow(self, player: Ship):
    direction = glm.normalize(player.position - self.position)
    target_angle = math.atan2(direction.y, direction.x)
    current_angle = math.atan2(self.direction.y, self.direction.x)
    
    angle_difference = self.calculate_angle_difference(target_angle, current_angle)
    self.update_turning_direction(angle_difference)

    self.front = True
  
  def calculate_angle_difference(self, target: float, current: float):
    return (target - current + math.pi) % (2 * math.pi) - math.pi

  def update_turning_direction(self, angle_difference: float, precision: float = 1e-10):
    if angle_difference > precision:
      self.left = True
      self.right = False
    elif angle_difference < -precision:
      self.left = False
      self.right = True
    else:
      self.left = False
      self.right = False