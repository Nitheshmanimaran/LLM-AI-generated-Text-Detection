   FROM python:3.12-slim

   ENV PYTHONDONTWRITEBYTECODE=1
   ENV PYTHONUNBUFFERED=1

   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code and model saves
   COPY . .
   EXPOSE 8000
   COPY model_saves /app/model_saves

   # Collect static files
   RUN python manage.py collectstatic --noinput

   # Run the application
   CMD gunicorn ai_text_detector.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120