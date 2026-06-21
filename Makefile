.PHONY: run up down logs

run up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f
