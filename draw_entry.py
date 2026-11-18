# draw_entry.py — draws the news-image-20261118 front page (1024x1024 PNG)
# with PIL. All text is rendered from strings below; no external images,
# no network. Run: python3 draw_entry.py  -> writes entry.png beside it.
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (179, 32, 44)
NAVY = (31, 58, 95)
GREY = (90, 86, 76)
LIGHT_GREY = (120, 116, 106)
RULE = (60, 56, 48)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def text_h(draw, text, fnt):
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[3] - b[1]

# ---- icons (simple line pictograms) -------------------------------------
def icon_drone(d, x, y, s, c):
    cx, cy = x + s / 2, y + s / 2
    r = s * 0.30
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ex, ey = cx + dx * r, cy + dy * r
        d.line((cx, cy, ex, ey), fill=c, width=4)
        d.ellipse((ex - 13, ey - 5, ex + 13, ey + 5), fill=c)
    d.ellipse((cx - 16, cy - 11, cx + 16, cy + 11), fill=c)
    d.ellipse((cx - 6, cy - 5, cx + 6, cy + 5), fill=PAPER)

def icon_globe(d, x, y, s, c):
    cx, cy = x + s / 2, y + s / 2
    r = s * 0.42
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=4)
    d.ellipse((cx - r * 0.45, cy - r, cx + r * 0.45, cy + r), outline=c, width=3)
    d.line((cx - r, cy, cx + r, cy), fill=c, width=3)
    d.arc((cx - r, cy - r * 0.55, cx + r, cy + r * 0.55), 0, 360, fill=c, width=3)

def icon_chart(d, x, y, s, c):
    ox, oy = x + 6, y + s - 8
    d.line((ox, y + 8, ox, oy), fill=c, width=4)
    d.line((ox, oy, x + s - 4, oy), fill=c, width=4)
    pts = [(ox + 4, y + 14), (ox + 22, y + 26), (ox + 34, y + 22),
           (ox + 48, y + 40), (ox + 62, y + 52)]
    d.line(pts, fill=c, width=4, joint="curve")
    d.polygon([(ox + 62, y + 52), (ox + 50, y + 50), (ox + 60, y + 40)], fill=c)

def icon_chip(d, x, y, s, c):
    m = s * 0.16
    d.rectangle((x + m, y + m, x + s - m, y + s - m), outline=c, width=4)
    d.rectangle((x + s * 0.36, y + s * 0.36, x + s * 0.64, y + s * 0.64),
                outline=c, width=3)
    for i in range(3):
        t = m + (s - 2 * m) * (0.25 + 0.25 * i)
        d.line((x + t, y + 2, x + t, y + m), fill=c, width=3)
        d.line((x + t, y + s - m, x + t, y + s - 2), fill=c, width=3)
        d.line((x + 2, y + t, x + m, y + t), fill=c, width=3)
        d.line((x + s - m, y + t, x + s - 2, y + t), fill=c, width=3)

def icon_scales(d, x, y, s, c):
    cx = x + s / 2
    d.line((cx, y + 6, cx, y + s - 12), fill=c, width=4)
    d.line((x + 8, y + 16, x + s - 8, y + 16), fill=c, width=4)
    d.line((cx - 4, y + 2, cx + 4, y + 2), fill=c, width=4)
    for sx in (x + 8, x + s - 8):
        d.line((sx, y + 16, sx - 10, y + 40), fill=c, width=3)
        d.line((sx, y + 16, sx + 10, y + 40), fill=c, width=3)
        d.arc((sx - 12, y + 32, sx + 12, y + 52), 0, 180, fill=c, width=3)
    d.line((x + 14, y + s - 8, x + s - 14, y + s - 8), fill=c, width=4)

def icon_ship(d, x, y, s, c):
    d.polygon([(x + 6, y + s * 0.62), (x + s - 6, y + s * 0.62),
               (x + s - 16, y + s * 0.86), (x + 16, y + s * 0.86)], fill=c)
    for i, col in enumerate((RED, NAVY, (60, 90, 60))):
        bx = x + 14 + i * (s * 0.24)
        d.rectangle((bx, y + s * 0.34, bx + s * 0.20, y + s * 0.60),
                    fill=col)
    d.line((x + 6, y + s * 0.94, x + s - 6, y + s * 0.94), fill=c, width=3)

# ---- page -----------------------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 34  # margin

# top eyebrow
f_eyebrow = font(SANS_B, 15)
eb = "ONE DAY  ·  SIX STORIES  ·  FROM THE WORLD'S NEWSWIRES"
d.text(((W - d.textlength(eb, font=f_eyebrow)) / 2, 26), eb,
       font=f_eyebrow, fill=GREY)

# masthead
f_mast = font(SERIF, 56)
mast = "THE WORLD IN ONE PAGE"
d.text(((W - d.textlength(mast, font=f_mast)) / 2, 48), mast,
       font=f_mast, fill=INK)
d.rectangle((M, 118, W - M, 122), fill=INK)
d.rectangle((M, 126, W - M, 128), fill=RED)

# date line
f_date = font(SERIF, 38)
date = "WEDNESDAY  18  NOVEMBER  2026"
d.text(((W - d.textlength(date, font=f_date)) / 2, 138), date,
       font=f_date, fill=RED)
