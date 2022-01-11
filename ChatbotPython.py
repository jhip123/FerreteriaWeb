import pandas as pd
import nltk
import numpy as np
import string
import warnings
import requests
import pickle
import random

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = [["Hi",0],["Hello",0],["Hey",0],["Heya",0],
        ["Can you suggest some flowers.",1],["Is flowers available?",1],["Is bouquet available?",1],["Are flowers fresh?",1],
        ["Suggest for birthday",2],["For Birthday",2],["I want some flowers for Birthday",2],["What type of flowers to give on Birthday?",2],["Suggest something for Birthday",2],["I want to give it to someone for Birthday",2],        
        ["Suggest for anniversary",3],["For Anniversary",3],["I want some flowers for Anniversary",3],["What type of flowers to give on Anniversary?",3],["Suggest something for Anniversary",3],["I want to give it to someone for Anniversary",3],
        ["Suggest for congratulations",4],["For Congratulations",4],["I want some flowers for Congratulating someone",4],["What type of flowers to give for Congratulations?",4],["Suggest something for Congratulations",4],["I want to give it to someone for Congratulating them",4],
        ["Suggest for wedding",5],["For Wedding",5],["I want some flowers for Wedding",5],["What type of flowers to give on Wedding?",5],["Suggest something for Wedding",5],["I want to give it to someone for Wedding",5],
        ["Suggest for sorry",6],["For Sorry",6],["I want some flowers for saying Sorry",6],["What type of flowers to give for saying Sorry?",6],["Suggest something for saying Sorry",6],["I want to give it to someone for saying Sorry",6],
        ["Suggest for miss you",7],["For Miss You",7],["Missing Someone",7],["I want some flowers for Miss You",7],["What type of flowers to give on Miss You?",7],["Suggest something for Miss You",7],["I want to give it to someone for Miss You",7],
        ["Suggest for get well soon",8],["For Get Well Soon",8],["I want some flowers for Get Well Soon",8],["What type of flowers to give for Get Well Soon?",8],["Suggest something for Get Well Soon",8],["I want to give it to someone for Get Well Soon",8],
        ["Goodbye",9],["Byebye",9],["Bye",9],
        ["Thanku",10],["Thank You",10],["Thanks",10],["Thanks a lot",10],["Thank you very much",10],["Thank you so much",10]]

df = pd.DataFrame(data, columns = ["Text","Intent"])
df

# Lemmitization

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

x = df['Text']
y = df['Intent']

vectorizer = TfidfVectorizer(tokenizer=Normalize,stop_words = 'spanish')

X = vectorizer.fit_transform(x)

# training a Naive Bayes classifier 
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()

lr.fit(X, y)

X_test = ["flowers"]
prediction = lr.predict(vectorizer.transform(X_test))

prediction

# To get the probability of test data to be present in each Intent

a = lr.predict_proba(vectorizer.transform(X_test))
a

responses = {0 : {"intent":"greetings","response":['Hi Dear','Hi','Hello', 'Nice to see you',]}, 
      1 : {"intent":"availability","response":['Yes it is available and I can suggest you some.','Yes it is fresh and available']},
      2 : {"intent":"flowers","response":['Endearing Red Roses','Sunshine Yellow Roses','Extravagant 40 Red Roses']},
      3 : {"intent":"flowers","response":['Lillies & Roses Elegant','15 Regal Carnations','Purple Orchids']},
      4 : {"intent":"flowers","response":['Purple Orchids','Yellow Asiatic Lillies','Dark Pink Roses']},
      5 : {"intent":"flowers","response":['Vivid Red Roses','Sweet Pink Roses','12 Purple Orchids']},
      6 : {"intent":"flowers","response":['Pure Love Carnations','Majestic 18 white Roses','Multicolour Roses']},
      7 : {"intent":"flowers","response":['White N Red Floral Beauty','Red Carnation N Leaves','Admirable Asiatic Pink Lillies']},
      8 : {"intent":"flowers","response":['Mesmerizing Charm','Serene Carnation','Unending Love 18 Light Pink Flowers']},
      9 : {"intent":"goodbye","response":['Goodbye','Byebye','Bye','Have a good day']},
      10 : {"intent":"thankyou","response":['You\'re welcome.' , 'No problem.', 'No worries.', ' My pleasure.' , 'Glad to help.']}}

      import json
token = "2016396929:AAGnKHlYNKIb4w8OJ0mmmBtH0vzG6lhCsmc"

class telegram_bot():
    def __init__(self):
        self.token=token 
        self.url = f"https://api.telegram.org/bot{self.token}"

    def get_updates(self,offset=None):
        url = self.url+"/getUpdates?timeout=100"
        if offset:
            url = url+f"&offset={offset+1}"
        url_info = requests.get(url)
        return json.loads(url_info.content)
    def send_message(self,msg,chat_id):
        url = self.url + f"/sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)

    def grab_token(self):
        return tokens

        # To get responnse

def response(user_response):
    text_test = [user_response]
    X_test = vectorizer.transform(text_test)
    prediction = lr.predict(X_test)
    reply = random.choice(responses[prediction[0]]['response'])
    return reply

# To get indent
def intent(user_response):
    text_intent = [user_response]
    X_test_intent = vectorizer.transform(text_intent)
    predicted_intent = lr.predict(X_test_intent)
    intent_predicted = responses[predicted_intent[0]]['intent']
    return intent_predicted

    import random

def bot_initialize(user_msg):
    flag=True
    while(flag==True):
        user_response = user_msg
        
        user_intent = intent(user_response)
        
        if(user_intent != 'goodbye'):
            if(user_response == '/start'):
                resp = """Hi! Here You can get suggestion of what type of Flowers you can give on a particular occasion.\nType Bye to Exit."""
                return resp
            
            elif (user_intent == 'greetings'):
                resp = str(random.choice(responses[0]['response'])) + ", How may I help you?"
                return resp
        
            elif(user_intent == 'thankyou'):
                resp = random.choice(responses[10]['response'])
                return resp
            
            elif(user_intent == 'availability'):
                resp = random.choice(responses[1]['response'])
                return resp
            
            elif(user_intent == "flowers"):
                user_response=user_response.lower()
                resp = "I will suggest you to give :-\n " + response(user_response)
                return resp
            
            else:
                resp = "Ummm! Please rephrase your sentence. I am not that smart."
                return resp
            
        else:
            flag = False
            resp = random.choice(responses[9]['response'])
            return resp

            tbot = telegram_bot()

update_id = None

def make_reply(msg):
    if msg is not None:
        reply = bot_initialize(msg)
    return reply


while True:
    print("...")
    updates = tbot.get_updates(offset=update_id)
    updates = updates['result']
    print(updates)
    if updates:
        for item in updates:
            update_id = item["update_id"]
            print(update_id)
            try:
                message = item["message"]["text"]
                print(message)
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            print(from_)

            reply = make_reply(message)
            tbot.send_message(reply,from_)