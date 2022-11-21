FROM python:3.5

RUN apt update && apt install -y python-dev libc-dev gettext sqlite3 libsqlite3-dev libpq-dev binutils libproj-dev gdal-bin

WORKDIR /usr/src/app
COPY ./requirements.txt ./
COPY ./requirements_dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi whitenoise
COPY uwsgi.ini /etc/uwsgi.ini
RUN apt update && apt -y --no-install-recommends install fish