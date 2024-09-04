FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY model_saves /app/model_saves
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN mkdir -p /app/static
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "ai_text_detector.wsgi:application", "--bind", "0.0.0.0:8000"]