f_sub = font(SERIF_IT, 20)
sub = "Six stories that defined the day — as reported on 18 November 2026"
d.text(((W - d.textlength(sub, font=f_sub)) / 2, 182), sub,
       font=f_sub, fill=GREY)

# ---- lead story: Iran / Bahrain -------------------------------------------
ly0, ly1 = 214, 392
d.rectangle((M, ly0, W - M, ly1), outline=RULE, width=2)
d.rectangle((M, ly0, W - M, ly0 + 4), fill=RED)
f_kick = font(SANS_B, 16)
d.text((M + 16, ly0 + 16), "THE GULF  —  LEAD STORY", font=f_kick, fill=RED)
f_h1 = font(SERIF, 33)
h1 = ["Iran's drones target US radar",
      "in Bahrain — America hits back"]
y = ly0 + 40
for ln in h1:
    d.text((M + 16, y), ln, font=f_h1, fill=INK)
    y += 40
f_b1 = font(SANS, 17)
b1 = ("Iran's Revolutionary Guard launched drones at a US radar at Isa Air "
      "Base. Bahrain and US Central Command say all were intercepted. "
      "US jets hit back on Qeshm Island.")
b1_lines = wrap(d, b1, f_b1, 720)
assert len(b1_lines) <= 2, b1_lines
for ln in b1_lines:
    d.text((M + 16, y + 6), ln, font=f_b1, fill=INK)
    y += 22
icon_drone(d, W - M - 150, ly0 + 52, 120, NAVY)

# ---- 2x2 grid --------------------------------------------------------------
cells = [
    ("ASIA  ·  DIPLOMACY", "Quad meets in Manila,",
     "first summit in two years",
     "Trump hosts Modi, Takaichi and Albanese. Joint maritime-patrol "
     "drills agreed. Trump meets Marcos today, then heads to APEC in "
     "Shenzhen.", icon_globe),
    ("MARKETS", "Dow plunges 1,000 points",
     "in a day of selling",
     "The Dow fell 849 to 50,759; the S&P 500 had its lowest close "
     "since late July. An NSA network outage scare and AI doubts hit "
     "tech; Salesforce fell 9.5%.", icon_chart),
    ("TECH  ·  AI", "Nvidia's record $115.8bn —",
     "but no Huang return",
     "Revenue up 103% beat forecasts. The board says it “does not "
     "intend to reinstate” ex-CEO Jensen Huang; CFO Colette Kress "
     "stays on as interim chief.", icon_chip),
    ("MIDDLE EAST", "UK sanctions eight",
     "settlement firms",
     "Britain froze the assets of Israeli firms building West Bank "
     "settlements, and of Tzav 9, accused of blocking Gaza aid. "
     "Israel vowed countermeasures.", icon_scales),
]
gx, gy = M, 408
cw, ch, gap = 468, 196, 20
f_k2 = font(SANS_B, 15)
f_h2 = font(SERIF, 27)
f_b2 = font(SANS, 17)
for i, (kick, h_a, h_b, body, icon) in enumerate(cells):
    cx = gx + (i % 2) * (cw + gap)
    cy = gy + (i // 2) * (ch + gap)
    d.rectangle((cx, cy, cx + cw, cy + ch), outline=RULE, width=2)
    d.text((cx + 14, cy + 12), kick, font=f_k2, fill=RED)
    icon(d, cx + cw - 66, cy + 10, 54, NAVY)
    d.text((cx + 14, cy + 38), h_a, font=f_h2, fill=INK)
    d.text((cx + 14, cy + 70), h_b, font=f_h2, fill=INK)
    yy = cy + 106
    for ln in wrap(d, body, f_b2, cw - 28):
        d.text((cx + 14, yy), ln, font=f_b2, fill=INK)
        yy += 22

# ---- bottom band: Canada–China ---------------------------------------------
by0, by1 = 828, 944
d.rectangle((M, by0, W - M, by1), outline=RULE, width=2)
d.rectangle((M, by0, M + 6, by1), fill=NAVY)
d.text((M + 18, by0 + 12), "TRADE", font=f_k2, fill=RED)
f_h3 = font(SERIF, 28)
d.text((M + 18, by0 + 36), "Canada and China cut tariffs in Shenzhen",
       font=f_h3, fill=INK)
f_b3 = font(SANS, 17)
b3 = ("Xi Jinping and Mark Carney agreed tariff relief on about C$400m of "
      "Canadian pork and seafood, while Canada extends steel and aluminium "
      "remissions for two more years.")
yy = by0 + 70
b3_lines = wrap(d, b3, f_b3, W - 2 * M - 36)
assert len(b3_lines) <= 2, b3_lines
for ln in b3_lines:
    d.text((M + 18, yy), ln, font=f_b3, fill=INK)
    yy += 20

# ---- footer ------------------------------------------------------------------
d.rectangle((M, 958, W - M, 959), fill=RULE)
f_f = font(SANS, 14)
foot = ("ALSO:  Cyclone Akvan strengthens into a severe storm off India's "
        "east coast  •  APEC leaders meet in Shenzhen  •  Fed minutes at "
        "19:00 GMT")
d.text((M, 968), foot, font=f_f, fill=INK)
f_src = font(SERIF_IT, 13)
src = "Sources: Reuters, AP, Al Jazeera, CNN, MarketWatch, FXStreet, IMD."
d.text((M, 988), src, font=f_src, fill=LIGHT_GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
