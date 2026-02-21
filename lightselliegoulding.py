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
# LIGHTS — Ellie Goulding  |  120 BPM  |  G# Minor  |  3:32
#
# Song map (approximate timestamps):
#   0:00 – 0:16  INTRO       Sparse synth arp, no vocals, 2 bars
#   0:16 – 0:47  VERSE 1     "I had a way then, losing it all on my own..."
#   0:47 – 1:18  CHORUS 1    "You show the lights that stop me turn to stone..."
#   1:18 – 1:49  VERSE 2     "Noises, I play within my head..."
#   1:49 – 2:20  CHORUS 2    Same chorus, more layered and full
#   2:20 – 2:51  BRIDGE      Vocal "calling, calling, calling me home" interlude
#   2:51 – 3:22  FINAL CHORUS Big, full production, everything open
#   3:22 – 3:32  OUTRO       Beat drops away, single synth note fades
#
# Color language:
#   Near-black deep blue    — the darkness the song is about; verse baseline
#   Soft teal shimmer       — the synth arp in the intro; delicate and electric
#   Warm white / gold       — the "lights" themselves; chorus payoff
#   Gentle cyan sparkles    — distant lights in the dark during verses
#   Rising silver           — pre-chorus build, light about to break through
#   Full bright white bloom — final chorus, the lights at their strongest
#   Slow fade to black      — outro, the lights going out again
# ---------------------------------------------------------------------------

BPM  = 120
BEAT = 60 / BPM    # 0.5s per beat
BAR  = BEAT * 4    # 2.0s per bar


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

def crossfade(c1, c2, duration, steps=60):
    step_time = duration / steps
    for s in range(steps):
        t = ease_inout(s / steps)
        fill_show(lerp_color(c1, c2, t))
        time.sleep(step_time)

def breathe_color(color, period, loops=1):
    """Pulse a color in and out — one full sine arc per loop."""
    steps = 80
    step_time = period / steps
    for _ in range(loops):
        for s in range(steps):
            scale = math.sin(math.pi * s / steps)
            c = tuple(int(v * scale) for v in color)
            fill_show(c)
            time.sleep(step_time)

def pulse_wave(color, duration, wave_len=20, speed=0.03):
    """Sine ripple along the strip — used for the synth arp feel."""
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

def chase_dim(color, wait=0.012, passes=1):
    """Comet chase with a soft quadratic tail."""
    r, g, b = color
    tail = 14
    for _ in range(passes):
        for i in range(NUM_LEDS):
            strip.fill((0, 0, 0))
            for t in range(tail):
                idx = (i - t) % NUM_LEDS
                scale = ((tail - t) / tail) ** 2
                strip[idx] = (int(r * scale), int(g * scale), int(b * scale))
            strip.show()
            time.sleep(wait)

def dark_sparkle(base_color, duration, density=3):
    """
    A few pixels flicker like distant lights in the dark.
    The base is kept very dim — the sparks are the point.
    """
    start = time.time()
    while time.time() - start < duration:
        fill_show(base_color)
        sparks = random.sample(range(NUM_LEDS), density)
        for p in sparks:
            # Sparks are warm white-gold, not pure white — like a candle
            strip[p] = (255, 220, 120)
        strip.show()
        time.sleep(0.07 + random.uniform(0, 0.10))

def drum_pulse(color, duration, intensity=0.5):
    """Strip breathes with the kick — full on the downbeat, dimmed on the off."""
    dim = tuple(int(v * intensity) for v in color)
    start = time.time()
    beat_count = 0
    while time.time() - start < duration:
        c = color if beat_count % 2 == 0 else dim
        fill_show(c)
        time.sleep(BEAT)
        beat_count += 1

def light_bloom(target, duration, steps=50):
    """
    Bloom from near-black into `target` color — used at the chorus hit.
    Faster than crossfade; feels like a light turning on rather than fading in.
    """
    step_time = duration / steps
    for s in range(steps):
        t = ease_inout(s / steps)
        fill_show(lerp_color((0, 0, 0), target, t))
        time.sleep(step_time)

