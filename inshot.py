# -*- coding: utf-8 -*-
import os
import re
import subprocess
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def connect_devices():
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']
    return valid_serials


def get_phone_info(dev):
    try:
        dics = {}
        cmd = 'adb -s %s shell "getprop | grep product"' % dev
        redcmd = str((os.popen(cmd).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").\
            replace("[", " ").replace(" ", "").split(",")
        for i in redcmd:
            if ":" in i:
                dic = {i.split(":")[0]: i.split(":")[-1]}
                dics.update(dic)
        cmd1 = 'adb -s %s shell cat /proc/meminfo' % dev
        redcmd1 = str((os.popen(cmd1).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("[", " ").replace(" ", "").split(",")[0]
        cmd2 = 'adb -s %s shell getprop ro.build.version.release' % dev
        redcmd2 = str((os.popen(cmd2).readlines())).replace("\\n", " ").replace("]", " ").replace("[", " ").replace("'", " ").replace(",", "").replace(" ", "")
        phone_info = dics["ro.product.manufacturer"] + " " + dics['ro.product.model'] + " " + \
                     str(round(int(re.findall(r"\d+\.?\d*", redcmd1)[0]) / 1024 / 1024, 2)) + "G " + redcmd2
        return phone_info
    except Exception as e:
        print(str(e), "get_mem(package)，请检查adb是否连通……")
        return 'xxx'


def find(driver, locator, timeout=10, t=0.5):
    """查找单个元素"""
    if not isinstance(locator, tuple):
        print("locator参数类型错误")
    elif locator[0] not in ["id", "xpath", "css selector", "class name"]:
        print("locator定位type错误，必须是['id', 'xpath', 'css selector', 'class name']中的一种")
    else:
        try:
            ele = WebDriverWait(driver, timeout, t).until(EC.presence_of_element_located(locator))
            return ele
        except:
            print("查找元素超时，没有找到元素(%s, %s)" % (locator[0], locator[1]))
            return ""


def click_element(driver, locator):
    """基础的点击事件"""
    el = find(driver, locator)
    el.click()


def get_driver(device, phone_version):
    caps1 = dict()
    caps1["platformName"] = 'Android'
    caps1["platformVersion"] = phone_version
    caps1["deviceName"] = device
    caps1["udid"] = device
    caps1["appPackage"] = "com.funnycat.virustotal"
    caps1["appActivity"] = "com.funnycat.virustotal.ui.splash.SplashActivity"
    caps1["noReset"] = True
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps1)
    time.sleep(1)
    return driver


def swipe_up(driver, ratio):
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    start = (int(width * 0.5), int(height * 0.5))
    end = (start[0], height*ratio)
    TouchAction(driver).long_press(None, start[0], start[1]).move_to(None, end[0], end[1]).release().perform()


def check_virus(driver, app_loc):
    User_Apps = ('xpath', '//androidx.appcompat.app.ActionBar.Tab[@content-desc="User Apps"]')
    AVs_Reports = ('xpath', '//androidx.appcompat.app.ActionBar.Tab[@content-desc="AVs Reports"]')
    MaxSecure = ('xpath', '//*[@resource-id="com.camerasideas.instashot:id/recycle_animation_rv"]/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]')
    while True:
        if find(driver, User_Apps):
            break
        else:
            continue
    for i in range(10):
        if find(driver, app_loc, 1):
            break
        else:
            swipe_up(driver, 0.1)
    swipe_up(driver, 0.45)
    click_element(driver, app_loc)
    if find(driver, AVs_Reports):
        click_element(driver, AVs_Reports)
        if find(driver, MaxSecure):
            return "app检测结果：有毒"
        else:
            return "app检测结果：无毒"
    else:
        return "app未被杀毒软件识别"


def run_check(app_loc):
    device = connect_devices()
    phone_info = get_phone_info(device[0])
    driver = get_driver(device[0], phone_info.split(' ')[3])
    result = check_virus(driver, app_loc)
    return result


if __name__ == '__main__':
    dev = connect_devices()
    print(dev)
    phone_info = get_phone_info(dev[0])
    print(phone_info.split(' '))
    # get_driver('2ac9a6a6', '9')
    VideoGuru = ('xpath', '//android.widget.TextView[contains(@text, "VideoGuru")]')
    YouCut = ('xpath', '//android.widget.TextView[contains(@text, "YouCut")]')
    InShot = ('xpath', '//android.widget.TextView[contains(@text, "InShot")]')
    Lumii = ('xpath', '//android.widget.TextView[contains(@text, "Lumii")]')
    result = run_check(VideoGuru)
    print(result)
