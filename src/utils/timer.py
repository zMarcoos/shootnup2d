import time

class Timer:
  def __init__(self):
    self.timers = []

  def add_timer(self, duration, callback, repeat=False):
    timer = {
      'duration': duration,
      'callback': callback,
      'start': time.time(),
      'repeat': repeat,
      'active': True
    }
    self.timers.append(timer)

  def update_timers(self):
    current_time = time.time()
    for timer in self.timers[:]:
      if timer['active'] and (current_time - timer['start'] < timer['duration']):
        timer['callback']()
        if timer['repeat']:
          timer['start'] = current_time
      else:
        self.timers.remove(timer)

  def clear_timers(self):
    for timer in self.timers:
      timer['active'] = False

  def remove_inactive_timers(self):
    self.timers = [timer for timer in self.timers if timer['active']]
