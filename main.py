import random
import sys
import os
from PIL import Image, ImageDraw, ImageFont

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

levels = ["10", "9", "8", "7", "6", "5", "4", "3", "j2", "2", "j1", "1"]
using_levels = list(range(12))
firsts = ["人", "言", "事", "無", "情", "私", "彼", "魔", "僕", "俺", "禾", "丿"]

kanjis = []

# params

width = 3830
height = 2174

random.seed(10)
use_random = True
save_path = "kanji_wallpaper.png"

kanji_size = 26
font = "Arial Unicode.ttf"
imagefont = ImageFont.truetype(font, kanji_size)
margin = 10

background_color = "#ffffff"
text_color = "#000000"
overwrite = True

level_color = {
    0: "#000000",    # 10級 
    1: "#000000",    # 9級
    2: "#000000",    # 8級
    3: "#000000",    # 7級
    4: "#000000",    # 6級
    5: "#000000",    # 5級
    6: "#000000",    # 4級
    7: "#000000",    # 3級
    8: "#000000",    # 準2級
    9: "#000000",    # 2級
    10: "#000000",   # 準1級
    11: "#000000",   # 1級
}

# read in settings
def apply_settings(path):
    global width, height, use_random, save_path, kanji_size, font, imagefont, margin, background_color, text_color, overwrite
    settings = []

    with open(path, "r") as f:
        for l in f.readlines():
            l = l[:-1]
            if ":" not in l:
                continue
            s = l.split(":")[1]
            s = s.strip()
            settings.append(s)

    # these settings must always be provided
    width = int(settings[0])
    height = int(settings[1])
    if settings[2].isdigit():
        random.seed(int(settings[2]))
    else:
        use_random = False
    save_path = settings[3]
    kanji_size = int(settings[4])
    font = settings[5]
    imagefont = ImageFont.truetype(font, kanji_size)
    margin = int(settings[6])
    background_color = settings[7]
    text_color = settings[8]
    overwrite = (settings[9] == "True")
    using_levels.clear()
    for lvl in settings[10].split(" "):
        if lvl:
            using_levels.append(levels.index(lvl))

    # level text color settings are optional
    for i in range(12):
        if settings[11+i]:
            level_color[i] = settings[11+i]
    
# read kanji
def read_kanji():
    lvl = -1
    with open("kanken6355.txt", "r") as f:
        for line in f.readlines():
            line = line[:-1]
            if line in firsts:
                lvl += 1
            if lvl in using_levels:
                kanjis.append((line, lvl))
    
    if use_random:
        random.shuffle(kanjis)

# generate wallpaper   
def generate_wallpaper():
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    x, y = margin, margin
    for k in kanjis:
        kanji, lvl = k
        color = text_color if overwrite else level_color[lvl]
        color = hex_to_rgb(color)
        draw.text((x, y), kanji, color, font=imagefont)

        x += kanji_size + margin
        if x + kanji_size + margin > width:
            x = margin
            y += kanji_size + margin

    image.save(save_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        apply_settings(os.path.join("settings", sys.argv[1] + ".txt"))

    read_kanji()
    generate_wallpaper()