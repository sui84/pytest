#encoding=utf-8



class GZHelper(object):
    def __init__(self):
        self.nontaxincome = 0.25
        self.proftaxdeduction = 0.30
        self.taxtable = []
        #montyly
        self.taxtable.append({"paytype":"m","from":0.00,"to":12000.00,"taxpercentage":0,"taxamount":0,"accumulatedtaxamt":0})
        self.taxtable.append({"paytype":"m","from":12000.01,"to":13666.67,"taxpercentage":0.07,"taxamount":117,"accumulatedtaxamt":117})
        self.taxtable.append({"paytype":"m","from":13666.68,"to":15333.33,"taxpercentage":0.08,"taxamount":133,"accumulatedtaxamt":250})
        self.taxtable.append({"paytype":"m","from":15333.34,"to":18666.67,"taxpercentage":0.09,"taxamount":300,"accumulatedtaxamt":550})
        self.taxtable.append({"paytype":"m","from":18666.68,"to":25333.33,"taxpercentage":0.10,"taxamount":667,"accumulatedtaxamt":1217})
        self.taxtable.append({"paytype":"m","from":25333.34,"to":35333.33,"taxpercentage":0.11,"taxamount":1100,"accumulatedtaxamt":2317})
        self.taxtable.append({"paytype":"m","from":35333.34,"to":99999999.99,"taxpercentage":0.12,"taxamount":11995760,"accumulatedtaxamt":11998077 })
        
        #yearly
        self.taxtable.append({"paytype":"y","from":0.00,"to":144000.00,"taxpercentage":0,"taxamount":0,"accumulatedtaxamt":0})
        self.taxtable.append({"paytype":"y","from":144000.01,"to":164000.00,"taxpercentage":0.07,"taxamount":1400,"accumulatedtaxamt":1400})
        self.taxtable.append({"paytype":"y","from":164000.01,"to":184000.00,"taxpercentage":0.08,"taxamount":1600,"accumulatedtaxamt":3000})
        self.taxtable.append({"paytype":"y","from":184000.01,"to":224000.00,"taxpercentage":0.09,"taxamount":3600,"accumulatedtaxamt":6600})
        self.taxtable.append({"paytype":"y","from":224000.01,"to":304000.00,"taxpercentage":0.10,"taxamount":8000,"accumulatedtaxamt":14600})
        self.taxtable.append({"paytype":"y","from":304000.01,"to":424000.00,"taxpercentage":0.11,"taxamount":13200,"accumulatedtaxamt":27800})
        self.taxtable.append({"paytype":"y","from":424000.01,"to":99999999.99,"taxpercentage":0.12,"taxamount":11949120,"accumulatedtaxamt":11976920 })
        

    def GetProfTax(self , wageamt = 267419.54 , paytype="m"):
        nontaxincome = wageamt * self.nontaxincome
        print "nontaxincome : ",nontaxincome
        nettaxincome = wageamt - nontaxincome
        print "nettaxincome : ",nettaxincome
        rfntaximcoe = wageamt * (5.00/100) * ( 1- (self.nontaxincome/100)) * (1-(self.proftaxdeduction/100))
        print "rfntaximcoe : ",rfntaximcoe
        
        f = lambda x:x["paytype"]==paytype
        newtaxtable = filter(f,self.taxtable)
        taxamt = 0
        for i in range(0,len(newtaxtable)):
            if nettaxincome >= newtaxtable[i]["from"] and nettaxincome <= newtaxtable[i]["to"]:
                diff = nettaxincome - newtaxtable[i]["from"]
                print "level : " newtaxtable[i]["from"],"~",newtaxtable[i]["to"]
                lastleveltaxamt = newtaxtable[i]["accumulatedtaxamt"]-newtaxtable[i]["taxamount"]
                taxamt = (lastleveltaxamt+diff*newtaxtable[i]["taxpercentage"])*(1-self.proftaxdeduction)
                break
        return taxamt


