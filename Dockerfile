FROM python:3.10-slim

WORKDIR /var/task

RUN apt-get update && apt-get install -y wget unzip

WORKDIR /var/task/

RUN python -m pip install --upgrade pip

# Lord this is bad
RUN wget -N https://interactivebrokers.github.io/downloads/twsapi_macunix.1019.02.zip
RUN unzip -f twsapi_macunix.1019.02.zip -d ./twsapi
RUN pip wheel -w /var/task /var/task/twsapi/IBJts/source/pythonclient

COPY .env ./
COPY src ./
COPY requirements.txt ./

RUN pip install pip-tools
RUN pip-sync requirements.txt

RUN touch proccess.log

CMD ["/bin/bash", "-c", "tail -f /var/task/proccess.log"]
