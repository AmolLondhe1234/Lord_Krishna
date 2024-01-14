from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import requests
from logging import Logger

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# External chatbot API link
chatbot_api_url = "https://the-krishna.onrender.com/chat"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@socketio.on('send_message')
def handle_message(data):
    user_input = data['user_input']

    # Emit user message to all clients
    emit('receive_message', {'nickname': 'User', 'text': user_input}, broadcast=True)

    # Request to the chatbot API
    response = requests.post(chatbot_api_url, json={'prompt': user_input})

    # Chatbot message
    chatbot_response = response.json().get('completion', 'Error getting response from the chatbot API')
    Logger.log(chatbot_response)
    chatbot_message = {
        'nickname': 'Kridhna',
        'text': chatbot_response,
        'avatar': 'https://example.com/chatbot-avatar.png',
        'reversed': True
    }

    # Emit chatbot message to all clients
    emit('receive_message', chatbot_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
