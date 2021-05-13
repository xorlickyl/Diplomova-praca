import json
import requests as rq
from bs4 import BeautifulSoup
from flask import Response
from flask_restful import Resource


from service import checkRobots, create_json, findAllUrl, findElement

class Get_elements(Resource):
    def get(self, url, prefix,check):
        url = url.replace("X", "/")
        if str(url).find("YZ")>0:
            url = url.replace("YZ","?")
        if str(url).find("KO")>0:
            url = url.replace("KO","#")
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
            url_1 = prefix + "://" + url
            print(url_1)
            page = rq.get(url_1)
            soup = BeautifulSoup(page.content, 'html.parser')
            next_p=[]
            if check=="True":
                tag_a= soup.find_all("a")
                next_p=findAllUrl(tag_a,disallow,main_url)
            if next_p==[]:
                return_json = findElement(soup)
                #return_json=return_json.replace('inner":[','inner":{').replace(']},','}},')
                return Response(return_json, mimetype='application/json')
            else:
                tmp_2=str(url)[tmp:len(url)]
                tmp_2 = tmp_2.replace("/","",1)
                if tmp_2 not in next_p:
                    next_p.append(tmp_2)
                ret=""
                next_p.remove("#")
                for postfix in next_p:
                    page = rq.get(prefix+"://"+main_url+"/"+postfix)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    return_json = findElement(soup)
                    ret = ret+","+str(return_json)
                ret = ret.replace(",","",1)
                ret="["+ret+"]"

                return Response(ret, mimetype='application/json')
        except:
            return Response({}, status=400, mimetype='application/json')
