import json
import os.path
from typing import List

import mif
import numpy as np

DEFAULTS_DIR = "defaults"
GENERATED_DIR = "generated"

CHARMAP_FILE = "charmap.mif"
CHARMAP_DESCRIPTION_FILE = "charmapDescription.json"


def read_charmap_from_mif(filepath: str):
    with open(filepath) as mif_file:
        binary_content = mif.load(mif_file)
    binary_content = binary_content.reshape(-1, 8, 8)
    charmap = binary_content.tolist()
    for char in charmap:
        for index, row in enumerate(char):
            char[index] = "".join(map(str, row))[::-1]
    return charmap


def save_charmap_to_mif(charmap: List[List[str]], filepath: str, as_64bit_wide: bool):
    width = 64 if as_64bit_wide else 8

    bin_charmap = []
    for char in charmap:
        bin_charmap.append([])
        for row in char:
            bin_row = [int(element) for element in row[::-1]]
            bin_charmap[-1].append(bin_row)

    bin_charmap = np.array(bin_charmap).reshape(-1, width)
    with open(filepath, "w") as mif_file:
        mif.dump(bin_charmap, mif_file, address_radix="UNS")


def read_charmap_and_description():
    charmap_file = os.path.join(GENERATED_DIR, CHARMAP_FILE)
    charmap_description_file = os.path.join(GENERATED_DIR, CHARMAP_DESCRIPTION_FILE)

    if not os.path.isfile(charmap_file) or not os.path.isfile(charmap_description_file):
        charmap_file = os.path.join(DEFAULTS_DIR, CHARMAP_FILE)
        charmap_description_file = os.path.join(DEFAULTS_DIR, CHARMAP_DESCRIPTION_FILE)

    charmap = read_charmap_from_mif(charmap_file)
    with open(charmap_description_file, "r") as f:
        charmapDescription = json.load(f)

    return charmap, charmapDescription


def save_charmap_and_description(charmap: List[List[str]], description, as_64bit_wide: bool):
    os.makedirs(GENERATED_DIR, exist_ok=True)

    charmap_file = os.path.join(GENERATED_DIR, CHARMAP_FILE)
    save_charmap_to_mif(charmap, charmap_file, as_64bit_wide)

    charmap_description_file = os.path.join(GENERATED_DIR, CHARMAP_DESCRIPTION_FILE)
    with open(charmap_description_file, "w") as f:
        json.dump(description, f, indent=4)
