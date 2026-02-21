# The trail gets progressively brighter each lap — on lap 1 it's barely visible, by lap 3 it's full portal purple. This gives the feeling of the mirror slowly charging up rather than just looping the same animation three times.
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
    """Smoothly blend the whole strip from c1 to c2 over `duration` seconds."""
    step_time = duration / steps
    for s in range(steps):
        t = ease_inout(s / steps)
        fill_show(lerp_color(c1, c2, t))
        time.sleep(step_time)


# ── boot sequence ──────────────────────────────────────────────────────────

def boot_sequence(loops=3, wait=0.012):
    """
    Startup trail animation — a dark violet comet circles the full strip
    continuously, like the mirror is powering up and coming to life.
    Runs `loops` full laps then fades out cleanly.
    """
    PORTAL   = (60, 0, 110)   # dark deep violet
    TAIL_LEN = 20             # longer tail = more ghostly and flowing

    for lap in range(loops):
        # On each successive lap, slightly brighten toward full portal purple
        # so the strip feels like it's warming up and gaining energy
        progress = (lap + 1) / loops
        r = int(PORTAL[0] * progress)
        g = int(PORTAL[1] * progress)
        b = int(PORTAL[2] * progress)
        color = (r, g, b)

        for i in range(NUM_LEDS):
            strip.fill((0, 0, 0))
            for t in range(TAIL_LEN):
                idx = (i - t) % NUM_LEDS
                # Cubic falloff — sharp bright head, long ghostly tail
                scale = ((TAIL_LEN - t) / TAIL_LEN) ** 3
                strip[idx] = (
                    int(color[0] * scale),
                    int(color[1] * scale),
                    int(color[2] * scale),
                )
            strip.show()
            time.sleep(wait)

    # After the laps, bloom the full strip to portal purple then fade out
    crossfade((0, 0, 0), PORTAL, duration=0.8, steps=30)
    time.sleep(0.4)
    crossfade(PORTAL, (0, 0, 0), duration=1.2, steps=50)
    all_off()


# ── run ────────────────────────────────────────────────────────────────────

boot_sequence()
