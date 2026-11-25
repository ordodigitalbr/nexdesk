#!/usr/bin/env python3
"""Gera o papel de parede padrão (original): gradiente pastel rosa/lilás/azul
com formas grandes, suaves e translúcidas."""
import os
import numpy as np
from PIL import Image, ImageFilter

W, H = 2560, 1440
out = os.path.join(os.path.dirname(__file__), "..", "config", "includes.chroot",
                   "usr", "share", "backgrounds", "nexdesk", "default.png")
os.makedirs(os.path.dirname(out), exist_ok=True)

y, x = np.mgrid[0:H, 0:W].astype(np.float32)
x /= W
y /= H

# Gradiente diagonal: rosa -> lilás -> azul-pervinca
stops = [
    (0.00, np.array([248, 204, 220], np.float32)),
    (0.40, np.array([232, 198, 236], np.float32)),
    (0.72, np.array([196, 196, 242], np.float32)),
    (1.00, np.array([168, 186, 238], np.float32)),
]
t = np.clip(0.6 * x + 0.4 * y, 0, 1)
img = np.zeros((H, W, 3), np.float32)
for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
    m = (t >= t0) & (t <= t1)
    k = ((t - t0) / (t1 - t0))[..., None]
    img = np.where(m[..., None], c0 * (1 - k) + c1 * k, img)

def blob(cx, cy, rx, ry, alpha):
    """Círculo/elipse suave e branco translúcido."""
    d = np.sqrt(((x - cx) * W / rx) ** 2 + ((y - cy) * H / ry) ** 2)
    a = np.clip(1.0 - (d - 0.85) / 0.30, 0, 1)  # borda suave
    a = a * a * (3 - 2 * a) * alpha
    return a[..., None]

for (cx, cy, rx, ry, al) in [
    (0.05, 0.80, 900, 900, 0.22),
    (0.62, -0.05, 950, 900, 0.16),
    (0.95, 0.70, 800, 800, 0.14),
]:
    b = blob(cx, cy, rx, ry, al)
    img = img * (1 - b) + 255.0 * b

# Brilhos coloridos suaves
def glow(cx, cy, r, color, strength):
    d = np.sqrt(((x - cx) * W / H) ** 2 + (y - cy) ** 2)
    a = np.clip(1 - d / r, 0, 1) ** 2 * strength
    return a[..., None] * np.array(color, np.float32)

img += glow(0.15, 0.20, 0.55, [30, 0, 10], 0.6)
img += glow(0.85, 0.15, 0.50, [0, 0, 30], 0.6)

rng = np.random.default_rng(7)
img += rng.normal(0, 0.9, img.shape)

im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
im = im.filter(ImageFilter.GaussianBlur(0.6))
im.save(out, optimize=True)
print("ok:", os.path.normpath(out), im.size)
