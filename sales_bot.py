# sales_bot.py
import openai

import os
from config import MODEL, TEMP, VERBOSE
from utils import remove_newlines
from text_processing import summarize_dialog, extract_entity_from_statement
from knowledge_base import get_knowledge_base




openai.api_key = os.getenv("OPENAI_API_KEY")

def get_seller_answer(history_user, history_manager, history_chat):
    """Основной процесс генерации ответа продавца на основе истории диалога."""

    # Получение базы знаний с кэшированием
    knowledge_base = get_knowledge_base()

    # Выделение сущностей из последнего сообщения клиента
    output_needs = extract_entity_from_statement(
        name="Потребности", 
        system="...",
        instructions="...",
        question=history_user[-1],
        history=[],
        temp=TEMP,
        verbose=VERBOSE
    ).choices[0].message.content

    # Суммаризация диалога
    summarized_dialog = summarize_dialog(
        dialog=history_chat, 
        history=history_chat, 
        temp=TEMP, 
        verbose=VERBOSE
    ).choices[0].message.content

    # Генерация ответа продавца
    messages = [
        {"role": "system", "content": " בשום אופן אל תוסיף כלום חוץ מאינפורמציה שקיבלת תמיד תענה ללקוח בשפה של הלקוח אתה מוכר במאפייה. ענה ללקוח בצורה הגיונית ורציפה."},


        {"role": "user", "content": f"Диалог: {summarized_dialog}\n\nВопрос клиента: {history_user[-1]}\n\nОтвет:"}
    ]

    completion = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMP
    )

    return completion.choices[0].message.content
