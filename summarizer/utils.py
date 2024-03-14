import fitz
from logger import log


def extract_text_from_pdf(filename: str):
    try:
        doc = fitz.open(filename)
        total_words = 0
        extracted_text = ""
        page_count = 0

        for page in doc:
            page_text: str = page.get_text()
            page_count += 1
            without_new_line = page_text.strip().replace("\n", " ") 
            log("Page", str(page_count) + ":", without_new_line)
            extracted_text += without_new_line
            total_words += len(page_text.split())

        return extracted_text, total_words
    except Exception as e:
        print(f"Error occurred while extracting text: {e}")
        return None, 0


def split_text(text: str, word_length: int, split_in_words: int) -> list[str]:
    try:
        text_array = []
        remaining_length = word_length

        while remaining_length >= 0:
            part = " ".join(text.split()[:split_in_words])
            text = " ".join(text.split()[split_in_words:])
            remaining_length -= split_in_words
            text_array.append(part)

        return text_array
    except Exception as e:
        print(f"Error occurred while splitting text: {e}")
        return []
