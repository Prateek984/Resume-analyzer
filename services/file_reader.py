import fitz  # PyMuPDF
from docx import Document
import pytesseract
from PIL import Image
import io
import os
from dotenv import load_dotenv


load_dotenv()

tesseract_path = os.getenv("TESSERACT_PATH")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def read_pdf(uploaded_file) -> str:
    """Extract text from PDF resume with OCR fallback"""

    file_bytes = uploaded_file.read()
    text = ""

    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")

        for page in pdf:
            text += page.get_text("text") + "\n"

    except Exception as e:
        print("PDF READ ERROR:", e)

    text = clean_text(text)

    # If very little text → scanned PDF → OCR
    if len(text) < 300:
        print("Running OCR fallback...")
        class TempFile:
            def read(self): return file_bytes
        return ocr_pdf(TempFile())

    return text

def ocr_pdf(uploaded_file) -> str:
    """OCR scanned PDF"""
    text = ""
    try:
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        for page in pdf:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text += pytesseract.image_to_string(img) + "\n"

    except Exception as e:
        print("OCR ERROR:", e)

    return clean_text(text)

def read_docx(uploaded_file) -> str:
    """Extract text from DOCX resume"""
    text = ""
    try:
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print("DOCX READ ERROR:", e)
    return clean_text(text)


def read_txt(uploaded_file) -> str:
    """Read plain text resume"""
    try:
        return clean_text(uploaded_file.read().decode("utf-8"))
    except Exception as e:
        print("TXT READ ERROR:", e)
        return ""


def extract_text(uploaded_file) -> str:
    """
    Detect file type and extract text automatically
    Streamlit uploader compatible
    """

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return read_pdf(uploaded_file)

    elif filename.endswith(".docx"):
        return read_docx(uploaded_file)

    elif filename.endswith(".txt"):
        return read_txt(uploaded_file)

    else:
        return ""


def clean_text(text: str) -> str:
    """Basic cleaning for better LLM parsing"""

    # Remove excessive blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    cleaned = "\n".join(lines)

    # Limit size (very large resumes break token limits)
    return cleaned[:15000]