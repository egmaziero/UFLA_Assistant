import os
import elasticsearch
import elasticsearch.helpers
from flask import Flask, request
from subprocess import run

es = elasticsearch.Elasticsearch()
app = Flask(__name__)


@app.route('/uflassist/crawled_pages', methods=['GET'])
def crawled_pages():
    res = elasticsearch.helpers.scan(es, index="uflaassist", query={
                                     "query": {"match_all": {}}})
    response = ""
    i = 0
    for item in res:
        response += "{}  ".format(i)
        response += "%(title)s <b>%(date_publish)s </b> %(url)s<br>" % item["_source"]
        i += 1

    return response


@app.route('/uflassist/crawled_pages_number', methods=['GET'])
def crawled_pages_number():
    res = es.search(index="uflaassist", body={"query": {"match_all": {}}})

    return "Já foram <i>crawleadas</i> %d páginas:" % res['hits']['total']['value']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
