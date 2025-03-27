#!make
.PHONY: up clean

up:
	docker compose up -d db #profile-service
	sleep 1
	docker exec -i postgresql psql -U postgres -d postgres < ./schema.sql
	

clean:
	docker compose down
