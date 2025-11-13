from functions import *

def test_pdf_workflow():
    # Step 1: Read template to get page size
    template_reader, page_width, page_height = read_template()
    
    # Step 2: Create an overlay with a test text
    overlay_path = "overlay.pdf"
    texts = ["5", "Juan Carlos Guarino", "Daniel García"]
    
    # Call the function from functions.py
    make_overlay(page_width, page_height, overlay_path, texts,
                font_name="Helvetica-Bold", font_size=8.5)
    
    # Step 3: Merge overlay with template and save final PDF
    output_path = "scorecard_filled.pdf"
    apply_overlay(overlay_path=overlay_path, output_path=output_path)
    
    print("Test PDF workflow completed. Check 'scorecard_filled.pdf'.")

if __name__ == "__main__":
    test_pdf_workflow()