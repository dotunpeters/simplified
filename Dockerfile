FROM python
RUN apt-get update
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
COPY . /opt/app
WORKDIR /opt/app
ENTRYPOINT FLASK_APP=/opt/app/application.py flask run
ENV DATABASE_URL postgres://cmehgjnylkevlo:2a0a1d2d4f46fd73748c8b47d57b452532a4b928ef1f7912287f71c31ae3b6ae@ec2-34-195-169-25.compute-1.amazonaws.com:5432/dcrnemrsq9rteu
ENV SECRET_KEY 5685fab554f78bee40b8d0e681a1a981