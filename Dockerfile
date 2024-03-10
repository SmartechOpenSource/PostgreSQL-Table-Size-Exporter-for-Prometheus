FROM python:latest

ADD requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD app.py /var/server/app.py

EXPOSE 5000

CMD python /var/server/app.py
