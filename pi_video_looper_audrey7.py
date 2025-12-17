#!/usr/bin/env python3
import subprocess, shutil
from pathlib import Path

v=(Path.cwd()/"eyes.mp4")
if not v.is_file():
    p=subprocess.run(["bash","-lc","find /home -type f -name eyes.mp4 -print -quit"], capture_output=True, text=True).stdout.strip()
    if p: v=Path(p)
if not v.is_file(): raise SystemExit("Couldn't find eyes.mp4 (checked current dir, then searched /home).")
vlc=shutil.which("cvlc") or shutil.which("vlc")
if not vlc: raise SystemExit("vlc not found. Install: sudo apt-get install -y vlc")
subprocess.run([vlc,"--fullscreen","--repeat","--input-repeat=-1","--no-video-title-show","--quiet",str(v)])

