from flask import Flask
from flask import request
from flask import jsonify


from neo4j.v1 import GraphDatabase
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/graph/query', methods=['POST'])
def run_query():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "blacky"))
    query = request.get_json()['query']
    print(query)

    with driver.session() as session:
        with session.begin_transaction() as tx:
            result = tx.run(query)

    if not result:
        return jsonify(result=None)

    keys = result.keys()
    values = []
    for record in result.records():
        values.append(record.values())
    return jsonify(result={'keys': keys, 'values': values})


if __name__ == '__main__':
    app.run()
