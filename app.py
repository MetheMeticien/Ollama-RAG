from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import ollama

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('send_message')
def handle_message(data):
    user_input = data['message']
    print(user_input)
    
    # Initialize your Ollama chat session here
    stream = ollama.generate(model='gemma:2b-instruct', prompt= user_input, stream=True)
    # Emit each chunk of the AI response as it's generated
    for chunk in stream:
        if chunk["response"]:
            emit('receive_message', {'message': chunk['response']}, broadcast=True)
            print(chunk['response'], end='', flush=True)
        
        
        

    print("Finished generating output")        

if __name__ == '__main__':
    socketio.run(app, debug=True)
