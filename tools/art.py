from PIL import Image, ImageDraw, ImageFilter
import math

S = 8
W, H = 27, 18
INK = (28, 24, 40, 255)


def new():
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def sc(p):
    return [(x * S, y * S) for x, y in p]


def poly(d, p, c):
    d.polygon(sc(p), fill=c)


def ell(d, x0, y0, x1, y1, c):
    d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=c)


def rect(d, x0, y0, x1, y1, c):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=c)


def line(d, p, c, w):
    d.line(sc(p), fill=c, width=int(w * S), joint="curve")


def finish(im, outline=True):
    if outline:
        a = im.split()[3].filter(ImageFilter.MaxFilter(5))
        base = Image.new("RGBA", im.size, INK)
        base.putalpha(a)
        base.alpha_composite(im)
        im = base
    return im.resize((W, H), Image.LANCZOS)


def flag(amp=0.0, ph=0.0):
    im, d = new()
    blue, red = (3, 46, 161, 255), (224, 0, 37, 255)
    rect(d, 0, 0, 27, 4.5, blue)
    rect(d, 0, 4.5, 27, 13.5, red)
    rect(d, 0, 13.5, 27, 18, blue)
    wh = (255, 255, 255, 255)
    poly(d, [(7.5, 12), (7.5, 10.8), (19.5, 10.8), (19.5, 12)], wh)
    poly(d, [(8.5, 10.8), (8.5, 9.4), (18.5, 9.4), (18.5, 10.8)], wh)
    for cx, h in ((8.3, 3.2), (11.0, 4.4), (13.5, 6.0), (16.0, 4.4), (18.7, 3.2)):
        w = 0.9 if cx != 13.5 else 1.3
        poly(d, [(cx - w, 9.4), (cx - w * 0.7, 9.4 - h * 0.55), (cx, 9.4 - h), (cx + w * 0.7, 9.4 - h * 0.55), (cx + w, 9.4)], wh)
    if amp:
        out = Image.new("RGBA", im.size, (0, 0, 0, 0))
        for x in range(im.size[0]):
            o = int(math.sin(x / S * 0.38 + ph) * amp * S)
            out.paste(im.crop((x, 0, x + 1, im.size[1])), (x, o))
        im = out
    return finish(im, True)


def heart(k=1.0):
    im, d = new()
    pts = []
    for i in range(0, 361, 4):
        t = math.radians(i)
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((9 + x * 0.5 * k, 9.5 - y * 0.5 * k))
    poly(d, pts, (232, 36, 62, 255))
    ell(d, 4.2, 4.2, 6.6, 6.2, (255, 170, 180, 255))
    return finish(im)


def star(sx=1.0):
    im, d = new()
    pts = []
    for i in range(10):
        r = 8.6 if i % 2 == 0 else 3.7
        a = math.radians(-90 + i * 36)
        pts.append((9 + r * math.cos(a) * sx, 9.8 + r * math.sin(a)))
    poly(d, pts, (255, 200, 30, 255))
    poly(d, [(9, 9.8), (9 + 3.7 * math.cos(math.radians(-54)) * sx, 9.8 + 3.7 * math.sin(math.radians(-54))), (9, 1.2)], (255, 236, 130, 255))
    return finish(im)


def crown():
    im, d = new()
    g = (255, 200, 30, 255)
    poly(d, [(1.5, 14.5), (1, 5), (5.5, 9), (9, 2.5), (12.5, 9), (17, 5), (16.5, 14.5)], g)
    rect(d, 1.5, 13.5, 16.5, 16, (240, 160, 20, 255))
    for x, c in ((4.5, (230, 40, 60, 255)), (9, (40, 130, 240, 255)), (13.5, (40, 200, 90, 255))):
        ell(d, x - 1.1, 11.3, x + 1.1, 13.5, c)
    return finish(im)


def fire(ph=0.0):
    im, d = new()
    def fl(w, h, c, dy=0):
        a = math.sin(ph) * 0.9
        b = math.cos(ph) * 0.9
        base = 16.3 - dy
        ell(d, 9 - w, base - w * 1.3, 9 + w, base + w * 0.3, c)
        poly(d, [(9 - w, base - w * 0.5), (9 - w * 0.75 + a, base - h * 0.45), (9 - w * 0.2, base - h * 0.6),
                 (9 + a * 1.5, base - h), (9 + w * 0.3, base - h * 0.55), (9 + w * 0.8 - b, base - h * 0.4),
                 (9 + w, base - w * 0.5)], c)
    fl(5.6, 15, (240, 90, 20, 255))
    fl(3.9, 10.5, (255, 170, 30, 255), 0.4)
    fl(2.2, 6.5, (255, 240, 150, 255), 0.8)
    return finish(im)


def check():
    im, d = new()
    ell(d, 1, 1, 17, 17, (40, 190, 90, 255))
    line(d, [(4.8, 9.3), (7.8, 12.5), (13.4, 5.6)], (255, 255, 255, 255), 2.2)
    return finish(im)


def cross():
    im, d = new()
    ell(d, 1, 1, 17, 17, (225, 50, 60, 255))
    line(d, [(5.6, 5.6), (12.4, 12.4)], (255, 255, 255, 255), 2.2)
    line(d, [(12.4, 5.6), (5.6, 12.4)], (255, 255, 255, 255), 2.2)
    return finish(im)


def coin(sx=1.0):
    im, d = new()
    w = 8 * sx
    ell(d, 9 - w, 1, 9 + w, 17, (240, 170, 20, 255))
    ell(d, 9 - w * 0.78, 2.9, 9 + w * 0.78, 15.1, (255, 215, 70, 255))
    if sx > 0.5:
        rect(d, 8.2, 5.5, 9.8, 12.5, (230, 150, 15, 255))
    return finish(im)
