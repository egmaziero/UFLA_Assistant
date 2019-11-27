import os
import json
import elasticsearch
import elasticsearch.helpers
from flask import Flask, request
from subprocess import run
import requests

es = elasticsearch.Elasticsearch()
app = Flask(__name__)


# process_data
@app.route('/uflassist/process_pages', methods=['GET'])
def process_pages():
    res = elasticsearch.helpers.scan(es, index="uflaassist", query={
                                     "query": {"match_all": {}}})

    header = {'Content-Type': 'application/json'}

    processed_pages = 0

    for item in res:
        _id = item["_id"]

        title = item["_source"]["title"]
        text = item["_source"]["text"]

        if title is None or text is None:
            continue

        payload = {"text": title + " " + text}

        annotation = requests.post(
            "http://0.0.0.0:5000/uflassist/nlu", data=json.dumps(payload), params=header)

        if annotation.status_code == 200:
            nlu_interpretation = json.loads(annotation.text)
            processed_pages += 1
        else:
            return "Error calling nlu service. Did you run it?"

        #
        # Pessoal, implementem a extração do WA (what about?)
        # Basicamente, busquem pela menor quantidade de termos que identifiquem
        # sobre o que a página está falando.
        #
        # adicionem um campo ao dicionário nlu_interpretation (nlu_interpretation['WA'])
        # Se conseguirem insiram esse novo dicionário no elasticsearch e adicionem o _id da página

    return "<h1>Foram processadas {} páginas</h1>".format(processed_pages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
