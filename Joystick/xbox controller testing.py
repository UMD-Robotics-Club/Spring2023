import pygame


# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# -------- Main Program Loop -----------
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.

    #
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # For each joystick:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    x = joystick.get_axis(0)
    y = joystick.get_axis(1)
    throttle = (-(joystick.get_axis(3)-1))/2
    brake = joystick.get_button(0)
    deadzone = 0.3
    ratio = 10/(10*(1-deadzone))
    
    speed = 0
    if(y > deadzone and brake == 0):
        speed = -(y-deadzone)*(100)*ratio*throttle
    elif(y < -deadzone and brake == 0):
        speed = -(y+deadzone)*(100)*ratio*throttle
    
    angle = 0
    if(x > deadzone):
        angle = -(x-deadzone)*(60)*ratio
    elif(x < -deadzone):
        angle = -(x+deadzone)*(60)*ratio
    
    # WHEEL TURN ANGLE VALUES
    textPrint.tprint(screen, "Turn Angle: {:3.2f}° Clockwise".format(angle))

    # READ MOTOR SPEED VALUES
    textPrint.tprint(screen, "Speed: {:5.2f}%".format(speed))
   
    # BRAKE VALUES
    if(brake == 1):
        textPrint.tprint(screen, "Braking")
    else:
        textPrint.tprint(screen, "Not Braking")

    
    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()