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

# ______________________________________________________________________
# Flashing Lights - Kanye West

def flashing_lights_kanye(strip):
    import random

    total_leds = 134
    BPM = 90
    beat_interval = 60 / BPM  # ~0.667 seconds per beat

    # --- Color palette ---
    PURPLE_DIM    = (40, 0, 60)
    PURPLE_MID    = (80, 0, 120)
    PURPLE_BRIGHT = (140, 0, 200)
    PINK          = (180, 0, 140)
    VIOLET        = (100, 0, 255)
    WHITE         = (255, 255, 255)
    WHITE_DIM     = (80, 80, 80)
    OFF           = (0, 0, 0)

    # --- Timestamps ---
    T_BASS        = 22.0
    T_VERSE1      = 42.0
    T_CHORUS1     = 83.0   # 1:23
    T_VERSE2      = 106.0  # 1:46
    T_CHORUS2     = 147.0  # 2:27
    T_BREAKDOWN   = 191.0  # 3:11
    T_FLASH       = 202.0  # 3:22
    T_OUTRO       = 212.0  # 3:32
    T_END         = 237.0  # 3:57

    # --- Helper: fill all LEDs one color ---
    def fill(color):
        for i in range(total_leds):
            strip[i] = color

    # --- Helper: add random sparkles ---
    def add_sparkles(count, color=WHITE):
        for _ in range(count):
            pos = random.randint(0, total_leds - 1)
            strip[pos] = color

    # --- Helper: beat pulse, full strip flashes bright then settles to base ---
    def beat_pulse(base_color, bright_color):
        fill(bright_color)
        show(strip)
        time.sleep(0.08)
        fill(base_color)

    # --- State tracking ---
    start_time     = time.time()
    last_beat_time = start_time
    chase_step     = 0
    train_length   = 5
    sparkle_states = {}  # pos: (color, expiry_time)

    def get_section(t):
        if t < T_BASS:      return "intro"
        if t < T_VERSE1:    return "bass"
        if t < T_CHORUS1:   return "verse1"
        if t < T_VERSE2:    return "chorus1"
        if t < T_CHORUS2:   return "verse2"
        if t < T_BREAKDOWN: return "chorus2"
        if t < T_FLASH:     return "breakdown"
        if t < T_OUTRO:     return "flash"
        if t < T_END:       return "outro"
        return "done"

    while True:
        now     = time.time()
        elapsed = now - start_time
        section = get_section(elapsed)

        if section == "done":
            fill(OFF)
            show(strip)
            break

        beat_due = (now - last_beat_time) >= beat_interval

        # -------------------------------------------------------
        # INTRO: slow building purple pulse, no beat
        # -------------------------------------------------------
        if section == "intro":
            progress   = elapsed / T_BASS  # 0.0 to 1.0
            brightness = 0.1 + 0.4 * math.sin(math.pi * progress * 2)
            brightness = max(0.1, brightness)
            val_r = int(40 * brightness * 3)
            val_b = int(200 * brightness)
            val_g = 0
            fill((val_r, val_g, val_b))
            show(strip)
            time.sleep(0.05)

        # -------------------------------------------------------
        # BASS ENTERS: 90bpm pulse, dim purple, minimal sparkles
        # -------------------------------------------------------
        elif section == "bass":
            if beat_due:
                beat_pulse(PURPLE_DIM, PURPLE_MID)
                last_beat_time = now
                if random.random() < 0.3:
                    add_sparkles(2, WHITE_DIM)
            show(strip)
            time.sleep(0.03)

        # -------------------------------------------------------
        # VERSE 1: chase train + beat pulse + light sparkles
        # -------------------------------------------------------
        elif section == "verse1":
            if beat_due:
                beat_pulse(PURPLE_DIM, PURPLE_BRIGHT)
                last_beat_time = now
                chase_step = (chase_step + 8) % total_leds

            fill(PURPLE_DIM)
            # Clockwise chase train
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = PURPLE_BRIGHT

            # Light sparkles
            if random.random() < 0.4:
                add_sparkles(3, WHITE_DIM)

            show(strip)
            time.sleep(0.03)

        # -------------------------------------------------------
        # CHORUS 1: heavier sparkles, pink/violet, intense chase
        # -------------------------------------------------------
        elif section == "chorus1":
            if beat_due:
                beat_pulse(PURPLE_MID, VIOLET)
                last_beat_time = now
                chase_step = (chase_step + 10) % total_leds

            fill(PURPLE_MID)
            # Faster chase train in violet
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = VIOLET

            # Heavier sparkles, mix of white and pink
            if random.random() < 0.6:
                add_sparkles(5, WHITE)
            if random.random() < 0.4:
                add_sparkles(3, PINK)

            show(strip)
            time.sleep(0.03)

        # -------------------------------------------------------
        # VERSE 2: chase + beat pulse, moderate sparkles
        # -------------------------------------------------------
        elif section == "verse2":
            if beat_due:
                beat_pulse(PURPLE_DIM, PURPLE_BRIGHT)
                last_beat_time = now
                chase_step = (chase_step + 8) % total_leds

            fill(PURPLE_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = PURPLE_BRIGHT

            if random.random() < 0.5:
                add_sparkles(4, WHITE_DIM)
            if random.random() < 0.2:
                add_sparkles(2, PINK)

            show(strip)
            time.sleep(0.03)

        # -------------------------------------------------------
        # CHORUS 2: most intense, full white flashes, all colors
        # -------------------------------------------------------
        elif section == "chorus2":
            if beat_due:
                # Occasional full white flash on the beat
                if random.random() < 0.35:
                    fill(WHITE)
                    show(strip)
                    time.sleep(0.06)
                else:
                    beat_pulse(PURPLE_BRIGHT, VIOLET)
                last_beat_time = now
                chase_step = (chase_step + 12) % total_leds

            fill(PURPLE_MID)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = VIOLET

            if random.random() < 0.7:
                add_sparkles(7, WHITE)
            if random.random() < 0.5:
                add_sparkles(4, PINK)
            if random.random() < 0.3:
                add_sparkles(3, VIOLET)

            show(strip)
            time.sleep(0.03)

        # -------------------------------------------------------
        # BREAKDOWN: slow hypnotic pulse, minimal sparkles
        # -------------------------------------------------------
        elif section == "breakdown":
            progress  = (elapsed - T_BREAKDOWN) / (T_FLASH - T_BREAKDOWN)
            breathing = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * progress * 3))
            val_r = int(80 * breathing)
            val_b = int(160 * breathing)
            fill((val_r, 0, val_b))

            if random.random() < 0.1:
                add_sparkles(1, WHITE_DIM)

            show(strip)
            time.sleep(0.05)

        # -------------------------------------------------------
        # FLASHING LIGHTS SECTION: peak moment 3:22-3:32
        # Rapid white/purple strobe with violet bursts
        # -------------------------------------------------------
        elif section == "flash":
            progress = (elapsed - T_FLASH) / (T_OUTRO - T_FLASH)
            # Alternate rapidly between white strobe and deep purple
            strobe_interval = 0.08 - (0.03 * progress)  # speeds up slightly
            phase = int(elapsed / strobe_interval) % 4

            if phase == 0:
                fill(WHITE)
            elif phase == 1:
                fill(PURPLE_BRIGHT)
            elif phase == 2:
                fill(VIOLET)
                add_sparkles(10, WHITE)
            else:
                fill(OFF)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # OUTRO: gradual fade to dim pulse then dark
        # -------------------------------------------------------
        elif section == "outro":
            progress  = (elapsed - T_OUTRO) / (T_END - T_OUTRO)  # 0.0 to 1.0
            fade      = 1.0 - progress  # fades from 1.0 to 0.0
            breathing = 0.5 + 0.5 * math.sin(2 * math.pi * elapsed * 0.5)
            brightness = fade * (0.2 + 0.3 * breathing)

            val_r = int(40 * brightness * 3)
            val_b = int(200 * brightness)
            fill((val_r, 0, val_b))

            show(strip)
            time.sleep(0.05)


