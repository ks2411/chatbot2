# Dockerfile
# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Задаём переменную окружения с API-ключом (замени на свой ключ!)
ENV OPENAI_API_KEY= (=sk....)

# Указываем команду для запуска бота
CMD ["python", "main.py"]
