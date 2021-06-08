from flask import Flask,render_template,request, jsonify,make_response,redirect
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk import FreqDist
app = Flask(__name__)

tokenizer=ToktokTokenizer()

dataset = pd.read_csv("data/data_kichwa.csv")

def clean_data(text):
    tokens = tokenizer.tokenize(text)
    tokens = [ tokens.strip() for tokens in tokens]
    filtered_tokens=[token.lower() for token in tokens ]
    filtered_tokens=" ".join(filtered_tokens)
    
    return re.sub('[.+,]+', '', filtered_tokens)
def remove_stopwords(list):
  data = []
  data2 = []
  for i in list:
    if len(i)>len('karka'):
      data.append(re.sub('ka$','',i))  
    else:
      data.append(i)
  for j in data:
    data2.append(re.sub('ta$','',j))
  for i in data2:
    if i == 'shuk' :
      data2.remove(i)
    elif i =='chay':
      data2.remove(i)
  return data2

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisis',methods=['POST'])
def analisis_post():
    if request.method == 'POST':
        text = request.form['inputText']
        fdist = FreqDist(remove_stopwords(clean_data(text).split())).most_common()
        data_F_1 = []
        data_F_2 = []
        for i in fdist:
          data_F_1.append(i[0])
        for i in fdist:
          data_F_2.append(i[1])
        # dic = list(data_F_1)
        # di2 = list(data_F_2)
        data_json  = list(data_F_1)
        data_num =   list(data_F_2) 

    return render_template('analisis.html', data_num=data_num,data_json=data_json)




app.run(host='0.0.0.0',port='8080')