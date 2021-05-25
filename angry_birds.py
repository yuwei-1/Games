import numpy as np
from vpython import sphere, color, rate, canvas, vector, curve, label, box, cross, mag, random, arrow, cylinder

###########################################################################################
#                                                                                         #
#                        ANGRY BIRDS CODE PHAS 0007 17TH JAN 2020                         #
#                                                                                         #
###########################################################################################
#                                                                                         #
#               Stating constants, defining variables and creating loop variables         #
#                                                                                         #
###########################################################################################

################ Firstly, I have defined any constants I will use in my code.##############

w = 0.5  # This is the thickness of the object we are trying to knock down.

m_ball = 0.1  # mass of the bird in kg

m_target = 100  # mass of the target object in kg

impact_t = 0.01  # the time impact lasts

g = 9.81  # gravitational acceleration, metres per seconds squared

dt = 0.0001  # time interval for loop animation, in seconds

##############Now i need to give some values to variables I will use in my game.###########

y = 0
# This is the y position of the ball. We set this to 0. When the bird is in motion this will change in order to model the
# movements of the bird. NB this is NOT the initial y position

x = 0  # Bird will initally start at position x = 0

Trestoring = m_target * g * (w / 2)  # this is calculating the restoring torque using equation

x_target = random() * 10 + 5
# random position for the target between x = 5 and x = 15. It works as random() gives a random
# number between 1 and 0 - so it can be treated as a percentage. Multiply this by 10 to get a point between 0 and 10
# Add 5 to move this range to 5 - 15

y0 = random() + 0.3
# generates a random height for platform ball is launched from between 0 to 1 metres. 0.3 is added
# to make sure the bird is not 'inside' the platform as python treats the bird as a point mass

################################   Loop variables   ######################################

retry = True
# When this retry is true, the game will continue to loop - asking the user to enter
# an angle and speed. We will set it to true when the user knocks the target down. Initially it is true to start off the loop

hit = False
# this variable will tell python when the user has hit the target. If the user does not hit the target, we
# want the ball to keep moving until it hits the floor.


##########################################################################################
#                                                                                        #
#                            Creating the environment                                    #
#                                                                                        #
##########################################################################################

scene = canvas(width=640, height=480, center=vector(8, 5, 0), range=8,
               background=color.blue)  # creating the world - blue to represent sky

ground = curve(pos=[(0, 0, 0), (16, 0, 0)], color=color.green)  # making the ground 16m long as specified

## The following objects do not interact with the game and are only for graphic purposes##

floor = box(pos=vector(0, -0.2, 0), length=1000, height=0.1, width=1000, color=color.green)
# adding grass
# I have made a very large box to represent the floor.

cloud1 = sphere(pos=vector(0, 12, -15), radius=2, color=color.white)  # big white spheres represent clouds
cloud2 = sphere(pos=vector(2, 12, -15), radius=2, color=color.white)
cloud3 = sphere(pos=vector(4, 12, -15), radius=2, color=color.white)
cloud4 = sphere(pos=vector(2, 13, -15), radius=2, color=color.white)

sun = sphere(pos=vector(30, 20, -20), radius=5, color=color.yellow)  # big yellow sphere to represent the sun

target = box(pos=vector(x_target, 1, 0), length=w, height=2, color=color.blue)
# Target created. x_target variable used so it spawns at a random point between 5m and 15m
# This is done before loop so it stays in the same position until user runs the game again

platform = cylinder(pos=vector(0, 0, 0), radius=0.5, axis=vector(0, y0, 0), color=vector(0.76, 0.456, 0.24))
# Platform created. y0 is used, so the platform spawns at a random height between 0 and 1.
# the colour represented by the vector is in RGB form and it is brown.

###########################################################################################
#                                                                                         #
#                            Creating graphics of bird                                    #
#                                                                                         #
###########################################################################################

ball = sphere(pos=vector(x, y0 + 0.3, 0), radius=0.3,
              color=color.red)  # create a ball which starts off at initial position
beak = arrow(pos=ball.pos, axis=vector(0.5, 0, 0), shaftwidth=0.1, color=color.yellow)
eyes = sphere(pos=ball.pos + vector(0.1, 0.18, 0.24), radius=0.05, color=color.black)
bird_label = label(pos=ball.pos + vector(0, 1, 0), text='Terence', height=25, color=color.white)

# The position of all the features of the bird are given as relative to the main body. I called the bird terence
# as a reference to the real angry birds game


# I have made the labels for when the user loses here but have made them invisible - this is to save me from writing
# unneccesary repeated code. It is shorter to write lose.visible than repeated writing the lines below.One is no_power. this
# label is for when the user hits the target but the bird does not have enough power.

lose = label(pos=vector(8, 8, 0), text='You missed the target! Please try again.', height=25, color=color.green)
no_power = label(pos=vector(8, 8, 0), text='Not enough power! Please try again.', height=25, color=color.green)
lose.visible = False
no_power.visible = False  # label is invisible to user

############################################################################################
#                                                                                          #
#                                    Main loop                                             #
#                                                                                          #
############################################################################################

