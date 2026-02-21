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

def camera_flash(strip):
    # Rapid white strobe then hold for the shot
    for _ in range(6):
        strip.fill((255, 255, 255))
        show(strip)
        time.sleep(0.05)
        strip.fill((0, 0, 0))
        show(strip)
        time.sleep(0.05)

    # Hold full white for the actual shot
    strip.fill((255, 255, 255))
    show(strip)
    time.sleep(1.5)

    # Fade out
    for val in range(255, -1, -5):
        strip.fill((val, val, val))
        show(strip)
        time.sleep(0.01)


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

# __________________________
# GameCube Intro

def gamecube_intro(strip):
    import random

    total_leds = 134
    duration   = 7.0  # seconds total
    train_length = 4

    # --- Color palette for trail ---
    trail_colors = [
        (180, 0, 255),  # bright purple
        (140, 0, 200),  # mid purple
        (100, 0, 180),  # deep purple
        (200, 0, 180),  # purple-pink
        (255, 0, 180),  # hot pink-purple
        (220, 0, 140),  # pink
        (180, 0, 120),  # deep pink
        (255, 0, 220),  # light magenta
    ]

    TRAIN_COLOR = (220, 100, 255)  # bright leading purple
    OFF         = (0, 0, 0)

    # Train completes exactly one full loop in 7 seconds
    # Clockwise = decreasing index
    loop_steps  = total_leds
    step_delay  = (duration * 0.65) / loop_steps  # 65% of time for loop, rest for shimmer
    shimmer_duration = duration * 0.35

    # Track what color each LED was assigned as train passes
    trail = [OFF] * total_leds

    def fill(color):
        for i in range(total_leds):
            strip[i] = color

    # --- Phase 1: train sweeps clockwise leaving colored trail ---
    start_time = time.time()

    for step in range(loop_steps):
        # Assign a random trail color to the LED the train just left
        trail[( total_leds - 1 - step) % total_leds] = random.choice(trail_colors)

        # Draw trail
        for i in range(total_leds):
            strip[i] = trail[i]

        # Draw train on top
        for t in range(train_length):
            pos = (total_leds - 1 - step - t) % total_leds
            strip[pos] = TRAIN_COLOR

        show(strip)

        # Drift timing to avoid accumulation
        next_step_time = start_time + (step + 1) * step_delay
        sleep_time = next_step_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

    # --- Phase 2: shimmer/sparkle over the filled frame ---
    shimmer_start = time.time()

    while time.time() - shimmer_start < shimmer_duration:
        # Restore trail base
        for i in range(total_leds):
            strip[i] = trail[i]

        # Random sparkles from palette plus bright white flickers
        sparkle_count = random.randint(4, 10)
        for _ in range(sparkle_count):
            pos   = random.randint(0, total_leds - 1)
            if random.random() < 0.3:
                strip[pos] = (255, 255, 255)  # occasional white flash
            else:
                strip[pos] = random.choice(trail_colors)

        show(strip)
        time.sleep(0.07)

    # Leave strip in filled state on exit for clean transition
    for i in range(total_leds):
        strip[i] = trail[i]
    show(strip)

# ___________________________________________________________________________
# Piano Scale Egg Crack

