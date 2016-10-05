import os

from flask import Flask, request, jsonify
import sesamclient
from elasticsearch import Elasticsearch

app = Flask(__name__)

sesam_url = os.getenv('SESAM_URL', 'http://localhost:9042/api/')
elastic_search_host = os.getenv('ELASTICSEARCH_HOSTS', 'localhost:9200')

sesam = sesamclient.Connection(sesamapi_base_url=sesam_url)
elasticsearch = Elasticsearch([elastic_search_host])


@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = sesam.get_dataset("tasks").get_entity(task_id)
    task["_deleted"] = True
    sesam.get_pipe("tasks").post_entities([task])
    return jsonify(task)


@app.route('/task/<task_id>', methods=['PUT'])
def put_task(task_id):
    task = request.json
    task["_id"] = task_id
    sesam.get_pipe("tasks").post_entities([task])
    return jsonify(task)


@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id):
    return jsonify(sesam.get_dataset("tasks").get_entity(task_id))


@app.route('/tasklist/<assignee>', methods=['GET'])
def get_tasklist(assignee):
    return jsonify(sesam.get_dataset("tasklists-view").get_entity(assignee))


@app.route('/task', methods=['GET'])
def get_tasks():
    return jsonify(list(sesam.get_dataset("tasks-view").get_entities(history=False, deleted=False)))


@app.route('/search/<query>', methods=['GET'])
def search(query):
    return jsonify(elasticsearch.search(body={
        "query": {
            "simple_query_string": {
                "query": query,
            }
        }
    }))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
