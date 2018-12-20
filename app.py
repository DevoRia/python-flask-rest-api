from bson import ObjectId
from cassandra.cqlengine import connection
from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
from flask_pymongo import PyMongo
from cassandra.cluster import Cluster

from models.names import Person

__author__ = "Riabchenko Vadim"

KEYSPACE = "cassandra_final_try"


def create_app():
    app = Flask(__name__)

    app.debug = True

    cluster = Cluster()
    session = cluster.connect()
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS cassandra_final_try WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
        """)
    session = cluster.connect(keyspace=KEYSPACE)

    app.config['MONGO_DBNAME'] = 'rest'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/rest'

    return app


app = create_app()
CORS(app)

connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)

mongo = PyMongo(app)


@app.route('/come')
def find_all_mongo():
    star = mongo.db.stars
    output = []
    for s in star.find():
        output.append({'name': s['name']})
    return jsonify(output)


@app.route('/')
def page():
    return render_template('index.html')


@app.route('/come', methods=['POST'])
def save_mongo():
    star = mongo.db.stars
    name = request.json['name']
    if name != "":
        star.insert({'name': name})
    return 'success'


@app.route('/come/<string:id>', methods=['DELETE'])
def delete_mongo(id):
    star = mongo.db.stars
    star.delete_one({'name': id})
    return 'success'


@app.route('/cass')
def find_all_cassandra():
    persons = Person.objects().all()
    incomes = []
    for person in persons:
        incomes.append({'id': person.get_id(), 'name': person.get_name()})
    return jsonify(incomes)


@app.route('/cass', methods=['POST'])
def save_cassandra():
    name = request.json['name']
    if name != "":
        Person.create(name=name)
    return 'success'


@app.route('/cass/<string:id>', methods=['DELETE'])
def delete_cassandra(id):
    connection.execute("""DELETE FROM cassandra_final_try.person WHERE id = %s;""" % id)
    return 'success'


if __name__ == '__main__':
    app.run()
