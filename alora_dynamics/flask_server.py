from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket
import controller
app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  


@socketio.on('update_positions')
def handle_update_positions(resp):
    print(f"Received positions update: {resp}")
    try:
        data_str = str(resp)
        with open("temp.txt","w") as f:
            f.write(data_str)
        print(f"Data sent to server: {resp}")
        emit('response', {'message': 'Positions updated successfully!'})
    except Exception as e:
        print(f"Error while sending data: {e}")
        emit('response', {'message': f'Failed to update positions: {e}'})

@app.route('/')
def index():
    return render_template('index.html')  

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0",port=6550)
