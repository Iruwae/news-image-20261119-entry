#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: one broadsheet front page, 1024x1024.
All facts verified for Thursday 19 November 2026 (brief supplied by coordinator).
Every illustration is drawn here with PIL -- no photos, no downloads.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (192, 57, 43)
NAVY = (20, 38, 74)
BLUE = (43, 108, 176)
TAN = (217, 201, 163)
GREY = (90, 88, 80)
FD = "/usr/share/fonts/truetype/dejavu/"

def F(name, size):
    return ImageFont.truetype(FD + name, size)
SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)

def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(d, x, y, text, font, maxw, fill=INK, leading=None):
    lh = leading or int(font.size * 1.28)
    for line in wrap(d, text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y

def kicker(d, x, y, num, place, topic="", color=RED):
    txt = f"{num}  {place} · {topic}" if topic else f"{num}  {place}"
    d.text((x, y), txt, font=SANS_B(10), fill=color)
    return y + 14

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 16
CW = W - 2 * MX

d.text((MX, 8), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=RED)
right = "30 STORIES · 6 REGIONS · EVERY ONE DATED THURSDAY 19 NOVEMBER 2026"
d.text((W - MX - d.textlength(right, font=SANS_B(11)), 10),
       right, font=SANS_B(11), fill=INK)
d.line([(MX, 30), (W - MX, 30)], fill=INK, width=2)

title = "Thursday 19 November 2026"
tw = d.textlength(title, font=SERIF_B(58))
d.text(((W - tw) / 2, 36), title, font=SERIF_B(58), fill=INK)
sub = ("Kerch bridge attacked again · The Hague rules Myanmar guilty of genocide · "
       "Anthropic's record IPO soars")
sw = d.textlength(sub, font=SERIF(16))
d.text(((W - sw) / 2, 106), sub, font=SERIF(16), fill=INK)
d.line([(MX, 130), (W - MX, 130)], fill=INK, width=2)

stats = [
    ("9–6", "World Court vote: Myanmar guilty of genocide"),
    ("227 m", "of Kerch bridge road deck already down"),
    ("$97.17", "Anthropic's close, up 17% on its first day"),
    ("−3.24%", "Taiwan's share index, Thursday's close"),
    ("€45bn", "EU loan proposed for Ukraine for 2027"),
    ("700,000+", "Rohingya who fled to Bangladesh since 2017"),
]
sx, sy, swd = MX, 138, CW // 6
for i, (num, lab) in enumerate(stats):
    x = sx + i * swd
    if i:
        d.line([(x, sy + 4), (x, sy + 52)], fill=RED, width=2)
    d.text((x + 8, sy), num, font=SANS_B(26), fill=INK)
    para(d, x + 8, sy + 32, lab, SANS(10), swd - 14, leading=12)
d.line([(MX, 200), (W - MX, 200)], fill=INK, width=1)

regions = [("Europe 6", (43, 108, 176)), ("Asia 9", (192, 57, 43)),
           ("Middle East 4", (150, 110, 40)), ("Africa 3", (39, 120, 70)),
           ("Americas 1", (110, 60, 140)), ("Oceania 2", (30, 130, 140)),
           ("Global 5", (90, 88, 80))]
rx, ry, rh = MX, 206, 20
seg = CW // 7
for i, (lab, col) in enumerate(regions):
    x = rx + i * seg
    wdt = seg - 2 if i < 6 else CW - 6 * seg
    d.rectangle([x, ry, x + wdt, ry + rh], fill=col)
    tw2 = d.textlength(lab, font=SANS_B(11))
    d.text((x + (wdt - tw2) / 2, ry + 4), lab, font=SANS_B(11), fill=(255, 255, 255))

LY, LH_IMG = 234, 148
COLW = (CW - 16) // 3

def kerch(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 78))
    for sx_, sy_ in [(20, 12), (60, 26), (110, 10), (180, 20), (240, 14), (290, 30), (150, 34)]:
        d.ellipse([x + sx_, y + sy_, x + sx_ + 2, y + sy_ + 2], fill=(255, 255, 255))
    # sea
    d.rectangle([x, y + h - 52, x + w, y + h], fill=(28, 68, 120))
    # bridge deck with a collapsed gap in the middle
    d.rectangle([x, y + h - 78, x + 130, y + h - 66], fill=(200, 200, 200))
    d.rectangle([x + 190, y + h - 78, x + w, y + h - 66], fill=(200, 200, 200))
    for px in (30, 80, 230, 280):
        d.line([(x + px, y + h - 78), (x + px, y + h - 52)], fill=(160, 160, 160), width=3)
    # fallen deck pieces in the water
    d.polygon([(x + 140, y + h - 40), (x + 175, y + h - 30), (x + 160, y + h - 18),
               (x + 135, y + h - 26)], fill=(120, 120, 120))
    # fire + smoke at the gap
    d.ellipse([x + 150, y + h - 96, x + 176, y + h - 72], fill=(255, 140, 0))
    d.polygon([(x + 152, y + h - 76), (x + 163, y + h - 100), (x + 174, y + h - 76)], fill=(255, 200, 0))
    d.ellipse([x + 158, y + h - 118, x + 172, y + h - 104], fill=(180, 180, 180))
    # drone above
    d.ellipse([x + 250, y + 18, x + 282, y + 30], fill=(40, 40, 40))
    d.line([(x + 246, y + 24), (x + 286, y + 24)], fill=(200, 200, 200), width=2)
    for t in range(0, 8):
        tt = t / 7
        px = x + 266 - 60 * tt
        py = y + 32 + 50 * tt * tt
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 130))
    d.rectangle([x + 8, y + 8, x + 78, y + 30], fill=RED)
    d.text((x + 13, y + 12), "KERCH", font=SANS_B(15), fill=(255, 255, 255))
    d.rectangle([x + 8, y + 34, x + 108, y + 52], fill=(255, 255, 255))
    d.text((x + 12, y + 37), "227 m down", font=SANS_B(12), fill=INK)
    d.rectangle([x + 8, y + h - 20, x + 128, y + h - 4], fill=(0, 0, 0))
    d.text((x + 12, y + h - 18), "Traffic closed", font=SANS_B(10), fill=(255, 255, 255))

