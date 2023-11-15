FROM python:3.10.10

COPY . .
WORKDIR /jgw_attendance

WORKDIR ..
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN rm -rf ./logs
RUN mkdir ./logs

EXPOSE 50005

ENTRYPOINT gunicorn --bind=0.0.0.0:50005 jgw_attendance.wsgi:application