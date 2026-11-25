import hashlib, io, json, os, zipfile
from PIL import Image
import art2 as art

COLS = 16
names, frames = [], []
for n, f in art.STATIC:
    names.append(n)
    frames.append(f())
anim_map = {}
for n, fl in art.ANIM.items():
    anim_map[n] = []
    for i, f in enumerate(fl):
        anim_map[n].append(len(frames))
        names.append("%s_%d" % (n, i + 1))
        frames.append(f())

rows = (len(frames) + COLS - 1) // COLS
sheet = Image.new("RGBA", (COLS * art.W, rows * art.H), (0, 0, 0, 0))
chars = []
for r in range(rows):
    line = ""
    for c in range(COLS):
        i = r * COLS + c
        if i < len(frames):
            sheet.paste(frames[i], (c * art.W, r * art.H))
            line += "\\u%04X" % (0xE000 + i)
        else:
            line += "\\u0000"
    chars.append(line)

font = '{"providers":[{"type":"bitmap","file":"minecraft:font/rwchatemoji.png","ascent":8,"height":9,"chars":[%s]}]}' % ",".join('"%s"' % c for c in chars)
png = io.BytesIO()
sheet.save(png, "PNG")
icon = io.BytesIO()
frames[0].resize((135, 90), Image.NEAREST).crop((0, 0, 90, 90)).save(icon, "PNG")
mcmeta = '{"pack":{"description":"RW ChatEmoji emoji","min_format":69,"max_format":999}}'

os.makedirs("pack", exist_ok=True)
out = "pack/RWChatEmoji-pack.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in (("pack.mcmeta", mcmeta.encode()), ("pack.png", icon.getvalue()),
                       ("assets/minecraft/font/default.json", font.encode()),
                       ("assets/minecraft/textures/font/rwchatemoji.png", png.getvalue())):
        zi = zipfile.ZipInfo(name, (2024, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(zi, data)
open("pack/RWChatEmoji-pack.sha1", "w").write(hashlib.sha1(open(out, "rb").read()).hexdigest() + "\n")
with open("pack/codes.txt", "w") as f:
    for i, n in enumerate(names):
        f.write("%s \\u%04X\n" % (n, 0xE000 + i))
print(len(frames), "glyphs")