def hague(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    cx = x + w // 2
    # bigger courthouse: wide pediment, tall entablature, 6 tall columns
    d.polygon([(x + 8, y + 18), (cx, y + 4), (x + w - 8, y + 18)], fill=NAVY)
    d.rectangle([x + 8, y + 18, x + w - 8, y + 26], fill=NAVY)
    for i in range(6):
        bx = x + 22 + i * 48
        d.rectangle([bx, y + 26, bx + 20, y + 96], fill=(120, 110, 90))
        d.rectangle([bx - 2, y + 26, bx + 22, y + 31], fill=(90, 82, 66))
    # base + steps
    d.rectangle([x + 12, y + 96, x + w - 12, y + 104], fill=NAVY)
    d.rectangle([x + 8, y + 104, x + w - 8, y + 108], fill=(150, 140, 120))
    d.rectangle([x + 4, y + 108, x + w - 4, y + 112], fill=(150, 140, 120))
    # larger scales of justice, in front of the columns
    scx, scy = cx, y + 62
    d.ellipse([scx - 3, scy - 16, scx + 3, scy - 10], fill=INK)
    d.line([(scx, scy - 12), (scx, scy + 40)], fill=INK, width=4)
    d.line([(scx - 44, scy - 10), (scx + 44, scy - 10)], fill=INK, width=4)
    d.line([(scx - 44, scy - 10), (scx - 44, scy + 8)], fill=INK, width=2)
    d.line([(scx + 44, scy - 10), (scx + 44, scy + 8)], fill=INK, width=2)
    d.polygon([(scx - 58, scy + 8), (scx - 30, scy + 8), (scx - 44, scy + 22)], fill=RED)
    d.polygon([(scx + 30, scy + 8), (scx + 58, scy + 8), (scx + 44, scy + 22)], fill=RED)
    # "9-6" vote badge, top right
    bx0, by0 = x + w - 46, y + 44
    d.ellipse([bx0, by0, bx0 + 40, by0 + 40], fill=(255, 255, 255), outline=RED, width=3)
    tv = d.textlength("9–6", font=SANS_B(17))
    d.text((bx0 + 20 - tv / 2, by0 + 10), "9–6", font=SANS_B(17), fill=RED)
    # small flags flanking the pediment
    for fx, fcol in [(x + 16, (0, 120, 60)), (x + w - 30, (200, 16, 46))]:
        d.line([(fx, y + 40), (fx, y + 72)], fill=INK, width=2)
        d.polygon([(fx, y + 40), (fx + 16, y + 44), (fx, y + 48)], fill=fcol)
    # small figures at the foot of the steps
    for px in (x + 52, x + 78, x + w - 92, x + w - 66):
        d.ellipse([px - 4, y + 113, px + 4, y + 120], fill=INK)
        d.polygon([(px - 6, y + 120), (px + 6, y + 120), (px + 4, y + 127), (px - 4, y + 127)], fill=INK)
    d.rectangle([x + 8, y + 8, x + 108, y + 30], fill=RED)
    d.text((x + 13, y + 12), "THE HAGUE", font=SANS_B(15), fill=(255, 255, 255))
    d.rectangle([x + 8, y + 34, x + 150, y + 52], fill=(255, 255, 255))
    d.text((x + 12, y + 37), "GENOCIDE · VOTE 9–6", font=SANS_B(12), fill=INK)
    d.rectangle([x + 8, y + h - 20, x + 168, y + h - 4], fill=(0, 0, 0))
    d.text((x + 12, y + h - 18), "First state found guilty", font=SANS_B(10), fill=(255, 255, 255))

def ipo(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 26, 40))
    for gy in (y + 40, y + 70, y + 100):
        d.line([(x + 10, gy), (x + w - 10, gy)], fill=(70, 70, 95), width=1)
    pts = [(x + 16, y + 118), (x + 60, y + 104), (x + 100, y + 110),
           (x + 150, y + 66), (x + 200, y + 78), (x + 250, y + 40), (x + 296, y + 30)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(80, 220, 120), width=3)
    d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5], fill=(80, 220, 120))
    d.text((x + 12, y + 12), "$83 → $111.50 → $97.17", font=SANS_B(15), fill=(255, 255, 255))
    d.text((x + 12, y + 34), "priced · opened · closed", font=SANS(11), fill=(180, 180, 180))
    d.rectangle([x + 8, y + h - 44, x + 232, y + h - 24], fill=(255, 255, 255))
    d.text((x + 12, y + h - 41), "CLOSED +17% ON DAY ONE", font=SANS_B(12), fill=INK)
    d.rectangle([x + 8, y + h - 20, x + 158, y + h - 4], fill=(0, 0, 0))
    d.text((x + 12, y + h - 18), "$772m retail trading", font=SANS_B(10), fill=(255, 255, 255))

