from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
import base64
import json
app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def handle_request():
  try:
      url=str(request.args.get("url"))
      if(url!='' && base64.b64encode(base64.b64decode(s)) == url):
          decodedurl=base64.b64decode(url)
        response = requests.get(decodedurl)
        doc=BeautifulSoup(response.content,"html.parser")
        JsonString=[] 
        mydivs = doc.find_all("div", {"class": "views-row"})
        for item in mydivs:
            previewVideo=str(item.find("article").find_all("div")[0].find("div").find("a").find("video")['src'])
            JsonString.append({
              "title": str(item.find("article").find("div",attrs= {'class':'movement-title'}).find("a").find("span").text),
              "preview_video":"https://mocap.market"+previewVideo,
              "download_link":"https://mocap.market"+"/download/"+previewVideo.split("/sites/default/files/")[1].split(".fbx")[0]+".fbx"
           })
            lastindex=doc.find('li',attrs={'class':'pager__item--last'}).find('a')['href'].replace('?page=','')
          return json.dumps({'AllAnimations':JsonString, 'tabscount':lastindex})
      else:
        return 'no data available'
  except Exception:
        return 'no data available'
if __name__ == '__main__':
    app.run()
