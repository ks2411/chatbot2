#knowledge_base.py
import os
from openai import OpenAI


import hashlib
import shutil
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from utils import split_text, load_googledoc_by_url
from config import KNOWLEDGE_DB_URL, CHUNK_SIZE, CHUNK_OVERLAP

# Директория для кэша
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)  # Создаём директорию, если её нет

def get_cache_key(text):
    """Создаёт хеш-код для текста, чтобы использовать его в качестве ключа кэша."""
    return hashlib.md5(text.encode()).hexdigest()

def load_from_cache(key):
    """Загружает FAISS индекс из кэша, если он существует."""
    cache_path = os.path.join(CACHE_DIR, key)
    if os.path.exists(cache_path):
       
        try:
            return FAISS.load_local(cache_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"❌ Ошибка загрузки кэша: {e}")
    else:
        print(f"⚠️ Кэш не найден: {cache_path}")
    return None

def save_to_cache(key, vectordb):
    """Сохраняет FAISS индекс в кэш."""
    cache_path = os.path.join(CACHE_DIR, key)
    
    # Удаляем старый кэш, если он есть
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    
    try:
        print(f"💾 Сохраняем FAISS в {cache_path}")
        vectordb.save_local(cache_path)
        print(f"✅ Кэш сохранён в {cache_path}")
    except Exception as e:
        print(f"❌ Ошибка при сохранении FAISS: {e}")

def get_knowledge_base():
    """Загружает базу знаний из Google Docs, кэширует и индексирует её."""
    text = load_googledoc_by_url(KNOWLEDGE_DB_URL)
    cache_key = get_cache_key(text)
    
    cached_data = load_from_cache(cache_key)
    if cached_data:
       
        return cached_data  # Используем кэшированные данные

    print(f"⚠️ Кэш не найден. Загружаем базу знаний...")
    # Разбиение на части
    chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

    # Проверяем корректность разбиения
    if not chunks:
        print("❌ Ошибка: разбиение текста на части вернуло пустой список.")
        return None

    # Создание эмбеддингов и индексирование
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

    try:
        vectordb = FAISS.from_documents(chunks, embeddings)
    except Exception as e:
        print(f"❌ Ошибка создания FAISS: {e}")
        return None

    # Сохранение в кэш
    save_to_cache(cache_key, vectordb)
    
    return vectordb