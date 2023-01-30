PORT ?= 5000

run-local:	## run project
	uvicorn --host 0.0.0.0 --port $(PORT) main:app --lifespan=on --reload

run:
	docker-compose up -d

down:
	docker-compose down
