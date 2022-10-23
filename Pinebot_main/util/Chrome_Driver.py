#!/usr/bin/env python3

__author__ = "Yxzh"

from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
# chrome_options.add_argument('blink-settings=imagesEnabled=false')
prefs = {
	'profile.default_content_setting_values': {
		'notifications': 2
	}
}
chrome_options.add_experimental_option('prefs', prefs)  # 禁用浏览器弹窗

browser = webdriver.Chrome("/usr/bin/chromedriver", options = chrome_options)

	