def piano_scale_egg(strip):
    import random
    time.sleep(3.6)

    # --- Adjustable timing ---
    BPM           = 153  # adjust to match video
    note_duration = 60 / BPM  # seconds per note

    # --- Layout ---
    TOP_CENTER    = 44
    CORNER_BL     = 98
    CORNER_BR     = 124
    total_leds    = 134

    # --- C major scale 2 octaves up then down, 29 notes total ---
    # Each color maps to a scale degree, consistent across octaves
    note_colors = {
        'C':  (255, 50, 50),    # warm red
        'D':  (255, 140, 0),    # orange
        'E':  (255, 220, 0),    # yellow
        'F':  (0, 200, 80),     # green
        'G':  (0, 180, 255),    # sky blue
        'A':  (0, 60, 255),     # deep blue
        'B':  (160, 0, 255),    # violet
    }

    # Scale sequence: 2 octaves up then down
    scale_sequence = ['C','D','E','F','G','A','B','C','D','E','F','G','A','B','C',
                      'B','A','G','F','E','D','C','B','A','G','F','E','D','C']

    # Right drip: clockwise from top center (44) down to bottom right corner (124)
    right_path = []
    i = TOP_CENTER
    while True:
        right_path.append(i)
        if i == CORNER_BR:
            break
        i = (i - 1) % total_leds

    # Left drip: counterclockwise from top center (44) down to bottom left corner (98)
    left_path = []
    i = TOP_CENTER
    while True:
        left_path.append(i)
        if i == CORNER_BL:
            break
        i = (i + 1) % total_leds

    def fill_base():
        for i in range(total_leds):
            strip[i] = (255, 255, 255)

    # --- Initialize strip to white ---
    fill_base()
    show(strip)

    for note_index, note_name in enumerate(scale_sequence):
        color        = note_colors[note_name]
        note_start   = time.time()
        right_done   = False
        left_done    = False
        right_corner_flashed = False
        left_corner_flashed  = False

        right_steps = len(right_path)
        left_steps  = len(left_path)
        max_steps   = max(right_steps, left_steps)

        # Step delay so drip reaches corners in exactly one note duration
        step_delay = note_duration / max_steps

        for step in range(max_steps):
            # Paint right drip step
            if step < right_steps:
                strip[right_path[step]] = color
                if step == right_steps - 1 and not right_corner_flashed:
                    right_done = True

            # Paint left drip step
            if step < left_steps:
                strip[left_path[step]] = color
                if step == left_steps - 1 and not left_corner_flashed:
                    left_done = True

            show(strip)

            # Corner flash when drip hits
            if right_done and not right_corner_flashed:
                strip[CORNER_BR] = (255, 255, 255)
                show(strip)
                time.sleep(0.06)
                strip[CORNER_BR] = color
                right_corner_flashed = True

            if left_done and not left_corner_flashed:
                strip[CORNER_BL] = (255, 255, 255)
                show(strip)
                time.sleep(0.06)
                strip[CORNER_BL] = color
                left_corner_flashed = True

            # Drift-safe timing
            next_step_time = note_start + (step + 1) * step_delay
            sleep_time = next_step_time - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)

    # Hold final state briefly then return to white
    time.sleep(0.5)
    fill_base()
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

# ___________________________________________________________
# All of the Lights - Kanye West

