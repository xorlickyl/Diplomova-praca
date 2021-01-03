import requests as rq
from bs4 import BeautifulSoup
import json
from flask import request
from flask_restful import Resource
import numpy as np

class Get_elements(Resource):
    def get(self,url):
        print(url)
        url = url.replace("-","/")
        print(url)
        url = "https://"+url
        print(url)
        page = rq.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        print(soup)
        print()

        array = np.array(['html'])
        doc = soup.find_all()
        for n in doc:
            if n.name not in array:
                array=np.append(array,n.name)
        array_l= array.tolist()
        js=json.dumps(array_l)
        print(js)
        return js


