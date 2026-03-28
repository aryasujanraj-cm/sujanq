import streamlit as st
from PIL import Image
import pytesseract
from categorize import categorize
from advice import give_advice
from extract import extract_amount
from storage import save_expense

# Tesseract path (Windows)

st.title("💰 Financial Advisor & Expense Manager AI")

# Upload image
uploaded_file = st.file_uploader("📤 Upload a payment screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Show image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Extract text
    text = pytesseract.image_to_string(img)
    
    st.subheader("📝 Extracted Text")
    st.write(text)

    # Extract amount
    amount = extract_amount(text)
    st.subheader("💵 Amount")
    st.write(amount)

    # Categorize
    category = categorize(text)
    st.subheader("📂 Category")
    st.write(category)

    # Save expense
    save_expense(amount, category)
    st.success("✅ Expense saved!")

    # Advice button
    if st.button("💡 Get Financial Advice"):
        advice = give_advice(category)
        st.subheader("📊 Advice")
        st.write(advice)
