FROM python:3.6-alpine
ENV LIBRARY_PATH=/lib:/usr/lib
RUN apk --no-cache add gcc postgresql-dev musl-dev zlib-dev jpeg-dev libffi-dev git
RUN mkdir /app
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
RUN python ./manage.py collectstatic --noinput
EXPOSE 8000
