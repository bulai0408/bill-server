FROM sanicframework/sanic:LTS

RUN mkdir -p /srv/app

RUN apk update
RUN apk add git

RUN cd /srv/app && git clone https://github.com/bulai0408/bill-server.git


WORKDIR /srv/app/bill-server

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3", "main.py"]