while retry is True:

    scene.waitfor('redraw')

    # This line above is to allow python to synchronise updates in the code with the display
    # for my code it is to make sure the loss message appears after the user loses

    lose.visible = False
    no_power.visible = False
    # these lines are to remove any loss messages before the next attempt

    x0 = 0.0  # initial ball x-coordinate (metres)
    t = 0  # time reset to zero every time loop happens in order to reset position of bird in seconds
    y = y0

    x = x0
    # all variables reset each time code loops again so bird returns to normal position

    px = 0
    py = 0
    # momentum of bird reset to zero

    # input initial conditions (angle and speed)

    dtheta = float(input("Input the initial angle in degrees: "))
    theta = np.radians(dtheta)  # convertion of degrees into radians

    v0 = float(input("Input the initial speed in metres/second: "))
    # Here I have set the values of coordinates and speed equal to their initial values. Later the values will change as the
    # ball moves through the air

    v = v0
    momentum = arrow(pos=vector(x, y, 0), axis=vector(px, py, 0), shaftwidth=0.05, color=color.cyan)

    # we create the momentum arrow once per loop. We will use other imbedded loops to update its position, size and direction

    ###############################################################################################
    #                                                                                             #
    #                               CODE FOR MOTION OF BIRD                                       #
    #                                                                                             #
    ###############################################################################################

    while y >= 0.3 and hit is False:
        # the simulation will keep running until the ball touches the ground or user hits target
        rate(1000)
        t = t + dt
        # time increasing by small increments
        y = y0 + 0.3 + v * np.sin(theta) * t - 0.5 * g * t ** 2
        x = x0 + v * np.cos(theta) * t
        # position of bird calculated using equations in the introduction
        py = m_ball * v * np.sin(theta) - m_ball * g * t
        px = m_ball * v * np.cos(theta)

        # momentum of the bird calculated using eq in intro
        ball.pos = vector(x, y, 0)  # 'updating' the position of the bird
        momentum.pos = ball.pos  # making sure the momentum arrow stays with the bird
        momentum.axis = vector(px, py, 0)  # updating the size and direction of the momentum vector

        # making sure the features of the bird stay with the bird
        beak.pos = ball.pos
        eyes.pos = ball.pos + vector(0.1, 0.18, 0.24)
        bird_label.pos = ball.pos + vector(0, 1, 0)

        # equations to calculate applied torque same as in intro. This is placed here so the correct values are calculated
        # as y values change in next part of code.
        da = vector(-w, y, 0)
        Fapplied = vector(px, py, 0) / impact_t
        Tapplied = mag(cross(da, Fapplied))

        ################################################################################################
        #                                                                                              #
        #                          Calculating what happens to the bird                                #
        #                                                                                              #
        ################################################################################################

        # Code below decides what happens to the bird. There are 3 options. First, the ball collides with the left side
        # of the object. Second, the ball lands on top of the object. Last, the ball doesn't hit the object.

        if x_target - 0.55 < x < x_target + 0.55 and 0.3 < y < 2.3:
            # This if statement is for when the bird hits the left of the target
            hit = True
            # hit set to true so ball doesnt continue moving
            t = 0
            momentum.visible = False  # momentum arrow will disappear as the bird is not moving

            # while loop is for the animation of the bird falling to the ground
            while y >= 0.3:
                rate(1000)
                t = t + dt
                y = y - 0.5 * g * t ** 2  # free fall of an object due to gravity
                # again updating the features of the bird
                ball.pos = vector(x, y, 0)
                beak.pos = ball.pos
                eyes.pos = ball.pos + vector(0.1, 0.18, 0.24)
                bird_label.pos = ball.pos + vector(0, 1, 0)


        elif x_target - w / 2 < x < x_target + w / 2 and y == 2.3:
            # bird hits top of target. hit is true so bird doesnt keep moving
            hit = True
        else:
            # bird does not hit target so continues moving
            hit = False

    ###################      for the scenario that the bird hits target     ######################
    momentum.visible = False
    if hit is True:
        print('The height of impact of impact was', y, 'm')
        print('The momentum at point of impact was', np.sqrt(px ** 2 + py ** 2), 'kgm/s')
        print('The applied torque was', Tapplied, 'Nm')
        print('The magnitude of the restoring torque was', Trestoring, 'Nm')
        # all required print statements are displayed here. They will only print if there is a collision

        # if statement decides if the target topples or not
        if Tapplied > Trestoring:
            target.rotate(angle=-np.pi / 2, axis=vector(0, 0, 1), origin=vector(x_target + 0.25, 0, 0))
            # if target is hit, the target will 'topple'. rotate function is used here.The target will rotate 90 degrees clockwise
            t = 0
            # Repeated while loop from previous code - for the animation of the bird freefalling
            while y >= 0.3:
                rate(1000)
                t = t + dt
                y = y - 0.5 * g * t ** 2
                ball.pos = vector(x, y, 0)
                beak.pos = ball.pos
                eyes.pos = ball.pos + vector(0.1, 0.18, 0.24)
                bird_label.pos = ball.pos + vector(0, 1, 0)
            # target is topples, so user wins. End entire loop by setting retry to false
            retry = False
            win = label(pos=vector(8, 8, 0), text='You toppled the object! YOU WIN!', height=25, color=color.green)
        # display win label
        else:  # if not enough power, this will be displayed to the user. Hit is set to false for the next loop
            no_power.visible = True
            hit = False
    else:  # user misses, and is told where the bird landed.
        print('The bird has landed at', x, 'm')
        lose.visible = True
        hit = False
