# File used for testing different SenseHat methods
# Brody Williams

from sense_hat import SenseHat
import time

sense = SenseHat()

def humidity_test():
    humidity = sense.get_humidity()
    print("Humidity: %s %%rh" % humidity)

def pressure_test():
    pressure = sense.get_pressure()
    print("Pressure: %s Millibars" % pressure)

def temperature_test():
    press_temp = sense.get_temperature_from_pressure()
    humid_temp = sense.get_temperature_from_humidity()
    print("Temperature from humidity: %s C\nTemperature from pressure: %s C"\
          % (humid_temp,press_temp))

def all_sensor_orientation_test():
    sense.set_imu_config(True, True, True)
    orientation_r = sense.get_orientation_radians()
    orientation_d = sense.get_orientation_degrees()
    print("Orientation (Radians): Pitch = {pitch} Roll = {roll} Yaw = {yaw}" \
          .format(**orientation_r))
    print("Orientation (Degrees): Pitch = {pitch} Roll = {roll} Yaw = {yaw}" \
          .format(**orientation_d))

def loop_orientation():
    while True:
        all_sensor_orientation_test()
        time.sleep(.5)

def magnetometer_test():
    north = sense.get_compass()
    raw_data = sense.get_compass_raw()
    print("North (degrees): %s" % north)
    print("Raw Data (microTeslas) - X: {x} Y:{y} Z:{z}"\
          .format(**raw_data))

def loop_magnetometer():
    while True:
        magnetometer_test()
        time.sleep(.5)

def gyroscope_test():
    orientation = sense.get_gyroscope()
    raw_data = sense.get_gyroscope_raw()
    print("Orientation (Degrees): Pitch: {pitch} Roll: {roll} Yaw:{yaw}"\
          .format(**orientation))
    print("Raw Data (radians per second): X: {x} Y: {y} Z: {z}"\
          .format(**raw_data))

def loop_gyroscope():
    while True:
        gyroscope_test()
        time.sleep(.5)
    
def accelerometer_test():
    orientation = sense.get_accelerometer()
    raw_data = sense.get_accelerometer_raw()
    x,y,z = raw_data["x"], raw_data["y"], raw_data["z"]
    pitch, roll, yaw = orientation["pitch"], orientation["roll"], orientation["yaw"]
    print("Orientation (Degrees): Pitch: {:.2} Roll: {:.2} Yaw:{:.2}"\
          .format(pitch, roll, yaw))
    print("Raw Data (Gs): X: {:.2} Y: {:.2} Z: {:.2}"\
          .format(x,y,z))

def loop_accelerometer():
    while True:
        accelerometer_test()
        time.sleep(.5)
