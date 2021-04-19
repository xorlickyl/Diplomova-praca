import json
import requests as rq
from bs4 import BeautifulSoup
from flask import Response
from flask_restful import Resource

class Element():
    element=""
    inner=[]

def create_json(parent):
    ejson=Element()
    inner=[]
    children=parent.findChildren()
    if(len(children)>0):
        ejson.element=parent.name
        ejson.inner=inner
        for c in children:
            inn=create_json(c)
            inner.append(inn)
    else:
        ejson.element=parent.name
    return ejson.__dict__


class Get_elements(Resource):
    def get(self,url, prefix):
        url = url.replace("-","/")
        url = prefix+"://"+url
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