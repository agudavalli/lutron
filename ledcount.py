import board
import neopixel

NUM_LEDS   = 160
BRIGHTNESS = 0.4

strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# Light up LED 140 in white
strip[135] = (255, 255, 255)
strip.show()
