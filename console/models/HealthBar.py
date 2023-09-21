class HealthBar:
    def __init__(self, max_health, curr_health, bar_length=30):
        self.max_health = max_health
        self.curr_health = curr_health
        self.bar_length = bar_length

    def __str__(self):
        progress = self.curr_health / self.max_health
        filled_length = int(self.bar_length * progress)
        bar = '█' * filled_length + '-' * (self.bar_length - filled_length)
        return f'[{bar}] {self.curr_health}/{self.max_health} HP'
