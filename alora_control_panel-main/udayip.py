import socketio

# Create a Socket.IO client
sio = socketio.Client(reconnection_attempts=3)

# Define the event handlers
@sio.event
def connect():
    print("Successfully connected to server!")

@sio.event
def disconnect():
    print("Disconnected from server!")

# Emit the data to the 'update_positions' event
def send_position_update(data):
    try:
        sio.emit('update_positions', data)
        print(f"Sent data: {data}")
    except Exception as e:
        print(f"Error while sending data: {e}")

if __name__ == '__main__':
    # Connect to the server at the correct IP and port
    sio.connect('http://localhost:6550')

    # Example data to send (this should match the data you expect in the Flask server)
    data = [1, 2, 3, 4, 5]
    
    # Send position update
    send_position_update(data)

    # Disconnect after sending the data
    sio.disconnect()
