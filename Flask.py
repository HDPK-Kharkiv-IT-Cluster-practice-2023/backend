from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Разрешить доступ только с этого источника

class Mob:
    def __init__(self, name):
        self.name = name
        self.health = random.randint(20, 70)
        self.armor = random.randint(1, 10)
        self.attack = random.randint(2, 15)
        self.luck = random.randint(1, 5)
        self.critical_attack = self.attack * 2 if self.luck > 5 else self.attack

    def to_dict(self):
        return {
            "name": self.name,
            "critical_attack": self.critical_attack,
            "health": self.health,
            "armor": self.armor,
            "attack": self.attack,
            "luck": self.luck
        }

def generate_mobs(num_mobs):
    mob_list = []
    mob_names = ["Zombie", "Skeleton", "Spider", "Slime", "Goblin"]
    for i in range(num_mobs):
        name = random.choice(mob_names)
        mob_list.append(Mob(name))
    return mob_list

@app.route('/')
def get_mobs():
    num_mobs = 1  #количество мобов, которое хотите сгенерировать
    mobs = generate_mobs(num_mobs)
    mob_data = [mob.to_dict() for mob in mobs]
    return jsonify(mob_data)

@app.route('/create', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type', 'Authorization'])
def create_mob():
    # Ваш код для создания нового моба здесь
    new_mob = create_new_mob()
    return jsonify(new_mob.to_dict())

if __name__ == '__main__':
    app.run()
