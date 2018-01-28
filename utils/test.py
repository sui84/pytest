#coding=utf-8
import time
import traceback
import sys

if __name__ == '__main__':
    print time.ctime(), 'Start...'
    try:
        if len(sys.argv) > 1:
            print sys.argv[1]
    except Exception,e:
        print time.ctime(), 'Error:',e.message,'\n',traceback.format_exc()


import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui

class GetCookie(object):
    def getCookie(self, account, password):
        """ 根据QQ号和密码获取cookie """
        failure = 0
        while failure < 2:
            try:
                browser = webdriver.PhantomJS()
                wait = ui.WebDriverWait(browser, 10)
                browser.get('http://qzone.qq.com/?s_url=http://user.qzone.qq.com/1813710279/')
                browser.switch_to_frame('login_frame')
                wait.until(lambda browser: browser.find_element_by_id('switcher_plogin'))
                plogin = browser.find_element_by_id('switcher_plogin')
                plogin.click()
                wait.until(lambda browser: browser.find_element_by_id('u'))
                u = browser.find_element_by_id('u')
                u.send_keys('%s' % (account))
                p = browser.find_element_by_id('p')
                p.send_keys('%s' % (password))
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="login_button"]'))
                login = browser.find_element_by_xpath('//*[@id="login_button"]')
                time.sleep(2)
                login.click()
                time.sleep(1)
                try:
                    browser.switch_to_frame('vcode')
                    print 'Failed!----------------reason:该QQ首次登录Web空间，需要输入验证码！'
                    break
                except Exception:
                    pass
                try:
                    err = browser.find_element_by_id('err_m')
                    time.sleep(2)
                    d = err.text
                    print account, d
                    if u'您输入的帐号或密码不正确' in d:
                        print 'Failed!----------------reason:账号或者密码错误！'
                        break
                    if u'网络繁忙' in d:
                        time.sleep(2)
                except Exception, e:
                    # wait.until(lambda browser: browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/b/b/textarea'))
                    # msg_b = browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/b/b/textarea')
                    # msg_b.send_keys(u'Glory Be to Jehovah')
                    # wait.until(lambda browser: browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]/a'))
                    # btn = browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]/a')
                    # btn.click()
                    cookie = {}
                    for ck in browser.get_cookies():
                        cookie[ck['name']] = ck['value']
                    browser.quit()
                    print "Get the cookie of QQ:%s successfully!(共%d个键值对)" % (account, len(cookie))
                    return cookie
            except Exception:
                failure = failure + 1
            except KeyboardInterrupt, e:
                raise e

GetCookie().getCookie('1250577179','baguawuliao')
