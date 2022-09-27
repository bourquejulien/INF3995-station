from flask import Flask
from src.controllers.web_controller import WebController
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
CORS(app)
api.add_resource(WebController, "/command")


@app.route('/health')
def health():  # put application's code here
    return 'healthy'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
