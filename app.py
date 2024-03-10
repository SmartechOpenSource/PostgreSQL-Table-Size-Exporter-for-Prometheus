import requests, datetime, psycopg2
from prometheus_client import make_wsgi_app
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import prometheus_client as prom
from prometheus_client.registry import Collector
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from os import environ


# Replace these values with your actual PostgreSQL database credentials
host = environ.get("POSTGRES_HOST", "localhost")
port = environ.get("POSTGRES_PORT", "5432")  # Replace with your actual port number
dbname = environ.get("POSTGRES_DB", "example")
user = environ.get("POSTGRES_USER", "postgres")
password = environ.get("POSTGRES_PASS", "password123")


class CustomCollector(Collector):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
            print("Connected to database successfully")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def get_metrics(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT schema_name, relname, pg_size_pretty(table_size) AS size, table_size
            FROM (
            SELECT pg_catalog.pg_namespace.nspname AS schema_name, relname, pg_relation_size(pg_catalog.pg_class.oid) AS table_size
            FROM pg_catalog.pg_class
            JOIN pg_catalog.pg_namespace ON relnamespace = pg_catalog.pg_namespace.oid
            ) t
            WHERE schema_name NOT LIKE 'pg_%'
            ORDER BY table_size DESC;
        """)
        rows = cursor.fetchall()
        table_list = list()
        for row in rows:
            if row[0] == "public":
                table_list.append((row[1], row[3]))
        cursor.close()
        return table_list

    def collect(self):       
        
        table_list = self.get_metrics()
        
        table_size_metrics = GaugeMetricFamily('postgres_table_size', 'size(Byte) of each table in postgres labeled based on table_name, host and port', labels=['table_name', 'host', 'port'])

        for i in table_list:
            table_size_metrics.add_metric([i[0], host, port], i[1])  # add_metric([labels,], metric_value)     
        
        yield table_size_metrics


if __name__ == "__main__":
    app = Flask(__name__)
    REGISTRY.unregister(prom.PROCESS_COLLECTOR)
    REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
    REGISTRY.unregister(prom.GC_COLLECTOR)
    REGISTRY.register(CustomCollector())
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
    })
    app.run("0.0.0.0", 5000, threaded=True)
