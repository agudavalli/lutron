import sys

import board
import neopixel
import time

NUM_LEDS   = 160
BRIGHTNESS = 0.4

strip = neopixel.NeoPixel(board.D18, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# --- Static fills ---

def all_red():
    strip.fill((255, 0, 0))
    strip.show()

def all_white():
    strip.fill((255, 255, 255))
    strip.show()

def all_off():
    strip.fill((0, 0, 0))
    strip.show()


# --- Section test: lights up each quarter one at a time so you can spot dead zones ---

def section_test():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    section = NUM_LEDS // len(colors)
    for i, color in enumerate(colors):
        strip.fill((0, 0, 0))
        for j in range(i * section, (i + 1) * section):
            strip[j] = color
        strip.show()
        time.sleep(1)


# --- Chase: a single bright pixel runs down the strip ---

def chase(color=(255, 255, 255), wait=0.03):
    for i in range(NUM_LEDS):
        strip.fill((0, 0, 0))
        strip[i] = color
        strip.show()
        time.sleep(wait)


# --- Theater chase: every 3rd pixel marches forward ---

def theater_chase(color=(255, 100, 0), wait=0.08, loops=5):
    for _ in range(loops):
        for offset in range(3):
            strip.fill((0, 0, 0))
            for i in range(offset, NUM_LEDS, 3):
                strip[i] = color
            strip.show()
            time.sleep(wait)


# --- Rainbow: spreads a full hue wheel across the strip and rotates it ---

def wheel(pos):
    """0-255 position on color wheel -> (R, G, B)"""
    pos = pos % 256
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait=0.02, loops=3):
    for _ in range(loops):
        for offset in range(256):
            for i in range(NUM_LEDS):
                strip[i] = wheel((i * 256 // NUM_LEDS + offset) & 255)
            strip.show()
            time.sleep(wait)


# --- Breathe: fades a color in and out ---

def breathe(color=(0, 100, 255), steps=100, loops=3):
    r, g, b = color
    for _ in range(loops):
        for step in range(steps):
            scale = step / steps
            strip.fill((int(r * scale), int(g * scale), int(b * scale)))
            strip.show()
            time.sleep(0.01)
        for step in range(steps, 0, -1):
            scale = step / steps
            strip.fill((int(r * scale), int(g * scale), int(b * scale)))
            strip.show()
            time.sleep(0.01)

def all_yellow():
    strip.fill((255, 255, 0))
    strip.show()

def nether():
    strip.fill((60,0,110))
    #strip.fill((97,0,178))
    #strip.fill((150,50,255))
    strip.show()


# --- Run all tests in sequence ---

def run_all_tests():
    print("Static red..."); all_red();          time.sleep(2)
    print("Static white..."); all_white();      time.sleep(2)
    print("Section test..."); section_test()
    print("Chase...");        chase()
    print("Theater chase..."); theater_chase()
    print("Rainbow...");      rainbow_cycle()
    print("Breathe...");      breathe()
    print("Done!"); all_off()


for line in sys.stdin:
    line = line.strip()
    if line == 'all_red':
        all_red()
    elif line == 'all_white':
        all_white()
    elif line == 'all_off':
        all_off()
    elif line == 'section_test':
        section_test()
    elif line == 'chase':
        chase()
    elif line == 'theater_chase':
        theater_chase()
    elif line == 'rainbow_cycle':
        rainbow_cycle()
    elif line == 'breathe':
        breathe()
    elif line == 'all_yellow':
        all_yellow()
    elif line == 'nether':
        nether()
