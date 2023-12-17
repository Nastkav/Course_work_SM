import element as e


class Pause(e.Element):
    def __init__(self, name, duration, start_time):
        super().__init__()
        self.start_time = 0
        self.count_pause = 0

    def in_act(self):
        self.count_pause += 1
        super().in_act()