leads = [
    ("1", "KERCH, CRIMEA · WAR", "Kerch bridge attacked again",
     "Traffic closed after an overnight drone attack early Thursday. Tuesday's "
     "strike had already collapsed 227 m of road deck; the rail line still "
     "stands. (BBC, Guardian)", kerch),
    ("2", "THE HAGUE · WORLD COURT", "Myanmar guilty of genocide against the Rohingya",
     "The ICJ rules 9–6 — the first time a state has been found guilty of "
     "genocide. The 2017 campaign killed 10,000+ and drove 700,000+ to "
     "Bangladesh. Case brought by The Gambia in 2019. (UN News, BBC, AP)", hague),
    ("3", "NEW YORK · MARKETS", "Anthropic's record IPO soars on day one",
     "Priced at $83, it opened at $111.50 and closed Thursday at $97.17, up "
     "17%. First-day retail trading hit $772m; about 5,000 staff became "
     "millionaires.", ipo),
]
for i, (num, place, head, body, fn) in enumerate(leads):
    x = MX + i * (COLW + 8)
    fn(x, LY, COLW, LH_IMG)
    d.rectangle([x, LY, x + COLW, LY + LH_IMG], outline=INK, width=1)
    ty = LY + LH_IMG + 8
    kicker(d, x, ty, num, place, "")
    hy = ty + 16
    hy = para(d, x, hy, head, SANS_B(18), COLW, leading=21)
    para(d, x, hy + 2, body, SANS(11), COLW, leading=14)

