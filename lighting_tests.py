import board
import neopixel
import time
import math

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

### ___________________________________________ Flashing lights music test

def flashing_lights():
    # 90 BPM = one beat every 0.667s, each color holds for one beat then crossfades to the next
    colors = [
        (148, 0,   211),  # purple
        (0,   0,   255),  # blue
        (255, 255, 255),  # white
    ]
    beat      = 60 / 90        # 0.667s per beat
    duration  = 30             # total seconds
    steps     = 40             # crossfade steps per beat
    step_time = beat / steps

    start     = time.time()
    color_idx = 0

    while time.time() - start < duration:
        c1 = colors[color_idx % len(colors)]
        c2 = colors[(color_idx + 1) % len(colors)]

        for s in range(steps):
            if time.time() - start >= duration:
                break
            t = s / steps
            # ease in-out for a punchy strobe feel rather than a linear crossfade
            t_eased = t * t * (3 - 2 * t)
            r = int(c1[0] + (c2[0] - c1[0]) * t_eased)
            g = int(c1[1] + (c2[1] - c1[1]) * t_eased)
            b = int(c1[2] + (c2[2] - c1[2]) * t_eased)
            strip.fill((r, g, b))
            strip.show()
            time.sleep(step_time)

        color_idx += 1

    all_off()


# def next_feature():
#     pass


### _________________________________ Run all tests

def run_all_tests():
    print("Photo countdown..."); photo_countdown()
    print("Flashing lights..."); flashing_lights()
    # print("Next feature..."); next_feature()
    print("All tests done!"); all_off()


run_all_tests()


#     pass
