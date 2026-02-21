import board
import neopixel
import time
import math
import random

NUM_LEDS   = 160
BRIGHTNESS = 0.4

strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# ---------------------------------------------------------------------------
# FLASHING LIGHTS — Kanye West (feat. Dwele)  |  90 BPM  |  F# Minor  |  3:58
#
# Song map (approximate timestamps):
#   0:00 – 0:18  INTRO      Eerie string swell, no drums
#   0:18 – 0:52  VERSE 1    Drums kick in, Kanye rapping
#   0:52 – 1:10  CHORUS 1   Dwele: "But what do I know?" — big & open
#   1:10 – 1:44  VERSE 2    More intense, breakup narrative
#   1:44 – 2:02  CHORUS 2   Perspective shifts to her POV
#   2:02 – 2:36  BRIDGE     Instrumental, synth swells
#   2:36 – 3:10  VERSE 3    Final rap section, most emotional
#   3:10 – 3:58  OUTRO      Beat strips back, strings return, fades
#
# Color language:
#   Deep purple / indigo  — the moody, cinematic baseline of the song
#   Cold blue             — verses, introspective and low-key
#   Warm amber / gold     — pre-chorus tension building
#   White camera flash    — chorus hits (paparazzi theme)
#   Soft lavender pulse   — bridge / string swells
#   Slow fade to black    — outro
# ---------------------------------------------------------------------------

BPM       = 90
BEAT      = 60 / BPM          # 0.667s per beat
BAR       = BEAT * 4          # 2.667s per bar


# ── helpers ────────────────────────────────────────────────────────────────

def all_off():
    strip.fill((0, 0, 0))
    strip.show()

def fill_show(color):
    strip.fill(color)
    strip.show()

def lerp_color(c1, c2, t):
    """Linear interpolate between two RGB tuples. t = 0..1"""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def ease_inout(t):
    """Smooth step — feels more musical than a linear blend"""
    return t * t * (3 - 2 * t)

def crossfade(c1, c2, duration, steps=60):
    """Slowly blend the whole strip from c1 to c2 over `duration` seconds."""
    step_time = duration / steps
    for s in range(steps):
        t = ease_inout(s / steps)
        fill_show(lerp_color(c1, c2, t))
        time.sleep(step_time)

def breathe_color(color, period, loops=1):
    """Pulse a color in and out. period = full cycle in seconds."""
    steps = 80
    step_time = period / steps
    for _ in range(loops):
        for s in range(steps):
            angle = math.pi * s / steps      # 0 → π gives one smooth arc
            scale = math.sin(angle)
            c = tuple(int(v * scale) for v in color)
            fill_show(c)
            time.sleep(step_time)

def camera_flash(count=1, hold=0.08, gap=0.12):
    """
    Bright white strobe — mimics paparazzi camera pops.
    Used on every chorus hit and the 'Flashing lights' lyric moments.
    """
    for _ in range(count):
        fill_show((255, 255, 255))
        time.sleep(hold)
        fill_show((0, 0, 0))
        time.sleep(gap)

def slow_sparkle(base_color, duration, density=4):
    """
    Random pixels flicker above the base color — like distant camera flashes
    in a crowd. Used during verses to keep motion while staying low-key.
    """
    start = time.time()
    while time.time() - start < duration:
        fill_show(base_color)
        # Light a handful of random pixels brighter
        sparks = random.sample(range(NUM_LEDS), density)
        for p in sparks:
            strip[p] = (255, 255, 255)
        strip.show()
        time.sleep(0.08 + random.uniform(0, 0.12))

def pulse_wave(color, duration, wave_len=25, speed=0.04):
    """
    Sine-wave ripple across the strip — used during the bridge string swells.
    """
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
    """Single-pixel chase — used in the intro as the strings build."""
    r, g, b = color
    tail = 12
    for _ in range(passes):
        for i in range(NUM_LEDS):
            strip.fill((0, 0, 0))
            for t in range(tail):
                idx = (i - t) % NUM_LEDS
                scale = ((tail - t) / tail) ** 2   # quadratic falloff = sharper head
                strip[idx] = (int(r * scale), int(g * scale), int(b * scale))
            strip.show()
            time.sleep(wait)

