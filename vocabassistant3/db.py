import psycopg2 as pg

def connect():
    return pg.connect(host="localhost", database="testdb", user="dba", password="abc123")

