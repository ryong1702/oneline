FROM --platform=linux/x86_64 python:3.9.10-slim-buster

ENV TZ Asia/Tokyo

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]