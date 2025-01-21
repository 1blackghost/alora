import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket
app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

SHOULDER1_PIN = 14
SHOULDER2_PIN = 15
ELBOW_PIN = 18
WRIST_PIN = 23
FINGERS_PIN = 24

GPIO.setup(SHOULDER1_PIN, GPIO.OUT)
GPIO.setup(SHOULDER2_PIN, GPIO.OUT)
GPIO.setup(ELBOW_PIN, GPIO.OUT)
GPIO.setup(WRIST_PIN, GPIO.OUT)
GPIO.setup(FINGERS_PIN, GPIO.OUT)

shoulder1 = GPIO.PWM(SHOULDER1_PIN, 50)  
shoulder2 = GPIO.PWM(SHOULDER2_PIN, 50)  
elbow = GPIO.PWM(ELBOW_PIN, 50)          
wrist = GPIO.PWM(WRIST_PIN, 50)          
fingers = GPIO.PWM(FINGERS_PIN, 50)    



angle_base=0
angle_shoulder1=90
angle_shoulder2=90
angle_elbow=90
angle_wrist=90
angle_fingers=30



def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 18.0)  

def move_servo(servo,angle):
    duty_cycle = angle_to_duty_cycle(angle)
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.02)  
    servo.ChangeDutyCycle(angle_to_duty_cycle(angle))



@socketio.on('hold')
def hold_position(resp):
    print("Holding...")
    time.sleep(0.1)  
    shoulder1.ChangeDutyCycle(angle_to_duty_cycle(angle_shoulder1))
    shoulder2.ChangeDutyCycle(angle_to_duty_cycle(angle_shoulder2))
    elbow.ChangeDutyCycle(angle_to_duty_cycle(angle_elbow))
    wrist.ChangeDutyCycle(angle_to_duty_cycle(angle_wrist))
    fingers.ChangeDutyCycle(angle_to_duty_cycle(angle_fingers))


@socketio.on('update_positions')
def handle_update_positions(resp):
    global angle_base,angle_elbow,angle_fingers,angle_shoulder2,angle_shoulder1,angle_wrist
    global shoulder1,shoulder2,wrist,elbow,fingers
    print(f"Received positions update: {resp}")
    data=list(resp)
    if data[0]!=0:
        print()
    if data[1]!=0:
        if data[1]==-1:
            step=-5
            angle_shoulder1=angle_shoulder1+step
            angle_shoulder2=180-angle_shoulder1

            if angle_shoulder1<=0:
                angle_shoulder1=0
                angle_shoulder2=180-angle_shoulder1             
                
            threads = [
                threading.Thread(target=move_servo, args=(shoulder1,angle_shoulder1)),
                threading.Thread(target=move_servo, args=(shoulder2,angle_shoulder2)),
            ]

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        if data[1]==1:
            step=5
            angle_shoulder1=angle_shoulder1+step
            angle_shoulder2=180-angle_shoulder1
            if angle_shoulder1>=180:
                angle_shoulder1=180
                angle_shoulder2=180-angle_shoulder1
   
            threads = [
                threading.Thread(target=move_servo, args=(shoulder1,angle_shoulder1)),
                threading.Thread(target=move_servo, args=(shoulder2,angle_shoulder2)),
            ]

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
    if data[2]!=0:
        if data[2]==-1:
            step=-5
            angle_elbow=angle_elbow+step
            threads = [
                threading.Thread(target=move_servo, args=(elbow,angle_elbow)),
            ]

            if angle_elbow<=0:
                angle_elbow=0
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        if data[2]==1:
            step=5
            angle_elbow=angle_elbow+step
            threads = [
                threading.Thread(target=move_servo, args=(elbow,angle_elbow)),
            ]
            if angle_elbow>=180:
                angle_elbow=180

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
    if data[3]!=0:
        if data[3]==-1:
            step=-5
            angle_wrist=angle_wrist+step
            threads = [
                threading.Thread(target=move_servo, args=(wrist,angle_wrist)),
            ]

            if angle_wrist<=0:
                angle_wrist=0
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        if data[3]==1:
            step=5
            angle_wrist=angle_wrist+step
            threads = [
                threading.Thread(target=move_servo, args=(wrist,angle_wrist)),
            ]
            if angle_wrist>=180:
                angle_wrist=180

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
    if data[4]!=0:
        if data[4]==-1:
            step=-5
            angle_fingers=angle_fingers+step
            threads = [
                threading.Thread(target=move_servo, args=(fingers,angle_fingers)),
            ]

            if angle_fingers<=0:
                angle_fingers=0
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        if data[4]==1:
            step=5
            angle_fingers=angle_fingers+step
            threads = [
                threading.Thread(target=move_servo, args=(fingers,angle_fingers)),
            ]
            if angle_fingers>=180:
                angle_fingers=180

            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join() 
        if data[1]==0:
            angle_shoulder1=angle_shoulder1
            angle_shoulder2=180-angle_shoulder1
            threads = [
                threading.Thread(target=move_servo, args=(shoulder1,angle_shoulder1)),
                threading.Thread(target=move_servo, args=(shoulder2,angle_shoulder2)),
            ]  
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join() 
        if data[2]==0:

            threads = [
                threading.Thread(target=move_servo, args=(elbow,angle_elbow)),
            ]       
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join() 
        if data[3]==0:

            threads = [
                threading.Thread(target=move_servo, args=(wrist,angle_wrist)),
            ]       
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join() 
        if data[4]==0:

            threads = [
                threading.Thread(target=move_servo, args=(fingers,angle_fingers)),
            ]       
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join() 
    print(f"Base Angle: {angle_base}°")
    print(f"Shoulder 1 Angle: {angle_shoulder1}°")
    print(f"Shoulder 2 Angle: {angle_shoulder2}°")
    print(f"Elbow Angle: {angle_elbow}°")
    print(f"Wrist Angle: {angle_wrist}°")
    print(f"Fingers Angle: {angle_fingers}°")
   
    try:
        
        emit('response', {'message': 'Positions updated successfully!'})
    except Exception as e:
        print(f"Error while sending data: {e}")
        
        emit('response', {'message': f'Failed to update positions: {e}'})
        
        
if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0",port=6550)