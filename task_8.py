from task_6 import *
from flask import Response, Flask, request, jsonify
from flasgger import Swagger, swag_from
import xmltodict

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/report', methods=['GET'])
@swag_from('get_recers.yaml')
def get_racers_and_times():
    format = request.args.get('format')
    if format == 'json':
        return jsonify(return_res(calculate(), read_abbreviations())) 
    elif format == 'xml':
        racers_and_times = return_res(calculate(), read_abbreviations())
        xml_data = xmltodict.unparse({'racers_and_time': {'racers_and_times': racers_and_times}}, pretty=True)
        return Response(xml_data, mimetype='text/xml')
    else:
        return jsonify({'error': 'Invalid format'}), 400

if __name__ == '__main__':
    app.run(debug=True)