# The trail gets progressively brighter each lap — on lap 1 it's barely visible, by lap 3 it's full portal purple. This gives the feeling of the mirror slowly charging up rather than just looping the same animation three times.
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
