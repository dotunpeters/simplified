FROM ubuntu

RUN apt-get update -y && \
    apt-get install -y python-pip3 python3-dev

RUN apt-get pip3 install --upgrade setuptools

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "application.py" ]