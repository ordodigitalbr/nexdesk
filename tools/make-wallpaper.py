#!/usr/bin/env python3
"""Gera o papel de parede padrão (original, gradiente com brilhos suaves)."""
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

# Gradiente diagonal azul-petróleo -> violeta
t = np.clip(0.55 * x + 0.45 * y, 0, 1)[..., None]
c1 = np.array([8, 18, 48], np.float32)
c2 = np.array([58, 24, 110], np.float32)
img = c1 * (1 - t) + c2 * t

def glow(cx, cy, r, color, strength):
    d = np.sqrt(((x - cx) * W / H) ** 2 + (y - cy) ** 2)
    a = np.clip(1 - d / r, 0, 1) ** 2 * strength
    return a[..., None] * np.array(color, np.float32)

img += glow(0.22, 0.30, 0.55, [30, 110, 200], 1.0)
img += glow(0.80, 0.75, 0.60, [150, 50, 190], 0.9)
img += glow(0.55, 0.10, 0.35, [20, 160, 170], 0.5)

# Ruído leve para evitar faixas no gradiente
rng = np.random.default_rng(7)
img += rng.normal(0, 1.2, img.shape)

im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
im = im.filter(ImageFilter.GaussianBlur(0.6))
im.save(out, optimize=True)
print("ok:", os.path.normpath(out), im.size)
