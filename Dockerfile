FROM python:3.10.8-buster

WORKDIR /usr/src/app

COPY assets ./assets
COPY app1.py ./app1.py
COPY utils.py ./utils.py
COPY requirements.txt ./requirements.txt

# RUN pip3 install --no-cache-dir -r ./requirements.txt
RUN pip3 install --no-cache-dir Flask

CMD ["python", "app1.py"]