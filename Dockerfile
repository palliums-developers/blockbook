FROM python:3.8

RUN apt-get update
RUN apt-get upgrade -y

WORKDIR .
RUN mkdir app
COPY . /app/
RUN pip3.8 install -r /app/requirements.txt

CMD ["python3.8", "/app/app.py"]