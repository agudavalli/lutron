import board
import neopixel
import time
import math
import random

NUM_LEDS   = 145
BRIGHTNESS = 0.4

_raw_strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)


# ---------------------------------------------------------------------------
# Mirror wrapper — any pixel written to index 0-11 is also written to 134-145
# and vice versa, so the overlapping corner always stays in sync.
# ---------------------------------------------------------------------------

class MirroredStrip:
    MIRROR_START = 134   # physical LED where the overlap begins
    MIRROR_LEN   = 11    # number of overlapping LEDs (0-11 <-> 134-145)

    def __setitem__(self, index, color):
        _raw_strip[index] = color
        # If writing to the start of the strip, mirror to the overlap zone
        if index <= self.MIRROR_LEN:
            _raw_strip[self.MIRROR_START + index] = color
        # If writing to the overlap zone, mirror back to the start
        elif self.MIRROR_START <= index <= self.MIRROR_START + self.MIRROR_LEN:
            _raw_strip[index - self.MIRROR_START] = color

    def __getitem__(self, index):
        return _raw_strip[index]

    def fill(self, color):
        _raw_strip.fill(color)   # fill handles the whole strip at once — overlap included

    def show(self):
        _raw_strip.show()


strip = MirroredStrip()


# ---------------------------------------------------------------------------
# FLASHING LIGHTS — Kanye West (feat. Dwele)  |  90 BPM  |  F# Minor  |  3:58
# (everything below is unchanged — the wrapper handles the mirror silently)
# ---------------------------------------------------------------------------

BPM  = 90
BEAT = 60 / BPM
BAR  = BEAT * 4


def all_off():
    strip.fill((0, 0, 0))
    strip.show()

def fill_show(color):
    strip.fill(color)
    strip.show()

def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def ease_inout(t):
    return t * t * (3 - 2 * t)

def crossfade(c1, c2, duration, steps=60):
    step_time = duration / steps
    for s in range(steps):
        t = ease_inout(s / steps)
        fill_show(lerp_color(c1, c2, t))
        time.sleep(step_time)

def breathe_color(color, period, loops=1):
    steps = 80
    step_time = period / steps
    for _ in range(loops):
        for s in range(steps):
            scale = math.sin(math.pi * s / steps)
            c = tuple(int(v * scale) for v in color)
            fill_show(c)
            time.sleep(step_time)

def camera_flash(count=1, hold=0.08, gap=0.12):
    for _ in range(count):
        fill_show((255, 255, 255))
        time.sleep(hold)
        fill_show((0, 0, 0))
        time.sleep(gap)

def slow_sparkle(base_color, duration, density=4):
    start = time.time()
    while time.time() - start < duration:
        fill_show(base_color)
        sparks = random.sample(range(NUM_LEDS), density)
        for p in sparks:
            strip[p] = (255, 255, 255)   # mirror wrapper fires automatically here
        strip.show()
        time.sleep(0.08 + random.uniform(0, 0.12))

def pulse_wave(color, duration, wave_len=25, speed=0.04):
    r, g, b = color
    start = time.time()
    frame = 0
    while time.time() - start < duration:
        for i in range(NUM_LEDS):
            bright = (math.sin((i - frame) * (2 * math.pi / wave_len)) + 1) / 2
            strip[i] = (int(r * bright), int(g * bright), int(b * bright))
        strip.show()
        time.sleep(speed)
        frame += 1

def chase_dim(color, wait=0.015, passes=1):
    r, g, b = color
    tail = 12
    for _ in range(passes):
        for i in range(NUM_LEDS):
            strip.fill((0, 0, 0))
            for t in range(tail):
                idx = (i - t) % NUM_LEDS
                scale = ((tail - t) / tail) ** 2
                strip[idx] = (int(r * scale), int(g * scale), int(b * scale))
            strip.show()
            time.sleep(wait)

def drum_pulse(color, duration, intensity=0.6):
    dim = tuple(int(v * intensity) for v in color)
    start = time.time()
    beat_count = 0
    while time.time() - start < duration:
        c = color if beat_count % 2 == 0 else dim
        fill_show(c)
        time.sleep(BEAT)
        beat_count += 1

