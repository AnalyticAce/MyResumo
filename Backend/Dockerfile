FROM python:3.11

WORKDIR /code

RUN apt-get update && apt-get install -y python3-distutils

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]