def on_beat_flash(color, beats, hold_frac=0.3):
    """
    Fill the strip on every beat for `beats` beats.
    hold_frac = fraction of the beat the color stays on (rest is dark).
    """
    on_time  = BEAT * hold_frac
    off_time = BEAT * (1 - hold_frac)
    for _ in range(beats):
        fill_show(color)
        time.sleep(on_time)
        fill_show((0, 0, 0))
        time.sleep(off_time)

def drum_pulse(color, duration, intensity=0.6):
    """
    Subtle brightness pump on every beat — the strip breathes with the kick drum.
    Color is shown at full on the downbeat, drops to `intensity` fraction on the off-beat.
    """
    dim = tuple(int(v * intensity) for v in color)
    start = time.time()
    beat_count = 0
    while time.time() - start < duration:
        # Downbeats (1 & 3) slightly brighter
        c = color if beat_count % 2 == 0 else dim
        fill_show(c)
        time.sleep(BEAT)
        beat_count += 1


# ── song sections ──────────────────────────────────────────────────────────

def intro():
    """
    0:00 – 0:18  |  ~18s  |  4 bars + pickup
    Eerie string swell before the beat drops. A dim ghost-purple ghost-chase
    traces the strip while the strip slowly brightens from black.
    """
    GHOST_PURPLE = (40, 0, 60)
    DEEP_INDIGO  = (20, 0, 80)

    # Strings swell in from silence — crossfade dark → indigo
    crossfade((0, 0, 0), DEEP_INDIGO, duration=4, steps=40)

    # Two slow purple chases while the strings hold
    chase_dim(GHOST_PURPLE, wait=0.025, passes=2)

    # Anticipation — hold the color and let it breathe once before beat drops
    breathe_color(DEEP_INDIGO, period=4, loops=1)


def verse(duration_bars=8):
    """
    Verse feel: cold blue base with slow drum pulses and sparse white sparkles
    mimicking distant camera flashes in the crowd.
    90 BPM, 8 bars = ~21s per verse.
    """
    COLD_BLUE   = (0, 30, 120)
    VERSE_BEATS = duration_bars * 4

    duration = BEAT * VERSE_BEATS
    # Drum pulse carries the beat; sparkles keep the paparazzi vibe alive
    # We alternate: 4 beats drum pulse → 4 beats sparkle, cycling for the verse
    start = time.time()
    phase = 0
    while time.time() - start < duration:
        if phase % 2 == 0:
            drum_pulse(COLD_BLUE, duration=BEAT * 4)
        else:
            slow_sparkle(COLD_BLUE, duration=BEAT * 4, density=3)
        phase += 1


def pre_chorus():
    """
    Short 2-bar tension build before Dwele's chorus lands.
    Amber warmth rises — like stage lights swelling before a singer hits the mic.
    """
    AMBER = (180, 80, 0)
    crossfade((0, 30, 120), AMBER, duration=BAR, steps=40)
    # One rapid white flash on the final beat as the chorus hits
    time.sleep(BEAT * 3)
    camera_flash(count=1, hold=0.12)


def chorus():
    """
    Chorus: "But what do I know? / Flashing lights"
    This is the centrepiece — paparazzi camera pops in white, 4 bars.
    Every bar gets 2 camera flashes (on beats 1 and 3) with purple fill in between.
    """
    CHORUS_PURPLE = (120, 0, 200)
    CHORUS_BARS   = 4

    for bar in range(CHORUS_BARS):
        # Beat 1 — BIG camera flash
        camera_flash(count=1, hold=0.15, gap=0.0)
        fill_show(CHORUS_PURPLE)
        time.sleep(BEAT * 1.5)

        # Beat 3 — second flash, slightly softer
        camera_flash(count=1, hold=0.10, gap=0.0)
        fill_show(CHORUS_PURPLE)
        time.sleep(BEAT * 1.5)

    # Let the chorus colour linger before the next section fades it
    fill_show(CHORUS_PURPLE)
    time.sleep(BEAT)


