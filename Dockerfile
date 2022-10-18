FROM python:3.10.8-buster

WORKDIR /usr/src/app

COPY assets ./assets
COPY app.py ./app.py
COPY utils.py ./utils.py
COPY requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r ./requirements.txt

CMD ["python", "app.py"]