FROM python:3.10-slim

WORKDIR /var/task

RUN apt-get update && apt-get install -y wget unzip

WORKDIR /var/task/

RUN python -m pip install --upgrade pip

COPY .env ./
COPY src ./
COPY wheels/ ./
COPY requirements.txt ./

RUN pip install pip-tools
RUN pip-sync requirements.txt

RUN touch proccess.log

CMD ["/bin/bash", "-c", "tail -f /var/task/proccess.log"]
