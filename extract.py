import re
import pytesseract
from PIL import Image

# ⚠️ Set path if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 🔹 Convert words → number
def words_to_number(text):
    words = {
        "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,
        "ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,
        "sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,
        "thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,
        "hundred":100,"thousand":1000
    }

    text = text.lower().split()
    total = 0
    current = 0

    for word in text:
        if word in words:
            val = words[word]
            if val in [100, 1000]:
                current *= val
            else:
                current += val
        else:
            total += current
            current = 0

    return total + current


# 🔥 FINAL SMART AMOUNT EXTRACTION
def extract_amount(text):
    text_lower = text.lower()

    # ✅ 1. "Rupees ... Only"
    match = re.search(r'rupees (.*?) only', text_lower)
    if match:
        word_amount = words_to_number(match.group(1))
        if word_amount > 0:
            return float(word_amount)

    # ✅ 2. "Paid" or "Amount"
    match = re.search(r'(paid|amount)[^\d]{0,10}(\d+\.?\d*)', text_lower)
    if match:
        return float(match.group(2))

    # ✅ 3. ₹ symbol
    match = re.search(r'₹\s*(\d+\.?\d*)', text)
    if match:
        return float(match.group(1))

    # ✅ 4. Extract all numbers
    numbers = re.findall(r'\d+\.\d+|\d+', text)
    numbers = [float(n) for n in numbers]

    # Remove obvious noise (time, year, small numbers)
    candidates = [n for n in numbers if 100 <= n <= 10000]

    if candidates:
        # Choose smallest realistic value (avoids picking IDs like 3278)
        return min(candidates)

    return "Not found"


# 🔹 Main OCR function
def extract_text_and_amount(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)

    # Clean OCR noise
    text = re.sub(r'[^a-zA-Z0-9@.:₹\s]', '', text)

    amount = extract_amount(text)

    return text, amount
