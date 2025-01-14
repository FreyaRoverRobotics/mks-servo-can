import can 
import time
from mks_servo import MksServo
import time

import logging

# Stock slcan firmware on Windows
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
notifier = can.Notifier(bus, [])

def wait_for_motor_idle2(timeout):    
    start_time = time.perf_counter()
    while (time.perf_counter() - start_time < timeout) and servo.is_motor_running():
        print(servo.read_motor_speed(), flush=True)
        time.sleep(0.1)  # Small sleep to prevent busy waiting
    return servo.is_motor_running()

def move_motor(absolute_position):  
    print(f"Moving motor to absolute position {absolute_position}", flush=True)
    print(servo.run_motor_absolute_motion_by_axis(3000, 0, absolute_position), flush=True)
    wait_for_motor_idle2(30)
    value = servo.read_encoder_value_addition()
    error = absolute_position - value
    print(f"Movement at {absolute_position} with error {error}")    
    print(f"", flush=True)
    print()

servo = MksServo(bus, notifier, 1)

print(servo.set_work_mode(MksServo.WorkMode.SrClose))
print(servo.set_subdivisions(64))
print(servo.set_working_current(2000))
print(servo.b_go_home())

print(servo.set_current_axis_to_zero())

while True:
    move_motor(0x4000*13)
    move_motor(0)
    time.sleep(0)
