#!make
.PHONY: up clean

up:
	docker compose up -d db profiles-service
	sleep 1
	docker exec -i postgresql psql -U postgres -d postgres < ./schema.sql
	

clean:
	docker compose down
