import os

def cal_score(score_points, coin_count, time_taken, enemy_kills = 0):
    score_points += (coin_count + enemy_kills * 2) * 500
    score_points -= (time_taken) * 100
    return score_points

def score_keeping(path, name, score_points, info):
    coin_count = info[0]
    time_taken = info[1]
    enemy_kills = info[2]

    score_points = cal_score(score_points, coin_count, time_taken, enemy_kills)

    f = open(path + 'score', 'w')

    f.close()


