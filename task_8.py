from fastapi import FastAPI
import json
import xmltodict
from task_6 import *

app = FastAPI()

@app.get('/api/report/{format}')
def get_report(format: str = 'json'):
    if format == 'json':
        json_file = json.dumps(return_res(calculate(), read_abbreviations()))
        return json_file
    if format == 'xml':
        racers_and_times = return_res(calculate(), read_abbreviations())
        xml_data = xmltodict.unparse({'racers_and_time': {'racers_and_times': racers_and_times}}, pretty=True)
        return xml_data
    
@app.get('/api/report/racer/{racer_id}')
def get_user(racer_id: int):
    for i in return_res(calculate(), read_abbreviations()):
        if racer_id in i:
            return '  |  '.join(i[:4])
    else:
        return 'Your racer not in the list'
    
@app.patch('/api/report/racer')
def change_race_time(racer_id: int, time: str = '', name: str = ''):
    for i in return_res(calculate(), read_abbreviations()):
        if racer_id in i:
            racer = i
    if name and time:
        racer[0] = name
        racer[3] = time
        return {'status': 200, 'racer': racer}
    if time:
        racer[3] = time
        return {'status': 200, 'racer': racer}
    if name:
        racer[0] = name
        return {'status': 200, 'racer': racer}
    
@app.delete('/api/report/racer')
def delete_racer(racer_id: int):
    spis = return_res(calculate(), read_abbreviations())
    for i in spis:
        if racer_id in i:
            spis.remove(i)
            return {'status': 200, 'all list now': spis}

@app.post('/api/report/racer')
def add_racer(name: str, company: str, abriv: str, time: str):
    spis = return_res(calculate(), read_abbreviations())
    spis.append([name] + [company] + [abriv] + [time] + [len(spis) + 1])
    return {'status': 200, 'all list after add': spis}