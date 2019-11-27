import spacy
import json
import nltk
import nlpnet
from nltk.tokenize import sent_tokenize
from flask import Flask, request

app = Flask(__name__)

# loading models
nlp = spacy.load('pt_core_news_sm')
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
# srl_tagger = nlpnet.SRLTagger('srl-pt', language='pt')


@app.route('/uflassist/nlu', methods=['POST'])
def nlu():
    data = request.get_json(force=True)
    text = data.get('text')
    annotation = {"sentences": []}
    sentences = sent_tokenizer.tokenize(text)
    for sentence in sentences:
        ann = {"sentence": sentence, "tokens": [],
               "POS": [], "DEP": [], "NER": [], "SRL": []}
        doc = nlp(sentence)
        for token in doc:
            ann["tokens"].append(str(token.text))
            ann["POS"].append(str(token.pos_))
            ann["DEP"].append((str(token.dep_), str(token.head)))
            ann["NER"].append(str(token.ent_type_))

        # sent = srl_tagger.tag(u''+sentence)[0]
        # srl = []

        # for s in sent.arg_structures:

        #     for key, value in s[1].items():
        #         temp = {key: value}
        #         srl.append(temp)

        # ann["SRL"].append(srl)
        annotation["sentences"].append(ann)

    return json.dumps(annotation)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
