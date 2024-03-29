import json
import requests as rq
from rest_api.objekt import Element
import pandas as pd
import numpy as np
disall = ["link", "meta", "head", "script", "title", "br", "hr", "button", "picture", "svg", "use", "iframe", "header", "aside", "footer", "nav", "input", "noscript", "img"]

def createData(elm):
    data= pd.DataFrame(columns=["id","tag","class","value"])
    data=data.fillna(0)
    for n in elm:
        if n.name=="html":
            continue
        else:
            i=0
            tmp ="N"
            ch = n.findChildren()
            for c in ch:
                if c.has_attr('content') or c.has_attr('src') or c.has_attr(
                        'charset') or c.name in disall or (len(str(c.text).strip()))==0:
                    continue
                else:
                    if str(c.text).strip() not in tmp:
                        tmp = str(c.text).strip()
                        continue
                    else:
                        l=len(data)
                        data.at[l,"id"]=i
                        data.at[l,"tag"]=c.name
                        data.at[l,"value"]=tmp
                        if c.attrs.get('class') == None:
                            data.at[l,"class"]=""
                        else:
                            data.at[l,"class"]=c.attrs.get('class')
                        i=i+1

    return data

def createDataTag(elm):
    data= pd.DataFrame(columns=["id"])
    data=data.fillna(0)
    for n in elm:
        i=0
        if n.name == "html":
            continue
        else:
            tmp ="N"
            values = []
            classes =[]
            ch = n.findChildren()
            for c in ch:
                if c.has_attr('content') or c.has_attr('src') or c.has_attr(
                        'charset') or c.name in disall or (len(str(c.text).strip()))==0:
                    continue
                else:
                    if str(c.text).strip() not in tmp:
                        tmp = str(c.text).strip()
                        if values!=[] and classes!=[]:
                            l=len(data)
                            data.at[l,"id"]=i
                            for x,v in zip(classes,values):
                                if x not in data.columns:
                                    data[x]=np.nan
                                data.loc[l,x]=v
                        values=[]
                        classes=[]
                        i=i+1
                        continue
                    if c.attrs.get('class') == None:
                        string = str(c.text).strip()
                        if string in values:
                            values.append(string)
                            classes.append(" ")
                    else:
                        string = str(c.text).strip()
                        if string in values:
                            x = values.index(string)
                            classes[x]=str(c.attrs.get('class'))
                        else:
                            values.append(string)
                            classes.append(str(c.attrs.get('class')))
    return data

def create_json(parent, ins):
    js=''
    if parent.name in disall or parent.attrs.get('class') == None or str(parent.attrs.get('class')).find("nav")>0 or str(parent.attrs.get('class')).find("footer")>0 or str(parent.attrs.get('class')).find("error-message")>0  or str(parent.attrs.get('class')).find("logo")>0 \
            or str(parent.attrs.get('class')).find("sidebar")>0 or str(parent.attrs.get('class')).find("left_menu")>0 or str(parent.attrs.get('class')).find("hidden")>0 or str(parent.attrs.get('class')).find("breadcrumb")>0 or str(parent.attrs.get('class')).find("popoffer-close")>0:
        pass
    else:
        ejson = Element()
        children = parent.findChildren()
        if (len(children) > 0):
            ejson.element = parent.name
            ejson.classes = parent.attrs.get('class')
            ejson.inner = ins
            if js not in ["",None,"NULL","null",0,np.nan]:
                js= js+","+(str(ejson.__dict__))
            else:
                js= (str(ejson.__dict__))
            for c in children:
                inn = create_json(c, ins+1)
                if inn not in ["",None,"NULL","null",0,np.nan]:
                    js= js+","+(str(inn))
        else:
            ejson.element = parent.name
            ejson.classes = parent.attrs.get('class')
            ejson.inner=ins
            if js not in ["",None,"NULL","null",0,np.nan]:
                js= js+","+(str(ejson.__dict__))
            else:
                js= (str(ejson.__dict__))
        print(js)

        return js

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
    final=''
    elements = soup.find_all()
    for n in elements:
        if n.name == "html":
            element_json.element = n.name
            element_json.inner = 0
            final= (str(element_json.__dict__))
        else:
            inn = create_json(n,1)
            if inn is not None:
                final= final+","+(str(inn))
        return_json="["+final+"]"
        return_json = json.dumps(return_json)
    return return_json

def dfToJson(df):
    all=[]
    col = df.columns
    for index,r in df.iterrows():
        row ={}
        print(row)
        for c in col:
            print(c,r[c])
            if r[c] not in ["",None,"NULL","null",0,np.nan]:
                row[c]= r[c]
            else:
                row[c]=""
        all.append(row)
    all=json.dumps(all)
    return all