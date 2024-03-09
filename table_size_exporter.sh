#!/bin/bash

DB_NAME="<db_name>"
DB_USER="<db_user>"
OUT_FILE="<output_directory/metrics_file>"
DB_HOST='localhost'

QUERY="SELECT schema_name, relname, pg_size_pretty(table_size) AS size, table_size
FROM (
  SELECT pg_catalog.pg_namespace.nspname AS schema_name, relname, pg_relation_size(pg_catalog.pg_class.oid) AS table_size
  FROM pg_catalog.pg_class
  JOIN pg_catalog.pg_namespace ON relnamespace = pg_catalog.pg_namespace.oid
) t
WHERE schema_name NOT LIKE 'pg_%'
ORDER BY table_size DESC;"

output=$(psql -q --no-align -d "$DB_NAME" -U "$DB_USER" -h "$DB_HOST" -t -c "$QUERY" | awk -F'|' '{print $2 , $4}')

echo "# HELP database_table_size Size of tables in the database" > "$OUT_FILE"
echo "# TYPE database_table_size gauge" >> "$OUT_FILE"
while read -r line; do
    table_name=$(echo "$line" | awk '{print $1}')
    table_size=$(echo "$line" | awk '{print $2}')
    echo "database_table_size{table=\"$table_name\"} $table_size" >> "$OUT_FILE"
done <<< "$output"