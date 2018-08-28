import time
from helpers import *

colour = [250, 129, 0] # start colour
patterns = []

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
patterns.append(Chase)

class Bounce(Pattern):
    factor = 1.0
    def step(self):
        whole_ring(fade(colour, self.factor))
        self.factor *= 0.95
        if self.factor < 0.05:
            self.factor = 1.0
patterns.append(Bounce)

class KnightRider(Pattern):
    delay = 0.07
    pairs = [
        (0, 11), (1, 10), (2, 9),
        (3, 8), (4, 7), (5, 6)
    ]
    direction = 'left'
    i = 0

    def step(self):
        if self.direction == 'left':
            self.work(1)
            if self.i >= len(self.pairs) - 1:
                self.direction = 'right'

        if self.direction == 'right':
            self.work(-1)
            if self.i == 0:
                self.direction = 'left'

    def work(self, increment):
        self.light_pair(self.pairs[self.i])
        self.i += increment
        neopixels.show()
        time.sleep(self.delay)
        whole_ring(fade(self.colour, 0.1))

    def light_pair(self, pair):
        for light in pair:
            neopixels[light] = self.colour
patterns.append(KnightRider)

class JumpAround(Pattern):
    def step(self):
        whole_ring(fade(self.colour, 0.3))
        for i in range(random.randrange(1, 5)):
            neopixels[random.randrange(12)] = self.colour
            neopixels.show()
            time.sleep(0.05)
patterns.append(JumpAround)

class Rain(Pattern):
    def step(self):
        whole_ring(fade(self.colour, 0.2))
        neopixels[random.randrange(12)] = colour
        neopixels.show()
        time.sleep(random.randrange(10) * 0.1)
patterns.append(Rain)

class FillUp(Pattern):
    lights = set()

    def step(self):
        if len(self.lights) == 12:
            time.sleep(0.2)
            whole_ring(fade(self.colour, 0.3))
            self.lights = set()
        index = random.randrange(12)
        neopixels[index] = self.colour
        neopixels.show()
        self.lights.add(index)
        time.sleep(0.1)
patterns.append(FillUp)

######################### MAIN LOOP ##############################

whole_ring(colour)
pattern_index = random.randrange(len(patterns))
f = patterns[pattern_index](colour)

while True:
    colour = shade(colour)
    f.step()

    if not button.value:
        new_index = pattern_index
        while new_index == pattern_index:
            new_index = random.randrange(len(patterns))
        pattern_index = new_index
        f = patterns[pattern_index](colour)
        print(patterns[pattern_index])
        time.sleep(0.5)
