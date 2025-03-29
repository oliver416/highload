## Get started

```bash
docker compose up -d elasticsearch kibana

docker compose exec -it elasticsearch bash
bin/elasticsearch-create-enrollment-token --scope kibana
```

Copy the key and paste to the Kibana UI. Copy the code from Kibana logs and also 
paste to the Kibana UI.

```bash
bin/elasticsearch-users useradd admin
bin/elasticsearch-users roles -a superuser admin
```
