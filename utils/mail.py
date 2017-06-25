# coding:utf-8
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def send_mail(from_addr, from_pass,to_addr):
    if '@126' in from_addr:
        mail_163(from_addr, to_addr)
    elif '@gmail' in from_addr:
        mail_gmail(from_addr, to_addr)
    else:
        return 'Not support this email'


def mail_163(from_addr, from_pass, to_addr):
    # password = input('Password: ')
    password = from_pass
    smtp_server = 'smtp.126.com'

    msg = mail_content(from_addr, to_addr)
    # msg = mail_content_attach(from_addr, to_addr, ['文件.txt', 'csv.csv'])

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def mail_gmail(from_addr, from_pass,to_addr):
    # gmail需要设置安全性级别
    password = from_pass
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = mail_content_attach(from_addr, to_addr, ['文件.txt', 'csv.csv'])

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


# 邮件内容
def mail_content(from_addr, to_addr):
    msg = MIMEText('关于周末的会议', 'plain', 'utf-8')
    msg['From'] = Header('jam <%s>' % from_addr, 'utf-8')
    msg['To'] = Header('mary <%s>' % to_addr, 'utf-8')
    msg['Subject'] = Header('飞轮海', 'utf-8').encode()
    return msg


# 附件
def mail_content_attach(from_addr, to_addr, path):
    msg = MIMEMultipart()
    msg['From'] = Header('%s <%s>' % (from_addr, from_addr), 'utf-8')
    msg['To'] = Header('老师 <%s>' % to_addr, 'utf-8')
    msg['Subject'] = Header('周末计时会议', 'utf-8').encode()

    # 邮件正文内容
    msg.attach(MIMEText('关于周末会议', 'plain', 'utf-8'))

    # 构造附件，传送当前目录下的 path 文件
    for f in path:
        att = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(f)
        msg.attach(att)
    return msg

if __name__ == '__main__':
    from_addr = input('From:')
    to_addr = input('To:')
    from_pass = input('Password: ')
    send_mail(from_addr,from_pass, to_addr)
