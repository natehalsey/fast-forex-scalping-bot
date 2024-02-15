clean:
	rm -rf *.venv

start:
	sudo docker-compose up --build -d

stop:
	sudo docker-compose down

re:
	make docker.stop && make docker.start

logs:
	sudo docker-compose logs -f

ps:
	sudo docker ps

exec:
	sudo docker exec /bin/bash $$1

requirements:
	pip-compile requirements.in

tws.wheel.build:
	./script/build-tws-api-wheel

tws.wheel.re:
	rm -rf ./wheels/ibapi*.whl
	./script/build-tws-api-wheel

install:
	. ./script/bootstrap
