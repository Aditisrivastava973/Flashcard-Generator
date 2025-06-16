import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="🧠 Smart Flashcard Generator", page_icon="📚", layout="wide")

# Sidebar Input Selection
st.sidebar.header("📄 Choose Input Method")
input_method = st.sidebar.radio("Select input type:", ["PDF", "TXT", "Manual Text"])

uploaded_file = None
manual_input = ""

if input_method in ["PDF", "TXT"]:
    file_types = ["pdf"] if input_method == "PDF" else ["txt"]
    uploaded_file = st.sidebar.file_uploader(f"Upload your {input_method} file", type=file_types)
elif input_method == "Manual Text":
    manual_input = st.sidebar.text_area("✍ Paste your text here", height=200)

# App Title
st.title("🧠 Flashcard Generator")
st.markdown("""
Upload a *well-structured PDF or TXT file* or paste your own text with *clear headings* and *paragraphs*.
Headings will become flashcard questions; paragraphs will be the answers.
""")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Function to extract text from TXT
def extract_text_from_txt(txt_file):
    return txt_file.read().decode("utf-8")

# Function to generate flashcards
def generate_flashcards(text):
    # Pattern matches:
    # 1. Markdown-style headings (e.g., "# Heading")
    # 2. Numbered headings (e.g., "1. Introduction")
    # 3. Lines in Title Case or ALL CAPS
    pattern = r"(?m)^(?:#{1,6}\s*|(?:\d+\.\s*)?)\s*([A-Z][A-Za-z\s\d,:-]{3,})$"
    matches = list(re.finditer(pattern, text))

    flashcards = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading = match.group(1).strip()
        content = text[start:end].strip().replace("\n", " ")
        if content:
            flashcards.append((heading, content))
    return flashcards

    return flashcards

# Function to show flashcards
def show_flashcards(flashcards):
    for heading, content in flashcards:
        with st.expander(f"📌 {heading}"):
            st.write(content)

# Flashcard Generation Button
if st.button("🚀 Generate Flashcards"):
    raw_text = ""

    if input_method == "PDF" and uploaded_file:
        with st.spinner("🔍 Reading PDF..."):
            raw_text = extract_text_from_pdf(uploaded_file)

    elif input_method == "TXT" and uploaded_file:
        with st.spinner("📄 Reading TXT file..."):
            raw_text = extract_text_from_txt(uploaded_file)

    elif input_method == "Manual Text" and manual_input.strip():
        raw_text = manual_input.strip()

    if raw_text:
        flashcards = generate_flashcards(raw_text)
        if flashcards:
            st.success(f"✅ Generated {len(flashcards)} flashcards!")
            show_flashcards(flashcards)
        else:
            st.warning("⚠ No headings or flashcards found. Please check your formatting.")
    else:
        st.error("❌ No input found. Please upload a file or paste text.")
else:
    st.info("📥 Upload or enter text, then click *Generate Flashcards*.")