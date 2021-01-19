# -*- coding: utf-8 -*-
import os
import time

from appium import webdriver

caps1 = dict()

caps1["platformName"] = 'Android'
caps1["platformVersion"] = "9"
caps1["deviceName"] = "2ac9a6a6"
caps1["udid"] = "2ac9a6a6"
caps1["appPackage"] = "com.camerasideas.instashot"
caps1["appActivity"] = ".DummyActivity"
caps1["noReset"] = True

time.sleep(2)
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps1)
driver.implicitly_wait(20)
driver.find_element_by_id("com.camerasideas.instashot:id/btn_select_video").click()
driver.find_element_by_id("com.camerasideas.instashot:id/layout").click()
driver.tap([(120, 48)], 500)
driver.quit()
