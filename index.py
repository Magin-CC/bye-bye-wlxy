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
        print('退出类')

    def __init__(self, username, pwd, sc):
        self.startUrl = 'https://wlxy.8531.cn/learner/login'
        self.score = 0
        self.sc = sc
        self.username = username
        self.pwd = pwd
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        option.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})
        self.browser = webdriver.Chrome(options=option)
        self.browser.get(self.startUrl)
        self.window1Handle = self.browser.current_window_handle
        self.login()
        WebDriverWait(self.browser, 20, 0.5).until(self.waitHelper)
        self.browser.get('https://wlxy.8531.cn/learner/opencourse')
        # self.jump2List()
        time.sleep(5)
        # self.jump2NotMust()
        self.window1Handle = self.browser.current_window_handle

        time.sleep(5)
        for i in range(80):
            WebDriverWait(self.browser, 20, 0.5).until(self.waitHelper2)
            for i in range(10):
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
    # 登陆后的加载动作

    def waitHelper(self, browser):
        return browser.title == '首页' or browser.title == '浙报集团网络学院'
    # 课程列表的加载动作

    def waitHelper2(self, browser):
        _cond1 = len(browser.find_elements(By.CLASS_NAME, 'course-box')) > 0 or len(browser.find_elements(By.CLASS_NAME, 'single-course')) > 0
        _cond2 = len(browser.find_elements(By.CLASS_NAME, 
            'ant-spin-spinning')) == 0
        return _cond1 and _cond2
    # 课程详情的加载动作

    def waitHelper3(self, browser):
        _cond1 = len(browser.find_elements(By.CLASS_NAME, 'color-data')) > 0
        _cond2 = len(browser.find_elements(By.CLASS_NAME, 
            'ant-spin-spinning')) == 0
        return _cond1 and _cond2
    # tab到课程详情页

    def jump2Window2(self):
        newHandles = self.browser.window_handles
        # 跳转到新窗口
        for newhandle in newHandles:
            # 筛选新打开的窗口B
            if newhandle != self.window1Handle:
                    # 切换到新打开的窗口B
                self.browser.switch_to.window(newhandle)
                self.window2Handle = newhandle
    # tab到播放页

    def jump2Window3(self):
        newHandles = self.browser.window_handles
        # 跳转到新窗口
        for newhandle in newHandles:
            # 筛选新打开的窗口B
            if (newhandle != self.window1Handle and newhandle != self.window2Handle):
                # 切换到新打开的窗口B
                self.browser.switch_to.window(newhandle)
                self.window3Handle = newhandle

    # 关闭播放页
    def closeWindow3(self):
        self.browser.close()
        self.browser.switch_to.window(self.window2Handle)
    # 关闭课程详情页

    def closeWindow2(self):
        self.browser.close()
        self.browser.switch_to.window(self.window1Handle)
    # 登录动作

    def login(self):
        self.browser.switch_to.frame('idaasLoginPlugin')
        time.sleep(10)
        loginbox = self.browser.find_elements(By.CLASS_NAME, 'login-box')[2]
        loginbox.find_elements(By.CLASS_NAME, 
            'ivu-input')[0].send_keys(self.username)
        loginbox.find_elements(By.CLASS_NAME, 
            'ivu-input')[1].send_keys(self.pwd)

        loginbox.find_elements(By.CLASS_NAME, 
            'ivu-btn')[1].click()
    # 从首页跳转到列表页

    def jump2List(self):
        eles = self.browser.find_elements(By.CLASS_NAME, 'ng-tns-c2-0')
        print(len(eles));
        eles[4].click()
    # 从列表页跳转到详情页

    def jump2Must(self):
        # print(self.browser.find_element_by_xpath('span[text()="必修"]'))
        self.browser.find_element(By.XPATH, '//span[text()="必修"]').click()

    def jump2NotMust(self):
        self.browser.find_element(By.XPATH, '//span[text()="选修"]').click()

    def openVideoDetail(self, index):
        self.browser.find_elements(By.CLASS_NAME, 
            'course-info')[index - 1].click()
    # 从详情页到播放页

    def startVideo(self):
        score = float(self.browser.find_elements(By.CLASS_NAME, 
            'color-data')[2].text)
        print('进入课程: ' + self.browser.title + '(' + str(score) + '分)')
        if len(self.browser.find_elements(By.CLASS_NAME, 'study-type')) > 1:
            if self.browser.find_elements(By.CLASS_NAME, 'study-type')[1].text == '已完成':
                print('该课程已学过')
                return False
        self.addScoreAndPrint(score)
        self.browser.find_element(By.CLASS_NAME, 'info-btn').click()
        return True
    # 加分动作

    def addScoreAndPrint(self, score):
        self.score += score
        print('本次学习已得分：' + str(self.score))
        if(self.score > 90):
            print('已成功刷了', self.score, '分')
            sys.exit(0)
    # 核心代码

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
    # 保存并退出动作

    def saveAndQuit(self):
        btnDom = self.browser.find_elements(By.CLASS_NAME, 'ant-btn-primary')
        if len(btnDom) > 0:
            btnDom[0].click()
    # 列表页翻页动作

    def listNextPage(self):
        self.browser.execute_script(
            "$('.ant-pagination-item-active').next().click()")


print('\n\n===+++---this program power by Magin---+++===\n\n')
# username = input('输入账号: ')
# pwd = input('输入密码: ')
# sc = input('输入要刷的分数: ')
# wlxy = Wlxy(username, pwd, 50)

