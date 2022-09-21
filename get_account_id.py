import time

import numpy as np
import pandas as pd
import requests  # api 요청
import seaborn as sns
import api
from os.path import join

# from skimage import io  # 미니맵 처리

sns.set()

r = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')  # version data 확인
current_version = r.json()[0]  # 가장 최신 버전 확인 -> lol update 패치 최상위 패치 버전

r = requests.get('http://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/champion.json'.format(current_version))
parsed_data = r.json()  # 파싱
info_df = pd.DataFrame(parsed_data)
print(info_df.head())  # version 패치 정보 가져옴

# champ_info_df의 data 값들을 데이터프레임으로 변환

# 데이터의 각 행을 시리즈 형태로 변환하여 딕셔너리에 추가
champ_dic = {}
for i, champ in enumerate(info_df.data):
    champ_dic[i] = pd.Series(champ)

# 데이터 프레임 변환 후 Transpose
champ_df = pd.DataFrame(champ_dic).T

# output : 챔피언 데이터 안에도 info와 stats가 딕셔너리 형태임
# 이 데이터들을 데이터프레임으로 변환하여 각 챔피언에 대한 변수로 추가해야 한다.

# champ_df의 info, stats의 데이터를 변수로 추가
champ_info_df = pd.DataFrame(dict(champ_df['info'])).T
champ_stats_df = pd.DataFrame(dict(champ_df['stats'])).T

# 데이터 합치기
champ_df = pd.concat([champ_df, champ_info_df], axis=1)
champ_df = pd.concat([champ_df, champ_stats_df], axis=1)
# 이번 분석에서 필요없는 데이터 제거
champ_df = champ_df.drop(['version', 'image', 'info', 'stats'], axis=1)
champ_df.info()  # 필요한 패치에 대한 정보를 가져옴

index_of_api = 0
api_key = api.api_keys[index_of_api]
error_count = 0

for tier in api.tiers:
    for division in api.divisions:
        filename = str(tier) + "_" + division
        full_filename = filename + '_raw.csv'
        league_df = pd.read_csv(join('data', full_filename))
        league_df['account_id'] = np.nan  # account_id 초기화
        # for i, summoner_id in enumerate(league_df['summonerId']):
        for i, summoner_name in enumerate(league_df['summonerName']):
            is_api_connected = True
            # 각 소환사의 SummonerId와 API Key를 포함한 url을 만들고, Summoner API에서 AccountId를 가져와 채워넣는다.
            # print(summoner_name, api_key)
            api_url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + api_key
            # api_url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/' + summoner_id + '?api_key=' + api_key
            r = requests.get(api_url)
            while r.status_code != 200:  # 요청 제한 또는 오류로 인해 정상적으로 받아오지 않는 상태라면, 5초 간 시간을 지연
                error_count += 1
                if r.status_code == 404 or error_count > 7:
                    error_count = 0
                    is_api_connected = False
                    break
                if error_count == 5:
                    time.sleep(120)
                print("request error", r.status_code)
                time.sleep(3)
                index_of_api = (index_of_api + 1) % len(api.api_keys)
                api_key = api.api_keys[index_of_api]
                r = requests.get(api_url)
            if is_api_connected:
                account_id = r.json()['accountId']
            else:
                account_id = np.nan
            league_df.iloc[i, -1] = account_id
            time.sleep(1)
        league_df.to_csv("nextdata/" + filename + '_next.csv')
