import pdfplumber
import PyPDF2
import io


def extract_text_from_pdf(uploaded_file):
    """Try pdfplumber first, fall back to PyPDF2."""
    text = ""
    file_bytes = uploaded_file.read()

    # pdfplumber handles complex layouts better
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed: {e}, trying PyPDF2")

    # fallback
    if not text.strip():
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"PyPDF2 also failed: {e}")

    return text


def clean_resume_text(text):
    """Remove excessive blank lines and strip whitespace."""
    lines = text.splitlines()
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)


def truncate_resume(text, max_chars=4000):
    """Keep API costs low by capping resume length sent to Gemini."""
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]"
    return text


def get_resume_text(uploaded_file):
    """Full pipeline: extract → clean → truncate."""
    raw_text = extract_text_from_pdf(uploaded_file)
    cleaned = clean_resume_text(raw_text)
    return truncate_resume(cleaned)
