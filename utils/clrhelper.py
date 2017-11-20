#encoding=utf-8
import clr

def Test():
        clr.AddReference(r'd:\temp\test.dll')
        import testns
        test=testns.testclass()
        str=test.testfunc('test')        
        
if __name__ == '__main__':
    pass
