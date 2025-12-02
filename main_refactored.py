import os
import json
from core.data_handling import load_matches_from_csv, read_template
from core.pdf_generation import make_overlay, apply_overlay, merge_pdfs_in_folder, cleanup

CONFIG_PATH = "config.json"
OUT_DIR = "output"
TMP_DIR = "tmp_overlays"

def load_config(path=CONFIG_PATH):
    """Load config.json"""
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


def main():
    cfg = load_config()
    
    # Ensure dirs exist
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)

    # Load matches directly from CSV
    matches = load_matches_from_csv(path=cfg["FIGHTCARD_CSV_PATH"], delimiter=",", has_header=True)
    
    template_reader, page_width, page_height = read_template(cfg["TEMPLATE_PATH"])

    for i, (match, blue, red) in enumerate(matches, start=1):
        texts = [match, blue, red]
        overlay = os.path.join(TMP_DIR, f"overlay_{i}.pdf")
        out = os.path.join(OUT_DIR, f"scorecard_{i:02d}.pdf")

        make_overlay(page_width, page_height, overlay, texts,
                     font_match=cfg["FONT_MATCH"], size_match=cfg["FONT_SIZE_MATCH"],
                     font_athlete=cfg["FONT_ATHLETE"], size_athlete=cfg["FONT_SIZE_ATHLETE"])

        apply_overlay(cfg["TEMPLATE_PATH"], overlay_path=overlay, output_path=out)
    
    cleanup(TMP_DIR)

    # Merge all scorecards into one file
    merged_output_path = os.path.join(OUT_DIR, cfg["MERGED_OUTPUT_FILENAME"])
    pattern = os.path.join(OUT_DIR, "scorecard_*.pdf")

    merge_pdfs_in_folder(pattern, merged_output_path, keep_inputs=cfg["KEEP_SINGLE_SCORECARDS"])

    print(f"Merged scorecards written to: {merged_output_path}")
    
    pass

if __name__ == "__main__":
    main()