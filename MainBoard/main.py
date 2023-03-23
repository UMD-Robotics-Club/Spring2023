import serial
from Motor import motor
from IMU import IMU


turn_motor = motor(123, 13425) # TODO: fill with real values later
power_motor = motor(678, 5786) # TODO: fill with real values later

ser = serial.Serial('/dev/ttyUSB0')  # open serial port TODO: fill with real value later
imu = IMU(ser)

while 1: 
#read from joystick (IMU for now)
#use to write to motors

    imu.update()
    x = imu.acc[0]
    y = imu.acc[1]
    turn_motor.set_target_velocity(x)
    power_motor.set_target_velocity(y)
    turn_motor.update()
    power_motor.update()