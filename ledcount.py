import board
import neopixel

NUM_LEDS   = 160
BRIGHTNESS = 0.4

strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# Light up LED 140 in white
# 134 for switchover back to first LED 
# 145 for total LED count
# Bottom Right Corner, 124
# Bottom Left Corner, 98
# Top Left Corner, 57
# Top Right Corner, 31
strip[134] = (255, 255, 255)
strip.show()
