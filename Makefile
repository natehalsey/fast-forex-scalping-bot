# Docker stuff
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

docker.shell:
	sudo docker run -it --name 

requirements:
	pip-compile requirements.in

clean:
	rm -rf ./*.venv

# TWS wheel building
tws.build:
	./script/build-tws-api-wheel

tws.re:
	rm -rf ./wheels/ibapi*.whl
	./script/build-tws-api-wheel

# Linting
lint.check:
	pylint ./src || true
	black ./src --check --diff

lint.fix:
	black ./src

test:
	pytest src/