def on_beat_flash(color, beats, hold_frac=0.3):
    on_time  = BEAT * hold_frac
    off_time = BEAT * (1 - hold_frac)
    for _ in range(beats):
        fill_show(color)
        time.sleep(on_time)
        fill_show((0, 0, 0))
        time.sleep(off_time)


# ── song sections (identical to before) ───────────────────────────────────

def intro():
    GHOST_PURPLE = (40, 0, 60)
    DEEP_INDIGO  = (20, 0, 80)
    crossfade((0, 0, 0), DEEP_INDIGO, duration=4, steps=40)
    chase_dim(GHOST_PURPLE, wait=0.025, passes=2)
    breathe_color(DEEP_INDIGO, period=4, loops=1)

def verse(duration_bars=8):
    COLD_BLUE = (0, 30, 120)
    duration  = BEAT * duration_bars * 4
    start     = time.time()
    phase     = 0
    while time.time() - start < duration:
        if phase % 2 == 0:
            drum_pulse(COLD_BLUE, duration=BEAT * 4)
        else:
            slow_sparkle(COLD_BLUE, duration=BEAT * 4, density=3)
        phase += 1

def pre_chorus():
    AMBER = (180, 80, 0)
    crossfade((0, 30, 120), AMBER, duration=BAR, steps=40)
    time.sleep(BEAT * 3)
    camera_flash(count=1, hold=0.12)

def chorus():
    CHORUS_PURPLE = (120, 0, 200)
    for bar in range(4):
        camera_flash(count=1, hold=0.15, gap=0.0)
        fill_show(CHORUS_PURPLE)
        time.sleep(BEAT * 1.5)
        camera_flash(count=1, hold=0.10, gap=0.0)
        fill_show(CHORUS_PURPLE)
        time.sleep(BEAT * 1.5)
    fill_show(CHORUS_PURPLE)
    time.sleep(BEAT)

def bridge():
    LAVENDER = (80, 20, 160)
    pulse_wave(LAVENDER, duration=BAR * 8, wave_len=30, speed=0.03)

def outro():
    INDIGO = (20, 0, 80)
    fill_show(INDIGO)
    breathe_color(INDIGO, period=BAR * 2, loops=2)
    camera_flash(count=1, hold=0.3, gap=0.5)
    crossfade(INDIGO, (0, 0, 0), duration=20, steps=100)
    all_off()


# ── full song choreography ─────────────────────────────────────────────────

def flashing_lights_kanye():
    print("0:00 — Intro: string swell")
    intro()

    print("0:18 — Verse 1: cold blue + sparkles")
    verse(duration_bars=8)

    print("0:40 — Pre-chorus: amber tension build")
    pre_chorus()

    print("0:52 — Chorus 1: camera flash strobes")
    chorus()

    print("1:10 — Verse 2: same feel, more intense")
    verse(duration_bars=8)

    print("1:32 — Pre-chorus 2")
    pre_chorus()

    print("1:44 — Chorus 2: her POV — slightly warmer purple")
    WARM_PURPLE = (150, 0, 160)
    for bar in range(4):
        camera_flash(count=1, hold=0.15, gap=0.0)
        fill_show(WARM_PURPLE)
        time.sleep(BEAT * 1.5)
        camera_flash(count=1, hold=0.10, gap=0.0)
        fill_show(WARM_PURPLE)
        time.sleep(BEAT * 1.5)
    fill_show(WARM_PURPLE)
    time.sleep(BEAT)

    print("2:02 — Bridge: lavender pulse wave swells")
    bridge()

    print("2:36 — Verse 3: final rap, most emotional")
    verse(duration_bars=8)

    print("3:05 — Peak strobe before outro")
    camera_flash(count=4, hold=0.08, gap=0.1)

    print("3:10 — Outro: strings return, slow fade to black")
    outro()

    print("Done — lights out.")
    all_off()


flashing_lights_kanye()
