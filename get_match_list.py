import time

import numpy as np
import pandas as pd
import requests  # api 요청
import seaborn as sns
import api
from os.path import join

# Match 데이터 받기 (gameId를 통해 경기의 승패, 팀원과 같은 정보가 담겨있다.)

now_season = 10
error_count = 0

index_of_api_key = 0
api_key = api.api_keys[index_of_api_key]

season = str(now_season)
for tier in api.tiers:
    for division in api.divisions:
        filename = str(tier) + "_" + division
        full_filename = filename + '_next.csv'
        league_df = pd.read_csv(join('nextdata', full_filename))

        match_info_df = pd.DataFrame()  # match data 저장 하는 공간

        for account_id in league_df['account_id']:
            is_api_connected = True
            if pd.isnull(account_id):
                continue
            # 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/'
            api_url = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + account_id + '?api_key=' + api_key
            r = requests.get(api_url)
            while r.status_code != 200:  # 요청 제한 또는 오류로 인해 정상적으로 받아오지 않는 상태라면, 5초 간 시간을 지연
                error_count += 1
                if r.status_code == 404 or error_count > 7:
                    print("404 error")
                    error_count = 0
                    is_api_connected = False
                    break
                if error_count > 10:
                    time.sleep(120)
                print("request error", r.status_code)
                time.sleep(3)
                index_of_api_key = (index_of_api_key + 1) % len(api.api_keys)
                api_key = api.api_keys[index_of_api_key]
                r = requests.get(api_url)
            if is_api_connected:
                match_info_df = pd.concat([match_info_df, pd.DataFrame(r.json()['matches'])])
            time.sleep(1)
        match_info_df.to_csv('matchlistdata/' + filename + '_match_list.csv')

# match_info_df = pd.read_csv('MatchInfoData.csv', index_col=0)
# match_info_df.reset_index(inplace=True)
#
# match_info_df = match_info_df.drop_duplicates('gameId')
#
# match_df = pd.DataFrame()
# for game_id in match_info_df['gameId']:  # 이전의 매치에 대한 정보 데이터에서 게임 아이디를 가져온다
#     api_url = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + str(game_id) + '?api_key=' + api_key
#     r = requests.get(api_url)
#     while r.status_code != 200:  # 요청 제한 또는 오류로 인해 정상적으로 받아오지 않는 상태라면, 5초 간 시간을 지연
#         time.sleep(5)
#         r = requests.get(api_url)
#     r_json = r.json()
#     temp_df = pd.DataFrame(list(r_json.values()), index=list(r_json.keys())).T  # 게임 아이디에 대한 매치 데이터를 받아서 추가
#     match_df = pd.concat([match_df, temp_df])
#
# match_df.to_csv('MatchData.csv')  # 파일로 저장
