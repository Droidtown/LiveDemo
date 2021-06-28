#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
from pprint import pprint
from requests import post

username = ""
apikey = ""
articut = Articut(username=username, apikey=apikey)



def main(inputSTR):
    resultDICT = articut.parse(inputSTR)
    return resultDICT



if __name__ == "__main__":
    inputSTR = inputSTR = """位於台南的50年老房子，
              地址是台南市東區長榮路3段30巷3號。
              這裡承載著曾經是學生宿舍的使命。
              我們繼續把這樣的溫度傳遞，
              讓往來的人都把這裡當做家，
              用緩慢的步調體驗台南的在地生活。""".replace(" ", "").replace("\n", "")
    resultDICT = main(inputSTR)

    #pprint(resultDICT)

    #取得完整地址
    addTWLIST = articut.getAddTWLIST(resultDICT)
    #pprint(addTWLIST)

    addSTR = [a for a in addTWLIST if a!=[]][0][0][2]
    #pprint(addSTR)


    #套用 SPACE (Doc:https://api.droidtown.co/document/#Space)
    url = "https://api.droidtown.co/Space/API/"
    payload = {
        "username": "",
        "api_key": "",
        "type": "geocoding",
        "site": addSTR
    }

    response = post(url, json=payload)
    jsonResults = response.json()
    #pprint(jsonResults)
    mapDICT = {"lat": jsonResults["results"][0]["lat"], "lng":jsonResults["results"][0]["lng"]}
    mapSTR = "https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=16/{lat}/{lng}".format(**mapDICT)
    #print(mapSTR)

    #取得地址分段 (localRE)
    resultDICT = articut.parse("桃園市○○區○○路000巷0號")
    city = articut.localRE.getAddressCity(resultDICT)
    print(city)