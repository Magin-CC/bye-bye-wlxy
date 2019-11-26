from selenium import webdriver, common
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import os
import time
import random
import sys
import math


class Wlxy:
    def __del__(self):
        self.browser.quit()
        self.b2.quit()

    def __init__(self, username, pwd):
        self.startUrl = 'https://wlxy.8531.cn/learner/login'
        self.score = 0
        self.username = username
        self.pwd = pwd
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        # option.add_experimental_option(
        #     "prefs", {"profile.managed_default_content_settings.images": 2})
        self.browser = webdriver.Chrome(options=option)
        self.browser.get(self.startUrl)
        self.window1Handle = self.browser.current_window_handle
        self.login()
        WebDriverWait(self.browser, 20, 0.5).until(self.waitHelper)
        self.jump2List()
        for i in range(80):
            WebDriverWait(self.browser, 20, 0.5).until(self.waitHelper2)
            for i in range(23):
                self.openVideoDetail(i + 1)
                self.jump2Window2()
                WebDriverWait(self.browser, 20, 0.5).until(self.waitHelper3)
                time.sleep(1)
                if self.startVideo():
                    self.jump2Window3()
                    time.sleep(1)
                    self.execScript()
                    time.sleep(1)
                    self.saveAndQuit()
                    time.sleep(1)
                    self.closeWindow3()
                    time.sleep(1)
                    self.closeWindow2()
                    time.sleep(1)
                else:
                    self.closeWindow2()
                    time.sleep(1)
            self.listNextPage()
        time.sleep(1000000)

    def waitHelper(self, browser):
        return browser.title == '首页'

    def waitHelper2(self, browser):
        _cond1 = len(browser.find_elements_by_class_name('course-box')) > 0
        _cond2 = len(browser.find_elements_by_class_name(
            'ant-spin-spinning')) == 0
        return _cond1 and _cond2

    def waitHelper3(self, browser):
        _cond1 = len(browser.find_elements_by_class_name('color-data')) > 0
        _cond2 = len(browser.find_elements_by_class_name(
            'ant-spin-spinning')) == 0
        return _cond1 and _cond2

    def jump2Window2(self):
        newHandles = self.browser.window_handles
        # 跳转到新窗口
        for newhandle in newHandles:
            # 筛选新打开的窗口B
            if newhandle != self.window1Handle:
                    # 切换到新打开的窗口B
                self.browser.switch_to.window(newhandle)
                self.window2Handle = newhandle

    def jump2Window3(self):
        newHandles = self.browser.window_handles
        # 跳转到新窗口
        for newhandle in newHandles:
            # 筛选新打开的窗口B
            if (newhandle != self.window1Handle and newhandle != self.window2Handle):
                # 切换到新打开的窗口B
                self.browser.switch_to.window(newhandle)
                self.window3Handle = newhandle

    def closeWindow3(self):
        self.browser.close()
        self.browser.switch_to.window(self.window2Handle)

    def closeWindow2(self):
        self.browser.close()
        self.browser.switch_to.window(self.window1Handle)

    def login(self):
        self.browser.find_elements_by_class_name(
            'ant-input')[0].send_keys(self.username)
        self.browser.find_elements_by_class_name(
            'ant-input')[1].send_keys(self.pwd)

        captcha = self.browser.find_elements_by_class_name(
            'img-box')[1].get_attribute('src')
        self.b2 = webdriver.Chrome()
        self.b2.set_window_size(300, 100)
        self.b2.get(captcha)
        captcha_str = input('请输入显示的验证码: ')
        sessionId = self.b2.get_cookie('SESSION')
        self.browser.add_cookie(
            {'name': 'SESSION', 'value': sessionId.get('value')})
        self.b2.close()
        self.browser.find_elements_by_class_name(
            'input-box')[0].send_keys(captcha_str)
        self.browser.find_elements_by_class_name(
            'login-form-button')[0].click()

    def jump2List(self):
        self.browser.find_elements_by_class_name('ng-tns-c8-0')[5].click()

    def openVideoDetail(self, index):
        self.browser.find_elements_by_class_name(
            'course-box')[index - 1].click()

    def startVideo(self):
        score = float(self.browser.find_elements_by_class_name(
            'color-data')[2].text)
        print('进入课程: ' + self.browser.title + '(' + str(score) + '分)')
        if len(self.browser.find_elements_by_class_name('study-type')) > 1:
            if self.browser.find_elements_by_class_name('study-type')[1].text == '已完成':
                print('该课程已学过')
                return False
        self.addScoreAndPrint(score)
        self.browser.find_element_by_class_name('info-btn').click()
        return True

    def addScoreAndPrint(self, score):
        self.score += score
        print('本次学习已得分：' + str(self.score))
        if(self.score > 70):
            raise Exception('70分都不止了，够高了，别刷了大哥！')

    def execScript(self):
        self.browser.execute_script('XMLHttpRequest.prototype._send = XMLHttpRequest.prototype.send;' +
                                    'XMLHttpRequest.prototype.send = function(data) {' +
                                    "if('function' === typeof window.beforeXMLHttpRequestSend) {" +
                                    '   if(!window.beforeXMLHttpRequestSend(this, data)) {' +
                                    '       return;' +
                                    '   }' +
                                    '}' +
                                    'this._send(data);' +
                                    '};' +
                                    'window.beforeXMLHttpRequestSend = function(xhr, data) {' +
                                    "if(xhr.__zone_symbol__xhrURL.includes('/api/learner/play/course/')){" +
                                    "   data.set('sessionTime', '22:00:10');" +
                                    '}' +
                                    '  return true;' +
                                    '};')

    def saveAndQuit(self):
        btnDom = self.browser.find_elements_by_class_name('ant-btn-primary')
        if len(btnDom) > 0:
            btnDom[0].click()

    def listNextPage(self):
        self.browser.execute_script(
            "$('.ant-pagination-item-active').next().click()")


print('\n\n===+++---this program power by Magin---+++===\n\n')
username = input('输入账号: ')
pwd = input('输入密码: ')
try:
    wlxy = Wlxy(username, pwd)
except:
    print(sys.exc_info()[0])
    time.sleep(1000000)