def calling_pulse(color, beats):
    """
    On-beat staccato pulse for the 'calling, calling, calling' bridge section.
    Short flash on every beat, like a lighthouse beam sweeping past.
    """
    on_time  = BEAT * 0.25
    off_time = BEAT * 0.75
    for _ in range(beats):
        fill_show(color)
        time.sleep(on_time)
        fill_show((0, 0, 20))   # never fully dark — always a hint of blue
        time.sleep(off_time)


# ── song sections ──────────────────────────────────────────────────────────

def intro():
    """
    0:00 – 0:16  |  ~16s  |  2 bars
    Just the synth arpeggio — no drums, no vocals yet. The song begins in near-
    darkness. A delicate teal pulse wave traces the strip like a single synth note
    repeating, building just enough tension before the verse arrives.
    """
    SYNTH_TEAL = (0, 80, 120)

    # Start from complete darkness
    all_off()
    time.sleep(0.5)

    # Teal pulse wave for the full intro — 2 bars at 120 BPM = 4 seconds each
    pulse_wave(SYNTH_TEAL, duration=BAR * 2, wave_len=18, speed=0.025)


def verse(duration_bars=8, intensity=1.0):
    """
    Verse feel: deep near-black blue as the darkness, with warm gold sparkles
    drifting across like distant lights through a window.
    intensity=1.0 for verse 1 (quieter), can be nudged up for verse 2.
    At 120 BPM, 8 bars = 16 seconds.
    """
    # Scale the blue slightly brighter for verse 2 to reflect the added production
    base_r = int(0 * intensity)
    base_g = int(10 * intensity)
    base_b = int(int(50 * intensity))
    DARK_BLUE = (base_r, base_g, base_b)

    duration = BEAT * duration_bars * 4
    start    = time.time()
    phase    = 0

    while time.time() - start < duration:
        if phase % 2 == 0:
            # Drum pulse — the kick anchors the beat against the darkness
            drum_pulse(DARK_BLUE, duration=BEAT * 4, intensity=0.4)
        else:
            # Sparkle phase — distant lights flickering in the black
            dark_sparkle(DARK_BLUE, duration=BEAT * 4, density=3)
        phase += 1


def pre_chorus():
    """
    Short 2-bar rising silver swell — the light is coming.
    Crossfades from dark blue toward a cool silver, then one final beat of
    near-white before the chorus blooms open.
    """
    DARK_BLUE  = (0, 10, 50)
    SILVER     = (160, 180, 200)

    # Rising swell over 1 bar
    crossfade(DARK_BLUE, SILVER, duration=BAR, steps=40)

    # Hold the silver tension for 3 beats
    time.sleep(BEAT * 3)

    # One sharp dip back to near-dark on the final beat — makes the chorus hit harder
    crossfade(SILVER, (10, 10, 20), duration=BEAT * 0.5, steps=10)


def chorus(warm=False):
    """
    Chorus: "You show the lights that stop me turn to stone..."
    The darkness breaks. Warm white-gold light blooms across the entire strip
    and breathes in time with the chord progression — 8 bars of light payoff.

    warm=True for the second and final chorus where the production is fuller;
    shifts the white slightly warmer and brighter.
    """
    CHORUS_WHITE = (255, 240, 180) if warm else (255, 230, 150)
    CHORUS_BARS  = 8   # 8 bars × 2s = 16s

    # Bloom in fast — the light turns ON
    light_bloom(CHORUS_WHITE, duration=0.3, steps=20)

    # Hold and breathe across the chorus bars — light that's alive, not static
    for bar in range(CHORUS_BARS):
        # Each bar: subtle brightness pump on beat 1
        fill_show(CHORUS_WHITE)
        time.sleep(BEAT * 2)

        # Gentle dip on beats 3-4 — breathing with the chord change
        dim = tuple(int(v * 0.7) for v in CHORUS_WHITE)
        crossfade(CHORUS_WHITE, dim, duration=BEAT, steps=15)
        crossfade(dim, CHORUS_WHITE, duration=BEAT, steps=15)

    # Leave the light on — crossfade will handle the transition out
    fill_show(CHORUS_WHITE)


