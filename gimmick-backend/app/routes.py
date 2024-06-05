from flask import request, jsonify, Blueprint

main = Blueprint('main', __name__)


@main.route('/', methods= ['GET'])
def index():
    if request.method == 'GET':
        return jsonify('Hello, baby!')


def init_app(app):
    app.register_blueprint(main)
