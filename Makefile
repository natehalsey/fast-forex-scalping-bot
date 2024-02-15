clean:
	rm -rf *.venv

docker.start:
	sudo docker-compose up --build -d

docker.stop:
	sudo docker-compose down

docker.re:
	make docker.stop && make docker.start

docker.logs:
	sudo docker-compose logs -f

docker.ps:
	sudo docker ps

docker.exec:
	sudo docker exec /bin/bash $$1

requirements:
	pip-compile requirements.in

install:
	. ./script/bootstrap
