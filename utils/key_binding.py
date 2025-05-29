# key_binding.py
import time

# key_binding.py
class KeyBinding:
    def __init__(self, key, interval_sec, condition_type=None, threshold=None):
        self.key = key
        self.condition_type = condition_type  # None, 'lt', 'gt'
        self.threshold = threshold
        self.interval = interval_sec
        self.last_triggered = 0.0

    def try_trigger(self, current_hp, arduino):
        now = time.time()
        condition_met = True

        if self.condition_type == 'lt':
            condition_met = current_hp <= self.threshold
        elif self.condition_type == 'gt':
            condition_met = current_hp >= self.threshold

        if condition_met and (now - self.last_triggered) >= self.interval:
            arduino.send_key(self.key)
            self.last_triggered = now

class KeyManager:
    def __init__(self, arduino):
        self.bindings = []
        self.arduino = arduino

    def add_key(self, key, minutes, seconds, condition_type=None, threshold=None):
        interval_sec = minutes * 60 + seconds
        binding = KeyBinding(key, interval_sec, condition_type, threshold)
        self.bindings.append(binding)

    def update(self, current_hp):
        for binding in self.bindings:
            binding.try_trigger(current_hp, self.arduino)

    def get_keys(self):
        return self.bindings

    def remove_binding(self, binding):
        self.bindings = [b for b in self.bindings if b is not binding]
