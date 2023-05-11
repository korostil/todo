FROM python:3.10 as base_image
WORKDIR /app
RUN apt update && apt install -y make build-essential
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir --no-deps

FROM base_image as local_image
WORKDIR /app
COPY ./requirements.dev.txt /app/requirements.dev.txt
RUN python -m pip install -r /app/requirements.dev.txt --no-cache-dir
COPY . .
CMD make migrate && python main.py runserver

FROM base_image as production_image
COPY . .
CMD make migrate && python main.py runserver

