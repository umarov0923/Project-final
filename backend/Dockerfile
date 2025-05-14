# Используем официальный образ Python
FROM python:3.10-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска будет задаваться в docker-compose

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]


