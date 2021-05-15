#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

from requests import get
from requests import post
from requests import codes
from datetime import datetime
import rapidjson as json
import os
import re
import math
try:
    from intent import Loki_Exchange
except:
    from .intent import Loki_Exchange

BASE_PATH = os.path.dirname(__file__)
try:
    configDICT = json.load(open(os.path.join(BASE_PATH, "config.json"), encoding="utf-8"))
except:
    configDICT = {
        "username"   : "",
        "articut_key": "",
        "loki_key"   : ""
    }

LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"

# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": configDICT["username"],
                "input_list": inputLIST,
                "loki_key": configDICT["loki_key"],
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {
        "config": configDICT,
        "result_list": []
    }
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # Exchange
                if lokiRst.getIntent(index, resultIndex) == "Exchange":
                    resultDICT = Loki_Exchange.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)

# 取得匯率
def getRate(source, target):
    result = None

    rateDICT = getRateData()
    if rateDICT:
        source = currencyConverter(source)
        target = currencyConverter(target)

        # [全球即時匯率API] 是以美金爲主
        # source 是美金
        if source == "USD":
            result = rateDICT["USD{}".format(target)]["Exrate"]

        # target 是美金
        elif target == "USD":
            result = 1 / rateDICT["USD{}".format(source)]["Exrate"]

        # source / target 都不是美金，必須先轉換爲美金的匯率
        if source != "USD" and target != "USD":

            # 轉換爲 [全球即時匯率API] 匯率格式
            source = "USD{}".format(source)
            target = "USD{}".format(target)

            # 計算匯率
            if source in rateDICT and target in rateDICT:
                result = 1 / rateDICT[source]["Exrate"] * rateDICT[target]["Exrate"]

    return result


# 取得當天的匯率資料
def getRateData():
    rateDICT = None

    dateSTR = datetime.utcnow().strftime("%Y%m%d")
    filePath = os.path.join(BASE_PATH, "rate_{}.json".format(dateSTR))

    # 如果本機已有當天的匯率資料，直接讀取使用
    if os.path.exists(filePath):
        rateDICT = json.load(open(filePath, encoding="utf-8"))

    # 本機無資料時，利用 [全球即時匯率API] 取得最新匯率
    else:
        # 取得最新的匯率資料
        result = get("https://tw.rter.info/capi.php")
        if result.status_code == codes.ok:
            rateDICT = result.json()

            # 儲存匯率資料，下次就可以直接讀取
            with open(filePath, "w", encoding="utf-8") as f:
                json.dump(rateDICT, f, ensure_ascii=False)

        else:
            print("[ERROR] getRateData() status_code => {}".format(result.status_code))

    return rateDICT

# 轉換對應的貨幣代號
def currencyConverter(currency):
    # 貨幣代號表
    currencyDICT = {
        "USD": re.compile("USD|美元|美金", re.IGNORECASE),
        "EUR": re.compile("EUR|歐元", re.IGNORECASE),
        "JPY": re.compile("JPY|日元|日幣", re.IGNORECASE),
        "HKD": re.compile("HKD|港元|港幣", re.IGNORECASE),
        "GBP": re.compile("GBP|英鎊", re.IGNORECASE),
        "CHF": re.compile("CHF|瑞士法郎", re.IGNORECASE),
        "CNY": re.compile("CNY|人民幣", re.IGNORECASE),
        "KRW": re.compile("KRW|韓國圓|韓圓|韓圜|韓元|韓幣", re.IGNORECASE),
        "AUD": re.compile("AUD|澳洲元|澳元|澳幣", re.IGNORECASE),
        "NZD": re.compile("NZD|紐西蘭元|紐元|紐幣|紐紙", re.IGNORECASE),
        "SGD": re.compile("SGD|新加坡元|新加坡幣", re.IGNORECASE),
        "THB": re.compile("THB|泰銖|泰幣", re.IGNORECASE),
        "SEK": re.compile("SEK|瑞典克朗|瑞典幣", re.IGNORECASE),
        "MYR": re.compile("MYR|馬來西亞令吉|馬來西亞幣|馬來幣|馬幣|令吉", re.IGNORECASE),
        "CAD": re.compile("CAD|加拿大元|加拿大幣|加元|加幣", re.IGNORECASE),
        "VND": re.compile("VND|越南盾|越南幣|越幣", re.IGNORECASE),
        "MOP": re.compile("MOP|澳門元|澳門幣", re.IGNORECASE),
        "PHP": re.compile("PHP|菲律賓披索|菲律賓比索|菲幣", re.IGNORECASE),
        "INR": re.compile("INR|印度盧比|印度幣|盧比", re.IGNORECASE),
        "IDR": re.compile("IDR|印尼盾|印尼幣", re.IGNORECASE),
        "DKK": re.compile("DKK|丹麥克朗|丹麥幣", re.IGNORECASE),
        "ZAR": re.compile("ZAR|南非蘭特|南非幣|蘭特", re.IGNORECASE),
        "MXN": re.compile("MXN|墨西哥披索|墨西哥比索|墨西哥幣|墨幣", re.IGNORECASE),
        "TRY": re.compile("TRY|新土耳其里拉|土耳其里拉|土耳其幣|新里拉|里拉", re.IGNORECASE),
        "TWD": re.compile("TWD|NTD|新臺幣|新台幣|臺幣|台幣", re.IGNORECASE)
    }

    # 貨幣轉換爲代號
    for code in currencyDICT:
        if currencyDICT[code].search(currency):
            return code

    return None


if __name__ == "__main__":
    # Exchange
    #print("[TEST] Exchange")
    #inputLIST = ['100台幣換美金','我想要100元美金','我想要美金100元','我想買100元美金','我想買美金100元','100美金要台幣多少','100美金要多少台幣','美金100要台幣多少','美金100要多少台幣','100元美金要台幣多少','100元美金要多少台幣','100美金能換多少台幣','美金100元要台幣多少','美金100元要多少台幣','今天美金兌換台幣是多少','100元美金可以兌換台幣多少','100元美金可以兌換多少台幣','美金100元可以兌換台幣多少','美金100元可以兌換多少台幣']
    #testLoki(inputLIST, ['Exchange'])
    #print("")

    # 輸入其它句子試看看
    inputLIST = ["人民幣五十萬元可以換多少歐元"]
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Result => {}".format(resultDICT["result_list"]))

    amount = resultDICT["result_list"][0]["amount"]
    print("Amount:{}".format(amount))

    source = currencyConverter(resultDICT["result_list"][0]["source"])
    print("Source:{}".format(source))

    target = currencyConverter(resultDICT["result_list"][0]["target"])
    print("Target:{}".format(target))

    rate = getRate(source, target)
    print("Rate:{}".format(rate))

    print("Response: 要{}{}元".format(target, round(rate*amount, 2)))