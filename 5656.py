import numpy as np
import pandas as pd
from os.path import join
import api
from sklearn.linear_model import LogisticRegression

for tier in api.tiers:
    sum_train_x = None
    sum_train_y = None
    sum_test_x = None
    sum_test_y = None
    for division in api.divisions:
        filename = str(tier) + "_" + division + "_match.csv"
        league_data = pd.read_csv(join('match', filename), header=None)  # data 정보 전부 가져옴
        # print(league_data.head())
        data = np.array(league_data)
        size_x, size_y = data.shape
        train_size = int(0.7 * size_x)
        print(train_size)
        test_size = size_x - train_size
        train_x = data[0:train_size, 0:296]  # input data
        a = data[0:train_size, 148:296]
        b = data[0:train_size, 0:148]
        reverse_train_x = np.concatenate((a, b), axis=1)
        train_y = data[0:train_size, 296]  # result data
        reverse_train_y = np.where(train_y == 1, 2, train_y)
        reverse_train_y = np.where(reverse_train_y == 0, 1, reverse_train_y)
        reverse_train_y = np.where(reverse_train_y == 2, 0, reverse_train_y)
        test_x = data[train_size + 1:, 0:296]
        test_y = data[train_size + 1:, 296]
        train_x = np.concatenate((train_x, reverse_train_x), axis=0)
        train_y = np.concatenate((train_y, reverse_train_y), axis=0)
        if sum_train_x is None:
            sum_train_x = train_x
            sum_train_y = train_y
            sum_test_x = test_x
            sum_test_y = test_y
        else:
            sum_train_x = np.concatenate((sum_train_x, train_x), axis=0)
            sum_train_y = np.concatenate((sum_train_y, train_y), axis=0)
            sum_test_x = np.concatenate((sum_test_x, test_x), axis=0)
            sum_test_y = np.concatenate((sum_test_y, test_y), axis=0)
    model = LogisticRegression(random_state=0)
    result = model.fit(sum_train_x, sum_train_y)
    print(model.score(sum_train_x, sum_train_y))
    print(model.score(sum_test_x, sum_test_y))