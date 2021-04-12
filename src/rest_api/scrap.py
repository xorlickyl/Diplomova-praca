import requests as rq
from bs4 import BeautifulSoup
from flask import request
from flask_restful import Resource, reqparse
import pandas as pd

parser = reqparse.RequestParser()

def someThing(elm,data):
    #global data
    for n in elm:
        if n.name=="html":
            continue
        else:
            ch= n.findChildren()
            for c in ch:
                if c.has_attr('content') or c.has_attr('src') or c.has_attr('charset') or c.name=='br'or c.name=='link' or c.name=='script' or c.text==None:
                    continue
                else:
                    if c.attrs.get('class') == None:
                        data=data.append({'tag':c.name, 'value':str(c.text).strip()},ignore_index=True)
                    else:
                        data=data.append({'tag':c.name, 'class':c.attrs.get('class'), 'value':str(c.text).strip()},ignore_index=True)
    return data

class Scrap_page(Resource):
    def get(self,url):
        url = url.replace("-","/")
        url = "https://"+url
        page = rq.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        columns =['tag', 'class', 'value']
        data= pd.DataFrame(columns=columns)
        data = data.fillna(0)
        elm =soup.find_all()
        data = someThing(elm, data)
        print(data)
        return data.to_json(orient='records')[1:-1].replace('},{', '} {')

class Download_data(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        data = request.get_json(force=True)
        print(data)
        df = pd.read_json(data,orient='records')
        df.to_csv("data.csv", index=False)
        return df


