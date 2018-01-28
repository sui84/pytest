#encoding=utf-8
# from jpype import *


jvmpath=r"E:\01_SOFT\Java\jdk1.8.0_60\jre\bin\server\jvm.dll"
jarpath=r'D:\TEMP\java\test.jar'


def CallBase():
    startJVM(jvmpath,"-ea")
    java.lang.System.out.println("Hello World")
    #shutdownJVM()

def CallHanlp():
    import jpype
    jarpath=r"D:\TEMP\java\hanlp-portable-1.2.8.jar"
    jvmArg = "-Djava.class.path=%s" % jarpath
    jpype.startJVM(jvmpath,jvmArg)
    HanLP = jpype.JClass('com.hankcs.hanlp.HanLP')
    print(HanLP.segment(u'你好，欢迎在Python中调用HanLP的API'))
    #Tedt=JPackage('com').Test

if __name__ == '__main__':
    CallHanlp()
