build:
	docker compose build

up:
	docker compose up -d api

down:
	docker compose down

test:
	docker compose up -d api_test && \
	docker compose exec -it api_test pytest -v -s && \
	docker compose down

lint:
	docker run --rm --volume ./:/src --workdir /src pyfound/black:latest_release black --check .

format:
	docker run --rm --volume ./:/src --workdir /src pyfound/black:latest_release black .