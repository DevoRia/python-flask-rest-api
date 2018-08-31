from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'rest'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/rest'
mongo = PyMongo(app)


@app.route('/come')
def hello_world():
    star = mongo.db.stars
    output = []
    for s in star.find():
        output.append({'name': s['name']})
    return jsonify(output)


@app.route('/')
def page():
    return render_template('index.html')


@app.route('/come', methods=['POST'])
def put():
    star = mongo.db.stars
    name = request.json['name']
    if name != "":
        star.insert({'name': name})
    return 'success'


@app.route('/come/<string:id>', methods=['DELETE'])
def dele(id):
    star = mongo.db.stars
    star.delete_one({'name': id})
    return 'success'


if __name__ == '__main__':
    app.run()
