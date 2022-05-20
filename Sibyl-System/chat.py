import nltk
#nltk.download()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

import pickle
import numpy as np
import urllib

from keras.models import load_model
model = load_model('Chatbot\chatbot_model_test3.h5')
import json
import random
with urllib.request.urlopen("https://raw.githubusercontent.com/Jeli04/ChatBot/main/sibyl_test_data.json") as url:
    training = json.loads(url.read().decode())
words = pickle.load(open('Chatbot\words.pkl','rb'))
classes = pickle.load(open('Chatbot\classes.pkl','rb'))




# Cleans up the users response 
def clean_up_sentences(sentence):
  #print(sentence)
  sentence_words = nltk.word_tokenize(sentence)
  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
  return sentence_words




# Bag Of Words (bow)
def bow(sentence, words, show_details = True):
  # Tokenize the patterns 
  sentence_words = clean_up_sentences(sentence)
  # Bag of words
  bag = [0]*len(words)
  for s in sentence_words: 
    for i,w in enumerate(words):
      if w == s:
        # Assigns 1 if the current word is in the vocab position 
        bag[i] = 1
        #if show_details:
          #print("found in bag: %s" % w)
  return np.array(bag)




def predict_class(sentence, model):
  p = bow(sentence, words, show_details=False)
  result = model.predict(np.array([p]))[0]  # Uses the ML model to predict the intent classification results 
  ERROR_THRESHOLD = 0.00  # Threshold to prevent overfitting 
  #print("Model Prediction:", result)

  
  results = [[i,r] for i,r in enumerate(result) if r>ERROR_THRESHOLD]
  
  #print("test: ", results[0][1])

  results.sort(key=lambda x: x[1], reverse=True)
  return_list = []
  for r in results:
    return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

  return return_list





def getResponse(ints, intents_json):
    print(ints[0])
    intent = ints[0]["intent"]
    list_of_intents = intents_json['data']
    for i in list_of_intents:
        if(i['intent']== intent):
          result = random.choice(i['answerText'])
          break
    return result




def chatbot_response(msg):
  #print(msg)
  ints = predict_class(msg, model)
  if float(ints[0]["probability"]) < 0.75:
    return "Sorry I didn't quite get that"
  else:
    res = getResponse(ints, training)
    return res

print(chatbot_response("I am depressed"))