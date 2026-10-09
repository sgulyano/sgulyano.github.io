"""Generate the project-card thumbnails for the portfolio site.

Usage (from the repo root): python img/proj/thumbs/make_thumbs.py img/proj/thumbs

Each thumbnail is a flat project colour with a crop of the project's original image, recoloured as a
duotone in that colour and laid on a "paper" card that bleeds off the bottom-right edge.
Projects without a suitable original (sCT, Semanthai, microplastics) use a generated paper-style figure instead.
To add a project, add an entry to PROJECTS (a figure: an original crop or a generated one, a label, a colour) and rerun.
Needs numpy, Pillow and matplotlib; fonts are Windows' Segoe UI and Leelawadee UI (Thai).
"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)                   # img/proj, where the original images live
W, H = 1920, 1080                             # render size
OUT_W, OUT_H = 960, 540                       # saved size (cards show ~336px wide)
FONT = "C:/Windows/Fonts/seguisb.ttf"

# background, duotone shadow, duotone highlight
PALETTES = {
    "ink":        ("#22304a", "#0f1a2e", "#eef2f7"),
    "teal":       ("#0e5e6f", "#0a3640", "#eef7f6"),
    "terracotta": ("#b5523b", "#4a1d12", "#fbf1ea"),
    "indigo":     ("#4a3f8c", "#231c52", "#f3f1fb"),
    "forest":     ("#3b6e4f", "#173323", "#eff6f0"),
}


def flatten(im):
    """RGBA originals have transparent backgrounds; put them on white."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, "white")
        bg.alpha_composite(im)
        im = bg
    return im.convert("RGB")


def duotone(im, dark, light, gamma=1.0):
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
    if gamma != 1.0:                           # >1 darkens mid-tones, so thin plot lines stay visible
        g = g.point(lambda v: 255 * (v / 255) ** gamma)
    return ImageOps.colorize(g, black=dark, white=light)


def thumbnail(figure, label, palette, pad=56, gamma=1.0):
    bg, dark, light = PALETTES[palette]
    img = Image.new("RGB", (W, H), bg)

    # card geometry: starts left/top of centre and runs past the right and bottom edges
    cx, cy, cw, ch = 330, 240, W - 330 + 60, H - 240 + 60
    radius = 26

    # soft shadow
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((cx, cy + 18, cx + cw, cy + ch + 18), radius, fill=95)
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    img.paste(Image.new("RGB", (W, H), "#000000"), (0, 0), shadow)

    # card face with the duotoned figure inset by `pad` (0 = photo bleeds to the card edge)
    card = Image.new("RGB", (cw, ch), light)
    fig = duotone(figure, dark, light, gamma)
    scale = (cw - 2 * pad) / fig.width if pad else cw / fig.width
    fig = fig.resize((round(fig.width * scale), round(fig.height * scale)), Image.LANCZOS)
    card.paste(fig, (pad, pad))
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, ch - 1), radius, fill=255)
    img.paste(card, (cx, cy), mask)

    # category label, small caps with light tracking, in the card's highlight colour
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 60)
    x, y = 96, 112
    for ch_ in label.upper():
        d.text((x, y), ch_, font=font, fill=light, anchor="ls")
        x += d.textlength(ch_, font=font) + 5
    d.line((96, 150, 166, 150), fill=light, width=5)
    return img


