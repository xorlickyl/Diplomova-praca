import requests as rq

from rest_api.elements import Element


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
                        data = data.append({'tag': c.name, 'value': str(c.text).strip()}, ignore_index=True)
                    else:
                        data = data.append({'tag': c.name, 'class': c.attrs.get('class'), 'value': str(c.text).strip()},
                                           ignore_index=True)
    return data


def create_json(parent):
    ejson = Element()
    inner = []
    children = parent.findChildren()
    if (len(children) > 0):
        ejson.element = parent.name
        ejson.inner = inner
        for c in children:
            inn = create_json(c)
            inner.append(inn)
    else:
        ejson.element = parent.name
    return ejson.__dict__


def checkRobots(url_robot):
    robots = rq.get(url_robot)
    if robots.status_code == 200:
        r = str(robots.content).replace("b", "", 1).replace("'", "")
        print(r)
        rob = r.split("\\n")
        print(rob)
        disallow = []
        for n in rob:
            if n.count("Disallow") > 0:
                n = n.split(sep=" ")
                disallow.append(n[1])
    return disallow
