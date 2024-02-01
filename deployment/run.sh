#!/bin/bash

printf  "Launching the service.\n\n"
docker compose up -d
printf  "\n\nService started."

printf  "\n\nWaiting for DB to be ready."
sleep 5

printf  "\n\nStarting DB restoration using is_74.sql...\n\n"
docker compose cp ./is_74.sql postgres:var/lib/postgresql/
docker compose exec postgres dropdb is74
docker compose exec postgres createdb is74
docker compose exec postgres pg_restore -d is74 var/lib/postgresql/is_74.sql
printf  "\n\nDB restoration finished."
sleep 3