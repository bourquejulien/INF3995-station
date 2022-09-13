from flask import Flask
from src.controllers.basic_controller import blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(blueprint, url_prefix='/basic')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
