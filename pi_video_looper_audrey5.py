#!/usr/bin/env python3
import subprocess, shutil
from pathlib import Path

if not shutil.which("mpv"): raise SystemExit("mpv not found. Install: sudo apt-get install -y mpv")
conf=Path("/tmp/mpv_esc_quit.conf"); conf.write_text("ESC quit\n")
v=(Path.cwd()/"eyes.mp4")
if not v.is_file():
    p=subprocess.run(["bash","-lc","find /home -type f -name eyes.mp4 -print -quit"], capture_output=True, text=True).stdout.strip()
    if p: v=Path(p)
if not v.is_file(): raise SystemExit("Couldn't find eyes.mp4 (checked current dir, then searched /home).")
subprocess.run(["mpv","--fs","--loop-file=inf","--hwdec=auto-safe","--input-default-bindings=yes",f"--input-conf={conf}",str(v)])