# ---------- SMALL STORIES (2 rows x 5) ----------
SY = 516
SCW = (CW - 4 * 8) // 5
SH_IMG = 52

BANNERS = {
    "summit": "3-WAY SUMMIT",
    "gta": "GTA VI LAUNCHES",
    "euro": "EU €45BN LOAN",
    "refinery": "REFINERIES HIT",
    "mongolia": "PRESIDENT QUITS",
    "gaza": "GAZA OP ENDS",
    "yemen": "YEMEN WATER",
    "markets": "MARKETS SLIDE",
    "dhaka": "DHAKA UNREST",
    "apec": "OPEN TRADE",
}

def icon_panel(x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    # bold in-icon title banner (red strip, top of panel)
    d.rectangle([x, y, x + w, y + 19], fill=RED)
    bt = BANNERS[kind]
    fs = 13
    while fs > 10 and d.textlength(bt, font=SANS_B(fs)) > w - 10:
        fs -= 1
    twb = d.textlength(bt, font=SANS_B(fs))
    d.text((x + (w - twb) / 2, y + 3), bt, font=SANS_B(fs), fill=(255, 255, 255))
    # icon art lives in the 33 px zone below the banner
    iy = y + 19
    cx = x + w // 2
    if kind == "summit":  # three flags
        d.rectangle([x + 10, iy + 4, x + 56, iy + 30], fill=(200, 16, 46))
        d.rectangle([x + 10, iy + 15, x + 56, iy + 19], fill=(255, 255, 255))
        for sy_ in range(5):
            d.rectangle([x + 72, iy + 4 + sy_ * 5, x + 118, iy + 9 + sy_ * 5],
                        fill=(255, 255, 255) if sy_ % 2 else (222, 0, 0))
        d.rectangle([x + 134, iy + 4, x + 180, iy + 12], fill=(255, 255, 255))
        d.rectangle([x + 134, iy + 12, x + 180, iy + 21], fill=(0, 51, 153))
        d.rectangle([x + 134, iy + 21, x + 180, iy + 30], fill=(200, 16, 46))
    elif kind == "gta":  # game controller
        d.rectangle([x + 52, iy + 8, x + 140, iy + 26], fill=(30, 30, 30))
        d.ellipse([x + 44, iy + 18, x + 62, iy + 32], fill=(30, 30, 30))
        d.ellipse([x + 130, iy + 18, x + 148, iy + 32], fill=(30, 30, 30))
        d.rectangle([x + 60, iy + 12, x + 68, iy + 24], fill=(255, 255, 255))
        d.rectangle([x + 56, iy + 16, x + 72, iy + 20], fill=(255, 255, 255))
        for bx, by in [(118, iy + 10), (128, iy + 16), (118, iy + 20)]:
            d.ellipse([x + bx, by, x + bx + 7, by + 7], fill=(255, 200, 0))
    elif kind == "euro":  # euro coin + rising bars
        d.ellipse([x + 28, iy + 4, x + 76, iy + 30], fill=(255, 204, 0))
        d.text((x + 42, iy + 7), "€", font=SANS_B(20), fill=INK)
        for i, bh in enumerate((8, 14, 20, 26)):
            bx = x + 92 + i * 20
            d.rectangle([bx, iy + 30 - bh, bx + 14, iy + 30], fill=BLUE)
    elif kind == "refinery":  # refinery towers + flame
        for bx, bw, top in [(30, 18, 8), (58, 24, 6), (90, 16, 10)]:
            d.rectangle([x + bx, iy + top, x + bx + bw, iy + 30], fill=(90, 90, 90))
            d.polygon([(x + bx - 2, iy + top), (x + bx + bw // 2, iy + top - 6),
                       (x + bx + bw + 2, iy + top)], fill=(255, 140, 0))
        d.line([(x + 128, iy + 8), (x + 168, iy + 26)], fill=(120, 120, 120), width=4)
        d.text((x + 126, iy + 26), "x2", font=SANS_B(12), fill=RED)
    elif kind == "mongolia":  # parliament building
        d.polygon([(x + 20, iy + 10), (cx, iy + 2), (x + w - 20, iy + 10)], fill=INK)
        for i in range(4):
            bx = x + 34 + i * 40
            d.rectangle([bx, iy + 12, bx + 14, iy + 30], fill=(120, 110, 90))
        d.rectangle([x + 20, iy + 30, x + w - 20, iy + 32], fill=INK)
    elif kind == "gaza":  # aid boxes + cross
        for bx, by in [(24, 6), (84, 6), (54, 20)]:
            d.rectangle([x + bx, iy + by, x + bx + 44, iy + by + 12], fill=(200, 170, 120))
            d.rectangle([x + bx + 18, iy + by + 2, x + bx + 26, iy + by + 10], fill=RED)
            d.rectangle([x + bx + 14, iy + by + 4, x + bx + 30, iy + by + 8], fill=RED)
        d.text((x + 140, iy + 8), "4/26", font=SANS_B(13), fill=RED)
    elif kind == "yemen":  # water drop + tap
        d.polygon([(x + 46, iy + 2), (x + 32, iy + 20), (x + 60, iy + 20)], fill=BLUE)
        d.ellipse([x + 32, iy + 14, x + 60, iy + 30], fill=BLUE)
        d.rectangle([x + 90, iy + 8, x + 130, iy + 14], fill=(120, 120, 120))
        d.text((x + 136, iy + 6), "HALVED", font=SANS_B(11), fill=INK)
        d.text((x + 136, iy + 20), "800k cut off", font=SANS(9), fill=INK)
    elif kind == "markets":  # falling chart
        pts = [(x + 12, iy + 8), (x + 44, iy + 14), (x + 70, iy + 11), (x + 96, iy + 20),
               (x + 122, iy + 26), (x + 150, iy + 22), (x + 176, iy + 30)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=RED, width=3)
    elif kind == "dhaka":  # burning building
        d.rectangle([x + 44, iy + 6, x + 124, iy + 32], fill=(150, 140, 120))
        for wy in (14, 24):
            for wx in (54, 76, 98):
                d.rectangle([x + wx, iy + wy, x + wx + 12, iy + wy + 6], fill=(255, 220, 130))
        d.polygon([(x + 76, iy + 6), (x + 84, iy + 0), (x + 92, iy + 6)], fill=(255, 140, 0))
        d.ellipse([x + 134, iy + 4, x + 160, iy + 20], fill=(255, 140, 0))
    elif kind == "apec":  # globe + trade arrow
        d.ellipse([x + 16, iy + 6, x + 54, iy + 30], fill=BLUE)
        d.ellipse([x + 24, iy + 12, x + 36, iy + 20], fill=(80, 180, 90))
        d.ellipse([x + 36, iy + 20, x + 48, iy + 28], fill=(80, 180, 90))
        d.line([(x + 72, iy + 18), (x + 168, iy + 18)], fill=INK, width=3)
        d.polygon([(x + 168, iy + 12), (x + 182, iy + 18), (x + 168, iy + 24)], fill=INK)

smalls = [
    ("4", "SHENZHEN · SUMMIT", "Trump, Xi and Putin meet three-way",
     "First-ever three-way summit, ~70 min at APEC. Peace declaration; "
     "no Ukraine or Iran mention. (Reuters, AP)", "summit"),
    ("5", "WORLDWIDE · GAMES", "GTA VI launches on Thursday",
     "$1.84bn revenue, 19.05m units by release day. Reviews 99/100; "
     "2.3m watching. (CNN, Le Monde)", "gta"),
    ("6", "BRUSSELS · EUROPE", "EU proposes a €45bn loan for Ukraine",
     "The loan would fund Kyiv from the 2027 budget. (Reuters)", "euro"),
    ("7", "UKRAINE · WAR", "Ukraine strikes two Russian oil refineries",
     "Two refineries hit on 19 November, Kyiv says. (Reuters)", "refinery"),
    ("8", "ULAANBAATAR · POLITICS", "Mongolia's president quits",
     "Parliament approves President Khurelsukh's resignation; a snap "
     "election follows. (Reuters)", "mongolia"),
    ("9", "GAZA · WAR", "IDF Nuseirat operation ends after one day",
     "At least 4 killed on Thursday. Aid groups score the UN-backed plan "
     "4 out of 26. (AP)", "gaza"),
    ("10", "TAIZ, YEMEN · AID", "Taiz water output nearly halved",
     "More than 800,000 people are cut off from aid, UNICEF says. (UNICEF)", "yemen"),
    ("11", "MARKETS · THURSDAY", "Thursday's closes: Asia falls, US slides",
     "TAIEX −3.24%; Hang Seng −1.89%; Nikkei +0.72%. S&P 500 "
     "−2.02%, its 6th straight loss; Nasdaq −2.25%.", "markets"),
    ("12", "DHAKA · UNREST", "Bangladesh unrest: 4 killed",
     "Muhammad Yunus's ancestral home is set ablaze as unrest spreads. (AP)", "dhaka"),
    ("13", "SHENZHEN · APEC", "Xi: Asia-Pacific must adopt open trade",
     "China's leader presses the open-trade case at the APEC summit. (Xinhua)", "apec"),
]
for idx, (num, place, head, body, kind) in enumerate(smalls):
    row, col = divmod(idx, 5)
    x = MX + col * (SCW + 8)
    y = SY + row * 144
    icon_panel(x, y, SCW, SH_IMG, kind)
    ty = y + SH_IMG + 5
    kicker(d, x, ty, num, place, "")
    hy = ty + 14
    hy = para(d, x, hy, head, SANS_B(13), SCW, leading=15)
    para(d, x, hy + 1, body, SANS(10), SCW, leading=12)

# ---------- BOTTOM: map + briefs ----------
BY = 806
d.text((MX, BY), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
d.text((MX + 312, BY), "ALSO ON THURSDAY 19 NOVEMBER — 17 MORE STORIES",
       font=SANS_B(12), fill=INK)
d.line([(MX, BY + 17), (W - MX, BY + 17)], fill=INK, width=1)

mx0, my0, mw, mh = MX, BY + 22, 296, 118
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(214, 228, 235))
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], outline=INK, width=1)
d.polygon([(mx0 + 8, my0 + 28), (mx0 + 70, my0 + 14), (mx0 + 96, my0 + 26),
           (mx0 + 80, my0 + 48), (mx0 + 44, my0 + 52), (mx0 + 16, my0 + 44)], fill=TAN)
