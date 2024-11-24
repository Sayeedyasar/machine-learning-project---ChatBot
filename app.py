from flask import Flask, render_template_string, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections

# Download required NLTK data
nltk.download('punkt')

app = Flask(__name__)

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>ChatBot-chan</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 20px;
        }
        #chat-container {
            width: 500px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        #chat-box {
            height: 400px;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow-y: scroll;
            margin-bottom: 20px;
            padding: 15px;
            background-color: #ffffff;


        }
        #user-input {
            width: 75%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
        }
        button {
            padding: 10px 20px;
            background-color: #0084ff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0066cc;
        }
        .message {
            margin: 10px 0;
            padding: 8px 12px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #0084ff;
            color: white;
            margin-left: auto;
        }
        .bot-message {
            background-color: #e9ecef;
            color: black;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <h1>AI ChatBot-Chan</h1>
    <div id="chat-container">
        <div id="chat-box">
            <div class="message bot-message">Hello! How can I help you today?</div>
        </div>
        <div style="display: flex;">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const userInput = document.getElementById('user-input');
            const message = userInput.value.trim();
            
            if (message) {
                displayMessage(message, 'user-message');
                
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    displayMessage(data.response, 'bot-message');
                })
                .catch(error => {
                    console.error('Error:', error);
                    displayMessage('Sorry, something went wrong. Please try again.', 'bot-message');
                });
                
                userInput.value = '';
            }
        }

        function displayMessage(message, className) {
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.textContent = className === 'user-message' ? 'You: ' + message : 'Bot: ' + message;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

# Define chat patterns and responses
patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey! How can I help you?']),
    (r'how are you', ['I am doing well, thank you!', 'I am fine, how are you?']),
    (r'what is your name', ['My name is ChatBot!', 'I am ChatBot, nice to meet you!']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye bye!']),
    (r'thank you|thanks', ['You\'re welcome!', 'No problem!', 'My pleasure!']),
    (r'what can you do', ['I can chat with you and help answer questions!', 
                         'I\'m a chatbot designed to have conversations and help you!']),
    (r'who made you|who created you', ['I was created as a simple chatbot using Python and Flask! by Sayeed yasar',
                      'I\'m a chatbot created for demonstration purposes! by Sayeed yasar for his ML project ']),
    (r'(.*)', ['I am not sure how to respond to that.', 
               'Could you please rephrase that?', 
               'Interesting, tell me more.'])
]

chatbot = Chat(patterns, reflections)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        response = chatbot.respond(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': 'Sorry, something went wrong. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)