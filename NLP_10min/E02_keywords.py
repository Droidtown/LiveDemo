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
    tfidfLIST = articut.analyse.extract_tags(resultDICT)
    return tfidfLIST

def textRank(resultDICT):
    textRankLIST = articut.analyse.textrank(resultDICT)
    return textRankLIST

if __name__ == "__main__":
    inputSTR01 = "禾馨營運長林思宏今召開記者會，拿出和北市衛生局所有對話紀錄打臉柯市府，北市衛生局長黃世傑怒嗆，「講難聽一點，根本得寸進尺」，黃世傑說，「委員一直在要東西嘛！」「感覺這個過程一直在要」，戴錫欽追問，說誰得寸進尺？黃世傑說，我沒有跟小禾馨聯繫，感覺上是高嘉瑜（得寸進尺），一開始說醫護人員，後來要要求房務人員、清潔人員。"
    inputSTR02 = "高嘉瑜說，她基於保護醫護、孕婦、新生兒的立場轉達訴求，相信北市衛生局也是，因此快速允諾協助，也很感謝衛生局長黃世傑及辛苦的衛生局同仁們協助。過程中，禾馨也多次表達4家診所共1000多名員工，都是符合1～3類的施打名單，希望能有足夠的疫苗給予孕婦最完善的保護，包括醫護及診所的工作人員，她幾次如實將訴求轉達給北市衛生局，都得到快速且善意的回應。"
    inputSTR03 = "晚餐的沙拉部分為煙燻鮭魚與漬蘿蔔沙拉佐香橙醬汁，主餐則是能吃到鮮蝦、螃蟹的海鮮風味茄汁奶油風味義大利麵，還可以搭配香烤麵包，十分有飽足感。甜點則是香草莓果慕斯搭配造型薄片巧克力，優雅酸甜的口感就如牧羊女帶給大家的印象。（特別套餐2,480日幣）"
    resultDICT = main(inputSTR03)
    #pprint(resultDICT)

    tf_idf = tfidf(resultDICT)
    pprint(tf_idf)

    text_rank = textRank(resultDICT)
    pprint(text_rank)