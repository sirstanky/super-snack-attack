import constants as c


class Timer:
    def __init__(self,
                 max_value: float):
        self.max_value = max_value
        self.value = 0.0
        self._expired = False
        self.ticks_down = True
        self.paused = False

    @property
    def ready(self):
        if self.value > 0.0:
            return False
        else:
            return True

    @property
    def expired(self):
        if self._expired:
            self._expired = False
            return True
        return False

    def start(self):
        if self.value == 0:
            self.value = self.max_value

    def restart(self):
        if self.value != 0:
            self.value = self.max_value

    def pause(self):
        self.paused = not self.paused

    def update(self):
        if self.value > 0 and not self.paused:
            self.value -= 1 / c.FPS
        if self.value < 0:
            self.value = 0
            self._expired = True
