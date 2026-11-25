from art import *


def diamond():
    im, d = new()
    poly(d, [(4, 2), (14, 2), (17.5, 7), (9, 16.5), (0.5, 7)], (60, 220, 230, 255))
    poly(d, [(4, 2), (9, 7), (0.5, 7)], (150, 245, 250, 255))
    poly(d, [(14, 2), (9, 7), (17.5, 7)], (30, 170, 190, 255))
    poly(d, [(0.5, 7), (9, 7), (9, 16.5)], (40, 190, 205, 255))
    return finish(im)


def skull():
    im, d = new()
    w = (240, 240, 245, 255)
    ell(d, 2, 1, 16, 12.5, w)
    rect(d, 5, 10, 13, 16, w)
    k = (30, 25, 40, 255)
    ell(d, 4.2, 5.2, 7.6, 9, k)
    ell(d, 10.4, 5.2, 13.8, 9, k)
    poly(d, [(9, 9.3), (8, 11.3), (10, 11.3)], k)
    for x in (7, 9, 11):
        rect(d, x - 0.2, 13, x + 0.2, 16, k)
    return finish(im)


def smile():
    im, d = new()
    ell(d, 1, 1, 17, 17, (255, 205, 40, 255))
    k = (60, 40, 20, 255)
    ell(d, 5.2, 5.5, 7.2, 8.5, k)
    ell(d, 10.8, 5.5, 12.8, 8.5, k)
    d.arc([4.5 * S, 5.5 * S, 13.5 * S, 14.2 * S], 20, 160, fill=k, width=int(1.5 * S))
    return finish(im)


def bolt():
    im, d = new()
    poly(d, [(10.5, 0.8), (3.5, 10), (8, 10), (6.5, 17.2), (14.5, 7), (9.8, 7)], (255, 220, 40, 255))
    return finish(im)


def sun():
    im, d = new()
    for i in range(8):
        a = math.radians(i * 45)
        line(d, [(9 + 6.2 * math.cos(a), 9 + 6.2 * math.sin(a)), (9 + 8.4 * math.cos(a), 9 + 8.4 * math.sin(a))], (255, 190, 30, 255), 1.6)
    ell(d, 4, 4, 14, 14, (255, 215, 50, 255))
    return finish(im)


def moon():
    im, d = new()
    ell(d, 2, 1, 16, 17, (250, 225, 120, 255))
    ell(d, 6, -0.5, 19, 15.5, (0, 0, 0, 0))
    return finish(im)


def music():
    im, d = new()
    c = (80, 200, 255, 255)
    ell(d, 2.5, 12, 8, 16.5, c)
    ell(d, 10, 10.5, 15.5, 15, c)
    rect(d, 7, 3, 8.4, 14, c)
    rect(d, 14.5, 1.5, 15.9, 12.5, c)
    poly(d, [(7, 3), (15.9, 1), (15.9, 4.5), (7, 6.5)], c)
    return finish(im)


def gift():
    im, d = new()
    rect(d, 2, 7, 16, 16.5, (225, 50, 70, 255))
    rect(d, 1, 4.5, 17, 8.5, (240, 80, 95, 255))
    rect(d, 8, 4.5, 10, 16.5, (255, 215, 60, 255))
    ell(d, 4.5, 1, 9, 5, (255, 215, 60, 255))
    ell(d, 9, 1, 13.5, 5, (255, 215, 60, 255))
    return finish(im)


def sword():
    im, d = new()
    poly(d, [(15.5, 1), (17, 2.5), (7.5, 12), (6, 10.5)], (215, 225, 235, 255))
    poly(d, [(5, 9.5), (8.5, 13), (7.3, 14.2), (3.8, 10.7)], (255, 200, 40, 255))
    poly(d, [(5.2, 12.2), (6.8, 13.8), (3, 17.2), (1.3, 15.6)], (140, 90, 50, 255))
    return finish(im)


def shield():
    im, d = new()
    poly(d, [(9, 0.8), (16.5, 3), (16, 10), (9, 17.2), (2, 10), (1.5, 3)], (70, 110, 220, 255))
    poly(d, [(9, 2.8), (14.5, 4.4), (14, 9.5), (9, 15), (4, 9.5), (3.5, 4.4)], (110, 150, 245, 255))
    return finish(im)


def angkor():
    im, d = new()
    c = (225, 205, 160, 255)
    rect(d, 0.5, 14, 17.5, 16.5, c)
    rect(d, 1.5, 11.5, 16.5, 14, c)
    for cx, h in ((3.2, 7), (14.8, 7), (6.3, 5), (11.7, 5), (9, 1)):
        poly(d, [(cx - 1.5, 11.5), (cx - 1.2, 11.5 - h * 0.45), (cx, 11.5 - h * 0.45 - 2), (cx, 11.5 - h), (cx, 11.5 - h * 0.45 - 2), (cx + 1.2, 11.5 - h * 0.45), (cx + 1.5, 11.5)], c)
    poly(d, [(7.6, 11.5), (8, 4), (9, 1.2), (10, 4), (10.4, 11.5)], c)
    return finish(im)


def sparkle(k=1.0):
    im, d = new()
    pts = []
    for i in range(8):
        r = (8.5 if i % 2 == 0 else 1.9) * k
        a = math.radians(-90 + i * 45)
        pts.append((9 + r * math.cos(a), 9 + r * math.sin(a)))
    poly(d, pts, (255, 245, 170, 255))
    return finish(im)


STATIC = [
    ("kh", flag), ("heart", heart), ("star", star), ("crown", crown), ("fire", fire),
    ("check", check), ("cross", cross), ("coin", coin), ("diamond", diamond), ("skull", skull),
    ("smile", smile), ("bolt", bolt), ("sun", sun), ("moon", moon), ("music", music),
    ("gift", gift), ("sword", sword), ("shield", shield), ("angkor", angkor), ("sparkle", sparkle),
]

ANIM = {
    "kh_wave": [lambda p=p: flag(1.0, p) for p in (0, 1.57, 3.14, 4.71)],
    "heart_beat": [lambda k=k: heart(k) for k in (0.9, 1.1, 1.25)],
    "fire_dance": [lambda p=p: fire(p) for p in (0, 2.1, 4.2)],
    "star_spin": [lambda s=s: star(s) for s in (1.0, 0.6, 0.18, 0.6)],
    "coin_spin": [lambda s=s: coin(s) for s in (1.0, 0.62, 0.2, 0.62)],
    "sparkle_pulse": [lambda k=k: sparkle(k) for k in (0.55, 1.0, 0.75)],
  }
