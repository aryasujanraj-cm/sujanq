from PIL import Image
import pytesseract
from categorize import categorize
from advice import give_advice
from extract import extract_amount
from storage import save_expense

# Set path for Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ask user for image path
image_path = input("Enter image path (example: test.png): ").strip()

try:
    # Load image
    img = Image.open(image_path)

    # Extract text using OCR
    text = pytesseract.image_to_string(img)

    print("\nExtracted Text:")
    print(text)

    # Extract amount
    amount = extract_amount(text)
    print("Amount:", amount)

    # Categorize expense
    category = categorize(text)
    print("Category:", category)

    # Save expense
    save_expense(amount, category)
    print("Expense saved!")

    # Ask user for financial advice
    user_input = input("\nDo you want financial advice? (yes/no): ").strip().lower()

    if user_input == "yes":
        print("Advice:", give_advice(category))
    elif user_input == "no":
        print("Okay 👍")
    else:
        print("Invalid input. Please type yes or no.")

except FileNotFoundError:
    print("Error: Image file not found. Please check the path.")
except Exception as e:
    print("Error:", e)