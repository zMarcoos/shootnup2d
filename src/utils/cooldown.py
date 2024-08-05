import time

class CooldownManager:
  def __init__(self):
    self.cooldowns = {}

  def start_cooldown(self, name, duration):
    self.cooldowns[name] = {
      'end_time': time.time() + duration,
      'duration': duration
    }

  def is_on_cooldown(self, name):
    if name in self.cooldowns:
      if time.time() < self.cooldowns[name]['end_time']:
        return True
      else:
        self.end_cooldown(name)
    return False

  def get_remaining_time(self, name):
    if name in self.cooldowns:
      remaining_time = self.cooldowns[name]['end_time'] - time.time()
      return max(0, remaining_time)
    return 0

  def end_cooldown(self, name):
    if name in self.cooldowns:
      del self.cooldowns[name]

  def clear_all_cooldowns(self):
    self.cooldowns.clear()
