#Importing our libraries
import turtle
import random
import time

#Creating all the turtles to be used:

#Player that we move around
player = turtle.Turtle()

#Border drawer
border = turtle.Turtle()

#Creates apples to be eaten by player
appleCreator = turtle.Turtle()

#Writes out countdown and score
textWriter = turtle.Turtle()

#Writes out timer
timeWriter = turtle.Turtle()

#List of colors for turtle to randomly select after eating a dot
colors = ["red", "green", "blue", "orange", "purple", "pink", "yellow"]

#
screen = player.getscreen()
screen.bgcolor("black")

#Setting up our turtles
#Setting up player
player.shape("turtle")
player.color("pink")
player.penup()
#Setting up border drawer.
border.color("blue")
border.ht()
#Setting up apple creator
appleCreator.ht()
#Setting up text writer
textWriter.color("yellow")
textWriter.ht()
#Setting up timer writer
timeWriter.color("yellow")
timeWriter.ht()

#Tracks player score for text writer to write on the left side of the screen
playerScore = 0

#Determines player base movement speed
playerSpeed = 0.5

#Turns the player left
def turn_left():
    player.left(90)

#Turns the player right
def turn_right():
    player.right(90)

#Draws border after countdown at beginning of game. x and y can be altered to change the size of the border rectangle
def draw_border(x, y):
    #Positioning at corner
    border.penup()
    border.setpos(x, y)
    border.pendown()
    #Drawing the border
    border.setpos(x, y)
    border.setpos(x, -y)
    border.setpos(-x, -y)
    border.setpos(-x, y)
    border.setpos(x, y)

#Creates a certain number of apples in a rectangle at random positions for the player to eat.
def createApples(xRange, yRange, apples):
    #creates an empty array to store apple locations in.
    applesPos = []
    #repeats loop for as many apples as are needed
    for i in range(0, apples):
        appleCreator.penup()
        #Goes to random location in bounds
        appleCreator.goto(random.randint(-xRange, xRange), random.randint(-yRange, yRange))
        appleCreator.pendown()
        #Draws apple
        appleCreator.dot(3, "gold")
        #Appends (puts at back of array) the position of the apple for later use
        #The position is a Vec2D, a tuple containing two floats.
        applesPos.append(appleCreator.pos())
    #Returns the array of Vec2Ds representing the apple positions
    return applesPos

#Plays the countdown animation at the start of the game
def countdown(countdownLength):
    #Input a string representing the countdown as "XYZ"
    #For example, "321" or "54321"
    for i in countdownLength:
        #Writes the countdown out, erasing textWriter's text each time.
        textWriter.write(i, False, align="center", font=("Arial", 40, "normal"))
        time.sleep(1)
        textWriter.clear()

#Detects collisions between apples and the player
def collisionDetection(turtlePos, appleLocationsArr, boxWidth, boxHeight):
    #Creates a temporary score boost to be added to the total score later
    tempScore = 0
    #For each Vec2D (remember, a tuple with two floats, X and Y) representing an apple location...
    for i in appleLocationsArr:
        #If the Vec2D's x-coordinate is within the extents of the player's hitbox's x-coordinates...
        if turtlePos[0] - boxWidth <= i[0] <= turtlePos[0] + boxWidth:
            #If the Vec2D's y-coordinate is within the extents of the player's hitbox's y-coordinates also..
            if turtlePos[1] - boxHeight <= i[1] <= turtlePos[1] + boxHeight:
                #Remove the apple Vec2D we are currently using from the the list of apple locations
                appleLocationsArr.remove(i)
                #Overwrites the dot  by moving the apple creator to the removed dot's location and drawing a black dot on top of it
                appleCreator.goto(i)
                appleCreator.dot(3)
                #Increments the temporary score to be added later
                tempScore += 1
                #Switches the player's color
                player.color(random.choice(colors))
    #Returns the temporary score so that it can increment the total score
    return tempScore

#Checks to make sure that the player is inside the borders, and wraps it if it is not
def borderCheck(turtlePos, borderWidth, borderHeight):
    #If it's outside the horizontal sides of the box, wrap it over to the other side
    if abs(turtlePos[0])> borderWidth:
        player.ht()
        player.setpos(turtlePos[0]*-1, turtlePos[1])
        player.st()
    #If it's outside the vertical sides of the box, wrap it over to the other side
    elif abs(turtlePos[1]) > borderHeight:
        player.ht()
        player.setpos(turtlePos[0], turtlePos[1]*-1)
        player.st()



#Setup of the game--counting down, drawing the border, and spawning the apples
countdown("321")
draw_border(120, 120)
appleLocations = createApples(110, 110, 10)

#Setting the apple creator's color to black so it can be used to delete apples
appleCreator.color("black")

#Moving the text writer outside of the borders so it can begin to write out the score
textWriter.penup()
textWriter.goto(-140, 0)
textWriter.pendown()
textWriter.write("0", False, align="center", font=("Arial", 20, "normal"))

#Moving the time writer outside of the borders so it can begin to write out the time
timeWriter.penup()
timeWriter.goto(140, 0)
timeWriter.pendown()
timeWriter.write("50", False, align="center", font=("Arial", 20, "normal"))

#Setting the time for the game to end to be 50 seconds from just before it starts

endTime = time.time() + 50

#Main game loop: runs for as long as there are apple locations within the list of apple locations
while len(appleLocations) > 0:
    #Moves player forward at base speed increased by the score (aka how many apples have been eaten)
    player.forward(playerSpeed + (playerScore/3))
    #Checks to see if player is outside of borders
    borderCheck(player.pos(), 120, 120)
    #Allows player to turn left/right once per loop
    screen.onkey(turn_left, "Left")
    screen.onkey(turn_right, "Right")
    #Detects input for left/right turns
    screen.listen()
    #Increments player score and runs collisions once per loop
    playerScore += collisionDetection(player.pos(), appleLocations, 10, 10)
    #Writes out score and time remaining.
    textWriter.clear()
    textWriter.write(str(playerScore), False, align="center", font=("Arial", 20, "normal"))
    timeWriter.clear()
    timeWriter.write(str(int(endTime-time.time())), False, align="center", font=("Arial", 20, "normal"))

#Prints out final score because why not!
#Hiding turtles to look nicer
player.clear()
player.ht()
border.clear()
textWriter.clear()
timeWriter.clear()
#Writing text
timeWriter.penup()
textWriter.penup()
textWriter.goto(0, 0)
timeWriter.goto(0, 25)
timeWriter.pendown()
textWriter.pendown()
timeWriter.write("Final Score:", False, align="center", font=("Arial", 20, "normal"))
textWriter.write(str(playerScore), False, align="center", font=("Arial", 20, "normal"))
#Delay to enjoy it
time.sleep(5)

