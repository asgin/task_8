import datetime
from pathlib import Path

def calculate_time(time1, time2):
    time_format = '%H:%M:%S.%f'
    datetime1 = datetime.datetime.strptime(time1.strip(), time_format)
    datetime2 = datetime.datetime.strptime(time2.strip(), time_format)
    time_diff = abs(datetime1 - datetime2)
    return str(time_diff)

def read_abbreviations():
    with open(Path('all_data/abbreviations.txt'), 'r') as f:
        racers = [i.strip() for i in f.readlines()]
        s = {}
        for i in racers:
            s[i.split('_')[0]] = i.split('_')[1:]
        f.seek(0) 
        return s


def calculate():
    with open(Path('all_data/start.log'), 'r') as f:
        with open(Path('all_data/end.log'), 'r') as fi:
            file_start = sorted([i.split('_') for i in f.readlines()], key=lambda x: x[0].strip())
            file_end = sorted([i.split('_') for i in fi.readlines()], key=lambda x: x[0].strip())
            s = {}
            del file_start[0]
            for i, j in zip(file_start, file_end):
                s[''.join([j for j in i[0] if j.isalpha()])] = calculate_time(j[1], i[1])
            fi.seek(0) 
        f.seek(0) 
    return s

def return_res(diction, dict2):
    dict2 = dict(sorted(dict2.items(), key=lambda x: x[0]))
    diction = dict(sorted(diction.items(), key=lambda x: x[0]))
    list_time = [dict2[abr] + [abr] + [diction[r]] for abr, r in zip(dict2.keys(), diction.keys())]
    list_time = sorted(list_time, key=lambda x: x[1])
    for i in range(len(list_time)):
        list_time[i].append(i + 1)
    return list_time