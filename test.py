import json
import numpy as np
import pandas as pd
import requests  # api 요청
import seaborn as sns
import api
from os.path import join
import pprint

# r = requests.get('http://ddragon.leagueoflegends.com/cdn/10.10.3216176/data/en_US/champion.json')
# json_data = json.loads(r.content)
# user_data = json_data['data']
#
# champ = dict()
# count = 0
# for key, value in user_data.items():
#     # print(key)
#     # print(value['key'], ":", value['id'])
#     count += 1
#     champ[int(value['key'])] = value['id']
#     # print('id :', value['id'])
#     # print('key :', value['key'])
#     # print('name :', value['name'])
#
# print(count)
# result = sorted(champ.items())
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(result)

nan = np.nan
pd_data = pd.DataFrame({
    'a': [nan, 1, 2, nan],
    'b': [2, 3, 4, 5],
    'c': [3, nan, 3, 4]
})
pd_data.to_csv("a.csv")

a = pd.read_csv('a.csv')
print(a.head())
index = 2
print(a['a'][index], pd.isnull(a['a'][index]))
