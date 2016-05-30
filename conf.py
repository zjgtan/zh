#!/usr/bin/env python
#coding:gb18030
####################################################
# Copyright(c) ,Baidu.com, Inc. All Rights Reserved
# @file        : conf.py
# @author      : chenjiawei, chenjiawei@baidu.com
# @revision    : 2015-12-27 21:06:41
# @brief       :
####################################################
import re
import utils

def load(conf_file, DATE):
    conf_dict = {}
    for line in file(conf_file):
        key, value = line.rstrip().split("=")
        if "$DATE" in value:
            value = value.replace("$DATE", DATE)
        if "DATE_SHIFT" in value:
            reg = re.compile(r'DATE_SHIFT\((\d+), ([+-])\)')
            delta, direction = re.findall(reg, value)[0]
            date = utils.date_shift(DATE, int(delta), direction)
            reg = re.compile(r'DATE_SHIFT\(\d+, [+-]\)')
            value = value.replace(reg.findall(value)[0], date)
        if "DATE_RANGE" in value:
            reg = re.compile(r'DATE_RANGE\((\d+), (\d+), ([+-])\)')
            start_date, delta, direction = re.findall(reg, value)[0]
            dates = utils.date_range(start_date, int(delta), direction)
            reg = re.compile(r'DATE_RANGE\(\d+, \d+, [+-]\)')
            value = value.replace(reg.findall(value)[0], "{%s}" % ",".join(dates))
        conf_dict[key] = value
    return conf_dict

            
