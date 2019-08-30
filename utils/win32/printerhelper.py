#encoding=utf-8
from win32print import *
import sys
import time
import traceback

PRINTER_DEFAULTS = {"DesiredAccess":PRINTER_ALL_ACCESS}

def ChangePrinters(ifile):
    with open(ifile,'r') as f:
        lines = f.readlines()
    for line in lines:
        try:
            print line
            strs = line.split(',')
            if len(strs) > 1:
                printerName = strs[0]
                location = strs[1] 
                handle=OpenPrinter(printerName, PRINTER_DEFAULTS)
                info = GetPrinter(handle, 2)
                info["pLocation"] = location
                info["pDriverName"] = "EPSON TM-T88IV ReceiptE4"
                SetPrinter(handle,2,info,0)
        except Exception,e:
            print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()

def GetPrinters(ofile):
    #for i in range(1,5):
    i = 2
    printers = EnumPrinters(i)
    print "Printer ",i," Count : ",len(printers)
    with open(ofile,'a') as f:    
        f.write('EnumPrinters'+str(i)+':'+str(len(printers))+"\n")
        for prt in printers:
            handle=OpenPrinter(prt[2])
            info = GetPrinter(handle, 2)
            line =  info["pPrinterName"]+','
            if info["pLocation"] <> None: 
                line += info["pLocation"].strip()
            line += ","+info["pDriverName"]
            line += "\n"
            print line
            f.write(line)


if __name__ == '__main__':
    try:
        fname=r"c:\\temp\\printers.csv"
        #print sys.argv,len(sys.argv)
        if len(sys.argv) > 2:
            fname = sys.argv[2]
        if len(sys.argv) > 1 and sys.argv[1]=="get":
            print 'Start Get Printer Location:'
            GetPrinters(fname)
        if len(sys.argv) > 1 and sys.argv[1]=="set":
            print 'Start Set Printer Location:'
            ChangePrinters(fname)
        print 'End.'
    except Exception,e:
        print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()
