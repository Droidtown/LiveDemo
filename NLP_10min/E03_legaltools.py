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

def crime(resultDICT):
    crimeLIST = articut.LawsToolkit.getCrime(resultDICT)
    return crimeLIST

def penalty(resultDICT):
    penaltyLIST = articut.LawsToolkit.getPenalty(resultDICT)
    return penaltyLIST

def article(resultDICT):
    articleLIST = articut.LawsToolkit.getLawArticle(resultDICT)
    return articleLIST


if __name__ == "__main__":
    inputSTR = "楊進勝犯血液中酒精濃度達百分之零點零五以上而駕駛動力交通工具罪，處有期徒刑參月，如易科罰金，以新臺幣臺仟元折算壹日。被告楊進勝所為，系犯刑法第185 條之3 第1項第1 款之血液中酒精濃度達百分之0.05以上而駕駛動力交通工具罪。"
    resultDICT = main(inputSTR)

    #basic.py
    #pprint(resultDICT)

    #keywords.py
    #pprint(tfidf(resultDICT))

    #legaltools.py
    pprint(crime(resultDICT))
    pprint(penalty(resultDICT))
    pprint(article(resultDICT))
