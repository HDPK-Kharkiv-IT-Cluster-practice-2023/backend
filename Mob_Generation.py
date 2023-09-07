import random

class Mob:
    def __init__(self, name):
        self.name = name
        self.health = random.randint(20, 70)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(2, 15)
        self.luck = random.randint(1, 5)
        self.critical_attack = self.attack * 2 if self.luck > 5 else self.attack

    def __str__(self):
        return f"{self.name}: критическая атака {self.critical_attack}, здоровье {self.health}, броня {self.armor}, атака {self.attack}, удача {self.luck}"

def generate_mobs(num_mobs):
    mob_list = []
    mob_names = ["Zombie", "Skeleton", "Spider", "Slime", "Goblin"]
    for i in range(num_mobs):
        name = random.choice(mob_names)
        mob_list.append(Mob(name))
    return mob_list

mobs = generate_mobs(10)
for mob in mobs:
    print(mob)
