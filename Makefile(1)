

test:
	pytest tests/

format:
	black .
	isort . --recursive --profile black

down-containers:
	docker-compose -f docker-compose.yml down 

up-containers:
	docker-compose -f docker-compose.yml up --build

up-containers-shadow:
	docker-compose -f docker-compose.yml up -d 

set-api:
	export PYTHONPATH="/media/rcastillo/DatosRC/ws/anyone-program/anyone-ws/spring3/assignment/api:$PYTHONPATH"

down-redis:
	docker-compose -f docker-compose-redis.yml down 

up-redis:
	docker-compose -f docker-compose-redis.yml up -d

up-ml:
	docker-compose -f docker-compose-ml.yml up --build
	
down-ml:
	docker-compose -f docker-compose.ml.yml down 