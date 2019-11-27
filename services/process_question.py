import os
import json
from flask import Flask, request
from subprocess import run
import requests

app = Flask(__name__)


# process_data
@app.route('/uflassist/process_question', methods=['GET'])
def process_pages():
    question = request.args.get('question')
    header = {'Content-Type': 'application/json'}
    payload = {"text": question}

    annotation = requests.post(
        "http://0.0.0.0:5000/uflassist/nlu", data=json.dumps(payload), params=header)

    if annotation.status_code == 200:
        nlu_interpretation = json.loads(annotation.text)
    else:
        return "Error calling nlu service. Did you run it?"

        #
        # Pessoal, implementem a extração do WA (what about?)
        # Basicamente, busquem pela menor quantidade de termos que identifiquem
        # sobre o que o usuário está buscando
        #
        # adicionem um campo ao dicionário nlu_interpretation (nlu_interpretation['WA'])

    return json.dumps(nlu_interpretation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