def save(img, path):
    img.resize((OUT_W, OUT_H), Image.LANCZOS).save(path, "JPEG", quality=88, optimize=True, progressive=True)
    print(path, os.path.getsize(path) // 1024, "KB")


# ---------------------------------------------------------------- sCT figure (no original image yet)
def shepp_logan(n=320):
    """Modified Shepp-Logan phantom, rendered with MRI-like and CT-like contrast."""
    E = [(1.0, .69, .92, 0, 0, 0), (-.8, .6624, .874, 0, -.0184, 0), (-.2, .11, .31, .22, 0, -18),
         (-.2, .16, .41, -.22, 0, 18), (.1, .21, .25, 0, .35, 0), (.1, .046, .046, 0, .1, 0),
         (.1, .046, .046, 0, -.1, 0), (.1, .046, .023, -.08, -.605, 0), (.1, .023, .023, 0, -.606, 0),
         (.1, .023, .046, .06, -.605, 0)]
    y, x = np.mgrid[1:-1:n * 1j, -1:1:n * 1j]
    ct = np.zeros((n, n))
    masks = []
    for v, a, b, x0, y0, phi in E:
        p = np.deg2rad(phi)
        xr = (x - x0) * np.cos(p) + (y - y0) * np.sin(p)
        yr = -(x - x0) * np.sin(p) + (y - y0) * np.cos(p)
        m = (xr / a) ** 2 + (yr / b) ** 2 <= 1
        masks.append(m)
        ct[m] += v
    head, brain = masks[0], masks[1]
    skull, ventricles = head & ~brain, masks[2] | masks[3]
    mri = np.zeros_like(ct)
    mri[brain] = 0.68
    mri[brain & (ct > 0.25)] = 0.88
    mri[ventricles & brain] = 0.28
    mri[skull] = 0.12
    mri[head] += np.random.default_rng(7).normal(0, 0.035, head.sum())
    sct = np.zeros_like(ct)
    sct[brain] = 0.32 + 0.25 * np.clip(ct[brain] - 0.2, -0.2, 0.2)
    sct[skull] = 0.97
    to_im = lambda a: Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return to_im(mri), to_im(sct)


def sct_figure():
    """A plain paper-style figure: MRI and synthetic CT panels with captions."""
    mri, sct = shepp_logan()
    s, gap, cap = 440, 150, 70
    fig = Image.new("RGB", (2 * s + gap, s + cap), "white")
    fig.paste(mri.resize((s, s)), (0, 0))
    fig.paste(sct.resize((s, s)), (s + gap, 0))
    d = ImageDraw.Draw(fig)
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 30)
    d.text((s / 2, s + 38), "(a) MRI", font=font, fill="#333333", anchor="mm")
    d.text((s + gap + s / 2, s + 38), "(b) Synthetic CT", font=font, fill="#333333", anchor="mm")
    ay = s / 2
    d.line((s + 30, ay, s + gap - 34, ay), fill="#333333", width=5)
    d.polygon([(s + gap - 24, ay), (s + gap - 46, ay - 14), (s + gap - 46, ay + 14)], fill="#333333")
    return fig


# ---------------------------------------------------------------- Semanthai figure
def semanthai_figure():
    """Semantic role labelling of a Thai sentence, drawn like a linguistics paper figure."""
    words = [("นักเรียน", "ARG0", "student"), ("อ่าน", "V", "read"),
             ("หนังสือ", "ARG1", "book"), ("ในห้องสมุด", "ARGM-LOC", "in the library")]
    fig = Image.new("RGB", (1500, 640), "white")
    d = ImageDraw.Draw(fig)
    thai = ImageFont.truetype("C:/Windows/Fonts/LeelaUIb.ttf", 76)   # avoid stacked tone marks: no text shaping
    role = ImageFont.truetype(FONT, 36)
    gloss = ImageFont.truetype("C:/Windows/Fonts/segoeuii.ttf", 34)
    ink = "#222222"
    gap, padx, y, bh = 34, 38, 330, 130
    widths = [d.textbbox((0, 0), w, font=thai)[2] + 2 * padx for w, _, _ in words]
    x = (fig.width - sum(widths) - gap * (len(words) - 1)) / 2
    centers = []
    for (w, r, g), bw in zip(words, widths):
        verb = r == "V"
        d.rounded_rectangle((x, y, x + bw, y + bh), 22, fill=ink if verb else "white", outline=ink, width=4)
        d.text((x + bw / 2, y + bh / 2 + 4), w, font=thai, anchor="mm", fill="white" if verb else ink)
        d.text((x + bw / 2, y + bh + 50), g, font=gloss, anchor="mm", fill="#555555")
        centers.append(x + bw / 2)
        x += bw + gap
    # arcs from the predicate to each argument, labelled with PropBank roles
    vx = centers[1]
    for cx, (_, r, _) in zip(centers, words):
        if r == "V":
            continue
        h = 230 if r == "ARGM-LOC" else 120
        left, right = min(cx, vx), max(cx, vx)
        d.arc((left, y - 8 - h, right, y - 8 + h), 180, 360, fill=ink, width=4)
        d.polygon([(cx - 12, y - 26), (cx + 12, y - 26), (cx, y - 6)], fill=ink)
        d.text(((left + right) / 2, y - 8 - h - 30), r, font=role, anchor="mm", fill=ink)
    return fig


