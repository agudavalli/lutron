import sys

import board
import neopixel
import time
import math

NUM_LEDS   = 160
BRIGHTNESS = 0.4

strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# _________________________________________ Camera

# Corner references (for future patterns):
# Bottom right: 134, Bottom left: 98, Top left: 57, Top right: 31
# LED 0 is just above bottom right, going counterclockwise

CORNER_BOTTOM_RIGHT = 124
CORNER_BOTTOM_LEFT  = 98
CORNER_TOP_LEFT     = 57
CORNER_TOP_RIGHT    = 31
NUM_VISUAL_LEDS     = 134  # 0-133, with 134-144 mirroring 0-10

def show(strip):
    for i in range(11):
        strip[134 + i] = strip[i]
    strip.show()

def photo_countdown(strip):
    # Colors: (dim background, bright train)
    phases = [
        ((80, 0, 0),    (255, 0, 0)),    # red
        ((80, 60, 0),   (255, 190, 0)),  # yellow
        ((0, 80, 0),    (0, 255, 0)),    # green
    ]

    phase_duration = 1.2   # seconds per color phase (3 phases = 3.6s total)
    train_length   = 3
    total_leds     = 134   # visual LEDs 0-133

    # Train travels clockwise = decreasing index (since LEDs go counterclockwise by index)
    # One full rotation over all 3 phases combined
    total_steps    = total_leds
    total_time     = phase_duration * 3
    step_delay     = total_time / total_steps

    start_time = time.time()

    for step in range(total_steps):
        elapsed       = time.time() - start_time
        phase_index   = min(int(elapsed / phase_duration), 2)
        bg_color, train_color = phases[phase_index]

        # Fill background
        for i in range(total_leds):
            strip[i] = bg_color

        # Draw train (clockwise = decreasing index, wrapping)
        for t in range(train_length):
            pos = (total_leds - 1 - step - t) % total_leds
            strip[pos] = train_color

        show(strip)

        # Sleep until next step is due
        next_step_time = start_time + (step + 1) * step_delay
        sleep_time     = next_step_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

    # White rapid flash x4 over 0.75 seconds
    flash_on_time  = 0.075
    flash_off_time = 0.1125
    for _ in range(4):
        for i in range(total_leds):
            strip[i] = (255, 255, 255)
        show(strip)
        time.sleep(flash_on_time)

        for i in range(total_leds):
            strip[i] = (0, 0, 0)
        show(strip)
        time.sleep(flash_off_time)

# _______________________________________________ Words of affirmation rainbow

def affirmation_rainbow(strip):
    duration = 10  # seconds, adjust as needed

    total_leds = 134
    band_width = 5

    # 7 rainbow colors in discrete bands
    rainbow_colors = [
        (255, 0, 0),    # red
        (255, 60, 0),   # orange
        (255, 220, 0),  # yellow
        (0, 255, 0),    # green
        (0, 100, 255),  # blue
        (80, 0, 255),   # indigo
        (200, 0, 255),  # violet
    ]

    total_colors = len(rainbow_colors)
    pattern_length = total_colors * band_width  # 35 LEDs = one full rainbow cycle

    step_delay = 0.5  # seconds per 1 LED shift clockwise, adjust for speed
    total_steps = int(duration / step_delay)

    for step in range(total_steps):
        for i in range(total_leds):
            # Clockwise = shift offset increases over time
            # Reverse index for clockwise direction
            pos = (total_leds - 1 - i + step) % pattern_length
            color_index = (pos // band_width) % total_colors
            strip[i] = rainbow_colors[color_index]

        show(strip)
        time.sleep(step_delay)

    # Leave strip dark on exit
    for i in range(total_leds):
        strip[i] = (0, 0, 0)
    show(strip)

# ___________________________________________________________
# Calendar Breathing White

def calendar_breathing(strip):
    duration = 10  # seconds, adjust as needed

    total_leds = 134
    breath_period = 3  # seconds per full breath cycle, adjust as needed

    start_time = time.time()

    while time.time() - start_time < duration:
        elapsed = time.time() - start_time

        # Sine wave oscillates -1 to 1, shift and scale to 0.2-1.0 brightness range
        brightness = 0.6 + 0.4 * math.sin(2 * math.pi * elapsed / breath_period)
        # 0.6 center + 0.4 amplitude gives range of 0.2 to 1.0

        val = int(255 * brightness)
        for i in range(total_leds):
            strip[i] = (val, val, val)

        show(strip)
        time.sleep(0.05)  # 20fps update rate, smooth enough for a slow fade

    # Leave strip dark on exit
    for i in range(total_leds):
        strip[i] = (0, 0, 0)
    show(strip)
