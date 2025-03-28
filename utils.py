#utils.py
import re
import requests
import tiktoken
from datetime import datetime
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

# Класс для ANSI-цветов в консоли
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    BGGREEN = "\033[102m"
    BGYELLOW = "\033[103m"
    BGCYAN = "\033[106m"
    BGMAGENTA = "\033[105m"
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def load_googledoc_by_url(url: str) -> str:
    """Загружает текст из Google Docs по указанному URL."""
    match_ = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError("Некорректный URL Google Docs")
    doc_id = match_.group(1)
    response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    response.raise_for_status()
    return response.text

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Подсчитывает количество токенов в строке."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

def remove_newlines(text: str) -> str:
    """Удаляет все символы новой строки в строке."""
    return text.replace("\n", " ")

def insert_newlines(text: str, max_len: int = 160) -> str:
    """Добавляет переносы строк в длинные текстовые блоки."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) > max_len:
            lines.append(current_line)
            current_line = ""
        current_line += f" {word}"
    lines.append(current_line)
    
    return "\n".join(lines)

def split_text(text: str, chunk_size: int, chunk_overlap: int):
    """Разбивает текст на части для индексации (для FAISS)."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in docs]
