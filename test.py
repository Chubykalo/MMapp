
"""
Quick test to verify the refactored code works
"""
from core.data_handling import read_template, load_matches_from_csv
from core.pdf_generation import make_overlay, apply_overlay

# Test 1: Can we read the template?
print("Test 1: Reading template...")
reader, width, height = read_template("assets/scorecard_template.pdf")
print(f"✓ Template size: {width} x {height}")

# Test 2: Can we load CSV data?
print("\nTest 2: Loading CSV...")
matches = load_matches_from_csv("assets/test_fightcard2.csv")
print(f"✓ Loaded {len(matches)} matches")
print(f"  First match: {matches[0]}")

print("\n✓ All tests passed! The refactored code works.")