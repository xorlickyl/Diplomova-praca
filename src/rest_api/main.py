from flask import Flask
from flask_restful import Api

from src.rest_api.elements import Get_elements

app = Flask(__name__)
api = Api(app)

api.add_resource(Get_elements,'/elements/<url>')

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')

