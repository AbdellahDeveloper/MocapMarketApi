from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup
import base64
import json
app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def handle_request():
    url=base64.b64decode(str(request.args.get("url")))
    response = requests.get(url)
    doc=BeautifulSoup(response,"html.parser")
    JsonString=[] 
    mydivs = doc.find_all("div", {"class": "views-row"})
    for item in mydivs:
        previewVideo=str(item.find("article").find_all("div")[0].find("div").find("a").find("video")['src'])
        JsonString.append({
          "title": item.find("article").find_all("div")[1].find("a").find("span").string,
          "preview_video":"https://mocap.market"+previewVideo,
          "download_link":"/download/"+previewVideo.split("/sites/default/files/")[1].split(".fbx")[0]+".fbx"
        })
    return json.dumps(JsonString)

if __name__ == '__main__':
    app.run()
