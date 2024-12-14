migrations:
	docker-compose run --rm web alembic revision --autogenerate

migrate:
	docker-compose run --rm web alembic upgrade head
