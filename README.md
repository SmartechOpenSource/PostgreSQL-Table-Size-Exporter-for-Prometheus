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
