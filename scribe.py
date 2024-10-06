import os
import time
from termcolor import colored
import math

# This is the Canvas class. It defines some height and width, and a 
# matrix of characters to keep track of where the TerminalScribes are moving
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the 
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    # Clear the terminal (used to create animation)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))
            
    

class TerminalScribe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.1
        self.pos = [0, 0]
        
        self.direction = [0, 1]
        
    def setDegrees(self, degrees):
        radians = (degrees/180) * math.pi 
        self.direction = [math.sin(radians), -math.cos(radians)]
        
    def setPosition(self, pos):
        self.pos = pos

    def up(self):
        self.direction = [0, -1]
        self.forward()

    def down(self):
        self.direction = [0, 1]
        self.forward()
        
    def right(self):
        self.direction = [1, 0]
        self.forward()
        
    def left(self):
        self.direction = [-1, 0]
        self.forward()
        
    def forward(self):
        pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def draw(self, pos):
        # Set the old position to the "trail" symbol
        self.canvas.setPos(self.pos, self.trail)
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)
    
    def drawSquare(self, size):
        
        for i in range(size):
            self.right()    
        for i in range(size):
            self.down()    
        for i in range(size):
            self.left()    
        for i in range(size):
            self.up()    

canvas = Canvas(30, 30)

scribes = [
    {'degrees': 30, 'position': [15,15], 'instructions': [
        {'function':'forward', 'duration': 100}
        ]},
    {'degrees': 135, 'position': [0, 0], 'instructions': [
        {'function':'forward', 'duration': 10},
        {'function':'down', 'duration': 2},
        {'function':'right', 'duration': 20},
        {'function':'down', 'duration': 2}
        ]},
    {'degrees': 180, 'position': [15, 0], 'instructions': [
        {'function':'down', 'duration': 10},
        {'function':'left', 'duration': 10},
        {'function':'drawSquare', 'size': 9},
        ]},
    {'degrees': 180, 'position': [20,20], 'instructions': [
        {'function':'drawSquare', 'size': 10},
        {'function':'drawSquare', 'size': 9},
        ]}
]

for scribeData in scribes:
    scribeData['scribe'] = TerminalScribe(canvas)
    scribeData['scribe'].setDegrees(scribeData['degrees'])
    scribeData['scribe'].setPosition(scribeData['position'])

    # Flatten instructions:
    # Convert "{'left': 10}" to ['left', 'left', 'left'...]
    scribeData['instructions_flat'] = []
    scribeData['square_sizes'] = []
    for instruction in scribeData['instructions']:
        if instruction['function'] == 'drawSquare':
            scribeData['square_sizes'].append(instruction['size'])
        else:
            scribeData['instructions_flat'] = scribeData['instructions_flat'] + [instruction['function']]*instruction['duration']
    
maxInstructionLength = max([len(scribeData['instructions_flat']) for scribeData in scribes])

for i in range(maxInstructionLength):
    for scribeData in scribes:
        if i < len(scribeData['instructions_flat']):
            if scribeData['instructions_flat'][i] == 'forward':
                scribeData['scribe'].forward()
            elif scribeData['instructions_flat'][i] == 'up':
                scribeData['scribe'].up()
            elif scribeData['instructions_flat'][i] == 'down':
                scribeData['scribe'].down()
            elif scribeData['instructions_flat'][i] == 'left':
                scribeData['scribe'].left()
            elif scribeData['instructions_flat'][i] == 'right':
                scribeData['scribe'].right()

for scribeData in scribes:
    if len(scribeData['square_sizes']) == 0:
        continue
    for size in scribeData['square_sizes']:
        scribeData['scribe'].drawSquare(size)

