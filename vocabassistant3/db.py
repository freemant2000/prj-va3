import psycopg2 as pg

def connect():
    return pg.connect(host="localhost", database="va3", user="dba", password="abc123")

