🐬 check the size of tables in a PostgreSQL database 🐬

This script is designed to export PostgreSQL table sizes in a format compatible with Prometheus. It provides a convenient way to monitor the size of individual tables in a PostgreSQL database, making it suitable for integration with Prometheus and visualization in Grafana.

## Features
- Retrieves size information for specified tables in a PostgreSQL database.
- Output table sizes in a human-readable format.
- Allows for easy integration into monitoring systems or scripts.

## Installation
- Just make sure the script has executable permission.

## Usage
1- Configure the script by setting the following variables at the beginning of the script:
```
DB_NAME="<your_database_name>"
DB_USER="<your_database_user>"
OUT_FILE="<path_to_output_directory/metrics_file>"
DB_HOST='localhost'
```
2- Run the script:
```
./table_size_exporter.sh
```
3- Configure Prometheus to scrape the generated metrics with a text file collector.
This config must be set to the Node_exporter setting:
```
--collector.textfile.directory=<path_to_output_directory/metrics_file>
```

## To run this exporter as a container with RESTful API

Note: Everytime localhost:5000/metrics is get called, CustomCollector from REGISTRY.register(CustomCollector()) is get called to update metrics and it depends on scrape interval of Prometheus
### Requirements

To install and run these examples you need:

- Python 3.3+
- python3-venv or python3-virtualenv
- git (only to clone this repository)
- docker

### Configuration

For connecting to the database you just need to change the .env file

## Installation for development purposes

The commands below set everything up to run the exporter app:

`apt install python3 python3-venv`

`git clone <git_repo>`

`cd <git_repo>`

`python3 -m venv venv`

`. venv/bin/activate`

`(venv) pip install -r requirements.txt`

`python app.py`


## Installation with docker

To install exporter app:

`cd <git_repo>`

`docker build -t postgres_exporter:1 .`

`docker run --restart always -itd --env-file .env --name postgres_exporter -p 5000:5000 postgres_exporter:1`

## Installation with docker-compose
`docker compose up -d`