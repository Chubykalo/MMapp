# main.py
"""
Main program for generating scorecards.
Keeps configuration and program logic separate from functions.py helpers.
"""

import os
from functions import *

# -----------------------
# Configuration (edit here)
# -----------------------

TEMPLATE_PATH = "assets/scorecard_template.pdf"
FONT_MATCH = "Helvetica-Bold"
FONT_ATHLETE = "Helvetica"
FONT_SIZE_MATCH = 14
FONT_SIZE_ATHLETE = 8.5
OUT_DIR = "output"
TMP_DIR = "tmp_overlays"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

matches = [
    ("1", "Juan Pizarro", "Daniel García"),
    ("2", "Juan Carlos Serrano", "Gonzalo Lázaro"),
]

def main():
    template_reader, page_width, page_height = read_template(TEMPLATE_PATH)
    for i, (match, blue, red) in enumerate(matches, start=1):
        texts = [match, blue, red]
        overlay = os.path.join(TMP_DIR, f"overlay_{i}.pdf")
        out = os.path.join(OUT_DIR, f"scorecard_{i}.pdf")

        make_overlay(page_width, page_height, overlay, texts,
                     font_match=FONT_MATCH, size_match=FONT_SIZE_MATCH,
                     font_athlete=FONT_ATHLETE, size_athlete=FONT_SIZE_ATHLETE)

        apply_overlay(TEMPLATE_PATH, overlay_path=overlay, output_path=out)
    cleanup(TMP_DIR)

if __name__ == "__main__":
    main()