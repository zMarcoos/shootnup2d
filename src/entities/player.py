from OpenGL.GL import *

from entities.ship import Ship
from utils.utility import load_texture


class Player(Ship):
  def __init__(self, x: float, y: float, type: dict) -> None:
    super().__init__(x, y, type)

    self.health = type['health']
    self.double_missile_texture = load_texture(type['double_shoot_texture'])
    self.special_missile_texture = load_texture(type['special_shoot_texture'])

    self.name = ''
    self.is_charging = False
    self.charge_time = 0
    self.damage_cooldown = 5
    self.last_damage_time = -self.damage_cooldown

  def draw(self):
    super().draw()
    self.draw_health_bar()
    
  def active_hability(self, hability_name: str):
    if hability_name == 'health':
      self.health = self.type[hability_name]
    elif hability_name == 'shoot':
      self.texture_missile = self.double_missile_texture
      self.shoot_cooldown = 0.5
  
  def clear_all_habilities(self):
    self.missile_texture = load_texture(self.type['shoot_texture'])
    self.shoot_cooldown = 1

  def is_invulnerable(self, current_time):
    return (current_time - self.last_damage_time) < self.damage_cooldown

  def take_damage(self, amount, current_time):
    if not self.is_invulnerable(current_time):
      self.damage(amount)
      self.last_damage_time = current_time
      return True
    return False
