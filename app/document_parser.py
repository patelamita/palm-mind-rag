from pypdf import PdfReader
from io import BytesIO


def extract_text_from_txt(content: bytes) -> str:
    return content.decode("utf-8")


def extract_text_from_pdf(content: bytes) -> str:
    pdf = PdfReader(BytesIO(content))

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text