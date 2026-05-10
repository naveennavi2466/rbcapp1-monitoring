from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")
INDEX = "rbcapp1-status"
SERVICES = ["httpd", "rabbitmq", "postgresql"]


@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "no data"}), 400
    es.index(index=INDEX, body=data)
    return jsonify({"message": "saved"})


@app.route("/healthcheck", methods=["GET"])
def healthcheck_all():
    res = es.search(index=INDEX, body={"query": {"match_all": {}}})
    seen = {}
    for hit in res["hits"]["hits"]:
        src = hit["_source"]
        svc = src["service_name"]
        if svc not in seen:
            seen[svc] = src["service_status"]

    overall = "UP"
    for svc in SERVICES:
        if seen.get(svc) == "DOWN":
            overall = "DOWN"

    return jsonify({"application_name": "rbcapp1", "application_status": overall, "services": seen})


@app.route("/healthcheck/<svc_name>", methods=["GET"])
def healthcheck_one(svc_name):
    res = es.search(index=INDEX, body={"query": {"match": {"service_name": svc_name}}})
    if res["hits"]["total"]["value"] == 0:
        return jsonify({"error": "not found"}), 404
    item = res["hits"]["hits"][0]["_source"]
    return jsonify({"service_name": svc_name, "service_status": item["service_status"]})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
