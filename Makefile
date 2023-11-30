build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

test:
	docker compose exec -it api pytest -v -s

lint:
	docker run --rm --volume ./:/src --workdir /src pyfound/black:latest_release black --check .

format:
	docker run --rm --volume ./:/src --workdir /src pyfound/black:latest_release black .