import cv2
from flask import Flask, render_template, Response, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit
import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  
camera = cv2.VideoCapture(4)

HOST = '127.0.0.1'
PORT = 6535

client_socket = None


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            height, width, _ = frame.shape
            start_x = int(width / 4)
            start_y = int(height / 4)
            end_x = int(3 * width / 4)
            end_y = int(3 * height / 4)
            frame = frame[start_y:end_y, start_x:end_x]

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        if username == 'aloraadmin' and password == 'alorapassword':
            session['username'] = username  
            return redirect(url_for('main'))  
        else:
            flash('Invalid username or password')  
            return redirect(url_for('index'))  

    return render_template('login.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    return redirect(url_for('index'))  

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('index'))  

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('message')
def handle_message(data):
    print(f"Received message: {data}")
    emit('response', {'message': 'Message received!'})

@socketio.on('custom_event')
def handle_custom_event(data):
    print(f"Received custom event data: {data}")
    emit('response', {'data': 'Custom event processed!'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")
