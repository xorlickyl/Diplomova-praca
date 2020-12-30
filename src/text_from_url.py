from __future__ import print_function
# import time
#from flask import Flask
import sys
import requests
from bs4 import BeautifulSoup

#app= Flask(__name__)

#@app.route("/")
#def getText(url):
   # URL = 'https://android.mpage.sk/index.php'
url = sys.argv[1]
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
print()

array = ['html',]
doc= soup.find_all()
for n in doc:
    if n.name not in array:
        array.append(n.name)
print(array)
sys.stdout.flush(array)

#if __name__ == '__main__':
    #print("hello")
    #app.run(host="127.0.0.1", port=5000)