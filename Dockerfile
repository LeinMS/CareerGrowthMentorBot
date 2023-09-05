FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*
# Устанавливаем зависимости
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY tg_sensei .

# Экспонируем порт, который будет слушать ваше Django-приложение (например, 8000)
EXPOSE 8000

# Запускаем Gunicorn
CMD ["gunicorn", "--bind", ":8000", "tg_sensei.wsgi:application"]