# ---------------------------------------------------------------- Microplastics figure
def ftir_figure():
    """(a) plastic fragments on a membrane filter, (b) FTIR transmittance of sample vs. filter."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Polygon

    rng = np.random.default_rng(11)
    plt.rcParams.update({"font.family": "Segoe UI", "font.size": 22, "axes.linewidth": 2,
                         "xtick.major.width": 2, "ytick.major.width": 2})
    fig = plt.figure(figsize=(14, 6.4), dpi=100)
    fig.patch.set_facecolor("white")

    # (a) filter disc with fragments
    ax = fig.add_axes([0.02, 0.12, 0.33, 0.82])
    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(-1.08, 1.08)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Circle((0, 0), 1, facecolor="#eeeeee", edgecolor="#222222", linewidth=2.5))
    for i in range(14):
        k = rng.integers(5, 9)
        rad = rng.uniform(0.05, 0.16) * rng.uniform(0.6, 1.2, k)
        ang = np.sort(rng.uniform(0, 2 * np.pi, k))
        c = rng.uniform(-0.62, 0.62, 2)
        ax.add_patch(Polygon(np.c_[c[0] + rad * np.cos(ang), c[1] + rad * np.sin(ang)],
                             facecolor="#555555" if i % 3 else "#999999", edgecolor="#222222", linewidth=1.2))
    fig.text(0.185, 0.03, "(a) Filter sample", ha="center", fontsize=24, color="#333333")

    # (b) FTIR spectrum: wavenumber decreases to the right, absorption bands point down
    ax = fig.add_axes([0.47, 0.25, 0.5, 0.68])
    wn = np.linspace(4000, 400, 1500)

    def bands(peaks):
        return sum(a * w ** 2 / ((wn - c) ** 2 + w ** 2) for c, w, a in peaks)

    plastic = 96 - 62 * bands([(2915, 60, .9), (2848, 48, .75), (1470, 30, .5), (1375, 22, .15), (720, 22, .4)])
    membrane = 92 - 50 * bands([(3350, 260, .25), (1735, 40, .3), (1210, 60, .7), (1150, 50, .55)])
    ax.plot(wn, membrane, color="#777777", lw=3, ls=(0, (6, 4)), label="Filter")
    ax.plot(wn, plastic, color="#111111", lw=3.6, label="Plastic")
    ax.set_xlim(4000, 400)
    ax.set_ylim(15, 100)
    ax.set_xticks([4000, 3000, 2000, 1000])
    ax.set_yticks([20, 60, 100])
    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("T (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0.3, 0.02), handlelength=1.6)
    fig.text(0.72, 0.03, "(b) FTIR spectra", ha="center", fontsize=24, color="#333333")

    fig.canvas.draw()
    im = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba(), "raw", "RGBA", 0, 1)
    plt.close(fig)
    return im.convert("RGB")


# ---------------------------------------------------------------- projects
def original(name, box):
    return flatten(Image.open(os.path.join(SRC, name))).crop(box)


PROJECTS = {
    # name: (figure factory, label, palette, card padding, duotone gamma)
    "sct":       (sct_figure, "Medical Imaging", "ink", 64, 1.0),
    "oja":       (lambda: original("oja.png", (0, 0, 860, 420)), "Data Visualization", "teal", 48, 1.15),
    "semanthai": (semanthai_figure, "Natural Language Processing", "terracotta", 64, 1.0),
    "raman":     (lambda: original("raman.jpg", (372, 0, 1105, 435)), "Raman Spectroscopy", "indigo", 48, 1.6),
    "ftir":      (ftir_figure, "Microplastics · FTIR", "forest", 64, 1.0),
}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else HERE
    os.makedirs(out, exist_ok=True)
    for name, (make, label, palette, pad, gamma) in PROJECTS.items():
        save(thumbnail(make(), label, palette, pad, gamma), os.path.join(out, name + ".jpg"))
