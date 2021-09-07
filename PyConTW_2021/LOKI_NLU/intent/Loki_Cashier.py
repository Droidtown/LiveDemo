#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Cashier

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

from ArticutAPI import Articut
import json

try:
    accountDICT = json.loads(open("./account.info", encoding="utf-8").read())
except:
    accountDICT = {"username":"", "apikey":""}

articut = Articut(username=accountDICT["username"], apikey=accountDICT["apikey"])

DEBUG_Cashier = True
userDefinedDICT = {"硬幣": ["銅板"]}

class CreditCard:
    def __init__(self):
        self.balance = 87
        self.owner = "Peter"
    def callToRaiseCredit(self, amount):
        self.balance = self.balance + amount

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Cashier:
        print("[Cashier] {} ===> {}".format(inputSTR, utterance))

def coinIntConv(intLIST):
    coinIntLIST = []
    for i in range(len(intLIST))[::2]:
        for r in range(intLIST[i]):
            coinIntLIST.append(intLIST[i+1])
    return coinIntLIST

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[100元]":
        amtINT = articut.parse(args[0], level="lv3")["number"][args[0]]
        if amtINT >= 87:
            print("找您 {} 元".format(amtINT - 87))

    if utterance == "[一個][50元]硬幣[三個][10元]硬幣[一個][5元]硬幣和[兩個][1元]硬幣":
        intLIST = [articut.parse(inputSTR, level="lv3")["number"][a] for a in args]
        coinIntLIST = coinIntConv(intLIST)
        print("共收您 {} 元硬幣".format(sum(coinIntLIST)))
        print("找您 {} 元".format(sum(coinIntLIST)-87))

    if utterance == "信用卡":
        card = CreditCard()
        if card.balance >= 87:
            print("請簽名：{}".format(card.owner))
        else:
            print("先生，您的餘額不足哦！")

    if utterance == "刷卡":
        card = CreditCard()
        if card.balance >= 87:
            print("請簽名：{}".format(card.owner))
        else:
            print("先生，您的餘額不足哦！")

    return resultDICT