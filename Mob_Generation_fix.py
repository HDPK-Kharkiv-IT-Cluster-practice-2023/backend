import random


class Mob:
    def __init__(self):
        mob_names = ["Zombie", "Skeleton", "Spider", "Slime", "Goblin"]
        self.name = random.choice(mob_names)
        self.health = random.randint(20, 70)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(2, 15)
        self.luck = random.randint(1, 10)
        self.alive = True
        self.critical_attack = self.attack * 2 if self.luck > 5 else self.attack

    def take_damage(self, damage):
        actual_damage = max(damage - self.armor, 0)
        self.health -= actual_damage
        if self.health < 0:
            self.health = 0

    def __str__(self):
        return f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, " \
               f"атака {self.attack}, удача {self.luck}"


mob1 = Mob()
print(mob1)
