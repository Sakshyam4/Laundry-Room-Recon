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
        time.sleep(1)

def magnetometer_test():
    #stuff

def gyroscope_test():
    #moar stuff

def accelerometer_test():
    #even moar stuff
