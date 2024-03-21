# Cloud-project
This repo contains my final projects for the Cloud computing (Basic) course 2024.
To start the containers, run: 
```
docker-compose up
docker exec --user www-data cc_nextcloud php occ config:system:set trusted_domains 1 --value=cc_nextcloud 
```
The last command allows Locust to connect to the Nextcloud web app.
It is recommended to wait a little bit before executing the second command since Nextcloud installation takes time.

In order for load testing to be performed, Locust expects the following files inside the working directory: kb, mb, and gb.