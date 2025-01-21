import RPi.GPIO as GPIO
import threading
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins for the servos
SHOULDER1_PIN = 14
SHOULDER2_PIN = 15
ELBOW_PIN = 18
WRIST_PIN = 23
FINGERS_PIN = 24

# Set up the pins
GPIO.setup(SHOULDER1_PIN, GPIO.OUT)
GPIO.setup(SHOULDER2_PIN, GPIO.OUT)
GPIO.setup(ELBOW_PIN, GPIO.OUT)
GPIO.setup(WRIST_PIN, GPIO.OUT)
GPIO.setup(FINGERS_PIN, GPIO.OUT)

# Set up PWM for the servos
shoulder1 = GPIO.PWM(SHOULDER1_PIN, 50)
shoulder2 = GPIO.PWM(SHOULDER2_PIN, 50)
elbow = GPIO.PWM(ELBOW_PIN, 50)
wrist = GPIO.PWM(WRIST_PIN, 50)
fingers = GPIO.PWM(FINGERS_PIN, 50)

# Start PWM with 0 duty cycle
shoulder1.start(0)
shoulder2.start(0)
elbow.start(0)
wrist.start(0)
fingers.start(0)

# Function to calculate duty cycle for a given angle
def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 18.0)

# Function to move a servo slowly to a target angle
def move_servo_to_angle(servo, current_angle, target_angle, step=1):
    step = step if target_angle > current_angle else -step
    for angle in range(current_angle, target_angle + step, step):
        duty_cycle = angle_to_duty_cycle(angle)
        servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.05)  # Slow down movement
    servo.ChangeDutyCycle(angle_to_duty_cycle(target_angle))

# Function to control all servos
def control_servos(angles):
    global current_angles

    # Calculate the second shoulder angle
    angles['shoulder2'] = 180 - angles['shoulder1']

    # Create threads for each servo
    threads = [
        threading.Thread(target=move_servo_to_angle, args=(shoulder1, current_angles['shoulder1'], angles['shoulder1'], 1)),
        threading.Thread(target=move_servo_to_angle, args=(shoulder2, current_angles['shoulder2'], angles['shoulder2'], 1)),
        threading.Thread(target=move_servo_to_angle, args=(elbow, current_angles['elbow'], angles['elbow'], 1)),
        threading.Thread(target=move_servo_to_angle, args=(wrist, current_angles['wrist'], angles['wrist'], 1)),
        threading.Thread(target=move_servo_to_angle, args=(fingers, current_angles['fingers'], angles['fingers'], 1))
    ]

    # Start and wait for all threads to finish
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Update current angles
    current_angles.update(angles)

# Initialize current angles
current_angles = {'shoulder1': 90, 'shoulder2': 90, 'elbow': 90, 'wrist': 90, 'fingers': 0}

# Cleanup function
def cleanup():
    shoulder1.stop()
    shoulder2.stop()
    elbow.stop()
    wrist.stop()
    fingers.stop()
    GPIO.cleanup()

# Main loop for reading temp.txt and controlling servos
if __name__ == "__main__":
    try:
        while True:
            try:
                with open("temp.txt", "r") as file:
                    data = eval(file.read())  # Read and evaluate the data from temp.txt

                    if isinstance(data, list) and len(data) == 5:  # Validate the data
                        b, s1, e, w, f = data
                        BASE = 90  # Placeholder for base, modify as needed
                        SHOULDER1 = min(max(0, current_angles['shoulder1'] + s1), 180)
                        ELBOW = min(max(0, current_angles['elbow'] + e), 180)
                        WRIST = min(max(0, current_angles['wrist'] + w), 180)
                        FINGERS = min(max(0, current_angles['fingers'] + f), 180)

                        # Update angles and control servos
                        control_servos({
                            'shoulder1': SHOULDER1,
                            'elbow': ELBOW,
                            'wrist': WRIST,
                            'fingers': FINGERS
                        })
                    else:
                        print("Invalid data format in temp.txt")

            except Exception as e:
                print(f"Error reading or parsing temp.txt: {e}")

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        cleanup()
