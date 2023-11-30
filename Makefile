build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

test:
	docker compose exec -it api pytest -v -s