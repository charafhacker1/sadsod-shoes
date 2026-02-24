FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "wsgi:app"]
