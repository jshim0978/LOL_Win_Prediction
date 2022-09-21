from os.path import join
import pandas as pd
import csv
import api
import requests
import time


def one_hot_encoding(arr, championId, team):
    # arr must be 148 * 2 size
    # 0 ~ 147 : Blue team, 148 ~ 295 : Red team
    # teamId 100 : Blue, 200 : Red
    key = str(championId)
    index = 0
    for i in range(len(champ_data)):
        if champ_data[i][0] == key:
            index = i
            break

    team = str(team)
    if team == '100':
        arr[index] = 1
    elif team == '200':
        arr[index + 148] = 1
    else:
        print('one hot encoding error occurred')


api_index = 0
api_key = api.api_keys[api_index]

for tier in api.tiers:
    for division in api.divisions:
        filename = tier + "_" + division
        full_filename = filename + "_match_list.csv"
        csvfile = open("match/" + filename + "_match.csv", 'w', newline="")
        csvwriter = csv.writer(csvfile)
        league_match_list = pd.read_csv(join('matchlistdata', full_filename))
        match_list = []
        for index, game_id in enumerate(league_match_list['gameId']):
            match_list.append(game_id)

        f = open('champdata/champ_data.csv', 'r')
        rdr = csv.reader(f)

        champ_data = list()
        for line in rdr:
            champ_data.append([line[1], line[2]])

        # total_list = list()
        for i in range(len(match_list)):
            time.sleep(0.9)
            number_of_request_fail = 0
            is_not_error = True
            request_url = 'https://kr.api.riotgames.com/lol/match/v4/matches/{}?api_key={}'.format(match_list[i],
                                                                                                   api_key)
            r = requests.get(request_url)
            print(r.status_code)

            while r.status_code != 200:
                time.sleep(3)
                if r.status_code == 404 or number_of_request_fail > 7:
                    is_not_error = False
                    break
                else:
                    if number_of_request_fail > 5:
                        time.sleep(3)
                    api_index = (api_index + 1) % len(api.api_keys)
                    api_key = api.api_keys[api_index]
                print("error happen :", r.status_code)
                r = requests.get(request_url)
                number_of_request_fail += 1

            if is_not_error:
                r = r.json()
                win = 1
                if r['participants'][0]['teamId'] == 100 and r['participants'][0]['stats']['win']:
                    win = 0
                else:
                    win = 1
                arr = [0 for _ in range(296)]
                for index_of_participants in range(len(r['participants'])):
                    championId = r['participants'][index_of_participants]['championId']
                    team = r['participants'][index_of_participants]['teamId']
                    one_hot_encoding(arr, championId, team)
                arr.append(win)
                csvwriter.writerow(arr)
                # total_list.append(arr)
        csvfile.close()

        # for row in total_list:
        #     csvwriter.writerow(row)
