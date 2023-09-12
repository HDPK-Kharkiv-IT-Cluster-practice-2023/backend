from flask import Flask, render_template, request

from characterCreation import character1, character2, Player_you

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'c1damage' in request.form:
            if request.form['c1damage'] == 'damage':
                character1.take_damage(Player_you.your_attack)
                Player_you.take_damage(character1.attack)
                Player_you.take_damage(character2.attack)
                character1.reset_attack()
                character2.reset_attack()
                Player_you.reset_your_attack()

        elif 'c2damage' in request.form:
            if request.form['c2damage'] == 'damage2':
                character2.take_damage(Player_you.your_attack)
                Player_you.take_damage(character1.attack)
                Player_you.take_damage(character2.attack)
                character1.reset_attack()
                character2.reset_attack()
                Player_you.reset_your_attack()

        if character1.health <= 0:
            character1.alive = False
        if character2.health <= 0:
            character1.alive = False
        if Player_you.health <= 0:
            return render_template('winner.html')

    return render_template('index.html', character1=character1, character2=character2, Player_you=Player_you)


if __name__ == "__main__":
    app.run(debug=True)
