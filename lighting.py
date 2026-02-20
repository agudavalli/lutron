import board
import neopixel

NUM_LEDS   = 160
BRIGHTNESS = 0.4

strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

strip.fill((255, 0, 0))
strip.show()