def bridge():
    """
    2:02 – 2:36  |  ~34s  |  ~8 bars
    Instrumental — synths swell over the stripped-back beat.
    Soft lavender pulse waves wash along the strip like slow camera sweeps.
    """
    LAVENDER = (80, 20, 160)
    pulse_wave(LAVENDER, duration=BAR * 8, wave_len=30, speed=0.03)


def outro():
    """
    3:10 – 3:58  |  ~48s
    Beat strips back, strings return, song fades to silence.
    Strip slowly dims from indigo → total darkness over the full outro.
    """
    INDIGO = (20, 0, 80)
    fill_show(INDIGO)

    # Gentle breathe as energy drains away
    breathe_color(INDIGO, period=BAR * 2, loops=2)

    # One last slow camera flash — the final 'flashing light'
    camera_flash(count=1, hold=0.3, gap=0.5)

    # Long crossfade to black — ~20 seconds
    crossfade(INDIGO, (0, 0, 0), duration=20, steps=100)
    all_off()


# ── full song choreography ─────────────────────────────────────────────────

def flashing_lights_kanye():
    """
    Full LED choreography for Flashing Lights — Kanye West (feat. Dwele)
    Run this while the track plays from the beginning.

    Timeline synced to 90 BPM / 4:04 total (with slight padding):
      0:00  Intro
      0:18  Verse 1
      0:40  Pre-chorus
      0:52  Chorus 1
      1:10  Verse 2
      1:32  Pre-chorus
      1:44  Chorus 2 (perspective shift — same flash, slightly warmer tint)
      2:02  Bridge
      2:36  Verse 3
      3:10  Outro → fade
    """

    print("0:00 — Intro: string swell")
    intro()                         # ~18s

    print("0:18 — Verse 1: cold blue + sparkles")
    verse(duration_bars=8)          # ~21s

    print("0:40 — Pre-chorus: amber tension build")
    pre_chorus()                    # ~8s

    print("0:52 — Chorus 1: camera flash strobes")
    chorus()                        # ~12s

    print("1:10 — Verse 2: same feel, more intense")
    verse(duration_bars=8)          # ~21s

    print("1:32 — Pre-chorus 2")
    pre_chorus()                    # ~8s

    print("1:44 — Chorus 2: her POV — slightly warmer purple")
    # Shift chorus tint slightly warmer to mark the perspective flip in lyrics
    WARM_PURPLE = (150, 0, 160)
    CHORUS_BARS = 4
    for bar in range(CHORUS_BARS):
        camera_flash(count=1, hold=0.15, gap=0.0)
        fill_show(WARM_PURPLE)
        time.sleep(BEAT * 1.5)
        camera_flash(count=1, hold=0.10, gap=0.0)
        fill_show(WARM_PURPLE)
        time.sleep(BEAT * 1.5)
    fill_show(WARM_PURPLE)
    time.sleep(BEAT)                # ~12s

    print("2:02 — Bridge: lavender pulse wave swells")
    bridge()                        # ~34s

    print("2:36 — Verse 3: final rap, most emotional")
    verse(duration_bars=8)          # ~21s

    # A burst of rapid camera flashes before the outro — the song's emotional peak
    print("3:05 — Peak strobe before outro")
    camera_flash(count=4, hold=0.08, gap=0.1)

    print("3:10 — Outro: strings return, slow fade to black")
    outro()                         # ~48s

    print("Done — lights out.")
    all_off()


flashing_lights_kanye()
