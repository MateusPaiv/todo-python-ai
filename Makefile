create-db-migration:
	@echo "Migration title: "; \
	read title; \
	poetry run alembic -c alembic.ini revision -m "$$title"

db-downgrade:
	@echo "Select version of migration (-1 to HEAD-1): "; \
	read title; \
	poetry run alembic -c alembic.ini downgrade $$title

db-migrate:
	@echo "\n➤ Starting database migration..."
	poetry run alembic -c alembic.ini upgrade head

update-dep-file:
	@echo "\n\x1b[1;32m➤ Updating file\x1b[0m requirements.txt\n"
	poetry run poetry export -f requirements.txt --without-hashes > requirements.txt

run-dev:
	poetry run uvicorn app.main:app --reload
