jenkins
D:\02_Software\Java\jre7\bin\java -jar D:\02_Software\Java\jenkins.war --httpPort=8080

winservice
sc create jenkins binpath= "E:\MyProjects\Github\pytest\pytest\bat\jenkins.bat" displayname= "jenkins" depend= Tcpip start= auto

start failed
sc create "Jenkins" binPath= "cmd.exe /c start D:\02_Software\Java\jre7\bin\java -jar D:\02_Software\Java\jenkins.war --httpPort=8080" start= auto


#Http:
python -m SimpleHTTPServer 8000
#FTP:
python -m pyftpdlib -p 21

logparser -i:CSV -iHeaderFile:"D:\TEMP\nginx.header" -headerRow:OFF -o:SQL  "SELECT * into Nginx from D:\TEMP\test.txt" -server:localhost\SQLEXPRESS -database:log -driver:"SQL Server" -username:sa -password:P@ssw0rd -createTable:ON
