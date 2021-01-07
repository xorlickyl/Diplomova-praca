import requests as rq
from bs4 import BeautifulSoup
#import json
from flask import request, jsonify
from flask_restful import Resource
import numpy as np

class Get_elements(Resource):
    def get(self,url):
        url = url.replace("-","/")
        url = "https://"+url
        page = rq.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        #array = np.array(['html'])
        x=[]
        doc = soup.find_all()
        for n in doc:
            #if n.name not in array:
                #array=np.append(array,n.name)
            x.append({"element":n.name})
        print(len(x))
        js=jsonify(x)
        print(js)
        return js