from flask import Flask

from src.controllers.basic_controller import blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(blueprint, url_prefix='/basic')


@app.route('/')
def health():  # put application's code here
    return 'healthy'


if __name__ == '__main__':
    app.run(host="0.0.0.0")

    # with SwarmClient(SwarmClient.Uris[1]) as client:
    #     client.blink()
    #     client.demo()

