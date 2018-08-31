import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

__author__ = "Riabchenko Vadim"


class Base(Model):
    __abstract__ = True
    __keyspace__ = "cassandra_final_try"


class Person(Base):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()

    def get_data(self):
        return {'id': str(self.id), 'name': self.name}

    def get_id(self):
        return str(self.id)

    def get_name(self):
        return self.name
