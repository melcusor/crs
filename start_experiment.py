from flaskApp import app, socketIo

if __name__ == "__main__":
    socketIo.run(app)
