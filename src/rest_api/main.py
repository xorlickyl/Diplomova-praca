from datetime import datetime

from flask import Flask, make_response
from flask_restful import Api
import simplejson as json

from src.rest_api.elements import Get_elements

app = Flask(__name__)
api = Api(app)

api.add_resource(Get_elements,'/elements/<url>')
"""
def encode_to_json(o):
"""
    #The default function for JSON encoding, used to process objects for
    #JSON encoding
"""
    if type(o) is datetime:
        return o.astimezone().isoformat()

    raise TypeError('Object of type {} is not JSON serializable'
                    .format(o.__class__.__name__))

json_encoder = json.JSONEncoder(default=encode_to_json,
                                for_json=True,
                                indent=4*' ')

@api.representation('application/json')
def output_json(data, code, headers=None):
    json_string = json_encoder.encode(data)
    resp = make_response(json_string, code)
    resp.headers.extend(headers or {})
    return resp
"""

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')

