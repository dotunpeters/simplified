FROM python

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5001

ENV DATABASE_URL="postgres://cmehgjnylkevlo:2a0a1d2d4f46fd73748c8b47d57b452532a4b928ef1f7912287f71c31ae3b6ae@ec2-34-195-169-25.compute-1.amazonaws.com:5432/dcrnemrsq9rteu"
ENV SECRET_KEY="5685fab554f78bee40b8d0e681a1a981"

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]