from flask import Flask

from app.authentication_module.routes import init_routes

app = Flask(__name__)
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)