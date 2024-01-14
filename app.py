from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# External chatbot API link
chatbot_api_url = "https://the-krishna.onrender.com/chat"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json['user_input']

    # Request to the chatbot API
    response = requests.post(chatbot_api_url, json={'prompt': user_input})

    # Chatbot message
    chatbot_response = response.json().get('completion', 'Error getting response from the chatbot API')
    print(chatbot_response)
    chatbot_message = {
        'nickname': 'Kridhna',
        'text': chatbot_response,
        'avatar': 'https://example.com/chatbot-avatar.png',
        'reversed': True
    }

    return jsonify({'user_message': user_input, 'chatbot_message': chatbot_message})

if __name__ == '__main__':
    app.run(debug=True)
