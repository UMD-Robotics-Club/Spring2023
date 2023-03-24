import serial
from Motor import Motor
from IMU import IMU


turn_motor = Motor.motor(123, 13425) # TODO: fill with real values later
power_motor = Motor.motor(678, 5786) # TODO: fill with real values later

ser = serial.Serial('/dev/ttyACM0')
imu = IMU.IMU(ser)

while 1: 
#read from joystick (IMU for now)
#use to write to motors

    imu.update()
    x = imu.acc[0]
    y = imu.acc[1]
    print(x,y)
    if -0.39 < x < 0.39:
        turn_motor.set_target_velocity(x)
    if -0.39 < y < 0.39:
        power_motor.set_target_velocity(y)
    turn_motor.update()
    power_motor.update()