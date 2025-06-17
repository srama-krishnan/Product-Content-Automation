import unicodedata
import re

def normalize_input(text):
    text = text.strip().replace('\\', '')
    text = unicodedata.normalize('NFKC', text)
    return text.replace('"', '').replace("'", "")

def slugify_url(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r"[^\w\s-]", '', text).strip().lower()
    text = re.sub(r"[\s_]+", '-', text)
    return text
