from flask import Flask, render_template, request, redirect, url_for
from characterCreation import Character, character1, character2


app = Flask(__name__, template_folder="teamplates")


def get_winner():
    if character1.health <= 0 and character2.health <= 0:
        return "Ничья"
    elif character1.health <= 0:
        return character2.name
    elif character2.health <= 0:
        return character1.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        character1.take_damage(character2.attack)
        character2.take_damage(character1.attack)
        character1.reset_attack()
        character2.reset_attack()
        if character1.health <= 0 or character2.health <= 0:
            winner = get_winner()
            return render_template('winner.html', winner=winner)
    return render_template('index.html', character1=character1, character2=character2)


if __name__ == "__main__":
    app.run(debug=True)
