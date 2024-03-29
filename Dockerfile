FROM python:3.9

COPY requirements.txt ./requirements.txt

RUN apt-get update \ 
    && apt-get install build-essential make gcc -y \
    && apt-get install dpkg-dev -y \ 
    && apt-get install libjpeg-dev -y \ 
    && pip install -r requirements.txt
#    && pip install --no-cache-dir . \

RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get auto-remove -y \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local/lib/python3.9 -name "*.pyc" -type f -delete

COPY . ./
WORKDIR "./app"
CMD gunicorn -b 0.0.0.0:80 app:server
