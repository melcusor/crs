from flask import Flask
from flask_socketio import SocketIO
from config.config import Config
from flask_bootstrap import Bootstrap


# create and configure the app
app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
socketIo = SocketIO(app)

from flaskApp import routes, socketIO_events

print("__init__.py here!")


