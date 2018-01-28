import jaydebeapi

'''
conn = jaydebeapi.connect('com.microsoft.sqlserver.jdbc.SQLServerDriver',
    [Server , Username,Password])

conn=jaydebeapi.connect('com.mysql.jdbc.Driver',['jdbc:mysql://localhost:3306/test','hive','hive']
                        ,'/data/users/huser/lan/codes/useJPype/mysql-connector-java-5.1.36/mysql-connector-java-5.1.36-bin.jar')

# 其中mysql的用户名和密码都是hive,最后一个参数是驱动的jar包curs=conn.cursor()curs.execute('create table CUSTOMER("ID" INTEGER not null primary key,"NAME" varchar not null)')curs.execute("insert into CUSTOMER values(1,'John')")curs.execute("select * from CUSTOMER")curs.fetchall()[(1,u'John')]
'''
