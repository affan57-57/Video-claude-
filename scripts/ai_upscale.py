"""AI 4x upscale (Real-ESRGAN realesr-general-x4v3, SRVGGNetCompact) for images and video clips.

Usage:
  python3 -I ai_upscale.py MODEL.pth image IN.jpg OUT.png [W H]
  python3 -I ai_upscale.py MODEL.pth video IN.mp4 OUT.mp4 SS DUR PREFILTER W H
    PREFILTER: ffmpeg -vf chain applied at source resolution before upscaling (crop/flip),
    the 4x result is then lanczos-resized to W x H.
"""
import subprocess, sys
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

torch.set_num_threads(4)
import os
ALPHA = float(os.environ.get("ALPHA", "0.65"))

class SRVGGNetCompact(nn.Module):
    def __init__(self, num_feat=64, num_conv=32, upscale=4):
        super().__init__()
        self.upscale = upscale
        body = [nn.Conv2d(3, num_feat, 3, 1, 1), nn.PReLU(num_parameters=num_feat)]
        for _ in range(num_conv):
            body += [nn.Conv2d(num_feat, num_feat, 3, 1, 1), nn.PReLU(num_parameters=num_feat)]
        body += [nn.Conv2d(num_feat, 3 * upscale * upscale, 3, 1, 1)]
        self.body = nn.ModuleList(body)
        self.upsampler = nn.PixelShuffle(upscale)

    def forward(self, x):
        out = x
        for m in self.body:
            out = m(out)
        out = self.upsampler(out)
        return out + F.interpolate(x, scale_factor=self.upscale, mode="nearest")

def load(path):
    m = SRVGGNetCompact()
    sd = torch.load(path, map_location="cpu", weights_only=True)
    m.load_state_dict(sd.get("params", sd))
    return m.eval()

@torch.inference_mode()
def up(model, rgb):  # HxWx3 uint8 -> 4Hx4Wx3 uint8
    x = torch.from_numpy(rgb.copy()).permute(2, 0, 1)[None].float() / 255
    y = model(x)
    # keep natural texture: blend the GAN output with a plain bicubic upscale
    y = ALPHA * y + (1 - ALPHA) * F.interpolate(x, scale_factor=4, mode="bicubic", align_corners=False)
    y = y.clamp(0, 1)[0].permute(1, 2, 0).numpy()
    return (y * 255 + 0.5).astype(np.uint8)

def probe(path, vf):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-frames:v", "1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    r = subprocess.run(["ffprobe", "-v", "error", "-f", "lavfi", "-i",
                        f"movie={path},{vf}", "-show_entries", "stream=width,height", "-of", "csv=p=0"],
                       capture_output=True, text=True)
    w, h = map(int, r.stdout.strip().split(",")[:2])
    return w, h

model = load(sys.argv[1])
mode = sys.argv[2]
if mode == "image":
    src, dst = sys.argv[3], sys.argv[4]
    w, h = probe(src, "null")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    img = np.frombuffer(raw, np.uint8).reshape(h, w, 3)
    out = up(model, img)
    vf = ["-vf", f"scale={sys.argv[5]}:{sys.argv[6]}:flags=lanczos"] if len(sys.argv) > 6 else []
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                        f"{out.shape[1]}x{out.shape[0]}", "-i", "-", *vf, dst], input=out.tobytes(), check=True)
    print("ok", dst, out.shape)
else:
    src, dst, ss, dur, pre, W, H = sys.argv[3:10]
    w, h = probe(src, pre)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", ss, "-t", dur, "-i", src, "-vf", f"{pre},fps=30",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                            f"{w*4}x{h*4}", "-r", "30", "-i", "-", "-vf",
                            f"scale={W}:{H}:flags=lanczos,setsar=1,eq=saturation=1.12:contrast=1.04",
                            "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", dst], stdin=subprocess.PIPE)
    n, fs = 0, w * h * 3
    while True:
        buf = dec.stdout.read(fs)
        if len(buf) < fs:
            break
        enc.stdin.write(up(model, np.frombuffer(buf, np.uint8).reshape(h, w, 3)).tobytes())
        n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print("ok", dst, n, "frames")
