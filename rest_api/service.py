import json
import requests as rq
from rest_api.objekt import Element, FullData
import pandas as pd


def createData(elm, data):
    for n in elm:
        if n.name == "html":
            continue
        else:
            ch = n.findChildren()
            for c in ch:
                if c.has_attr('content') or c.has_attr('src') or c.has_attr(
                        'charset') or c.name == 'br' or c.name == 'link' or c.name == 'script' or c.text == None or c.name == 'hr':
                    continue
                else:
                    if c.attrs.get('class') == None:
                        data = data.append({'tag': c.name, 'class':"", 'value': str(c.text).strip()}, ignore_index=True)
                    else:
                        data = data.append({'tag': c.name, 'class': str(c.attrs.get('class')), 'value': str(c.text).strip()},
                                           ignore_index=True)
    return data

def create_json(parent):
    ejson = Element()
    inner = []
    children = parent.findChildren()
    if (len(children) > 0):
        ejson.element = parent.name
        if parent.attrs.get('class') == None:
            ejson.classes=""
        else:
            ejson.classes = parent.attrs.get('class')
        ejson.inner = inner
        for c in children:
            inn = create_json(c)
            inner.append(inn)
    else:
        ejson.element = parent.name
        if parent.attrs.get('class') == None:
            ejson.classes=""
        else:
            ejson.classes = parent.attrs.get('class')
    return ejson.__dict__

def checkRobots(url_robot):
    robots = rq.get(url_robot)
    disallow = []
    if robots.status_code == 200:
        r = str(robots.content).replace("b", "", 1).replace("'", "")
        rob = r.split("\\n")
        for n in rob:
            if n.count("Disallow") > 0:
                n = n.split(sep=" ")
                disallow.append(n[1])
    return disallow

def findAllUrl(tag_a,disallow,main_url):
    next_p=[]
    for a in tag_a:
        if a.attrs.get('href').find("https")>=0:
            if a.attrs.get('href').find(main_url)>=0:
                x= str(a.attrs.get('href')).replace("https","").replace("://","").replace(main_url,"")
                print(x)
                if x in disallow:
                    continue
                else:
                    next_p.append(x)
        elif a.attrs.get('href').find("http")>=0:
            if a.attrs.get('href').find(main_url)>=0:
                x= str(a.attrs.get('href')).replace("http","").replace("://","").replace(main_url,"")
                print(x)
                if x in disallow:
                    continue
                else:
                    next_p.append(x)
        else:
            if a.attrs.get('href') in disallow:
                continue
            else:
                next_p.append(a.attrs.get('href').replace("/","",1))
    return next_p

def findElement(soup):
    element_json = Element()
    inner_json = []
    elements = soup.find_all()
    for n in elements:
        if n.name == "html":
            element_json.element = n.name
            element_json.inner = inner_json
        else:
            inn = create_json(n)
            inner_json.append(inn)
    return_json = json.dumps(element_json.__dict__)
    return return_json

def dfToJson(df):
    all=""
    for index, r in df.iterrows():
        row = FullData()
        row.element=r['tag']
        if pd.isnull(r['class'])==False:
            row.classes=r['class']
        if pd.isnull(r['value'])==False:
            row.value=str(r['value']).replace('"',"'").replace("\\n"," ")
        row_json = json.dumps(row.__dict__)
        all=all+","+str(row_json)
    all=all.replace(",","",1)
    all="["+all+"]"
    return all