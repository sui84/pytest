# coding = utf-8
from selenium import webdriver
import time
import traceback
import os
from selenium.webdriver.common.keys import Keys
'''
drivers download : http://download.csdn.net/download/shj0605010318/9726933
http://chromedriver.storage.googleapis.com/index.html
driver.find_elements_by_css_selector('#pricing-plans .price')
'''

chromepath=r'D:\TEMP\drivers\chromedriver.exe'
iepath= r'D:\TEMP\drivers\iedriver_64.exe'
firefoxpath= r'D:\TEMP\drivers\geckodriver.exe'
imagepath=r"D:\temp\test.png"

def HandleFileName(title):
    title=title.split(' -')[0]
    title=title.replace('/',' ').replace('_',' ').replace(':',' ').replace('*',' ').replace('?',' ').replace('|',' ').replace('#','sharp')
    title=title[0:255]
    return title

def ScreenShotUrls(urls,odir):
    for url in urls:
        ScreenShotUrl(url,odir)

def ScreenShotUrl(url,opath):
    #browser = webdriver.Chrome(chromepath)
    browser = webdriver.Ie(iepath)
    browser.get(url)
    time.sleep(1)
    if os.path.isdir(opath):
        fname = HandleFileName(browser.title+".png")
        ofile = os.path.join(opath,fname)
    browser.get_screenshot_as_file(ofile)

def GetPatronInfo(url,user,patronid):
    browser = webdriver.Chrome(chromepath)
    try:
        browser.get(url)
        time.sleep(2)
        
        uname=browser.find_element_by_id('LoginControl_UserName')
        pwd=browser.find_element_by_id('LoginControl_Password')
        login=browser.find_element_by_id('LoginControl_LoginButton')
        uname.clear()
        pwd.clear()
        uname.send_keys(user.get('uname'))
        pwd.send_keys(user.get('pwd'))
        login.click()
        time.sleep(5)
        print 'login in'

        menu=browser.find_element_by_id('NavigationMenu')
        a=menu.find_element_by_xpath("//a[@href='PatronEnquiry.aspx']")
        a.click()
        time.sleep(5)
        print 'click PatronEnquiry'
        
        patron=browser.find_element_by_id('SearchPatronId')
        patron.clear()
        patron.send_keys(patronid)
        ok=browser.find_element_by_id('OKButton')
        ok.click()
        time.sleep(5)
        print 'search patron'
        #browser.get_screenshot_as_file(imagepath)
        
        
        #browser.close()
        #browser.quit()
    except Exception,e:
        print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()
        browser.close()
        browser.quit()
        print time.ctime(), 'Done!'
    
if __name__ == '__main__':
    #GetPatronInfo(url='http://localhost:50503/WebLogin.aspx',user={'uname':'231','pwd':'1234567'},patronid='5001')
    ScreenShotUrl("www.baidu.com",r"d:\temp\test.png")

