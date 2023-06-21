from flask_socketio import emit
from flaskApp import socketIo, routes


@socketIo.on('joined', namespace='/crs')
def joined(message):
    emit('status',
         {'msg': 'Ich kann dir helfen, ein leckeres Rezept zu finden. Was würdest du gerne essen/zubereiten?'})


@socketIo.on('text', namespace='/crs')
def text(message):
    # Sent by a client when the user entered a new message.
    user_input = message['msg']
    emit('user_input', {'user_input': user_input})
    routes.process_input({'msg': user_input})
