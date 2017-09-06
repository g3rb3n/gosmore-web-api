import sys
import os
import os.path
import logging
import logging.config
import codecs
import json
import urllib
from flask import Flask, Response, request
from flask.ext.cors import CORS

from gosmorewebapi.util.json_response import json_response
from gosmorewebapi.util import icinga
import gosmorewebapi.gosmore as api
import gosmorewebapi.config as config

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

mimetypes = {
    'geojson':'application/json',
    'kml':'application/vnd.google-earth.kml+xml'
}

@app.errorhandler(500)
def internal_server_error(e):
    message = str(e)
    icinga.increment(icinga.critical, message)
    logger.exception(e)
    import traceback
    traceback.print_exc()
    return Response(
        json.dumps({'error': message}),
        mimetype='application/json'
    ),500

@app.errorhandler(404)
def not_found_error(e):
    message = str(e)
    icinga.increment(icinga.warning, message)
    logging.warn(e)
    import traceback
    traceback.print_exc()
    return Response(
        json.dumps({'error': message}),
        mimetype='application/json'
    ),404

@app.route('/api/icinga')
@json_response
def check_errors():
    return icinga.report()


@app.route('/api/1/route', methods=['POST'])
@json_response
def route():
    data = request.get_json()
    a = data['from']
    b = data['to']
    vehicle = data['vehicle']
    fastest = data['fastest']
    return api.route(a, b, [], vehicle, fastest)

@app.route('/api/1/route.<format>', methods=['POST'])
@json_response
def route_formatted(format):
    data = request.get_json()
    a = data['from']
    b = data['to']
    vehicle = data['vehicle']
    fastest = data['fastest']
    return api.route_formatted(a, b, vehicle, fastest, format)

@app.route('/api/1/compat.<format>', methods=['GET'])
def compat_formatted(format):
    a = {
        'latitude':float(request.args.get('flat')),
        'longitude':float(request.args.get('flon'))
    }
    b = {
        'latitude':float(request.args.get('tlat')),
        'longitude':float(request.args.get('tlon'))
    }
    vehicle = request.args.get('v')
    fastest = request.args.get('fast')
    resp = api.route_formatted(a, b, vehicle, fastest, format)
    return Response(resp, mimetype=mimetypes[format])

if __name__ == '__main__':
    '''
    Start the server
    '''
    logger.info('server started on port %s' % config.port)
    app.run(host='0.0.0.0', port=config.port, debug=config.dev_mode, use_reloader=not config.dev_mode, threaded=True)