def all_of_the_lights_kanye(strip):
    import random

    total_leds = 134
    BPM = 150
    beat_interval = 60 / BPM  # 0.4 seconds per beat

    # --- Color palette ---
    GOLD          = (255, 180, 0)
    GOLD_DIM      = (80, 50, 0)
    AMBER         = (255, 100, 0)
    AMBER_DIM     = (60, 25, 0)
    WHITE         = (255, 255, 255)
    WHITE_DIM     = (60, 60, 60)
    RED           = (255, 0, 0)
    ORANGE        = (255, 60, 0)
    CYAN          = (0, 255, 220)
    CYAN_DIM      = (0, 60, 55)
    BLUE          = (0, 80, 255)
    BLUE_DIM      = (0, 20, 80)
    ELECTRIC      = (100, 0, 255)
    OFF           = (0, 0, 0)

    # --- Timestamps ---
    T_RIHANNA     = 13.0
    T_BEAT        = 28.0
    T_CHORUS1     = 60.0
    T_VERSE2      = 90.0
    T_CHORUS2     = 120.0
    T_BRIDGE      = 150.0
    T_FINAL       = 180.0
    T_OUTRO       = 225.0
    T_END         = 300.0

    def fill(color):
        for i in range(total_leds):
            strip[i] = color

    def add_sparkles(count, color=WHITE):
        for _ in range(count):
            pos = random.randint(0, total_leds - 1)
            strip[pos] = color

    def beat_pulse(base_color, bright_color):
        fill(bright_color)
        show(strip)
        time.sleep(0.07)
        fill(base_color)

    def get_section(t):
        if t < T_RIHANNA:  return "trumpet"
        if t < T_BEAT:     return "rihanna"
        if t < T_CHORUS1:  return "verse1"
        if t < T_VERSE2:   return "chorus1"
        if t < T_CHORUS2:  return "verse2"
        if t < T_BRIDGE:   return "chorus2"
        if t < T_FINAL:    return "bridge"
        if t < T_OUTRO:    return "final"
        if t < T_END:      return "outro"
        return "done"

    start_time     = time.time()
    last_beat_time = start_time
    chase_step     = 0
    train_length   = 5

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
        # TRUMPET INTRO 0:00-0:13
        # Bright golds and whites, rapid horn energy
        # -------------------------------------------------------
        if section == "trumpet":
            progress = elapsed / T_RIHANNA
            # Rapid alternating flashes getting more intense
            strobe_interval = 0.12 - (0.05 * progress)
            phase = int(elapsed / strobe_interval) % 3

            if phase == 0:
                fill(WHITE)
            elif phase == 1:
                fill(GOLD)
            else:
                fill(AMBER)
                add_sparkles(8, WHITE)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # RIHANNA 0:13-0:28
        # Multi color chaos, strobing white/gold/red/orange
        # -------------------------------------------------------
        elif section == "rihanna":
            strobe_interval = 0.09
            phase = int(elapsed / strobe_interval) % 6

            colors = [WHITE, GOLD, RED, ORANGE, AMBER, WHITE]
            fill(colors[phase])
            if phase in [0, 5]:
                add_sparkles(12, GOLD)
            elif phase == 2:
                add_sparkles(8, WHITE)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # VERSE 1 0:28-1:00
        # 150bpm gold/amber base, white beat pulse, chase train
        # -------------------------------------------------------
        elif section == "verse1":
            if beat_due:
                beat_pulse(AMBER_DIM, GOLD)
                last_beat_time = now
                chase_step = (chase_step + 6) % total_leds

            fill(AMBER_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = GOLD

            if random.random() < 0.3:
                add_sparkles(3, WHITE_DIM)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # CHORUS 1 1:00-1:30
        # Gold/white base, cyan and blue burst in, energetic
        # -------------------------------------------------------
        elif section == "chorus1":
            if beat_due:
                if random.random() < 0.4:
                    beat_pulse(GOLD_DIM, CYAN)
                else:
                    beat_pulse(GOLD_DIM, WHITE)
                last_beat_time = now
                chase_step = (chase_step + 9) % total_leds

            fill(GOLD_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = CYAN

            if random.random() < 0.5:
                add_sparkles(5, WHITE)
            if random.random() < 0.35:
                add_sparkles(3, CYAN)
            if random.random() < 0.2:
                add_sparkles(2, BLUE)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # VERSE 2 1:30-2:00
        # Back to warm but slightly more energetic than verse 1
        # -------------------------------------------------------
        elif section == "verse2":
            if beat_due:
                beat_pulse(AMBER_DIM, GOLD)
                last_beat_time = now
                chase_step = (chase_step + 7) % total_leds

            fill(AMBER_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = GOLD

            if random.random() < 0.4:
                add_sparkles(4, WHITE_DIM)
            if random.random() < 0.15:
                add_sparkles(2, CYAN)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # CHORUS 2 2:00-2:30
        # More intense than chorus 1, electric and blue join in
        # -------------------------------------------------------
        elif section == "chorus2":
            if beat_due:
                roll = random.random()
                if roll < 0.3:
                    beat_pulse(BLUE_DIM, WHITE)
                elif roll < 0.6:
                    beat_pulse(BLUE_DIM, CYAN)
                else:
                    beat_pulse(BLUE_DIM, ELECTRIC)
                last_beat_time = now
                chase_step = (chase_step + 10) % total_leds

            fill(BLUE_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = ELECTRIC

            if random.random() < 0.6:
                add_sparkles(6, WHITE)
            if random.random() < 0.45:
                add_sparkles(4, CYAN)
            if random.random() < 0.3:
                add_sparkles(3, GOLD)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # BRIDGE 2:30-3:00
        # Slower, more minimal, breathing blue/cyan
        # -------------------------------------------------------
        elif section == "bridge":
            progress  = (elapsed - T_BRIDGE) / (T_FINAL - T_BRIDGE)
            breathing = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * progress * 4))
            val_b = int(180 * breathing)
            val_g = int(80 * breathing)
            fill((0, val_g, val_b))

            if random.random() < 0.15:
                add_sparkles(2, WHITE_DIM)

            show(strip)
            time.sleep(0.04)

        # -------------------------------------------------------
        # FINAL CHORUS 3:00-3:45
        # Everything at maximum, all colors, peak chaos
        # -------------------------------------------------------
        elif section == "final":
            if beat_due:
                roll = random.random()
                if roll < 0.25:
                    fill(WHITE)
                    show(strip)
                    time.sleep(0.06)
                elif roll < 0.5:
                    beat_pulse(GOLD_DIM, CYAN)
                elif roll < 0.75:
                    beat_pulse(BLUE_DIM, GOLD)
                else:
                    beat_pulse(CYAN_DIM, WHITE)
                last_beat_time = now
                chase_step = (chase_step + 12) % total_leds

            # Alternating base color for extra chaos
            base_phase = int(elapsed * 2) % 2
            fill(GOLD_DIM if base_phase == 0 else BLUE_DIM)

            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = WHITE

            if random.random() < 0.7:
                add_sparkles(8, WHITE)
            if random.random() < 0.5:
                add_sparkles(5, CYAN)
            if random.random() < 0.4:
                add_sparkles(4, GOLD)
            if random.random() < 0.3:
                add_sparkles(3, ELECTRIC)
            if random.random() < 0.2:
                add_sparkles(3, RED)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # OUTRO 3:45-5:00
        # Gradual fade, warm gold dying down to nothing
        # -------------------------------------------------------
        elif section == "outro":
            progress   = (elapsed - T_OUTRO) / (T_END - T_OUTRO)  # 0.0 to 1.0
            fade       = 1.0 - progress
            breathing  = 0.5 + 0.5 * math.sin(2 * math.pi * elapsed * 0.4)
            brightness = fade * (0.2 + 0.3 * breathing)

            val_r = int(255 * brightness)
            val_g = int(100 * brightness)
            fill((val_r, val_g, 0))

            if random.random() < 0.1 * fade:
                add_sparkles(2, WHITE_DIM)

            show(strip)
            time.sleep(0.04)

# _____________________________________________________________
# Blinding Lights - The Weeknd

def blinding_lights_weeknd(strip):
    import random

    total_leds = 134
    BPM = 85.5
    beat_interval = 60 / BPM  # ~0.702 seconds per beat

    # --- Color palette ---
    PINK_DIM      = (60, 0, 30)
    PINK_MID      = (180, 0, 80)
    PINK_BRIGHT   = (255, 0, 100)
    MAGENTA       = (255, 0, 180)
    MAGENTA_DIM   = (50, 0, 40)
    RED_DEEP      = (180, 0, 40)
    RED_DIM       = (40, 0, 10)
    WHITE         = (255, 255, 255)
    WHITE_DIM     = (60, 60, 60)
    HOT_PINK      = (255, 20, 120)
    OFF           = (0, 0, 0)

    # --- Timestamps ---
    T_BUILD       = 10.0
    T_VERSE1      = 30.0
    T_CHORUS1     = 60.0
    T_VERSE2      = 105.0
    T_CHORUS2     = 135.0
    T_OUTRO       = 180.0
    T_END         = 200.0

    def fill(color):
        for i in range(total_leds):
            strip[i] = color

    def add_sparkles(count, color=WHITE):
        for _ in range(count):
            pos = random.randint(0, total_leds - 1)
            strip[pos] = color

    def beat_pulse(base_color, bright_color):
        fill(bright_color)
        show(strip)
        time.sleep(0.07)
        fill(base_color)

    def get_section(t):
        if t < T_BUILD:   return "open"
        if t < T_VERSE1:  return "build"
        if t < T_CHORUS1: return "verse1"
        if t < T_VERSE2:  return "chorus1"
        if t < T_CHORUS2: return "verse2"
        if t < T_OUTRO:   return "chorus2"
        if t < T_END:     return "outro"
        return "done"

    start_time     = time.time()
    last_beat_time = start_time
    chase_step     = 0
    train_length   = 4

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
        # OPEN 0:00-0:10
        # Slow neon pink atmosphere, just a gentle pulse
        # -------------------------------------------------------
        if section == "open":
            progress   = elapsed / T_BUILD
            breathing  = 0.2 + 0.4 * math.sin(math.pi * progress * 1.5)
            val_r = int(180 * breathing)
            val_b = int(60 * breathing)

            if val_r > 256:
                val_r = 255
            if val_b > 256:
                val_b = 255
            if val_b < 0:
                val_b = 0
            if val_r < 0:
                val_r = 0
            fill((val_r, 0, val_b))
            show(strip)
            time.sleep(0.04)

        # -------------------------------------------------------
        # BUILD 0:10-0:30
        # Chase train spins up, magenta and deep red brightening
        # -------------------------------------------------------
        elif section == "build":
            progress = (elapsed - T_BUILD) / (T_VERSE1 - T_BUILD)  # 0.0 to 1.0

            # Train speeds up gradually through the build
            if beat_due:
                last_beat_time = now
                chase_step = (chase_step + 5) % total_leds

            # Background brightens from dim red to mid pink
            bg_r = int(40 + 140 * progress)
            bg_b = int(10 + 70 * progress)
            fill((bg_r, 0, bg_b))

            # Train color shifts from deep red to magenta
            train_r = 180
            train_g = 0
            train_b = int(40 + 140 * progress)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = (train_r, train_g, train_b)

            # Occasional early sparkles appearing more as build progresses
            if random.random() < 0.2 * progress:
                add_sparkles(2, WHITE_DIM)

            show(strip)
            time.sleep(0.03)

        # -------------------------------------------------------
        # VERSE 1 0:30-1:00
        # 85.5bpm beat pulse, neon pink base, train locked to beat
        # -------------------------------------------------------
        elif section == "verse1":
            if beat_due:
                beat_pulse(PINK_DIM, PINK_BRIGHT)
                last_beat_time = now
                chase_step = (chase_step + 7) % total_leds

            fill(PINK_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = MAGENTA

            if random.random() < 0.25:
                add_sparkles(2, WHITE_DIM)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # CHORUS 1 1:00-1:45
        # Brighter, faster chase, hot pink and white sparkles
        # -------------------------------------------------------
        elif section == "chorus1":
            if beat_due:
                if random.random() < 0.3:
                    beat_pulse(MAGENTA_DIM, WHITE)
                else:
                    beat_pulse(MAGENTA_DIM, HOT_PINK)
                last_beat_time = now
                chase_step = (chase_step + 10) % total_leds

            fill(MAGENTA_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = HOT_PINK

            if random.random() < 0.5:
                add_sparkles(4, WHITE)
            if random.random() < 0.3:
                add_sparkles(3, PINK_BRIGHT)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # VERSE 2 1:45-2:15
        # Back to verse energy, slightly warmer than verse 1
        # -------------------------------------------------------
        elif section == "verse2":
            if beat_due:
                beat_pulse(RED_DIM, PINK_BRIGHT)
                last_beat_time = now
                chase_step = (chase_step + 7) % total_leds

            fill(RED_DIM)
            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = RED_DEEP

            if random.random() < 0.3:
                add_sparkles(3, WHITE_DIM)
            if random.random() < 0.15:
                add_sparkles(2, PINK_MID)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # CHORUS 2 2:15-3:00
        # Most intense, white flashes on beat, full neon chaos
        # -------------------------------------------------------
        elif section == "chorus2":
            if beat_due:
                roll = random.random()
                if roll < 0.3:
                    fill(WHITE)
                    show(strip)
                    time.sleep(0.06)
                elif roll < 0.6:
                    beat_pulse(MAGENTA_DIM, HOT_PINK)
                else:
                    beat_pulse(PINK_DIM, WHITE)
                last_beat_time = now
                chase_step = (chase_step + 12) % total_leds

            # Alternating base for extra drive
            base_phase = int(elapsed * 2.5) % 2
            fill(MAGENTA_DIM if base_phase == 0 else RED_DIM)

            for t in range(train_length):
                pos = (total_leds - 1 - chase_step - t) % total_leds
                strip[pos] = WHITE

            if random.random() < 0.65:
                add_sparkles(6, WHITE)
            if random.random() < 0.45:
                add_sparkles(4, HOT_PINK)
            if random.random() < 0.3:
                add_sparkles(3, MAGENTA)

            show(strip)
            time.sleep(0.02)

        # -------------------------------------------------------
        # OUTRO 3:00-3:20
        # Gradual fade, dim pink pulse dying to dark
        # -------------------------------------------------------
        elif section == "outro":
            progress   = (elapsed - T_OUTRO) / (T_END - T_OUTRO)
            fade       = 1.0 - progress
            breathing  = 0.5 + 0.5 * math.sin(2 * math.pi * elapsed * 0.5)
            brightness = fade * (0.2 + 0.3 * breathing)

            val_r = int(255 * brightness)
            val_b = int(100 * brightness)
            fill((val_r, 0, val_b))

            if random.random() < 0.1 * fade:
                add_sparkles(2, WHITE_DIM)

            show(strip)
            time.sleep(0.04)
