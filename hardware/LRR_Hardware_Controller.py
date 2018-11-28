# LRR Hardware Subsystem Control Software
# Brody Williams

'''
Magnetic Contact Switch
    - Use GPIO Zero library?
    - Could also use button on breadboard/Sense hat joystick to simulate
    as suggested by Dr. Lim
'''

from sense_hat import SenseHat
from firebase import firebase
import time
import copy

# Debug Constant (Very C-esque, I know)
DEBUG = 1

# Globals
R = (255,0,0) # Red
G = (0,255,0) # Green

vib_threshold = 2

sense = SenseHat()
firebase = firebase.FirebaseApplication('https://laundry-room-recon.firebaseio.com', None)

running_dclosed = [
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G
]

running_dopen = [
G, G, G, R, R, G, G, G,
G, G, G, R, R, G, G, G,
G, G, G, R, R, G, G, G,
G, G, G, R, R, G, G, G,
G, G, G, R, R, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, R, R, G, G, G,
G, G, G, R, R, G, G, G
]

stopped_dclosed = [
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R
]

stopped_dopen = [
R, R, R, G, G, R, R, R,
R, R, R, G, G, R, R, R,
R, R, R, G, G, R, R, R,
R, R, R, G, G, R, R, R,
R, R, R, G, G, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, G, G, R, R, R,
R, R, R, G, G, R, R, R
]


# Main function for LRR hardware that loops
# and calls other functions as necessary.
def run_lrr():
    # Initialize values/display
    prev_raw_data = {'x': 0, 'y': 1.9, 'z': 95}
    prev_running_status = 0 # 0: Not running 1: Running
    prev_door_status = 0 # 0: Door closed 1: Door open
    sense.set_pixels(stopped_dclosed)
    
    while True:
        # Gather raw accelerometer data
        raw_data = sense.get_accelerometer_raw()

        # Modify raw data for easier visualization
        raw_data['x'] *= 100
        raw_data['y'] *= 100
        raw_data['z'] *= 100
        
        # Get new running status
        running_status = determine_running_status(prev_raw_data, raw_data)

        # Get new door status - TODO
        door_status = determine_door_status()

        # Debugging/Sensitivity adjustment output
        if DEBUG:
            debug_print(prev_raw_data, raw_data, prev_running_status, \
                        running_status, prev_door_status, door_status)

        # Update LED display and database if either status changes
        if (running_status != prev_running_status) or (door_status != prev_door_status):
            display_status(running_status, door_status)
            update_db(running_status, door_status)
            
        # Update previous values and wait before next loop iteration
        prev_raw_data = copy.deepcopy(raw_data)
        prev_running_status = running_status
        prev_door_status = door_status
        time.sleep(.5)

# Determines running/not running status by comparing
# raw accelerometer data with previous data. Returns
# 1 for running or 0 for not running.
def determine_running_status(prev_data, new_data):
    if(abs(new_data['x'] - prev_data['x']) > vib_threshold) or \
        (abs(new_data['y'] - prev_data['y']) > vib_threshold) or \
        (abs(new_data['z'] - prev_data['z']) > vib_threshold):
        return 1
    else:
        return 0
    
#TODO
def determine_door_status():
    pass
    
# Updates the Sense Hat LED display to reflect the current status
def display_status(running_status, door_status):
    # Device stopped / Door closed
    if(running_status == 0) and (door_status == 0):
        sense.set_pixels(stopped_dclosed)
    # Device stopped / Door open
    elif (running_status == 0) and (door_status == 1):
        sense.set_pixels(stopped_dopen)
    # Device running / Door closed
    elif (running_status == 1) and (door_status == 0):
        sense.set_pixels(running_dclosed)
    # Device running / Door open (possible for top load washers?)
    elif (running_status == 1) and (door_status == 1):
        sense.set_pixels(running_dopen)

# Updates the firebase database with the new status
def update_db(running_status, door_status):

    # Update the database
    firebase.put('https://laundry-room-recon.firebaseio.com','washingMachine/runningStatus', running_status)
    firebase.put('https://laundry-room-recon.firebaseio.com','washingMachine/doorStatus', door_status)

    if DEBUG:
        # Print new status
        print("\nUpdating database! Running status: {:d} Door status: {:d}\n" .format(running_status, door_status))
    

# Function to print x,y,z  vibration data values & current/previous
# statuses while developing/debugging
def debug_print(prev_raw_data, raw_data, prev_running_status, \
                    running_status, prev_door_status, door_status):
    print("\n Previous Data: x = %.5f, y = %.5f, z = %.5f," \
          "\n New Data :     x = %.5f, y = %.5f, z = %.5f," \
          "\n D(x) = %.5f, D(y) = %.5f, D(z) = %.5f" \
          "\n Previous Running Status: %d New Running Status: %d\n" \
          "\n Previous Door Status %d New Door Status: %d\n" \
           % (prev_data['x'], prev_data['y'], prev_data['z'], \
                  new_data['x'], new_data['y'], new_data['z'], \
                  abs(new_data['x'] - prev_data['x']), \
                  abs(new_data['y'] - prev_data['y']), \
                  abs(new_data['z'] - prev_data['z']), \
                  prev_running_status, running_status, \
                  prev_door_status, door_status))
    
    
