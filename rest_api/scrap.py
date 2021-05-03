import requests as rq
from bs4 import BeautifulSoup
from flask import request, make_response
from flask_restful import Resource
import pandas as pd
import json
from flask import Response

from rest_api.service import createData, checkRobots, findAllUrl, dfToJson


class Scrap_page(Resource):
    def get(self,url,prefix,check):
        url = url.replace("X", "/")
        tmp = str(url).find("/")
        if tmp > 0:
            main_url = str(url)[0:tmp]
        else:
            main_url = url
        url_rob = prefix + "://" + main_url + "/robots.txt"
        disallow = checkRobots(url_rob)
        if "*" in disallow:
            return Response({"Error": "This page can't scrap"}, status=200, mimetype='application/json')
        try:
            url_1=prefix+"://"+url
            page = rq.get(url_1)
            soup = BeautifulSoup(page.content, 'html.parser')
            next_p=[]
            if check=="True":
                tag_a= soup.find_all("a")
                next_p=findAllUrl(tag_a,disallow,main_url)

            columns =['tag', 'class', 'value']
            data= pd.DataFrame(columns=columns)
            data = data.fillna(0)
            if not next_p:
                elm =soup.find_all()
                data = createData(elm, data)
                df=dfToJson(data)
                return Response(df, mimetype='application/json')
            else:
                tmp_2=str(url)[tmp:len(url)]
                tmp_2 = tmp_2.replace("/","",1)
                if tmp_2 not in next_p:
                    next_p.append(tmp_2)
                next_p.remove("#")
                for postfix in next_p:
                    page = rq.get(prefix+"://"+main_url+"/"+postfix)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    elm =soup.find_all()
                    data = createData(elm, data)
                    df= dfToJson(data)
                    return Response(df, mimetype='application/json')
        except:
            return Response({},status=400, mimetype='application/json')

class Download_data(Resource):
    def post(self):
        data = request.get_data()
        data=data.decode("utf8")
        if str(data).startswith("b"):
            data = str(data).replace("b","",1)
        data= data.replace("'","").replace("\\n"," ")
        data = json.loads(data)
        columns =['tag', 'class', 'value']
        df= pd.DataFrame(columns=columns)
        for i in data:
            df=df.append({'tag':i["element"],'class':i["classes"],'value':i["value"]},ignore_index=True)
        output = make_response(df.to_csv())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-Type"] = "text/csv"
        return output

class Scrap_from_tag(Resource):
    def post(self):
        body= request.get_data()
        if str(body).startswith("b"):
            body = str(body).replace("b","",1)
        if str(body).startswith("'"):
            body= body.replace("'","")
        js = json.loads(body)
        try:
            page = rq.get(js['url'])
            soup = BeautifulSoup(page.content, 'html.parser')
            #href = soup.find_all('a', href=True)


            columns =['tag', 'class', 'value']
            data= pd.DataFrame(columns=columns)
            data = data.fillna(0)
            elm =soup.find_all(js['tag'], {"class": js['classes']})
            data = createData(elm, data)
            df=dfToJson(data)
            return Response(df, mimetype='application/json')
        except:
            return Response({},status=400, mimetype='application/json')
