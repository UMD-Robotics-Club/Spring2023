import Jetson.GPIO as GPIO
from time import time

class motor:
    """Allows for easy control of DC motor drivers using the jetson's GPIO pins."""

    def __init__(self, direction_pin : int, speed_pin : int, max_accel : float = 0.01):
        """Initialize the motor."""
        # define some default parameters
        self.is_inverted = False
        # define all pins
        self.__direction_pin = direction_pin
        self.__speed_pin = speed_pin
        # Pin Setup:
        # Board pin-numbering scheme
        GPIO.setmode(GPIO.BOARD)
        # Set both pins LOW and duty cycle to 0 to keep the motor idle
        GPIO.setup(self.__direction_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.__speed_pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(self.__direction_pin, GPIO.LOW)

        # set up PWM for speed control
        self.speed = GPIO.PWM(self.__speed_pin, 100)
        self.speed.start(5)
        self.speed.ChangeDutyCycle(0)
        # all of the variables below are responsible for a gentle acceleration curve
        self.old_time = time()
        self.current_time = time()
        self.accel = max_accel
        self.target_velocity = 0
        self.__current_velocity = 0

    def update_velocity(self, velocity : float):
        """Set the current velocity of the motor.
        
        This function is used to set the current velocity of the motor. 
        DO NOT CALL THIS FUCNTION DIRECTLY UNLESS YOU DON'T CARE ABOUT ACCELERATION!
        use set_target_velocity instead, and remember to coninually call update() to ensure the motor continues to accelerate.
        """
        self.__current_velocity = velocity
        # set direction based on if velocity is positive or negative
        if(self.__current_velocity < 0):
            # the False or self.is_inverted is a fast and fancy way of inverting the direction pin if is_inverted is true
            # Ask an EE major about it
            GPIO.output(self.__direction_pin, (False or self.is_inverted))
        else:
            # the True and not self.is_inverted is a fast and fancy way of inverting the direction pin if is_inverted is true
            # Ask an EE major about it
            GPIO.output(self.__direction_pin, (True and not self.is_inverted))
        # set speed based on velocity
        try:
            self.speed.ChangeDutyCycle(abs(self.__current_velocity)*100)
        except ValueError:
            print("Invalid value error inputted for motor.", self.__current_velocity, self.current_time - self.old_time)
    
    def set_target_velocity(self, velocity : float):
        """Set the target velocity of the motor.
        
        The motor will smoothly accelerate to the target velocity.
        """
        self.target_velocity = velocity
    
    def invert_dir_pin(self, is_inverted):
        """Change the default direction of the motor if the motor is wired in reverse."""
        self.is_inverted = is_inverted
    
    def update(self):
        """Incriment the velocity of the motor based on the target velocity and the current velocity.
        This function needs to be called as often as possible to ensure the motor continues accelerating properly.
        """
        self.current_time = time()
        # calculate the time difference between the current and old time
        delta_time = self.current_time - self.old_time
        #if delta_time > 0.3: delta_time = 0.05 # prevents random accelaration spikes
        # calculate the new current velocity based on the acceleration value
        vel_inc = self.accel * delta_time
        if self.target_velocity - self.__current_velocity < 0:
            vel_inc *= -1
    
        # check to see if the new velocity is going to be within 5% of the target velocity
        if self.__current_velocity + vel_inc < self.target_velocity*1.05 and self.__current_velocity + vel_inc > self.target_velocity*0.95:
            self.update_velocity(self.target_velocity)
        else: # if the new velocity is not within 5% of the target velocity, then accelerate
            if self.__current_velocity + vel_inc > 1:
                self.update_velocity(1)
            elif self.__current_velocity + vel_inc < -1:
                self.update_velocity(-1)
            else:
                self.update_velocity(self.__current_velocity + vel_inc)

        # set the old time to the current time
        self.old_time = self.current_time

class drive_train:
    """Keeps track of two motors and has a function to drive them in synchronicity."""

    # takes two motor objects and an optional IMU object to help with turning
    def __init__(self, motor1 : motor, motor2 : motor):
        """Initialize the drive train."""
        self.__motor1 = motor1
        self.__motor2 = motor2
        self.velocity = 0
        self.turn_ratio = 0
    
    # turn ratio is a number between 0 and 1 which controls how much the drive base will
    # turn relative to the velocity of the drive base
    def set_turn_velocity(self, velocity : float, turn_ratio : float = 0):
        """Set the velocity of the drive base."""
        velocity = round(velocity, 3)
        turn_ratio = round(turn_ratio, 4)
        self.velocity = velocity
        self.turn_ratio = turn_ratio

        # this is for emergency stops
        if velocity == 0 and turn_ratio == 0:
            self.__motor1.update_velocity(0)
            self.__motor2.update_velocity(0)
        # set the motor velocities based on the turn ratio and velocity
        if turn_ratio >= 0:
            self.__motor1.set_target_velocity(velocity)
            self.__motor2.set_target_velocity(-velocity*(1-2*turn_ratio))
        else:
            self.__motor1.set_target_velocity(velocity*(1-2*abs(turn_ratio)))
            self.__motor2.set_target_velocity(-velocity)

    def update(self):
        """Run motor updates so the motors can continue to accelerate."""
        self.__motor1.update()
        self.__motor2.update()

    def cleanup(self):
        GPIO.cleanup()