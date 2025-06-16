🧠 Flashcard Generator from PDF

A simple and powerful Streamlit web application that automatically generates flashcards from structured PDF documents. Ideal for students, educators, and self-learners who want to convert study material into bite-sized flashcards for effective revision.


📖 Description

The Flashcard Generator reads a PDF file, detects section headings, and uses them to create flashcard titles. The paragraphs under each heading become the corresponding answers. This offline tool does not rely on any AI or cloud-based services — it works entirely on your local machine.

🔍 How It Works
- Extracts text from PDF files using `pdfplumber`
- Uses a regular expression to detect section headings (e.g., `CHAPTER 1`, `1. INTRODUCTION`)
- Pairs each heading with its following paragraph(s) to create a flashcard
- Displays flashcards in an expandable format using Streamlit



🚀 Features

- 📄 PDF Upload from the sidebar
- 🔍 Auto-detects headings as flashcard questions
- ✍️ Captures related paragraphs as answers
- 📚 Clean and simple flashcard viewer
- ⚙️ No OpenAI or internet API dependency
- 🖥️ Runs locally in your browser via Streamlit
