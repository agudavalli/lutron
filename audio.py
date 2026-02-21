import os
import shutil
import subprocess
from typing import Optional, Union

def _find_player(preferred: Optional[str] = None) -> Optional[str]:
    candidates = []
    if preferred:
        candidates.append(preferred)
    candidates += ["mpg123", "mpg321", "omxplayer", "cvlc", "vlc", "ffplay"]
    seen = set()
    for c in candidates:
        if c and c not in seen and shutil.which(c):
            return c
        seen.add(c)
    return None

def play_mp3(path: str, blocking: bool = False, player: Optional[str] = None, volume: Optional[float] = None):
    """
    Play an MP3 file on a Raspberry Pi.
    - path: path to mp3 file
    - blocking: if True, function returns after playback finishes; if False returns subprocess.Popen
    - player: optional override (e.g. 'mpg123', 'omxplayer', 'cvlc', 'ffplay')
    - volume: optional volume/gain (supported only for some players; value interpretation varies)
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"MP3 not found: {path}")

    chosen = _find_player(player)
    if not chosen:
        raise RuntimeError(
            "No audio player found. Install mpg123, omxplayer, or vlc (cvlc)."
        )

    # Build command for known players
    cmd = []
    if chosen in ("mpg123", "mpg321"):
        cmd = [chosen, path]
        # mpg123/mpeg321 don't take a simple linear volume arg here; user can control OS mixer
    elif chosen == "omxplayer":
        # omxplayer prefers file last; -o local to force headphone jack if needed
        cmd = ["omxplayer", path]
        # omxplayer volume control is interactive; skip here
    elif chosen in ("cvlc", "vlc"):
        cmd = [chosen, "--play-and-exit", path]
        if volume is not None:
            # VLC expects gain, but value semantics may vary
            cmd += ["--gain", str(volume)]
    elif chosen == "ffplay":
        cmd = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path]
        if volume is not None:
            cmd += ["-af", f"volume={volume}"]
    else:
        # fallback: try to execute the player with the path
        cmd = [chosen, path]

    if blocking:
        # run and wait
        subprocess.run(cmd, check=False)
        return None
    else:
        # start and return Popen
        proc = subprocess.Popen(cmd)
        return proc

# New: stop playback started by play_mp3
def stop_mp3(proc: Optional[subprocess.Popen] = None, player: Optional[str] = None, force: bool = False) -> bool:
    """
    Stop MP3 playback.
    - proc: subprocess.Popen returned by play_mp3 (preferred). If supplied, this will be terminated/killed.
    - player: optional player name to target (e.g. 'mpg123', 'omxplayer', 'cvlc'). If proc is None this is used to pkill.
    - force: if True, escalate to SIGKILL where applicable.
    Returns True if any stop signal was issued, False otherwise.
    """
    signaled = False

    if proc is not None:
        try:
            proc.terminate()
            proc.wait(timeout=2)
            signaled = True
        except Exception:
            try:
                proc.kill()
                proc.wait(timeout=1)
                signaled = True
            except Exception:
                pass
        return signaled

    # No proc: try to stop by player name(s)
    targets = [player] if player else ["mpg123", "mpg321", "omxplayer", "omxplayer.bin", "cvlc", "vlc", "ffplay"]

    # Prefer pkill if available
    if shutil.which("pkill"):
        for t in targets:
            if not t:
                continue
            args = ["pkill"]
            if force:
                args.append("-9")
            args += ["-f", t]
            subprocess.run(args, check=False)
            signaled = True
        return signaled

    # Fallback: use pgrep + kill
    if shutil.which("pgrep") and shutil.which("kill"):
        for t in targets:
            if not t:
                continue
            p = subprocess.run(["pgrep", "-f", t], capture_output=True, text=True)
            if p.returncode == 0 and p.stdout.strip():
                for pid in p.stdout.split():
                    try:
                        if force:
                            subprocess.run(["kill", "-9", pid], check=False)
                        else:
                            subprocess.run(["kill", pid], check=False)
                        signaled = True
                    except Exception:
                        pass
        return signaled

    return False

# Example usage:
# play_mp3("/home/pi/music/song.mp3")            # blocking
# p = play_mp3("/home/pi/music/song.mp3", False) # non-blocking; p.terminate() to stop
