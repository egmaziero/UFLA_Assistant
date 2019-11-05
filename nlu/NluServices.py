import os
import spacy
import pandas as pd
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from contractions import CONTRACTION_MAP
import unicodedata
import json


nlp = spacy.load('pt', parse=True, tag=True, entity=True)
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')

#pre processing function : remove the accented chars of the text
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

#pre processing function : expand the contractions of the text using a the file contractions
def expand_contractions(text,contraction_mapping = CONTRACTION_MAP):

  contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),flags=re.IGNORECASE|re.DOTALL)

  def expand_match(contraction):
    match = contraction.group(0)
    first_char = match[0]
    expanded_contraction = contraction_mapping.get(match)\
                if contraction_mapping.get(match)\
                else contraction_mapping.get(match.lower())
    expanded_contraction = first_char+expanded_contraction[1:]
    return expanded_contraction

  expanded_text = contractions_pattern.sub(expand_match, text)
  expanded_text = re.sub("'","",expanded_text)
  return expanded_text

#pre processing function : remove the accented chars of the text
def simple_stemmer(text):
  ps = nltk.porter.PorterStemmer()
  text = ' '.join([ps.stem(word) for word in text.split()])
  return text

#pre processing function : remove the special chars of the text
def remove_special_characters(text,remove_digits=False):
  pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
  text = re.sub(pattern,'',text)
  return text

#pre processing function : lemmatizes the text
def lemmatize_text(text):
  text = nlp(text)
  text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
  return text

#pre processing function : remove the stopwords of the text
def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text

##pre processing function : normalize the text with chosen arguments
def normalize_corpus(corpus,contraction_expansion = True,accented_char_removal=True,text_lower_case = True,text_lemmatization=True,special_char_removal=True,stopwords_removal=True,remove_digits=True):

  normalized_corpus = corpus
  #normalize each document in the corpus

  #remove accented chars
  if accented_char_removal:
    normalized_corpus = remove_accented_chars(normalized_corpus)

  #expand contractions
  if contraction_expansion:
    normalized_corpus = expand_contractions(normalized_corpus)

  #lowercase text
  if text_lower_case:
    normalized_corpus = normalized_corpus.lower()

  #remove extra newlines
  normalized_corpus = re.sub(r'[\r|\n|\r|\n]+',' ',normalized_corpus)

  #lemmatize text
  if text_lemmatization:
    normalized_corpus = lemmatize_text(normalized_corpus)

  #remove special characters and/or digits
  if special_char_removal:
    #insert spaces between special chars to isolate them
    special_char_pattern = re.compile(r'([{.(-)!}])')
    normalized_corpus = special_char_pattern.sub("\\1",normalized_corpus)
    normalized_corpus = remove_special_characters(normalized_corpus,remove_digits=remove_digits)

  #remove extra whitespace
  normalized_corpus = re.sub(' +',' ',normalized_corpus)

  #remove stopwords
  if stopwords_removal:
    normalized_corpus = remove_stopwords(normalized_corpus,is_lower_case=text_lower_case)

  

  return normalized_corpus

#input
text = "este Texto aqui é um exemplo para ser@#  utilizado, durante o projeto ! nao é suposto que ele faça algum sentido"

# pre-process text and store the same
corpus = normalize_corpus(text , text_lower_case=False, 
                          text_lemmatization=False, special_char_removal=True)

#spacy nlp processing
sentence_nlp = nlp(corpus)

# POS tagging with Spacy 
spacy_pos_tagged = [(word.pos_) for word in sentence_nlp]
#create a dataset with needed
#spacyPosDF = pd.DataFrame(spacy_pos_tagged, columns=['Tag type'])

#synthatic parsinh with spacy
spacy_synthatic_parsed = [(word.dep_) for word in sentence_nlp]
#create a dataset with needed
#spacySynthaticDF = pd.DataFrame(spacy_synthatic_parsed, columns=['Tag'])

#create dict to be converted for json 
saida = {}
saida['Tokens'] = []
saida['Tokens'].append(tokenizer.tokenize(corpus))
saida['POS Tagging'] = []
saida['Synthatic'] = []
saida['POS Tagging'].append(spacy_pos_tagged)
saida['Synthatic'].append(spacy_synthatic_parsed)


#creating/writing json
with open('nlu.json','w',encoding='utf-8') as outfile:
  json.dump(saida , outfile,ensure_ascii=False,indent = 4)


# POS tagging with nltk , by now im just using spacy 
#nltk_pos_tagged = nltk.pos_tag(text.split())
#nltkDF = pd.DataFrame(nltk_pos_tagged, columns=['Word', 'POS tag'])

#printing the normalized text and the tags datasets
#print(text)
#print('Spacy POS: ')
#print(spacyPosDF.to_string())
#print('Spacy synthatic: ')
#print(spacySynthaticDF.to_string())