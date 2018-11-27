# LRR Hardware Subsystem Control Software
# Brody Williams

'''
Necessary Functionality:

Retrieve Sensor Data - IMU Unit & Magnetic Contact Switch
    - Appropriate IMU sensor sensitivity - Automatic
    - How often? .5 seconds?
    - Accelerometer raw data for vibration? - Working

Make device status determinations based on sensor data

Update database
    - How often? - only when status changes

Magnetic Contact Switch
    - Use GPIO Zero library?
    - Could also use button on breadboard/Sense hat joystick to simulate
    as suggested by Dr. Lim
    
Use LED to display running/not running status? -Green/Red? - Working
'''
from sense_hat import SenseHat
import time
import copy

from firebase import firebase
firebase = firebase.FirebaseApplication('https://laundry-room-recon.firebaseio.com',None)

#Globals
R = (255,0,0) #Red
G = (0,255,0) #Green

sense = SenseHat()

vib_threshold = 2

running_image = [
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G,
G, G, G, G, G, G, G, G
]

stopped_image = [
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R
]

# Main function for LRR hardware that loops
# and calls other functions as necessary.
def run_lrr():
    #Initialize values/display
    prev_raw_data = {'x': 0, 'y': 1.9, 'z': 95}
    prev_status = 0;
    sense.set_pixels(stopped_image)
    
    while True:
        #Gather raw accelerometer data
        raw_data = sense.get_accelerometer_raw()

        #Modify raw data for easier visualization
        raw_data['x'] *= 100
        raw_data['y'] *= 100
        raw_data['z'] *= 100
        
        #Get new device status
        status = determine_status(prev_raw_data, raw_data)
        
        #Debugging/Sensitivity adjustment output
        debug_print(prev_raw_data, raw_data, prev_status, status)

        #Update LED display and database if status changes
        if(status != prev_status):
            display_status(status)
            update_db(status)
            
        #Update previous values and wait before next loop iteration
        prev_raw_data = copy.deepcopy(raw_data)
        prev_status = status
        time.sleep(.5)

# Determines running/not running status by comparing
# raw accelerometer data with previous data. Returns
# 1 for running or 0 for not running.
def determine_status(prev_data, new_data):
    if(abs(new_data['x'] - prev_data['x']) > vib_threshold) or \
        (abs(new_data['y'] - prev_data['y']) > vib_threshold) or \
        (abs(new_data['z'] - prev_data['z']) > vib_threshold):
        return 1
    else:
        return 0

#Updates the Sense Hat LED display to reflect the current status
def display_status(status):
    if(status == 1):
        sense.set_pixels(running_image)
    else:
        sense.set_pixels(stopped_image)

#Updates the firebase database with the new status
def update_db(status):
    #Do database stuff
    
    if status == 0:
        #curl -X PUT -d '{"washingMachine": "0"}'\
        #     'https://laundry-room-recon.firebaseio.com'
        firebase.put('https://laundry-room-recon.firebaseio.com','washingMachine/runningStatus',0)
        status_string = '0'
    elif status == 1:
        #curl -X PUT -d '{"washingMachine": "1"}'\
         #    'https://laundry-room-recon.firebaseio.com'
        firebase.put('https://laundry-room-recon.firebaseio.com','washingMachine/runningStatus',1)
        status_string = '1'

    else:
        status_string = "Problem"
    print("\nUpdating database with {:s} status!\n" .format(status_string))
    
    #wmstatus.setValue(status_string)

#Function to print x,y,z values while developing/debugging
def debug_print(prev_data, new_data, prev_status, status):
    print("\n Previous Data: x = %.5f, y = %.5f, z = %.5f," \
          "\n New Data :     x = %.5f, y = %.5f, z = %.5f," \
          "\n D(x) = %.5f, D(y) = %.5f, D(z) = %.5f" \
          "\n Previous Status: %d New Status: %d\n" \
           % (prev_data['x'], prev_data['y'], prev_data['z'], \
                  new_data['x'], new_data['y'], new_data['z'], \
                  abs(new_data['x'] - prev_data['x']), \
                  abs(new_data['y'] - prev_data['y']), \
                  abs(new_data['z'] - prev_data['z']), \
                  prev_status, status))
    
    
