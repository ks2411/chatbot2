# text_processing.py
import openai
import os
from config import MODEL, TEMP, VERBOSE
from utils import remove_newlines





def get_hello(model, user_message, temp=TEMP, verbose=VERBOSE):
    """Определяет, есть ли приветствие в первом сообщении клиента и возвращает его."""

    system_prompt = '''
    ברכת פתיחה היא ביטוי של ברכה או הודעת פתיחה שנשלחת או נאמרת בתחילת שיחה עם מישהו.
    המטרה שלך היא לזהות את ברכת הפתיחה בטקסט של הלקוח.
    בתשובתך כלול רק את ברכת הפתיחה שנמצאה.
    'None' אם אין ברכת פתיחה, כתוב
    '''

    user_prompt = f'Текст клиента: {user_message}'

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    return openai.chat.completions.create(
        model=model, messages=messages, temperature=temp
    )

def summarize_dialog(dialog, history, temp=TEMP, verbose=VERBOSE, model=MODEL):
    """Создаёт краткое содержание диалога для логичного ответа модели."""

    last_statements = ' '.join(history[-2:]) if len(history) > 1 else history[-1]

    system_prompt = '''
    אתה מתקן-על (סופר-קורקטור), שיודע להדגיש בדיאלוגים את כל הדברים החשובים ביותר 
    משימתך: ליצור סיכום מלא ומדויק על בסיס ההיסטוריה של ההודעות הקודמות בדיאלוג ועל בסיס ההודעות האחרונות.
    אתה בשום אופן לא ממציא כלום ורק מסתמך על השיחה.
    '''

    user_prompt = f'''
    סכם את הדיאלוג מבלי להוסיף שום דבר מדמיונך.
    היסטוריית ההודעות הקודמות בדיאלוג: {dialog}.
    ההודעות האחרונות: {last_statements}.
    '''

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    return openai.chat.completions.create(
        model=model, messages=messages, temperature=temp
    )

def extract_entity_from_statement(name, system, instructions, question, history, temp=TEMP, verbose=VERBOSE, model=MODEL):
    """Выделяет сущности (потребности, возражения, тарифы) из сообщений клиента и менеджера."""

    history_content = history[-1] if history else "сообщений нет"

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"{instructions}\n\nВопрос клиента: {question}\n\nПредыдущий ответ менеджера: {history_content}\n\nОтвет: "}
    ]

    return openai.chat.completions.create(
        model=model, messages=messages, temperature=temp
    )

def remove_greeting(text):
    """Удаляет приветствие в начале сообщения."""

    system_prompt = '''
    אתה עורך טקסטים מצוין וטוב יותר מכולם במציאת ברכת פתיחה בטקסט.
    אם יש ברכת פתיחה, удали אותה והחזר רק את הטקסט שנותר.
    '''

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f'Исходный текст: {text}\n\nОтвет: '}
    ]

    response = openai.chat.completions.create(
        model=MODEL, messages=messages, temperature=TEMP
    )

    return response.choices[0].message.content
