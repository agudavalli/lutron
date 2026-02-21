import board
import neopixel
import time
import math
import random

NUM_LEDS   = 145
BRIGHTNESS = 0.4

_raw_strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

class MirroredStrip:
    MIRROR_START = 134
    MIRROR_LEN   = 11

    def __setitem__(self, index, color):
        _raw_strip[index] = color
        if index <= self.MIRROR_LEN:
            _raw_strip[self.MIRROR_START + index] = color
        elif self.MIRROR_START <= index <= self.MIRROR_START + self.MIRROR_LEN:
            _raw_strip[index - self.MIRROR_START] = color

    def __getitem__(self, index):
        return _raw_strip[index]

    def fill(self, color):
        _raw_strip.fill(color)

    def show(self):
        _raw_strip.show()

strip = MirroredStrip()

# ---------------------------------------------------------------------------
# BLINDING LIGHTS — The Weeknd  |  171 BPM  |  C Minor  |  3:20
#
# Song map (approximate timestamps):
#   0:00 – 0:22  INTRO         Dark synth swell, no drums yet
#   0:22 – 0:44  VERSE 1       Drums kick in, sparse and driving
#   0:44 – 0:55  PRE-CHORUS 1  "Sin City's cold and empty..."
#   0:55 – 1:17  CHORUS 1      "I'm blinded by the lights" + post-chorus riff
#   1:17 – 1:28  VERSE 2       Shorter, more urgent
#   1:28 – 1:39  PRE-CHORUS 2  Bigger, claps added, fuller production
#   1:39 – 2:12  CHORUS 2      Fully layered, most energy so far
#   2:12 – 2:34  BRIDGE        "I'm just calling back to let you know..."
#   2:34 – 3:09  FINAL CHORUS  Everything open, peak of the song
#   3:09 – 3:20  OUTRO         Beat falls away, held synth note fades
#
# Color language:
#   Deep crimson / dark red   — the dangerous, lonely night-drive baseline
#   Neon magenta / hot pink   — streetlights blurring past at speed
#   Electric blue             — the icy loneliness underneath the bravado
#   Blinding white strobe     — the literal "blinding lights" on chorus hits
#   Amber city glow           — pre-chorus, the city coming into view
#   Cold dark blue-black      — bridge, vulnerability stripped back
# ---------------------------------------------------------------------------

BPM  = 171
BEAT = 60 / BPM    # 0.351s per beat — this is fast, 80s synth-pop urgency
BAR  = BEAT * 4    # 1.404s per bar


# ── helpers ────────────────────────────────────────────────────────────────

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

def crossfade(c1, c2, duration, steps=40):
    step_time = duration / steps
    for s in range(steps):
        t = ease_inout(s / steps)
        fill_show(lerp_color(c1, c2, t))
        time.sleep(step_time)

def breathe_color(color, period, loops=1):
    steps = 60
    step_time = period / steps
    for _ in range(loops):
        for s in range(steps):
            scale = math.sin(math.pi * s / steps)
            c = tuple(int(v * scale) for v in color)
            fill_show(c)
            time.sleep(step_time)

def pulse_wave(color, duration, wave_len=20, speed=0.025):
    """Sine ripple — used for the synth arp feel in the intro."""
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

def blinding_flash(count=1, hold=0.06, gap=0.08):
    """
    Pure white strobe — the literal blinding streetlights of the song title.
    Faster and sharper than a camera flash; more aggressive, more disorienting.
    """
    for _ in range(count):
        fill_show((255, 255, 255))
        time.sleep(hold)
        fill_show((0, 0, 0))
        time.sleep(gap)

def neon_streak(color, wait=0.008, passes=1):
    """
    Fast comet chase — like neon streetlights blurring past a car window.
    At 171 BPM this needs to move quickly to feel in tempo.
    """
    r, g, b = color
    tail = 16
    for _ in range(passes):
        for i in range(NUM_LEDS):
            strip.fill((0, 0, 0))
            for t in range(tail):
                idx = (i - t) % NUM_LEDS
                scale = ((tail - t) / tail) ** 2
                strip[idx] = (int(r * scale), int(g * scale), int(b * scale))
            strip.show()
            time.sleep(wait)

def drum_strobe(color, duration, intensity=0.45):
    """
    On-beat color pulse synced to the 171 BPM kick.
    At this tempo the beat is very fast so the contrast between bright/dim
    needs to be sharper to be perceptible.
    """
    dim = tuple(int(v * intensity) for v in color)
    start = time.time()
    count = 0
    while time.time() - start < duration:
        c = color if count % 2 == 0 else dim
        fill_show(c)
        time.sleep(BEAT)
        count += 1

def city_sparkle(base_color, duration, density=5):
    """
    Random neon pixels flickering over the base — city lights seen through
    a windshield. Mix of hot pink and amber sparks, never just white.
    """
    SPARK_COLORS = [
        (255, 20, 80),    # neon red
        (255, 100, 0),    # amber streetlight
        (200, 0, 255),    # purple neon sign
        (255, 255, 255),  # blinding headlight
    ]
    start = time.time()
    while time.time() - start < duration:
        fill_show(base_color)
        sparks = random.sample(range(NUM_LEDS), density)
        for p in sparks:
            strip[p] = random.choice(SPARK_COLORS)
        strip.show()
        time.sleep(0.05 + random.uniform(0, 0.08))

def post_chorus_riff(loops=2):
    """
    The iconic synth riff after each chorus — the most recognizable part of the song.
    Represented as alternating neon magenta / dark pulses mimicking the staccato
    notes of the synth melody. Each 'note' is one beat long.
    """
    NEON_PINK = (255, 0, 120)
    DARK      = (20, 0, 10)

    # The riff is roughly 8 beats of synth stabs
    for _ in range(loops):
        for beat in range(8):
            # Odd beats are the staccato 'hit', even beats rest slightly
            if beat % 2 == 0:
                fill_show(NEON_PINK)
                time.sleep(BEAT * 0.35)
                fill_show(DARK)
                time.sleep(BEAT * 0.65)
            else:
                fill_show(DARK)
                time.sleep(BEAT)


# ── song sections ──────────────────────────────────────────────────────────

def intro():
    """
    0:00 – 0:22  |  ~22s
    The song opens with a single dark synth note — not the familiar riff yet,
    just an ominous low tone. Then the arp teaser begins.
    Deep crimson pulse wave builds from silence like distant city lights
    appearing on the horizon as you hit the highway.
    """
    DARK_RED   = (60, 0, 0)
    CITY_RED   = (120, 5, 10)

    all_off()
    time.sleep(0.3)

    # Dark synth swell — crossfade from black into deep crimson
    crossfade((0, 0, 0), DARK_RED, duration=5, steps=30)

    # Synth arp teaser — pulse wave in crimson, like the city coming into view
    pulse_wave(CITY_RED, duration=BAR * 4, wave_len=22, speed=0.022)

    # One neon streak right before the drums drop — the car hitting the gas
    neon_streak((180, 0, 60), wait=0.006, passes=1)


def verse(duration_bars=6, intensity=1.0):
    """
    Verse: driving, urgent, lonely.
    Deep crimson base with the drum pulse carrying the 171 BPM kick.
    City sparkles simulate the neon signs blurring past.
    At 171 BPM, 6 bars = ~8.4 seconds — verses are short and fast.
    """
    r = int(100 * intensity)
    DRIVE_RED = (r, 0, int(15 * i
