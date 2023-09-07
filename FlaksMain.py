from flask import Flask, render_template, request, redirect, url_for
from characterCreation import Character


app = Flask(__name__, template_folder="teamplates")


class Character:
    def __init__(self):
        self.health = 100  # Здоровье от 0 до 100
        self.attack = 0  # Урон от 0 до 20

    def take_damage(self, damage):
        self.health -= damage

    def reset_attack(self):
        import random
        self.attack = random.randint(1, 20)

character1 = Character()
character2 = Character()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        character1.take_damage(character2.attack)
        character2.take_damage(character1.attack)
        character1.reset_attack()
        character2.reset_attack()
        

        if character1.health <= 0 or character2.health <= 0:
            print("Персонаж 1" if character1.health > character2.health else "Персонаж 2")
            winner = "Персонаж 1" if character1.health > character2.health else "Персонаж 2"
            return render_template('winner.html', winner=winner)


    return render_template('index.html', character1=character1, character2=character2)
def get_winner():
    if character1.health <= 0 and character2.health <= 0:
        return "Ничья"
    elif character1.health <= 0:
        return "Персонаж 2"
    elif character2.health <= 0:
        return "Персонаж 1"


if __name__ == "__main__":
    app.run(debug=True)
