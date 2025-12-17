#!/usr/bin/env python3
import os, subprocess, shutil
from pathlib import Path

v=Path("/home/sam-robot-pi7/eyes.mp4")
conf=Path("/tmp/mpv_esc_quit.conf"); conf.write_text("ESC quit\n")
if not v.is_file(): raise SystemExit(f"Missing video: {v}")
if not shutil.which("mpv"): raise SystemExit("mpv not found. Install: sudo apt-get install -y mpv")
headless=not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
subprocess.run(["mpv","--fs","--no-border","--loop-file=inf","--hwdec=no","--input-default-bindings=yes",f"--input-conf={conf}",*(["--vo=drm"] if headless else []),str(v)])

