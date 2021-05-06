"""
from flask import Flask, request
from flask_restful import Api

from rest_api.elements import Get_elements
from rest_api.scrap import Scrap_from_tag, Scrap_page, Download_data

app = Flask(__name__)
api = Api(app)

api.add_resource(Get_elements,'/elements/<url>/<prefix>/<check>')
api.add_resource(Scrap_from_tag,'/scrap/tag')
api.add_resource(Scrap_page,'/scrap/<url>/<prefix>/<check>')
api.add_resource(Download_data,'/download')



if __name__ == '__main__':
    #app.run(debug=True,host='147.175.106.115:7799')
    app.run(debug=True,host='127.0.0.1')
"""
from flask import Blueprint
from flask_restful import Api
from rest_api.elements import Get_elements
from rest_api.scrap import Scrap_from_tag, Scrap_page, Download_data

app_bl = Blueprint('api',__name__)
api = Api(app_bl)

api.add_resource(Get_elements,'/elements/<url>/<prefix>/<check>')
api.add_resource(Scrap_from_tag,'/scrap/tag')
api.add_resource(Scrap_page,'/scrap/<url>/<prefix>/<check>')
api.add_resource(Download_data,'/download')

