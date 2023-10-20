from flask import Blueprint
from flask_restx import Api, Resource, fields

blueprint = Blueprint('documented_endpoint', __name__)
api = Api(blueprint, doc='/swagger', title='My API', version='1.0')

todo_model = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})

character_full_info_model = api.model('Character full info', {
    'id': fields.Integer(readonly=True, description='The Character unique identifier'),
    'name': fields.String(readonly=True, description='The Character name'),
    'level': fields.Integer(readonly=True, description='The Character level'),
    'xp_goal': fields.Integer(readonly=True, description='The Character xp needed to reach the next level'),
    'xp': fields.Integer(readonly=True, description='The Character current xp'),
    'max_health': fields.Integer(readonly=True, description='The Character max health'),
    'health': fields.Integer(readonly=True, description='The Character current health'),
    'armor': fields.Integer(readonly=True, description='The Character armor'),
    'attack': fields.Integer(readonly=True, description='The Character attack'),
    'luck': fields.Integer(readonly=True, description='The Character luck'),
    'balance': fields.Integer(readonly=True, description='The Character balance'),
    'alive': fields.Boolean(readonly=True, description='The Character is alive or not'),
    'critical_attack': fields.Integer(readonly=True, description='The Character critical attack modifier'),
    'playability': fields.Boolean(readonly=True, description='The Character is playable or not'),
    'stat_points': fields.Integer(readonly=True, description='The Character stat points')
})

ns = api.namespace('todos', description='TODO operations')


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo_model)
    def get(self):
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo_model)
    @ns.marshal_with(todo_model, code=201)
    def post(self):
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    @ns.doc('get_todo')
    @ns.marshal_with(todo_model)
    def get(self, id):
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        DAO.delete(id)
        return '', 204

    @ns.expect(todo_model)
    @ns.marshal_with(todo_model)
    def put(self, id):
        return DAO.update(id, api.payload)


game = api.namespace('game_dok', description='game operations')


class CharacterDAO(object):
    def __init__(self):
        self.counter = 0
        self.characters = []

    def get(self, id):
        for character in self.characters:
            if character['id'] == id:
                return character
        api.abort(404, "Todo {} doesn't exist".format(id))

    def get_by_playability(self, playability):
        characters_list = []
        for character in self.characters:
            if character['playability'] == playability:
                characters_list.append(character)
        return characters_list

    def create(self, data):
        character = data
        character['id'] = self.counter = self.counter + 1
        self.characters.append(character)
        return character

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.characters.remove(todo)


characterDAO = CharacterDAO()
characterDAO.create({
    'id': 1,
    'name': 'first',
    'level': 1,
    'xp_goal': 50,
    'xp': 10,
    'max_health': 10,
    'health': 10,
    'armor': 5,
    'attack': 5,
    'luck': 5,
    'balance': 0,
    'alive': True,
    'critical_attack': 2,
    'playability': True,
    'stat_points': 0
})
characterDAO.create({
    'id': 2,
    'name': 'second',
    'level': 2,
    'xp_goal': 50,
    'xp': 10,
    'max_health': 10,
    'health': 10,
    'armor': 5,
    'attack': 5,
    'luck': 5,
    'balance': 0,
    'alive': True,
    'critical_attack': 2,
    'playability': False,
    'stat_points': 0
})
characterDAO.create({
    'id': 3,
    'name': 'third',
    'level': 3,
    'xp_goal': 50,
    'xp': 10,
    'max_health': 10,
    'health': 10,
    'armor': 5,
    'attack': 5,
    'luck': 5,
    'balance': 100,
    'alive': False,
    'critical_attack': 2,
    'playability': True,
    'stat_points': 0
})


@game.route('/api/v1/characters/<string:playability>')
class CharacterList(Resource):
    @game.doc('list_characters')
    @game.marshal_list_with(character_full_info_model)
    def get(self, playability):
        if playability.lower() == 'true':
            playability = True
        elif playability.lower() == 'false':
            playability = False
        else:
            api.abort(400, "Invalid value for 'playability'. Use 'true' or 'false'.")
        characters = characterDAO.get_by_playability(playability)
        return characters


@game.route('/api/v1/character/<int:character_id>')
class CharacterResource(Resource):
    @game.doc('character_by_id')
    @game.marshal_with(character_full_info_model)
    def get(self, character_id):
        return characterDAO.get(character_id)


