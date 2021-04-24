import requests as rq
from bs4 import BeautifulSoup
from flask import request, make_response
from flask_restful import Resource, reqparse
import pandas as pd
import json
from flask import Response

from rest_api.service import createData, checkRobots


class Scrap_page(Resource):
    def get(self,url,prefix):
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
            columns =['tag', 'class', 'value']
            data= pd.DataFrame(columns=columns)
            data = data.fillna(0)
            elm =soup.find_all()
            data = createData(elm, data)
            return data.to_json(orient='records')[1:-1].replace('},{', '} {')
        except:
            return Response("Error", mimetype='application/json')

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
        columns =['tag', 'class', 'value']
        df= pd.DataFrame(columns=columns)
        for i in data:
            df=df.append({'tag':i["tag"],'class':i["class"],'value':i["value"]},ignore_index=True)
        output = make_response(df.to_csv())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-Type"] = "text/csv"
        return output


