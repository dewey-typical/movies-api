FROM python:3.10.12-alpine

WORKDIR /
ENV DATABASE_URL="postgresql://admin:adminadmin@localhost/tp"
COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app.py /app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]