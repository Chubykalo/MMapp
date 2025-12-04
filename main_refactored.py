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


def main(matches_data=None, output_path=None):
    cfg = load_config()

    # Ensure dirs exist
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)
    
    # Determine matches
    if matches_data is not None:
        matches = matches_data
    
    else:
        # Load matches directly from CSV
        matches = load_matches_from_csv(path=cfg["FIGHTCARD_CSV_PATH"], delimiter=",", has_header=True)

    # Determine output directory
    if output_path is not None:
        final_output = output_path
        output_directory = os.path.dirname(output_path)

    else:
        final_output = os.path.join(OUT_DIR, cfg["MERGED_OUTPUT_FILENAME"])
        output_directory = OUT_DIR

    # Read template
    template_reader, page_width, page_height = read_template(cfg["TEMPLATE_PATH"])

    # Main program logic
    for i, (match, blue, red) in enumerate(matches, start=1):
        texts = [match, blue, red]
        overlay = os.path.join(TMP_DIR, f"overlay_{i}.pdf")
        out = os.path.join(output_directory, f"scorecard_{i:02d}.pdf")

        make_overlay(page_width, page_height, overlay, texts,
                     font_match=cfg["FONT_MATCH"], size_match=cfg["FONT_SIZE_MATCH"],
                     font_athlete=cfg["FONT_ATHLETE"], size_athlete=cfg["FONT_SIZE_ATHLETE"])

        apply_overlay(cfg["TEMPLATE_PATH"], overlay_path=overlay, output_path=out)
    
    cleanup(TMP_DIR)

    # Merge all scorecards into one file
    
    pattern = os.path.join(output_directory, "scorecard_*.pdf")
    merge_pdfs_in_folder(pattern, final_output, keep_inputs=cfg["KEEP_SINGLE_SCORECARDS"])

    print(f"Merged scorecards written to: {output_directory}")
    

if __name__ == "__main__":
    main()