from digitalio import DigitalInOut, Direction, Pull
import neopixel
import board
import random

NUMPIXELS = 12
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.2, auto_write=False)
shade_step = 16 # how much the colour wanders around

button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

def fade(colour, amount):
  return list(map(lambda c: round(c * amount), colour))

def tail(colour, offset = 0):
  multiplier = 1.0
  for p in range(NUMPIXELS):
    neopixels[(p + offset) % NUMPIXELS] = fade(colour, multiplier)
    multiplier = multiplier * 0.9
  neopixels.show()

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
