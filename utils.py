import csv

def convert(val):
    try:
        return float(val)
    except ValueError:
        return val

with open("SETTINGS/EnvVars.csv", "r") as f:
    ENV_VAR_DICT = {key: convert(val) for key, val in csv.reader(f)}

def coords_to_pixels(cords):
    return tuple([cord*ENV_VAR_DICT["TILE_SIZE"]+ENV_VAR_DICT["TILE_SIZE"]//2 for cord in cords])


def load_level_from_txt():
    decode_emoji_lst = {"⬜":"coin",
                        "⬛":"wall",
                        "😐":"pacman",
                        "😡":"r_ghost",
                        "⭐":"y_ghost",
                        "📘":"b_ghost",
                        "😈":"p_ghost",
                        "🍎":"coin"}
    with open("SETTINGS/level.txt", "r", encoding="utf-8") as file:
        return [[decode_emoji_lst[emoji] for emoji in row.strip()] for row in file.readlines()]