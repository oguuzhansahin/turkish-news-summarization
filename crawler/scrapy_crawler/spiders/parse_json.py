
import json
# from pprint import pprint

json_file = 'webtekno.json'

with open(json_file, 'r') as content_file:
    content = content_file.read().strip()
    
   
contentsSs = content.split("\n")

#%%
url_list = []

for content in contentsSs:
    
    content_j = json.loads(content)
    url_list.append(content_j['url'])
    

clean_url = [url for url in url_list if url.endswith(".html")]

#%%

ornek = contentsSs[0]
ornek = json.loads(ornek)

#%%

import pandas as pd 

url_df = pd.DataFrame(clean_url, columns = ['url'])

url_df.to_csv("url_list.csv",index=False)
