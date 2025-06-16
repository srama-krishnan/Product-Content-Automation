import unicodedata

def normalize_input(text):
    # Remove non-printable characters
    text = text.strip().replace('\\', '')
    # Normalize Unicode (e.g. accented letters)
    text = unicodedata.normalize('NFKC', text)
    return text.replace('"', '').replace("'", "")
