#!make
.PHONY: run clean

run:
	docker compose up -d db
	sleep 1
	docker exec -i postgresql psql -U postgres -d postgres < ./schema.sql
	

clean:
	docker compose down
