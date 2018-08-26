import board
from digitalio import DigitalInOut, Direction, Pull
import time
import neopixel
import random

button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

NUMPIXELS = 12
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.2, auto_write=False)

colour = [127, 0, 127] # start colour
patterns = [
  # 'wheel',
  'chase',
  'bounce',
  'knight_rider',
  'jump_around'
]
pattern_index = random.randrange(len(patterns))
# pattern_index = 4
shade_step = 16 # how much the colour wanders around
pattern = patterns[pattern_index]

######################### HELPERS ##############################

# Helper to give us a nice color swirl
def wheel(pos):
  # Input a value 0 to 255 to get a color value.
  # The colours are a transition r - g - b - back to r.
  if (pos < 0) or (pos > 255):
    return (0, 0, 0)
  if pos < 85:
    return (int(255 - pos*3), int(pos*3), 0)
  elif pos < 170:
    pos -= 85
    return (0, int(255 - (pos*3)), int(pos*3))
  else:
    pos -= 170
    return (int(pos*3), 0, int(255 - pos*3))

def tail(colour, offset = 0):
  multiplier = 1.0
  for p in range(NUMPIXELS):
    neopixels[(p + offset) % NUMPIXELS] = fade(colour, multiplier)
    multiplier = multiplier * 0.9
  neopixels.show()

def fade(colour, amount):
  return list(map(lambda c: round(c * amount), colour))

def shade(colour):
  increment = shade_step
  index = random.randrange(3)
  component = colour[index]
  if component < (increment):
    component += increment
  elif component > (255 - increment):
    component -= increment
  else:
    component += random.randrange(-1, 2) * increment
  colour[index] = component

  return colour

def whole_ring(colour):
  for p in range(NUMPIXELS):
    neopixels[p] = colour
  neopixels.show()

def blank():
  whole_ring([0, 0, 0])

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

def jump_around(colour):
  whole_ring(fade(colour, 0.3))
  for i in range(random.randrange(1, 5)):
    neopixels[random.randrange(12)] = colour
  neopixels.show()
  time.sleep(0.05)

######################### MAIN LOOP ##############################

# i = 0

while True:
  colour = shade(colour)
  if pattern == 'chase':
    for p in [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
      tail(colour, p)

  # if pattern == 'wheel':
  #   for p in range(NUMPIXELS):
  #     idx = int ((p * 256 / NUMPIXELS) + i)
  #     neopixels[p] = wheel(idx & 255)
  #   neopixels.show()

  if pattern == 'bounce':
    factor = 1.0
    while factor > 0.05:
      whole_ring(fade(colour, factor))
      factor *= 0.95

  if pattern == 'knight_rider':
    knight_rider(colour)

  if pattern == 'jump_around':
    jump_around(colour)

  if not button.value:
    pattern_index += 1
    if pattern_index >= len(patterns):
      pattern_index = 0
    pattern = patterns[pattern_index]
    time.sleep(0.5)

  # i = (i+1) % 256  # run from 0 to 255 # only useful for `wheel`
