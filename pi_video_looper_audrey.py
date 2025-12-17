#!/usr/bin/env python3
import time, subprocess
from pathlib import Path

EXT={".mp4",".mkv",".mov",".avi",".webm",".m4v"}
ROOTS=[Path("/media"),Path("/run/media"),Path("/mnt")]
conf=Path("/tmp/mpv_esc_quit.conf"); conf.write_text("ESC quit\n")
while True:
    v=next((f for r in ROOTS if r.exists() for f in sorted(r.rglob("*")) if f.is_file() and f.suffix.lower() in EXT),None)
    if v: subprocess.run(["mpv","--fs","--no-border","--loop-file=inf","--no-terminal",f"--input-conf={conf}",str(v)]); break
    time.sleep(1)
