FROM python:3.10-slim

WORKDIR /var/task

RUN apt-get update && apt-get install -y procps

WORKDIR /var/task/

RUN python -m pip install --upgrade pip

COPY .env ./
COPY src ./
COPY wheels/ ./wheels
COPY requirements.txt ./
COPY setup.py ./

RUN pip install pip-tools
RUN pip-sync requirements.txt

RUN python setup.py install

ENTRYPOINT [ "python", "app.py" ]