d.polygon([(mx0 + 66, my0 + 62), (mx0 + 96, my0 + 58), (mx0 + 104, my0 + 82),
           (mx0 + 88, my0 + 106), (mx0 + 72, my0 + 88)], fill=TAN)
d.polygon([(mx0 + 128, my0 + 22), (mx0 + 168, my0 + 14), (mx0 + 186, my0 + 30),
           (mx0 + 172, my0 + 52), (mx0 + 146, my0 + 48)], fill=TAN)
d.polygon([(mx0 + 150, my0 + 56), (mx0 + 190, my0 + 52), (mx0 + 200, my0 + 80),
           (mx0 + 182, my0 + 104), (mx0 + 160, my0 + 88)], fill=TAN)
d.polygon([(mx0 + 190, my0 + 18), (mx0 + 268, my0 + 10), (mx0 + 288, my0 + 34),
           (mx0 + 272, my0 + 62), (mx0 + 226, my0 + 66), (mx0 + 200, my0 + 44)], fill=TAN)
d.polygon([(mx0 + 252, my0 + 88), (mx0 + 284, my0 + 84), (mx0 + 288, my0 + 102),
           (mx0 + 258, my0 + 106)], fill=TAN)
pins = {1: (176, 36), 2: (136, 22), 3: (88, 38), 4: (262, 44), 5: (52, 56),
        6: (154, 34), 7: (190, 26), 8: (244, 28), 9: (184, 50), 10: (196, 64),
        11: (128, 44), 12: (224, 58), 13: (242, 64)}
