import json

import pandas as pd
import requests  # api 요청
import api


def call_master_api_and_make_csv(request_result, filename):
    r_entries = json.loads(request_result.content)['entries']  # entries jason file 을 가져왔음
    league_df = pd.DataFrame(r_entries)
    print(league_df.info())
    print(league_df.head())
    league_df.to_csv(filename, mode='w')


def call_all_tier_api(request_result, filename):
    r_entries = json.loads(request_result.content)  # entries jason file 을 가져왔음
    league_df = pd.DataFrame(r_entries)
    print(league_df.info())
    print(league_df.head())
    league_df.to_csv(filename, mode='w')


# api 요청
# 마스터 데이터 가져와서 데이터프레임으로 변환
api_url_master = 'https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key={}'.format(
    api.api_keys[0])  # api key 넣기
r = requests.get(api_url_master)
call_master_api_and_make_csv(r, 'data/master_api.csv')  # 저장

for tier in api.tiers:
    for division in api.divisions:
        api_url_each_tier = 'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{}/{}?api_key={}'.format(
            tier, division, api.api_keys[1])  # api key 넣기
        request_result = requests.get(api_url_each_tier)
        call_all_tier_api(request_result, "data/" + str(tier) + "_" + division + "_raw.csv")
