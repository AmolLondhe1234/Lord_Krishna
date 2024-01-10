from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app)

# External chatbot API link
chatbot_api_url = "https://the-krishna.onrender.com/chat"

@app.route('/')
def index():
    return render_template('chatbot.html')

@socketio.on('send_message')
def handle_message(data):
    user_input = data['user_input']
    emit('receive_message', broadcast=True)
    response = requests.post(chatbot_api_url, json={'prompt': user_input})
    chatbot_response = response.json().get('completion', 'Error getting response from the chatbot API')
    print(chatbot_response)
    chatbot_message = {
        'nickname': 'Kridhna',
        'text': chatbot_response,
        'avatar': 'https://example.com/chatbot-avatar.png',
        'reversed': True
    }

    emit('receive_message', chatbot_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
