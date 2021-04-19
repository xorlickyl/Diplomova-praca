import requests as rq
from bs4 import BeautifulSoup
from flask import request, make_response
from flask_restful import Resource, reqparse
import pandas as pd
import json
import csv

parser = reqparse.RequestParser()

def someThing(elm,data):
    #global data
    for n in elm:
        if n.name=="html":
            continue
        else:
            ch= n.findChildren()
            for c in ch:
                if c.has_attr('content') or c.has_attr('src') or c.has_attr('charset') or c.name=='br'or c.name=='link' or c.name=='script' or c.text==None or c.name=='hr':
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
        return data.to_json(orient='records')[1:-1].replace('},{', '} {')

class Download_data(Resource):
    def post(self):
        data = request.get_data()
        if str(data).startswith("b"):
            data = str(data).replace("b","",1)
        data = str(data).replace("'","").replace("\\n","").replace("\\"," ").replace("} {","},{")
        data = data.replace("\"","'")
        data = data.replace("':'", "\":\"").replace("{'","{\"").replace("'}","\"}").replace("','","\",\"").replace("':['","\":[\"").replace("'],'","\"],\"").replace("':null,'","\":null,\"")
        print(data)
        data = "["+data+"]"
        data = json.loads(data)
        print(data)
        #df = pd.DataFrame.from_dict(data, orient="index")
        #df = pd.read_json(data.__dict__,orient='index')
        #print(df)
        #df.to_csv("data.csv", index=False)
        columns =['tag', 'class', 'value']
        df= pd.DataFrame(columns=columns)
        for i in data:
            df=df.append({'tag':i["tag"],'class':i["class"],'value':i["value"]},ignore_index=True)
        output = make_response(df.to_csv())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-Type"] = "text/csv"
        return output


