from task_6 import *
from flask import Response, Flask, request, jsonify
from flasgger import Swagger, swag_from
import xmltodict

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/report/<format>')
@swag_from('docs/get_recers.yml')
def get_racers_and_times(format):
    if format == 'json':
        return jsonify(return_res(calculate(), read_abbreviations())) 
    elif format == 'xml':
        racers_and_times = return_res(calculate(), read_abbreviations())
        xml_data = xmltodict.unparse({'racers_and_time': {'racers_and_times': racers_and_times}}, pretty=True)
        return Response(xml_data, mimetype='text/xml')
    else:
        return jsonify({'error': 'Invalid format'}), 400
    
@app.route('/api/report/driver/<racer_id>')
@swag_from('docs/get_recer_from_id.yml')
def get_racer_from_id(racer_id):
    for i in return_res(calculate(), read_abbreviations()):
        if int(racer_id) in i:
            return '  |  '.join(i[:4])
    else:
        return 'Your racer not in the list'

@app.route('/api/report/driver', methods=['POST'])
@swag_from('docs/add_new_racer.yml')
def add_racer():
    name_racer = request.args.get('name_racer')
    company = request.args.get('company')
    abriv = request.args.get('abbriviation')
    time = request.args.get('time')
    spis = return_res(calculate(), read_abbreviations())
    spis.append([name_racer] + [company] + [abriv] + [time] + [len(spis) + 1])
    return {'status': 200, 'all list after add': spis}

@app.route('/api/report/driver', methods=['PATCH'])
@swag_from('docs/change_racer.yml')
def change_racer():
    racer_id = request.args.get('racer_id')
    racer_id = int(racer_id)
    time = request.args.get('time')
    racer_name = request.args.get('neme_racer')
    for i in return_res(calculate(), read_abbreviations()):
        if racer_id in i:
            racer = i
    if racer_name and time:
        racer[0] = racer_name
        racer[3] = time
        return {'status': 200, 'racer': racer}
    if time:
        racer[3] = time
        return {'status': 200, 'racer': racer}
    if racer_name:
        racer[0] = racer_name
        return {'status': 200, 'racer': racer}
    
@app.route('/api/report/driver', methods=['DELETE'])
@swag_from('docs/delete_recer.yml')
def delete_racer():
    racer_id = request.args.get('rac_id')
    racer_id = int(racer_id)
    spis = return_res(calculate(), read_abbreviations())
    for i in spis:
        if racer_id in i:
            spis.remove(i)
            return {'status': 200, 'all list now': spis}

if __name__ == '__main__':
    app.run(debug=True)