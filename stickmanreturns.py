from crypt import methods
import json
from PIL import Image
import base64
from io import BytesIO
from flask import Flask, jsonify, request
import random
import utilityFunc
import glob

app = Flask(__name__)

@app.route("/api/imageFunc/number-generator", methods=['GET'])
def randy():
    baseFolder = "layers/StickMan/"
    folderMap = {}
    nftNumberArray = []
    nftNameBase = "StickMan"
    folderList = ["body", "legs", "shoes", "pants","cape", "arms", "shirt", "head", "mouth", "eyes"]
    count = 0
    for folder in folderList:
        if folder == "cape" or folder == "arms":
            position = random.randrange(0, 100)
            folderMap[folder] = position
            nftNumberArray.insert(count, position)
            count += 1
        else:
            generalFolder = baseFolder
            specificFolder = folder
            fileFinder = generalFolder + specificFolder + "/*.PNG"
            files = glob.glob(fileFinder, recursive=True)
            folderLength = len(files)
            position = random.randrange(0, folderLength)
            folderMap[folder] = position
            nftNumberArray.insert(count, position)
        count += 1
    
    nftNumber = utilityFunc.numJoin(nftNumberArray)
    nftName = nftNameBase + "-" + nftNumber

    data = {
        "nftName": nftName,
        "nftPositionArray": nftNumberArray,
        "folderMap": folderMap,
        "nftNumber": nftNumber
    }

    return jsonify(data), 200

@app.route("/api/imageFunc/image-generator", methods=['POST'])
def stickman():

    baseFolder = "layers/StickMan/"
    folderList = ["body", "legs", "shoes", "pants","cape", "arms", "shirt", "head", "mouth", "eyes"]
    reqData = request.json
    folderMap = reqData["folderMap"]

    baseFile = baseFolder + "base/" + str(0) + ".PNG"
    imgBody = Image.open(baseFile).convert("RGBA")

    for layer in folderList:
        if layer == "cape":
            print(folderMap[layer])
            if folderMap[layer] != 13:
                pass
            else:
                layerFile = baseFolder + layer + "/" + str(0) +".PNG"
                imgLayer = Image.open(layerFile).convert("RGBA")
                imgBody.paste(imgLayer, (0,0), mask = imgLayer)
        elif layer == "arms":
            print(folderMap[layer])
            if folderMap[layer] != 13:
                layerFile = baseFolder + layer + "/" + str(1) +".PNG"
                imgLayer = Image.open(layerFile).convert("RGBA")
                imgBody.paste(imgLayer, (0,0), mask = imgLayer)
            else:
                layerFile = baseFolder + layer + "/" + str(0) +".PNG"
                imgLayer = Image.open(layerFile).convert("RGBA")
                imgBody.paste(imgLayer, (0,0), mask = imgLayer)
        else:
            layerFile = baseFolder + layer + "/" + str(folderMap[layer]) +".PNG"
            
            imgLayer = Image.open(layerFile).convert("RGBA")
            
            # Pasting
            imgBody.paste(imgLayer, (0,0), mask = imgLayer)

    #imgBody.show()

    buffered = BytesIO()
    imgBody.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    #print(img_str)

    data = img_str
    return data, 200

app.run(host='0.0.0.0', port=8181)
  
