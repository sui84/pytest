#encoding=utf-8
import pandas as pd

if __name__ == '__main__':
    data=[{"year":2017,"month":8,"day":1,"name":"爬山，徒步","title":"test1"},{"year":2017,"month":9,"day":1,"name":"长线远游雾漫小东江","title":"test2"},{"year":2017,"month":10,"day":1,"name":"爬山，徒步","title":"test3"}]
    df=pd.DataFrame(data)
    df.loc[0:5,["title"]]
    df[df.title.str.contains('test1')]

    #将列表转成df
    lines=["aaa","nnn"]
    df=pd.DataFrame({"line":lines})

    #将df转成列表
    result=df[df.line.str.contains("youyicun22@")]
    result.line.tolist()

    #查询多个条件
    result=df[df.line.str.contains("youyicun22@") | df.line.str.contains("onyourmark5181")]
    result = df.query('line.str.contains("youyicun22@") | line.str.contains("onyourmark5181")')

    #去重
    result = df.query('line.str.contains("youyicun22@") | line.str.contains("onyourmark5181")').drop_duplicates()
