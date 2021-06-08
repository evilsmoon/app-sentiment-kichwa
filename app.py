from flask import Flask,render_template,request, jsonify,make_response,redirect
import re
import pandas as pd
import numpy as np
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
def compara(lista,dataset):
  s=[]
  cont=0
  r=0
  data1=[]
  data2=[]
  for i  in (dataset['Kichwa']):
    # print(i)
    r +=1
    for j in lista:
      # print(j)
      if i == j:
        # data2.append(dataset[r:r+1])
        # data1.append(dataset.iloc[r,0])
        # data1.append(dataset.iloc[r,1])
        data1.append(dataset.iloc[r-1,3])
        data2.append(dataset.iloc[r-1,1])

        cont +=1
        s.append(i)
  # print(len(data1))
  w=0
  for q in data1:
    w=q+w

  data_pro = w/len(data1)  
  data_n_p =''
  print('Promedio de palabras ',data_pro)
  if data_pro <=0.43:
    data_n_p += 'Negativo'
  elif data_pro >=0.7:
    data_n_p += 'Positivo'
  elif data_pro >0.43 and data_pro<0.7:
    data_n_p += 'Neutro'

  return data1,data2,data_pro,data_n_p
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisis',methods=['POST'])
def analisis_post():
    if request.method == 'POST':
        text = request.form['inputText']
        if text:
          fdist = FreqDist(remove_stopwords(clean_data(text).split())).most_common()
          data_F_1 = []
          data_F_2 = []
          for i in fdist:
            data_F_1.append(i[0])
          for i in fdist:
            data_F_2.append(i[1])

          data_json  = list(data_F_1)
          data_num   = list(data_F_2) 
          numero , label,por,val_por =compara(remove_stopwords(clean_data(text).split()),dataset)
          list_predict = list(zip(label,numero))
          data = []
          for i in list_predict:
            if i not in data:
              data.append(i)
          print(data)
          fdist_data = FreqDist(list_predict).most_common()
          data_names = []
          data_values = []
          data_values2 = []
          for i in fdist_data:
            for j in  data:
              if j == i[0]:
                data_names.append(j[0])
                data_values.append(j[1])
                data_values2.append(i[1])

          # data_final = list(zip(data_names,data_values,data_values2))
          return render_template('analisis.html', 
                                  data_num=data_num,
                                  data_json=data_json,
                                  data_names=data_names ,
                                  data_values=data_values , 
                                  data_values2=data_values2,
                                  por = por ,
                                  val_por= val_por
                                  )
        else:
          return render_template('index.html')



if __name__ == '__main__':
  app.run(host='0.0.0.0',port='80')

# app.run(debug=True)