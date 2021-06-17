#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
from pprint import pprint

username = ""
apikey = ""

def main(inputSTR):
    articut = Articut(username=username, apikey=apikey)
    resultDICT = articut.parse(inputSTR)
    return resultDICT


if __name__ == "__main__":
    inputSTR = "本件應認原告並未於100年7月20日將系爭土地所有權借名登記在被告名下。"
    resultDICT = main(inputSTR)
    pprint(resultDICT)

    articut = Articut(username=username, apikey=apikey)
