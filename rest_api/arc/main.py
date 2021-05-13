from flask import Blueprint
from flask_restful import Api
from elements import Get_elements
from scrap import Scrap_from_tag, Scrap_page, Download_data

app_bl = Blueprint('api',__name__)
api = Api(app_bl)

api.add_resource(Get_elements,'/elements/<url>/<prefix>/<check>')
api.add_resource(Scrap_from_tag,'/scrap/tag')
api.add_resource(Scrap_page,'/scrap/<url>/<prefix>/<check>')
api.add_resource(Download_data,'/download')

