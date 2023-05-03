FROM python:3.10
WORKDIR /app
RUN apt update && apt install -y make build-essential
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --no-deps
COPY . .
CMD make migrate && python main.py runserver

