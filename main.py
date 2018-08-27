import time
from helpers import *

colour = [127, 0, 127] # start colour
patterns = []

def chase(colour):
  for p in [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
    tail(colour, p)
patterns.append(chase)

def bounce(colour):
  factor = 1.0
  while factor > 0.05:
    whole_ring(fade(colour, factor))
    factor *= 0.95
patterns.append(bounce)

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

def jump_around(colour):
  whole_ring(fade(colour, 0.3))
  for i in range(random.randrange(1, 5)):
    neopixels[random.randrange(12)] = colour
  neopixels.show()
  time.sleep(0.05)
patterns.append(jump_around)

def rain(colour):
  whole_ring(fade(colour, 0.2))
  neopixels[random.randrange(12)] = colour
  neopixels.show()
  time.sleep(random.randrange(10) * 0.1)
patterns.append(rain)

def fill_up(colour):
  lights = set()
  while len(lights) < 12:
    index = random.randrange(12)
    neopixels[index] = colour
    neopixels.show()
    lights.add(index)
    time.sleep(0.1)
  time.sleep(0.5)
  bounce(colour)
patterns.append(fill_up)


######################### MAIN LOOP ##############################

whole_ring(colour)
pattern_index = random.randrange(len(patterns))

while True:
  colour = shade(colour)
  patterns[pattern_index](colour)

  if not button.value:
    pattern_index += 1
    if pattern_index >= len(patterns):
      pattern_index = 0
    pattern = patterns[pattern_index]
    time.sleep(0.5)
