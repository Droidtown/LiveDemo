#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
from pprint import pprint

username = ""
apikey = ""
articut = Articut(username=username, apikey=apikey)



def main(inputSTR):
    resultDICT = articut.parse(inputSTR)
    return resultDICT

def tfidf(resultDICT):
    keywordLIST = articut.analyse.extractTags(resultDICT, topK=3)
    return keywordLIST

if __name__ == "__main__":
    inputSTR = "新冠肺炎本土疫情嚴峻，中央流行疫情指揮中心宣布引進居家快篩試劑，以廣篩找出隱藏在社區中的感染個案。繼2款居家快篩產品獲准專案進口，食藥署今天宣布核准首款國產居家快篩試劑的專案製造，此產品為抗原快篩試劑，與PCR檢驗的陽性一致率達94%，待完成前置作業後即可開賣。"
    resultDICT = main(inputSTR)
    #pprint(resultDICT)


    pprint(tfidf(resultDICT))
