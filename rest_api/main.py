from flask import Flask
from flask_restful import Api

from src.rest_api.elements import Get_elements
from src.rest_api.scrap import Scrap_page, Download_data

app = Flask(__name__)
api = Api(app)

api.add_resource(Get_elements,'/elements/<url>/<prefix>')
api.add_resource(Scrap_page,'/scrap/<url>/<prefix>')
api.add_resource(Download_data,'/download')



if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')

