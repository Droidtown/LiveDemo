#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class CreditCard:
    def __init__(self):
        self.balance = 50
        self.owner = ""
    def callToRaiseCredit(self, amount):
        self.balance = self.balance + amount

def payment_processor(payment):
    match payment:
        case "100元":   # 1. Type? 2. Type Methods? 3. Length?  4. Element Type? ... and more
            print("找您 13 元！")
            quit()
        case [50, 10, 10, 10, 5, 1, 1]:
            print("收您 {} 元".format(sum(payment)))
            quit()
        case CreditCard:
            print("好的，收您信用卡！請稍待…")
            if payment.balance >= 87:
                print("請簽名：{}".format(payment.owner))
            else:
                print("先生，您的餘額不足哦！")
            quit()
        
def cashier():
    while True:
        payMethod = input("總共 87 元，您打算用什麼樣的貨幣組合來付呢？")
        
        if payMethod in ("信用卡", "刷卡"):
            payMethod = CreditCard()
            payMethod.owner = "Peter"
            payMethod.callToRaiseCredit(30)
        elif isinstance(payMethod, str) and "," in payMethod:
            payMethod = [int(v) for v in payMethod.split(",")]
            
        payment_processor(payMethod)


if __name__ == "__main__":
    cashier()