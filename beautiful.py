import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://www.linkedin.com/search/results/people/?origin=SWITCH_SEARCH_VERTICAL&sid=b%3A!"

reponse=requests.get(url)

soup = BeautifulSoup(reponse.text,"html.parser")
print(soup.find_all('div', attrs={'class' : 'mn-connection-card__name'}))

# intro = soup.find_all('span', {'class': 'app-aware-link'})
 
# print(intro)
# items = soup.find_all('a', class_='app-aware-link')
# new_items=[]

# # visible = soup.find_all('a', class_='app-aware-link')
# # for profile in visible:
# #     if profile.get('href').split('/')[3] == 'in':
# #         new_items(profile.get('href'))

# for i in items:
#     item={}
#     item['href']= i.href
#     new_items.append(item)

# print(new_items[0])

# df=pd.DataFrame(intro,columns=['ok'])
# df.to_csv('beau.csv',index=False,encoding='utf-8')