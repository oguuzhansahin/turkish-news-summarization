from flask import Flask,render_template,url_for,request
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from csv import reader
from IPython.display import clear_output
from bs4 import BeautifulSoup as bs

import pandas as pd
import numpy as np
import requests 
import re
import nltk

def GetData(url):
    
    try:    
        html = requests.get(url).text
        soup = bs(html, "lxml")
        
        body_text = soup.findAll("div", class_ = "content-body__detail")[0].findAll('p')          
        body_text_big = ""
        
        for i in body_text:
            body_text_big = body_text_big +i.text           
             
        return(body_text_big)
    
    except IndexError:       
        return ("Boş Data")

tokenizer = AutoTokenizer.from_pretrained("model")
model = AutoModelForSeq2SeqLM.from_pretrained("model")

def generate_summary(main_news):
  source_encoding=tokenizer(
    main_news,
    max_length=512,
    padding="max_length",
    truncation=True,
    return_attention_mask=True,
    add_special_tokens=True,
    return_tensors="pt")

  generated_ids=model.generate(
      input_ids=source_encoding["input_ids"],
      attention_mask=source_encoding["attention_mask"],
      num_beams=1,
      max_length=512,
      repetition_penalty=1,  
      use_cache=True
  )

  preds=[tokenizer.decode(gen_id, skip_special_tokens=True, clean_up_tokenization_spaces=True) 
         for gen_id in generated_ids]

  return "".join(preds)



app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        text = request.form['text']
        if text.startswith("https://"):
            
            data = GetData(text)
            
            summarized_text = generate_summary(data)
        else:
            summarized_text = generate_summary(text)
        
    return render_template('result.html', prediction = summarized_text)
            
    


if __name__ == '__main__':
    app.run(debug=True)