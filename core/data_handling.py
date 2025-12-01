from PyPDF2 import PdfReader
import csv
from typing import List, Tuple, Union
import os


def read_template(template_path):
    """Open the PDF template and return the reader object and page size in points."""
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    reader = PdfReader(template_path)
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    return reader, width, height

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