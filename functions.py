from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import os

TEMPLATE_PATH = "pdf/scorecard_template.pdf"  # relative to your project folder

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
