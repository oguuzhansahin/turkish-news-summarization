from csv import reader
from IPython.display import clear_output
from bs4 import BeautifulSoup as bs

import pandas as pd
import numpy as np
import requests 
import re
import nltk


DATA_PATH = "url_list.csv"
df = pd.read_csv(DATA_PATH)

#%% 
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
#%%
articles = []

for idx, url in enumerate(df.url):
    print(idx)
    articles.append(GetData(url))
   
#%%

df["Metin"] = articles
df['Metin'].replace('', np.nan, inplace = True)
df.dropna(subset=["Metin"],inplace = True)
df.drop(index=15,inplace = True)
df.to_csv("url_metin.csv",index = False)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    