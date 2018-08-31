from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from models.names import Person

__author__ = "Riabchenko Vadim"

connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)

sync_table(Person)