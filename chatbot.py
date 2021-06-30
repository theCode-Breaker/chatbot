import requests
import bs4

base_url=input('Enter the wikipedia link from which you want to train your bot: ')
r = requests.get(base_url)
if (r.status_code == 200):
  print('Found it')
else:
  print('Could not find it')

soup = bs4.BeautifulSoup(r.text,'html.parser')

headers = []
for url in soup.findAll("h3"):
    headers.append(url.text)

i = len(headers) - 1
counter = 0
while counter <= i:
    if headers[counter].startswith('\n'):
        headers.pop(counter)
        counter -= 1
    counter += 1
    i = len(headers) -1

r = requests.get(base_url)
all_para = ""
soup = bs4.BeautifulSoup(r.text,'html.parser')
for iteri in range(len(headers)):
    deet = soup.find('h3', text = headers[iteri])
    for para in deet.find_next_siblings():
        if para.name == "h2" or para.name == "h3":
            break
        elif para.name == "p":
            all_para += para.get_text()
            all_para += '\n'

with open('./wiki.txt', 'wb') as file_handler:
        file_handler.write(all_para.encode('utf8'))

import nltk # to process text data
import numpy as np # to represent corpus as arrays
import random 
import string # to process standard python strings
from sklearn.metrics.pairwise import cosine_similarity # We will use this later to decide how similar two sentences are
from sklearn.feature_extraction.text import TfidfVectorizer

#nltk.download('punkt')
#nltk.download('wordnet')

filepath='wiki.txt'
corpus=open(filepath,'r',errors = 'ignore')
raw_data=corpus.read()
raw_data=raw_data.lower()
sent_tokens=nltk.sent_tokenize(raw_data) 
word_tokens=nltk.word_tokenize(raw_data)

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ["hello", "hi", "greetings", "sup", "what's up","hey", "hey there"]
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split(): # Looks at each word in your sentence
        if word.lower() in GREETING_INPUTS: # checks if the word matches a GREETING_INPUT
            return random.choice(GREETING_RESPONSES) # replies with a GREETING_RESPONSE

def response(user_response):
    
    robo_response='' # initialize a variable to contain string
    sent_tokens.append(user_response) #add user response to sent_tokens
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english') 
    tfidf = TfidfVec.fit_transform(sent_tokens) #get tfidf value
    vals = cosine_similarity(tfidf[-1], tfidf) #get cosine similarity value
    idx=vals.argsort()[0][-2] 
    flat = vals.flatten() 
    flat.sort() #sort in ascending order
    req_tfidf = flat[-2] 
    
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

import datetime

def tell_time(sentence):
    for word in sentence.split():
        # your code here
            currentdt = datetime.datetime.now()
            return currentdt.strftime("%Y-%m-%d %H:%M:%S")

tell_time('time')

flag=True
print("CATHY: My name is Cathy. I will answer your queries. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("CATHY: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("CATHY: "+greeting(user_response))
            else:
                print("CATHY: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("CATHY: Bye! take care..")