for n, (px, py) in pins.items():
    d.ellipse([mx0 + px - 7, my0 + py - 7, mx0 + px + 7, my0 + py + 7],
              fill=RED, outline=(255, 255, 255), width=1)
    tw3 = d.textlength(str(n), font=SANS_B(8))
    d.text((mx0 + px - tw3 / 2, my0 + py - 5), str(n), font=SANS_B(8),
           fill=(255, 255, 255))
d.text((mx0 + 4, my0 + mh - 12), "Pins 1–13 mark the drawn stories",
       font=SANS(8), fill=GREY)

briefs = [
    "14 Berlin — Witkoff holds “substantive and frank” talks with Europe",
    "15 Paris — Le Monde exposes leak of probe into France’s RN party",
    "16 Global — Stocks fell Wed after Nvidia’s results",
    "17 Global — Dollar at a 19-month high after hawkish Fed signal",
    "18 Pakistan — Army killed at least 22 militants in raids",
    "19 Iraq — Deal at Jurf al-Sakhar with Kataib Hezbollah",
    "20 Gulf — US strike on Qeshm; Iran attacks in the Gulf",
    "21 Vietnam — Russian bombers return to Vietnam",
    "22 Global — WHO warns antibiotic resistance is worsening",
    "23 Space — Shenzhou-24 to carry first Pakistani astronaut",
    "24 India — 162.5% duty on bulk Scotch whisky",
    "25 Hobart — Duckett’s 133 leads England to victory",
    "26 Uganda — Bududa case at the UN Human Rights Committee",
    "27 Africa — Ethiopia and Eritrea mass troops at the border",
    "28 Antalya — COP31 talks grind into their final stretch",
    "29 Tonga — Tonga declares drought emergency (Reuters, RNZ)",
    "30 Senegal — Migrant boat sinks off Senegal (Reuters, AP)",
]
assert len(briefs) == 17, len(briefs)
bx0, by0 = MX + 312, BY + 24
bcolw = (W - MX - bx0 - 8) // 2
for i, b in enumerate(briefs):
    col, row = divmod(i, 10)
    x = bx0 + col * (bcolw + 8)
    y = by0 + row * 11
    d.text((x, y), b, font=SANS(8), fill=INK)

# ---------- DATE CHECK ----------
dy = 952
d.rectangle([MX, dy, W - MX, dy + 40], outline=RED, width=2)
dc = ("DATE CHECK  NOT 19 November, so left out: Nov 18 — House Democrats "
      "nominating Jeffries; Iran strikes on Kuwait and Bahrain. Nov 20 — the "
      "110+ missile attack on Kyiv; Cyclone Akvan's landfall; Friday's market "
      "closes; the UK–EU reset deal; COP31's final day. BepiColombo reaches "
      "Mercury on Sat 21 Nov.")
para(d, MX + 6, dy + 4, dc, SANS(10), CW - 12, leading=13)

# ---------- footer ----------
d.text((MX, 998), "Every story here happened, or was first reported, on Thursday "
       "19 November 2026. Officials' counts are attributed.",
       font=SANS(9), fill=INK)
ft = "Sources named beside each story · original drawings"
d.text((W - MX - d.textlength(ft, font=SANS(9)), 998), ft, font=SANS(9), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
