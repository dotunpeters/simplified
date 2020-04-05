FROM python
RUN apt-get update
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
COPY . /opt/app
WORKDIR /opt/app
ENTRYPOINT FLASK_APP=/opt/app/application.py flask run