from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def members():
    data = {"members": ["Member1", "Member2", "Member3"]}
    return jsonify(data)


@app.route('/', methods=['POST'])
def submit():
    name = request.form.get('name')
    return print(f'Привет, {name}! Форма отправлена.')


if __name__ == '__main__':
    app.run(debug=True)
