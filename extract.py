import re

def extract_amount(text):
    # Find numbers like 300, ₹300, 300.50
    match = re.search(r'(\₹?\d+\.?\d*)', text)
    
    if match:
        return match.group()
    else:
        return "Not found"