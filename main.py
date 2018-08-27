import time
from helpers import *

colour = [250, 129, 0] # start colour
patterns = []
classes = []

class Pattern:
    def __init__(self, colour):
        self.colour = colour

class Chase(Pattern):
    lights = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    index = 0

    def step(self):
        tail(self.colour, self.lights[self.index])
        self.index += 1
        if self.index > 11:
            self.index = 0
classes.append(Chase)

class Bounce(Pattern):
    factor = 1.0
    def step(self):
        whole_ring(fade(colour, self.factor))
        self.factor *= 0.95
        if self.factor < 0.05:
            self.factor = 1.0
classes.append(Bounce)

def knight_rider(colour):
    delay = 0.07
    pairs = [
        (0, 11), (1, 10), (2, 9),
        (3, 8), (4, 7), (5, 6)
    ]

    i = 0
    while i < len(pairs) - 1:
        for light in pairs[i]:
            neopixels[light] = colour
        i += 1
        neopixels.show()
        time.sleep(delay)
        whole_ring(fade(colour, 0.1))

    colour = shade(colour)

    while i > 0:
        for light in pairs[i]:
            neopixels[light] = colour
        i -= 1
        neopixels.show()
        time.sleep(delay)
        whole_ring(fade(colour, 0.1))
patterns.append(knight_rider)

class JumpAround(Pattern):
    def step(self):
        whole_ring(fade(self.colour, 0.3))
        for i in range(random.randrange(1, 5)):
            neopixels[random.randrange(12)] = self.colour
            neopixels.show()
            time.sleep(0.05)
classes.append(JumpAround)

class Rain(Pattern):
    def step(self):
        whole_ring(fade(self.colour, 0.2))
        neopixels[random.randrange(12)] = colour
        neopixels.show()
        time.sleep(random.randrange(10) * 0.1)
classes.append(Rain)

class FillUp(Pattern):
    lights = set()

    def step(self):
        if len(self.lights) == 12:
            bounce(self.colour)
            self.lights = set()
        index = random.randrange(12)
        neopixels[index] = self.colour
        neopixels.show()
        self.lights.add(index)
        time.sleep(0.1)
classes.append(FillUp)

######################### MAIN LOOP ##############################

whole_ring(colour)
pattern_index = random.randrange(len(classes))
f = classes[pattern_index](colour)

while True:
    colour = shade(colour)
    f.step()

    if not button.value:
        print("Button")
        pattern_index += 1
        if pattern_index >= len(classes):
            pattern_index = 0
        f = classes[pattern_index](colour)
        print(classes[pattern_index])
        time.sleep(0.5)