def bridge():
    """
    2:20 – 2:51  |  ~31s
    'Cause they're calling, calling, calling me home / Calling, calling, calling home'
    The word 'calling' is said 18 times in this song. The lights strobe gently
    on every beat like a lighthouse — rhythmic, searching, homing.
    """
    CALL_CYAN = (80, 180, 220)   # cooler than the chorus warm — these are distant lights

    # 16 beats of lighthouse-style calling pulse (4 bars)
    calling_pulse(CALL_CYAN, beats=16)

    # Swell back toward warmth as the bridge resolves into the final chorus
    crossfade((0, 0, 20), (200, 180, 100), duration=BAR * 2, steps=60)


def final_chorus():
    """
    2:51 – 3:22  |  ~31s
    The biggest moment — all production layers open, Ellie's voice at peak.
    Full warm white, brighter than either previous chorus. The strip is as
    close to 'blinding with light' as it gets, then gradually softens as the
    outro approaches.
    """
    BRIGHT_WHITE = (255, 255, 220)   # slightly warm, not clinical
    CHORUS_BARS  = 8

    light_bloom(BRIGHT_WHITE, duration=0.2, steps=15)

    for bar in range(CHORUS_BARS):
        fill_show(BRIGHT_WHITE)
        time.sleep(BEAT * 1.5)

        # On bar 5+ start dimming slightly — previewing the fade out
        if bar >= 5:
            scale = 1.0 - ((bar - 4) * 0.1)
            dim = tuple(int(v * scale) for v in BRIGHT_WHITE)
            fill_show(dim)

        time.sleep(BEAT * 2.5)

    fill_show(tuple(int(v * 0.5) for v in BRIGHT_WHITE))


def outro():
    """
    3:22 – 3:32  |  ~10s
    The beat drops away. Just a single held synth note fading to silence.
    The lights slowly go out — back to darkness, the same place the song began.
    A final faint teal pulse wave ghosts across before total black.
    """
    FAINT_TEAL = (0, 30, 50)

    # Crossfade from whatever the final chorus left behind down to near-black
    crossfade((120, 120, 80), FAINT_TEAL, duration=4, steps=60)

    # One last ghost of the intro's synth pulse — the lights fading out
    pulse_wave(FAINT_TEAL, duration=4, wave_len=25, speed=0.04)

    # Fade to black
    crossfade(FAINT_TEAL, (0, 0, 0), duration=2, steps=40)
    all_off()


# ── full song choreography ─────────────────────────────────────────────────

def lights_ellie_goulding():
    """
    Full LED choreography for Lights — Ellie Goulding
    Start this the moment the track begins.

    Timeline synced to 120 BPM / 3:32 total:
      0:00  Intro      — teal synth pulse in the dark
      0:16  Verse 1    — deep blue darkness, gold sparkles
      0:47  Chorus 1   — warm white light blooms open
      1:18  Verse 2    — back to darkness, slightly more intense
      1:49  Chorus 2   — warmer, fuller white
      2:20  Bridge     — cyan lighthouse calling pulse
      2:51  Final chorus — brightest white, full bloom
      3:22  Outro      — lights fade back to black
    """

    print("0:00 — Intro: synth arp teal pulse")
    intro()                                # ~16s

    print("0:16 — Verse 1: darkness + distant gold sparkles")
    verse(duration_bars=8, intensity=1.0)  # ~16s

    print("0:32 — Pre-chorus: silver swell")
    pre_chorus()                           # ~8s

    print("0:47 — Chorus 1: warm white light blooms")
    chorus(warm=False)                     # ~16s

    print("1:18 — Verse 2: darker, more fragile")
    verse(duration_bars=8, intensity=1.2)  # ~16s

    print("1:35 — Pre-chorus 2: silver swell")
    pre_chorus()                           # ~8s

    print("1:49 — Chorus 2: fuller, warmer white")
    chorus(warm=True)                      # ~16s

    print("2:20 — Bridge: calling, calling, calling home")
    bridge()                               # ~31s

    print("2:51 — Final chorus: brightest moment")
    final_chorus()                         # ~31s

    print("3:22 — Outro: lights fade to black")
    outro()                                # ~10s

    print("Done — lights out.")
    all_off()


lights_ellie_goulding()
