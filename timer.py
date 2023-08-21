from math import inf

ball_stored_speed_increase = 'ball_stored_speed_increase'
ball_temporary_speed_increase = 'ball_temporary_speed_increase'
bat_swing_charge = 'bat_swing_charge'
bat_swing_cooldown = 'bat_swing_cooldown'


def get_timer(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return None
    return wrapper


class Timer:

    def __init__(self, name: str):

        tick_speed = 0.0
        value = 0.0
        value_max = inf
        ticks_down = True

        # This is a garbage way of making a templet. Fix this
        if ball_stored_speed_increase == name:
            tick_speed = 0.0025
            value_max = 5.0
            ticks_down = False

        elif ball_temporary_speed_increase == name:
            tick_speed = 0.05

        elif bat_swing_charge == name:
            tick_speed = 0.05
            value_max = 5.0
            ticks_down = False

        elif bat_swing_cooldown == name:
            tick_speed = 0.1
            value_max = 5.0

        self.tick_speed = tick_speed
        self.value = value
        self.value_max = value_max
        self.ticks_down = ticks_down

    def tick(self):

        def tick_down():
            if self.value > 0.0:
                self.value -= self.tick_speed
            if self.value < 0.0:
                self.value = 0.0

        def tick_up():
            if self.value < self.value_max:
                self.value += self.tick_speed
            if self.value > self.value_max:
                self.value = self.value_max

        tick_down() if self.ticks_down else tick_up()

    def reset(self):
        self.value = 0.0

    def get_percent_charged(self):
        if self.value_max is not inf:
            return self.value / self.value_max

    def get_max(self):
        return self.value_max

    def set_max(self):
        if self.value_max is not None:
            self.value = self.value_max


class TimerManager:

    def __init__(self):
        self.timers: dict[str, Timer] = {}

    def add_timer(self, name: str):
        self.timers[name] = Timer(name)

    # TODO make this a decorator

    @get_timer
    def get_time(self, name: str):
        return self.timers[name].value

    @get_timer
    def set_time(self, name: str, time: float):
        self.timers[name].value = time

    @get_timer
    def get_percent_charged(self, name: str):
        return self.timers[name].value / self.timers[name].value_max

    @get_timer
    def get_max(self, name: str):
        return self.timers[name].value_max

    @get_timer
    def set_max(self, name: str):
        self.timers[name].set_max()

    @get_timer
    def adjust_time(self, name: str, value: float):
        self.timers[name].value += value

    @get_timer
    def tick(self, name: str):
        self.timers[name].tick()

    @get_timer
    def reset(self, name: str):
        self.timers[name].reset()
