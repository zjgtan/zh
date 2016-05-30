#coding: gbk

from ConfigParser import ConfigParser
import csv
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from scipy.stats.mstats import chisquare
import sys


def load_conf(conf_file):
    conf_dict = {}
    parser = ConfigParser()
    parser.read(conf_file)

    for sec in parser.sections():
        conf_dict[sec] = {}
        for opt in parser.options(sec):
            conf_dict[sec][opt] = parser.get(sec, opt)
            
    return conf_dict;

def load_csv(data_file):
    data = []
    for d in csv.DictReader(open(data_file)):
        tmp = {}
        for key in d:
            try:
                if d[key] == '' or d[key] == ' ':
                    value = float("nan")
                else:
                    value = float(d[key])
                tmp[key] = value
            except:
                tmp[key] = d[key]

        data.append(tmp)

    return data

def ttest(df, column, label):
    df_tmp = df.loc[:, [column, label]]
    df_tmp = df_tmp.dropna()
    A = df_tmp[df_tmp[label] == 1][column]
    B = df_tmp[df_tmp[label] == 0][column]
    
    statics, pvalue = ttest_ind(A, B)
    all_mean = np.mean(df_tmp[column].values)
    all_std = np.std(df_tmp[column].values)
    A_mean = np.mean(A)
    A_std = np.std(A)
    B_mean = np.mean(B)
    B_std = np.std(B)

    str1 = "%f(%f),%f(%f),%f(%f),%f" % (all_mean, all_std, B_mean, B_std, A_mean, A_std, pvalue)
    return str1

def kftest(df, column, label, tag):
    df_tmp = df.loc[:, [column, label]]
    df_tmp = df_tmp.dropna()
    
    col = dict(pd.value_counts(df_tmp[column]))
    lab = dict(pd.value_counts(df_tmp[label]))
    f_obs = []
    f_exp = []

    obs_d = {}
    for i in col:
        for j in lab:
            obs = sum([1 \
                    if df_tmp.iloc[k][column] == i and df_tmp.iloc[k][label] == j \
                    else 0 for k in range(len(df_tmp))])

            obs_d.setdefault(j, {})
            obs_d[j][i] = obs

            f_obs.append(obs)

            f_exp.append(1. * lab[j] / (sum(lab.values())) * col[i])

    statics, p_value = chisquare(f_obs, f_exp, ddof=len(f_obs) - 2)

    str1 = "%d(%f),%d(%f),%d(%f),%f" % (col[tag], col[tag] * 1. / sum(col.values()), 
            obs_d[0][tag],
            1. * obs_d[0][tag] / sum(obs_d[0].values()),
            obs_d[1][tag],
            1. * obs_d[1][tag] / sum(obs_d[1].values()),
            p_value)
    return str1

def main():

    outfile = open("stats.csv", "w")
    conf_dict = load_conf("zh.cfg")
    data = load_csv("data.csv")
    df = pd.DataFrame(data)

    col = "性别男1女2".decode("gbk").encode("utf8")
    for column in conf_dict:
        if conf_dict[column]["func"] == "ttest":
            str1 = ttest(df, column.decode("gbk").encode("utf8"), conf_dict[column]["label"])
        elif conf_dict[column]["func"] == "kftest":
            str1 = kftest(df, column.decode("gbk").encode("utf8"), conf_dict[column]["label"], float(conf_dict[column]["tag"]))
        print >>outfile, "%s,%s" % (column, str1)


if __name__ == "__main__":
    main()
