FROM python:3.9.6-slim

RUN python -m pip install colorama --upgrade pip

WORKDIR /app

COPY . .

CMD ["python", "matica.py"]
