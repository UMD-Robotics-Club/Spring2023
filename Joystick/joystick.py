import pygame
#The Dead Zone, maximum turning speed, and maximum speed
deadzone = 0.3
maxturn = 0.5
maxspeed = 1
#My Stuff (please let me know before you fuck with this)
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
ratio = 10/(10*(1-deadzone))

joystick.init()

#function to get the current statud of our brake, currently the trigger of the joystick
def get_brake():
    brake = joystick.get_button(0)
    if(brake == 1):
        return True
    else:
        return False

#determines our speed
def get_speed():
    y = joystick.get_axis(1) #gets the y value of our joystick
    throttle = (-(joystick.get_axis(3)-1))/2 #Gets the position of our throttle and converts from a -1 to 1 range to a percentage
    if(y > deadzone and get_brake == False): #determines if y is above the deadzone and we're not braking
        speed = -(y-deadzone)*(1000)*ratio*throttle*maxspeed #makes our speed a positive value in percentage of area outside the deadzone
    elif(y < -deadzone and get_brake == False): #determines if y is below the deadzone and we're not braking
        speed = -(y+deadzone)*(1000)*ratio*throttle*maxspeed #makes our speed a negative value in percentage of the area outside the deadzone
    else:
        speed = 0 #sets speed to 0 while in the deadzone
    return speed

def get_tspeed():
    x = joystick.get_axis(0) #gets the x value of our joystick
    if(x > deadzone): #determines if x is above the deadzone
        speed = -(x-deadzone)*(1000)*ratio*maxturn #spins our wheels at the positive perccentage of our max turn speed our joystick gives
    elif(x < -deadzone): #determines if x is below the deadzone 
        speed = -(x+deadzone)*(1000)*ratio*maxturn #spins our wheels at the negative perccentage of our max turn speed our joystick gives
    else:
        speed = 0 #sets the spin speed to 0 while in the deadzone
    return speed

while 1==1: #A loop for you to set motor values inside of.


    pygame.time.Clock().tick(1)#updates at a set speed. Number value is updates per second.