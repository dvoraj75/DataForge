FROM python:3.12
LABEL authors="Jan Dvorak"

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "gunicorn \"data_forge.main:create_app()\" -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers $APP_WORKERS"]