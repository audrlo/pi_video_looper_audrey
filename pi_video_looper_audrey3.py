#!/usr/bin/env python3
import os, time, subprocess, shutil
from pathlib import Path

EXT={".mp4",".mkv",".mov",".avi",".webm",".m4v"}
conf=Path("/tmp/mpv_esc_quit.conf"); conf.write_text("ESC quit\n")
if not shutil.which("mpv"): raise SystemExit("mpv not found. Install: sudo apt-get install -y mpv")
headless=not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
mpv_extra=(["--vo=drm"] if headless else [])  # let mpv auto-pick on desktop; use DRM on TTY

def usb_mounts():
    m=set()
    if shutil.which("lsblk"):
        try:
            for line in subprocess.check_output(["lsblk","-prno","NAME,RM,TYPE,MOUNTPOINT"], text=True).splitlines():
                dev,rm,typ,*rest=line.split(None,3); mp=rest[0] if rest else ""
                if rm=="1" and typ=="part":
                    if not mp and shutil.which("udisksctl"):
                        try:
                            out=subprocess.check_output(["udisksctl","mount","-b",dev], text=True, stderr=subprocess.STDOUT)
                            mp=out.split(" at ",1)[1].strip().rstrip(".\n") if " at " in out else ""
                        except subprocess.CalledProcessError: mp=""
                    if mp: m.add(mp)
        except Exception: pass
    for root in ("/media","/run/media","/mnt"):
        p=Path(root)
        if p.exists(): m |= {str(d) for d in p.iterdir() if d.is_dir()}
    return [Path(x) for x in sorted(m)]

def find_video():
    for mp in usb_mounts():
        for f in mp.rglob("*"):
            if f.is_file() and f.suffix.lower() in EXT: return f

print("Waiting for USB video...")
while True:
    v=find_video()
    if v:
        print("Playing:", v)
        rc=subprocess.run(["mpv","--fs","--no-border","--loop-file=inf","--hwdec=no","--log-file=/tmp/mpv.log","--input-default-bindings=yes",f"--input-conf={conf}",*mpv_extra,str(v)]).returncode
        if rc==0: break
    time.sleep(1)

