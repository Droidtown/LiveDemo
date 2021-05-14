#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Exchange

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

from requests import post
from requests import codes
import re

DEBUG_Exchange = True
userDefinedDICT = {}
amountPat = re.compile("^\d+(\.\d+)?$")
numPat = re.compile("[\d一二三四五六七八九十百千萬億兆]+")

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_Exchange:
        print("[Exchange] {} ===> {}".format(inputSTR, utterance))

# 文字轉換數字
def getNumber(configDICT, inputSTR):
    # 純數字直接轉換成 int
    if amountPat.search(inputSTR):
        return inputSTR, float(inputSTR)

    # 非純數字利用 Articut lv3 取得純數字
    else:
        try:
            result = post("https://api.droidtown.co/Articut/API/", json={
                "username" : configDICT["username"],
                "api_key"  : configDICT["articut_key"],
                "level"    : "lv3",
                "input_str": inputSTR
            })
            if result.status_code == codes.ok:
                result = result.json()

                # 檢查 Articut lv3 是否成功
                if result["status"]:

                    # 檢查 result["number"] 是否存在 inputSTR
                    if inputSTR in result["number"]:

                        # 抽取 Currency 的數字 (含中文)
                        numSTR = ""
                        for g in numPat.finditer(inputSTR):
                            numSTR = g.group(0)

                        textSTR = numSTR if numSTR else inputSTR
                        return textSTR, result["number"][inputSTR]

                    else:
                        print("[ERROR] getNumber() => {} Not Found!".format(inputSTR))
                else:
                    print("[ERROR] getNumber() => {}".format(result["msg"]))
            else:
                print("[ERROR] getNumber() status_code => {}".format(result.status_code))
        except Exception as e:
            print("[ERROR] getNumber() exception => {}".format(str(e)))

    return None, None

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)

    # [金額][貨幣] -> [X][貨幣]
    if utterance in [
        "[100元][美金]可以兌換[台幣]多少",
        "[100元][美金]可以兌換多少[台幣]",
        "[100元][美金]要[台幣]多少",
        "[100元][美金]要多少[台幣]"
    ]:
        textSTR, amount = getNumber(resultDICT["config"], args[0])
        if amount:
            resultDICT["result_list"].append({
                "amount": amount,
                "source": args[1],
                "target": args[2]
            })

    # [金額+貨幣] -> [X][貨幣]
    if utterance in [
        "[100台幣]換[美金]",
        "[100美金]能換多少[台幣]",
        "[100美金]要[台幣]多少",
        "[100美金]要多少[台幣]",
    ]:
        textSTR, amount = getNumber(resultDICT["config"], args[0])
        if amount:
            resultDICT["result_list"].append({
                "amount": amount,
                "source": args[0].replace(textSTR, ""),
                "target": args[1]
            })

    # [貨幣][金額] -> [X][貨幣]
    if utterance in [
        "[美金][100]要[台幣]多少",
        "[美金][100]要多少[台幣]",
        "[美金][100元]可以兌換[台幣]多少",
        "[美金][100元]可以兌換多少[台幣]",
        "[美金][100元]要[台幣]多少",
        "[美金][100元]要多少[台幣]"
    ]:
        textSTR, amount = getNumber(resultDICT["config"], args[1])
        if amount:
            resultDICT["result_list"].append({
                "amount": amount,
                "source": args[0],
                "target": args[2]
            })

    # [金額][貨幣] -> [X]台幣
    if utterance in [
        "我想買[100元][美金]",
        "我想賣[100元][美金]",
        "我想要換[100元][美金]"
    ]:
        textSTR, amount = getNumber(resultDICT["config"], args[0])
        if amount:
            resultDICT["result_list"].append({
                "amount": amount,
                "source": args[1],
                "target": "台幣"
            })

    # [貨幣][金額] -> [X]台幣
    if utterance in [
        "我想買[美金][100元]",
        "我想賣[美金][100元]",
        "我想要換[美金][100元]"
    ]:
        textSTR, amount = getNumber(resultDICT["config"], args[1])
        if amount:
            resultDICT["result_list"].append({
                "amount": amount,
                "source": args[0],
                "target": "台幣"
            })

    # [金額][貨幣] -> [X]台幣
    if utterance == "我想要換[100美金]":
        textSTR, amount = getNumber(resultDICT["config"], args[0])
        if amount:
            resultDICT["result_list"].append({
                "amount": amount,
                "source": args[0].replace(textSTR, ""),
                "target": "台幣"
            })

    # [金額][貨幣] -> [X]台幣
    if utterance == "我想要換[美金][100]":
        textSTR, amount = getNumber(resultDICT["config"], args[1])
        if amount:
            resultDICT["result_list"].append({
                "amount": amount,
                "source": args[0],
                "target": "台幣"
            })

    return resultDICT
