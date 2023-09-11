from flask import Flask, render_template, request, redirect, url_for
from characterCreation import Character, character1, character2, Player, Playeryou


app = Flask(__name__, template_folder="teamplates")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'c1damage' in request.form:
            if request.form['c1damage'] == 'damage':
                character1.take_damage(Playeryou.yourattack)
                Playeryou.take_damage(character1.attack)
                Playeryou.take_damage(character2.attack)
                character1.reset_attack()
                character2.reset_attack()
                Playeryou.reset_attackyour()

        elif 'c2damage' in request.form:
            if request.form['c2damage'] == 'damage2':
                character2.take_damage(Playeryou.yourattack)
                Playeryou.take_damage(character1.attack)
                Playeryou.take_damage(character2.attack)
                character1.reset_attack()
                character2.reset_attack()
                Playeryou.reset_attackyour()

        if character1.health <= 0:
            character1.alive = False
        if character2.health <= 0:
            character1.alive = False
        if Playeryou.health <= 0:
            return render_template('winner.html')

    return render_template('index.html', character1=character1, character2=character2, Playeryou=Playeryou)


if __name__ == "__main__":
    app.run(debug=True)
