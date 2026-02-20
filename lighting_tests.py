import board
import neopixel
import time

NUM_LEDS   = 160
BRIGHTNESS = 0.4

strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

### _________________________________ Helper functions

def all_off():
    strip.fill((0, 0, 0))
    strip.show()


### _________________________________ Feature functions

def photo_countdown():
    # --- White chase along the outside for ~5 seconds ---
    chase_duration = 5.0
    chase_start = time.time()
    tail = 8

    while time.time() - chase_start < chase_duration:
        for i in range(NUM_LEDS):
            strip.fill((0, 0, 0))
            for t in range(tail):
                idx = (i - t) % NUM_LEDS
                brightness_scale = (tail - t) / tail
                val = int(255 * brightness_scale)
                strip[idx] = (val, val, val)
            strip.show()
            time.sleep(0.02)
            if time.time() - chase_start >= chase_duration:
                break

    # --- Flash red twice ---
    for _ in range(2):
        strip.fill((255, 0, 0))
        strip.show()
        time.sleep(0.4)
        strip.fill((0, 0, 0))
        strip.show()
        time.sleep(0.2)

    # --- Flash yellow twice ---
    for _ in range(2):
        strip.fill((255, 180, 0))
        strip.show()
        time.sleep(0.4)
        strip.fill((0, 0, 0))
        strip.show()
        time.sleep(0.2)

    # --- Flash green twice ---
    for _ in range(2):
        strip.fill((0, 255, 0))
        strip.show()
        time.sleep(0.4)
        strip.fill((0, 0, 0))
        strip.show()
        time.sleep(0.2)

    # --- Rapid white fill across the strip ---
    for i in range(0, NUM_LEDS, 8):
        for j in range(i, min(i + 8, NUM_LEDS)):
            strip[j] = (255, 255, 255)
        strip.show()
        time.sleep(0.02)

    # Hold full white (photo is being taken here)
    time.sleep(1.5)

    # Fade out
    for val in range(255, -1, -5):
        strip.fill((val, val, val))
        strip.show()
        time.sleep(0.01)

    all_off()


# def next_feature():
#     pass


### _________________________________ Run all tests

def run_all_tests():
    print("Photo countdown..."); photo_countdown()
    # print("Next feature..."); next_feature()
    print("All tests done!"); all_off()


run_all_tests()
