import random
import numpy as np


def exp(time_mean):
    a = 0.0
    while a == 0:
        a = random.uniform(0, 1)
    a = -time_mean * np.log(a)
    return a


def uniform(time_min, time_max):
    a = 0.0
    while a == 0:
        a = random.random()
    a = time_min + a * (time_max - time_min)
    return a


def norm(time_mean, time_deviation):
    return time_mean + time_deviation * random.gauss(0.0, 1.0)


def erlang(time_mean, k):
    return np.random.gamma(k, time_mean / k)
