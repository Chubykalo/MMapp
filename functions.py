from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
import os
import shutil
import csv
from typing import List, Tuple, Union
import glob
from pathlib import Path

TEMPLATE_PATH = "assets/scorecard_template.pdf"  # relative to your project folder

def read_template(template_path=TEMPLATE_PATH):
    """Open the PDF template and return the reader object and page size in points."""
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    reader = PdfReader(template_path)
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    return reader, width, height

def make_overlay(page_width_pt, page_height_pt, overlay_path, texts,
                 font_match, size_match, font_athlete, size_athlete):
    """
    Draw 'text' centered horizontally at (x_pt, y_pt) on a blank page the same size as template.
    Coordinates are in points.
    """
    texts = list(texts)

    fixed_positions = [
    # Scorecard 1 (left card)
    (200, page_height_pt - 80),   # Match
    (20, page_height_pt - 136),   # Blue
    (190, page_height_pt - 136),  # Red

    # Scorecard 2 (middle card)
    (471, page_height_pt - 80),   # Match
    (290, page_height_pt - 136),  # Blue
    (460, page_height_pt - 136),  # Red

    # Scorecard 3 (right card)
    (742, page_height_pt - 80),   # Match
    (561, page_height_pt - 136),  # Blue
    (731, page_height_pt - 136),  # Red

    # add / change coordinates here...
    ]
# -----------------------------------------

    c = canvas.Canvas(overlay_path, pagesize=(page_width_pt, page_height_pt))

    # enumerate lets me loop through fixed_positions.
    for pos_index, (x, y) in enumerate(fixed_positions):
        text_index = pos_index % len(texts)        # maps 0.. -> 0..n_texts-1 cyclically
        txt = texts[text_index]
        if text_index == 0:
            c.setFont(font_match, size_match)
        else:
            c.setFont(font_athlete, size_athlete)        
        c.drawString(x, y, txt)
    c.save()

def apply_overlay(template_path=TEMPLATE_PATH, overlay_path="overlay.pdf", output_path="scorecard_filled.pdf"):
    """
    Merge the overlay PDF onto the template PDF and save the result.
    """
    # Read the template PDF
    template_reader, page_width, page_height = read_template(template_path)
    
    # Read the overlay PDF
    overlay_reader = PdfReader(overlay_path)
    
    # Merge overlay onto the first page of the template
    template_page = template_reader.pages[0]
    overlay_page = overlay_reader.pages[0]
    template_page.merge_page(overlay_page)
    
    # Create a writer and add the merged page
    writer = PdfWriter()
    writer.add_page(template_page)
    
    # Save the final PDF
    with open(output_path, "wb") as f:
        writer.write(f)
    
    print(f"PDF saved as {output_path}")

def cleanup(tmp_dir: str = "tmp_overlays"):
    """
    Deletes the entire tmp_dir folder and all its contents.
    """
    shutil.rmtree(tmp_dir)
    print("temp_overlays cleaned")

def load_matches_from_csv(
    path: str,
    delimiter: str = ",",
    has_header: bool = True,
    encoding: str = "utf-8",
) -> List[Tuple[Union[int, str], str, str]]:
    """
    Load matches from a CSV file in the format:
        match_number, blue_athlete, red_athlete

    Returns a list of tuples: (match_number, blue, red)
    - blue and red athletes may be empty
    - blank CSV rows become ("", "", "")
    - extra CSV columns are ignored
    - order is preserved exactly as in the CSV
    """

    matches: List[Tuple[Union[int, str], str, str]] = []

    # Open the CSV file
    with open(path, newline="", encoding=encoding) as input_file:
        reader = csv.reader(input_file, delimiter=delimiter)

        # Skip header row if CSV has one
        if has_header:
            try:
                next(reader)
            except StopIteration:
                print("Warning: CSV appears empty.")
                return []

        # Process each remaining row
        for row in reader:

            # Guarantee three values (pad if needed)
            match_number_raw, blue_raw, red_raw = (row + ["", "", ""])[:3]

            # Always strip whitespace
            match_number = match_number_raw.strip()
            blue = blue_raw.strip()
            red = red_raw.strip()

            # Add the processed tuple (even if fields are empty)
            matches.append((match_number, blue, red))

    return matches

def merge_pdfs_in_folder(input_glob_pattern: str, output_path: str, keep_inputs: bool = True):
    """
    Merge all PDFs matching `input_glob_pattern` into a single PDF at `output_path`.
    - input_glob_pattern: e.g. "output/scorecard_*.pdf"
    - output_path: e.g. "output/scorecards_all.pdf"
    - keep_inputs: if False, deletes input PDFs after successful merge.
    Files are merged in lexicographic order of filename.
    """
    pdf_paths = sorted(glob.glob(input_glob_pattern))
    if not pdf_paths:
        raise FileNotFoundError(f"No PDFs found matching: {input_glob_pattern}")

    merger = PdfMerger()
    try:
        for p in pdf_paths:
            # Append each file. PdfMerger will open and close them itself.
            merger.append(p)
        # Write merged PDF
        with open(output_path, "wb") as file_output:
            merger.write(file_output)
    finally:
        merger.close()

    # Optionally remove input files after successful write
    if not keep_inputs:
        all_deleted = True  # assume success unless proven otherwise

        for p in pdf_paths:
            try:
                os.remove(p)
            except Exception as e:
                all_deleted = False       # mark failure
                print(f"Warning: failed to delete {p}: {e}")

        if all_deleted:
            print("Single scorecards deleted")


    return output_path


