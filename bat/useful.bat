jenkins
D:\02_Software\Java\jre7\bin\java -jar D:\02_Software\Java\jenkins.war --httpPort=8080

winservice
sc create jenkins binpath= "E:\MyProjects\Github\pytest\pytest\bat\jenkins.bat" displayname= "jenkins" depend= Tcpip start= auto

nssm install NodeJS “\node.exe” “\server.js” net start NodeJS

nssm install NodeJS（安装后的服务名称） “(node.exe安装的地址)\node.exe” “（要启动的JS文件）\server.js” net start NodeJS（安装后的服务名称）

start failed
sc create "Jenkins" binPath= "cmd.exe /c start D:\02_Software\Java\jre7\bin\java -jar D:\02_Software\Java\jenkins.war --httpPort=8080" start= auto


#Http:
python -m SimpleHTTPServer 8000
#FTP:
python -m pyftpdlib -p 21

logparser -i:CSV -iHeaderFile:"D:\TEMP\nginx.header" -headerRow:OFF -o:SQL  "SELECT * into Nginx from D:\TEMP\test.txt" -server:localhost\SQLEXPRESS -database:log -driver:"SQL Server" -username:sa -password:"" -createTable:ON
