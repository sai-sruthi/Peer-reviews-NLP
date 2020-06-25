from tensorflow.keras.models import load_model
import pickle
import re
import string

import nltk
import pandas as pd
# !pip install pyspellchecker
from spellchecker import SpellChecker  # The above pyspellchecker refers to this library
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

spell = SpellChecker()
nltk.download('words')
def preprocess_review(reviews):
  comment = []
  for i in range(len(reviews)):
    if reviews[i] == "" or isinstance(reviews[i], str) == False or reviews[i] == " ":
            continue
    reviews[i] = re.sub(r'[!?]','.',reviews[i]) # Removing special character
    reviews[i] = re.sub(r'[^.a-zA-Z0-9\s]',' ',reviews[i]) # Removing special character
    reviews[i] = re.sub('\'',' ',reviews[i]) # Removing quotes
    reviews[i] = re.sub('#','',reviews[i]) # Removing quotes
    reviews[i] = re.sub('\d',' ',reviews[i]) # Replacing digits by space
    reviews[i] = re.sub(r'\s+[a-z][\s$]', ' ',reviews[i]) # Removing single characters and spaces alongside
    reviews[i] = re.sub(r'\s+', ' ',reviews[i]) # Replacing more than one space with a single space
    if 'www.' in reviews[i] or 'http:' in reviews[i] or 'https:' in reviews[i] or '.com' in reviews[i]:
          reviews[i] = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", "<url>", reviews[i])
    reviews[i] = reviews[i].lower()
    reviews[i] = reviews[i].rstrip()
    spot = reviews[i].find(' .')
    while spot != -1: # Fix lone periods in comment
      sl = list(reviews[i])
      sl[spot] = '.'
      sl[spot+1] = ''
      reviews[i] = "".join(sl)
      spot = reviews[i].find(' .')
    for word in reviews[i].split():
      if word == '.':
        continue
      word_base = word.translate(str.maketrans('', '', string.punctuation))  
      if(bool(spell.unknown([word_base]))):
        recommended = spell.correction(word_base)
        if (recommended in words.words()):
          reviews[i] = reviews[i].replace(word,recommended,1)
        else:
          reviews[i] = reviews[i].replace(word, '')
          reviews[i] = re.sub(r'\s+', ' ',reviews[i]) # Replacing more than one space with a single space
    reviews[i] = reviews[i].replace('..', '.')
    if reviews[i].find('.') == 0:
      reviews[i] = reviews[i].replace('.', '', 1)
      reviews[i] = reviews[i].replace(' ', '', 1)
    comment.append(reviews[i])
  return comment[0]
def load_items(filepath_model, filepath_tokenizer):
  model = load_model(filepath_model) # May need to alter filepath
  tokenizer = pickle.load(open(filepath_tokenizer, 'rb')) # May need to alter filepath
  return model, tokenizer
def predict_class(new_data, model, tokenizer,maxlen):
  new_data = preprocess_review([new_data])
  new_df = (pd.DataFrame([new_data]))[0]
  new_df = tokenizer.texts_to_sequences(new_df)
  new_df = pad_sequences(new_df, maxlen=maxlen, padding='post', truncating='post') # Set maxlen to 200 for suggestions
  predicted = int(model.predict_classes(new_df))
  predicted_confidence = float("{:.3f}".format(model.predict_proba(new_df)[0][0]))
  return predicted,predicted_confidence 
