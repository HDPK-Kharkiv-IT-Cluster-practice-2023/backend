from flask import Flask
from blueprints.documented_endpoints.documented_endpoints import blueprint as documented_endpoint
from blueprints.game_endpoints.game_endpoints import blueprint as game_endpoints

app = Flask(__name__)

app.register_blueprint(game_endpoints)
app.register_blueprint(documented_endpoint)

if __name__ == "__main__":
    app.run()
