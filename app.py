# app.py

import streamlit as st
import pdfplumber
import re
import os
from pathlib import Path

st.set_page_config(page_title="🧠 Smart Flashcard Generator", page_icon="📚", layout="wide")

# Sidebar
st.sidebar.header("📄 Upload your PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

st.title("🧠Flashcard Generator")
st.markdown("""
Upload a well-formatted PDF with **headings** and **paragraphs** under each heading. 
The app will extract headings as flashcard titles and show the paragraph content as the answer.
""")

# --- Function to extract text from PDF ---
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# --- Function to create flashcards ---
def generate_flashcards(text):
    # Split on heading-style lines (e.g., lines in ALL CAPS or numbered headings)
    pattern = r"(?m)^(?:\d+\.\s*)?[A-Z][A-Z\s\d\.:,-]{3,}$"
    matches = list(re.finditer(pattern, text))

    flashcards = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        heading = match.group().strip()
        content = text[start:end].strip().replace("\n", " ")
        if content:
            flashcards.append((heading, content))

    return flashcards

# --- Show flashcards ---
def show_flashcards(flashcards):
    for i, (heading, content) in enumerate(flashcards):
        with st.expander(f"📌 {heading}"):
            st.write(content)

# --- App logic ---
if uploaded_file is not None:
    with st.spinner("Reading and extracting content..."):
        raw_text = extract_text_from_pdf(uploaded_file)
        flashcards = generate_flashcards(raw_text)

    if flashcards:
        st.success(f"✅ Generated {len(flashcards)} flashcards!")
        show_flashcards(flashcards)
    else:
        st.warning("⚠️ No headings or flashcards found. Try uploading a PDF with clear section headings.")
else:
    st.info("📂 Upload a PDF from the left sidebar to begin.")
