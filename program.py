import nltk
import numpy as np
nltk.download('punkt')
nltk.download('wordnet')
import string
import warnings
warnings.filterwarnings("ignore")
 
para = """       
*** Repot Card ***
 
Name: Chirag Singh
Class: 12
Adm no: 2199
School: Doon International School
 
*** Marksheet ***
 
Maths :     97
Physics :   95
Chemistry : 98
English :   95
Computers : 100
 
Percentage : 97.0 %.
*** Repot Card ***
 
Name: Tirth Shah
Class: 12
Adm no: 3894
School: Doon International School
 
*** Marksheet ***
 
Maths :     97
Physics :   92
Chemistry : 97
English :   95
Computers : 100
 
Percentage : 96.2 %.
*** Repot Card ***
 
Name: Atharva
Class: 12
Adm no: 3100
School: Doon International School
 
*** Marksheet ***
 
Maths :     97
Physics :   92
Chemistry : 93
English :   96
Computers : 100
 
Percentage : 95.6 %.
*** Repot Card ***
 
Name: Niharika
Class: 12
Adm no: 9874
School: Doon International School
 
*** Marksheet ***
 
Maths :     97
Physics :   95
Chemistry : 98
English :   92
Computers : 100
 
Percentage : 96.4 %.
*** Repot Card ***
 
Name: Anirudh
Class: 12
Adm no: 3534
School: Doon International School
 
*** Marksheet ***
 
Maths :     97
Physics :   98
Chemistry : 94
English :   95
Computers : 100
 
Percentage : 96.8 %.
 
"""
 
sent_tokens = nltk.sent_tokenize(para)
word_tokens = nltk.word_tokenize(para)
 
lemmer = nltk.stem.WordNetLemmatizer()
 
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
 
remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
 
def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
 
from sklearn.feature_extraction.text import TfidfVectorizer
 
from sklearn.metrics.pairwise import cosine_similarity
 
def response(user_response):
    
    robo_response = ""
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer= Normalize,stop_words="english" )
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1],tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_fidf = flat[-2]
    if user_response == "/start":
        robo_response='''
        Reprt Card Bot:
 
        Choose any one name of the following :
        Tirth Shah
        Chirag Singh
        Niharika
        Anirudh
        Atharva
        '''
    elif (req_fidf==0):
        robo_response ="""I am sorry ,
Invalid Input
Please choose any one name from the following:
 
        Tirth Shah
        Chirag Singh
        Niharika
        Anirudh
        Atharva
        """
        sent_tokens.remove(sent_tokens[-1])
    
    else:
        robo_response = sent_tokens[idx]
        sent_tokens.remove(sent_tokens[-1])
    return robo_response
 
 
import requests
import json
 
 
class telegram_bot():
    def __init__(self):
        self.token = "1330119734:AAEHk9-UWLAh5wN7gw2G3t7c_nLdcOMHKrM"
    
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
tbot = telegram_bot()
 
update_id = None
 
def make_reply(msg):
    if msg is not None:
        reply = response(user_response=msg)
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
