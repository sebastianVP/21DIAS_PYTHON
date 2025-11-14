import re

def clean_text(text):
    """
    Limpia saltos, espacios, headers, footers repetidos.
    """
    text = re.sub(r'\n+', '\n', text)  
    text = re.sub(r'\s+', ' ', text)
    return text.strip()