import json
import requests as rq
from bs4 import BeautifulSoup
from flask import Response
from flask_restful import Resource

from rest_api.service import checkRobots, create_json


class Element():
    element=""
    inner=[]

class Get_elements(Resource):
    def get(self,url, prefix):
        url= url.replace("X","/")
        tmp = str(url).find("/")
        if tmp>0:
            url_rob = str(url)[0:tmp]
        else:
            url_rob=url
        url_rob=prefix + "://"+url_rob+"/robots.txt"
        url = prefix+"://"+url
        disallow = checkRobots(url_rob)

        try:
            page = rq.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            element_json=Element()
            inner_json=[]
            elements = soup.find_all()
            for n in elements:
                if n.name=="html":
                    element_json.element=n.name
                    element_json.inner=inner_json
                else:
                    inn=create_json(n)
                    inner_json.append(inn)
            return_json = json.dumps(element_json.__dict__)
            return Response(return_json, mimetype='application/json')
        except:
            return Response({},status=400, mimetype='application/json')