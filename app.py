from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
import base64
import json
app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def handle_request():
  #try:
      url=str(request.args.get("url"))
      if(url!=''):
        decodedurl=base64.b64decode(url)
        response = requests.get(decodedurl)
        doc=BeautifulSoup(response.content,"html.parser")
        JsonString=[]
        mydivs=[]
        alltags=[]
        if doc.find_all("div", {"class": "views-row"}) is not None:
          mydivs = doc.find_all("div", {"class": "views-row"})
        for item in mydivs:
            previewVideo=str(item.find("article").find_all("div")[0].find("div").find("a").find("video")['src'])
            JsonString.append({
              "title": str(item.find("article").find("div",attrs= {'class':'movement-title'}).find("a").find("span").text),
              "preview_video":"https://mocap.market"+previewVideo,
              "download_link":"https://mocap.market"+"/download/"+previewVideo.split("/sites/default/files/")[1].split(".fbx")[0]+".fbx"
            })
        lastindex='0'
        if doc.find('li',attrs={'class':'pager__item--last'}) is not None:
          lastindex=doc.find('li',attrs={'class':'pager__item--last'}).find('a')['href'].replace('?page=','')
        tags=doc.find_all("span", {"class": "facet-item__count"})
        for tag in tags:
          tag_name=tag.parent.children[0].text
          tag_count=tag.parent.children[1].text
          alltags.append({
            'tagName':str(tag_name),
            'tagCount': str(tag_count)
          })
        return json.dumps({'AllAnimations':JsonString, 'tabscount':lastindex, 'alltags':alltags})
      else:
        return 'no data available'
  #except Exception as e:
   #     return 'exeption, no data available'+str(e)
if __name__ == '__main__':
    app.run()
