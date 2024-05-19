FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir fastapi pydantic uvicorn requests \
    && pip install --no-cache-dir python-dotenv

ADD . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
