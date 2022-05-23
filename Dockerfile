FROM sanicframework/sanic:LTS

RUN sudo apt-get update -y
RUN sudo apt-get install git


RUN mkdir -p /srv/app
COPY . /srv/app


WORKDIR /srv/app

RUN pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3", "main.py"]