﻿#!/usr/bin/env python3

__author__ = "Yxzh"

from PIL import Image
from selenium import webdriver
import json
import difflib
import requests
from io import BytesIO
from os import path
from nonebot import *

bot = get_bot()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument('blink-settings=imagesEnabled=false')
prefs = {
	'profile.default_content_setting_values': {
		'notifications': 2
	}
}

chrome_options.add_experimental_option('prefs', prefs)  # 禁用浏览器弹窗
browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options = chrome_options)

# driver = Chrome(executable_path="/usr/bin/chromedriver", options = opt)
with open("./Pinebot_main/json/SDVXData.json", "r", encoding = "utf-8") as f:
	songs = json.load(f)

# with open("../dataSpider/JSON/SDVXData.json", "r", encoding = "utf-8") as f:
# 	songs = json.load(f)

diffcultyList = ["hardest", "z2", "n2", "a2", "e2", "m2", "f2", "i2", "g2", "h2", "v2"]

def get_chart_cmd(searchSongName, diffculty):
	searchSongName = "".join(searchSongName)
	if diffculty not in diffcultyList:
		return "谱面类型错误"
	
	try:
		l = []
		for song in songs:
			l.append([difflib.SequenceMatcher(None, song[0].lower(), searchSongName.lower()).ratio(), song])
		song = max(l)
		currentSongs = [x for x in songs if x[0] == song[1][0]]
		if diffculty != "hardest":
			if diffculty not in [d[1] for d in currentSongs]:
				return song[1][0] + "无此难度的谱面。", False
			else:
				song = [x for x in currentSongs if x[1] == diffculty][0]
		else:
			currentSongs.sort(key = lambda t: int(t[2]), reverse = True)
			song = currentSongs[0]
		print(song)
	except Exception as e:
		print(e)
		return "搜索歌曲错误。", False
	
	try:
		url = song[3]
		browser.get(url)
		bgImgUrl = browser.find_element("xpath","/html/body/table[5]/tbody/tr[2]/td[1]/table/tbody/tr/td/img").get_attribute("src")
		chartImgUrl = browser.find_element("xpath","/html/body/table[5]/tbody/tr[2]/td[1]/table/tbody/tr/td/p[1]/img").get_attribute("src")
		barImgUrl = browser.find_element("xpath","/html/body/table[5]/tbody/tr[2]/td[1]/table/tbody/tr/td/p[2]/img").get_attribute("src")
		
		bgImg = Image.open(BytesIO(requests.get(bgImgUrl).content))
		chartImg = Image.open(BytesIO(requests.get(chartImgUrl).content))
		barImg = Image.open(BytesIO(requests.get(barImgUrl).content))
		
		bgImg = bgImg.convert("RGBA")
		chartImg = chartImg.convert("RGBA")
		barImg = barImg.convert("RGBA")
		
		resultImg = Image.alpha_composite(Image.alpha_composite(bgImg, chartImg), barImg)
		resultImg.save("./go-cqhttp/data/images/chart.png")
	# resultImg.save("./result.png")
	except Exception as e:
		print(e)
		return song[0] + "的谱面图片暂时无法显示。", False
	
	
	# notes = driver.find_element_by_xpath(
	# 	"/html/body/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/div/table/tbody/tr/td[3]/div").text
	# bpm = driver.find_element_by_xpath(
	# 	"/html/body/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td[3]/div").text
	# generation = driver.find_element_by_xpath(
	# 	"/html/body/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td/img").get_attribute(
	# 	"src")
	# if "sdvx01" in generation:
	# 	generation = "1代谱面"
	# elif "sdvx02" in generation:
	# 	generation = "2代谱面"
	# elif "sdvx03" in generation:
	# 	generation = "3代谱面"
	# elif "sdvx04" in generation:
	# 	generation = "4代谱面"
	# elif "sdvx05" in generation:
	# 	generation = "5代谱面"
	# elif "sdvx06" in generation:
	# 	generation = "6代谱面"
	# else:
	# 	generation = ""
	
	# return "Level " + song[2] + "\n" + song[
	# 	0] + "\n" + generation + "\nCHAIN " + notes + "  BPM " + bpm + "\n", True
	return "Level " + song[2] + "\n" + song[0], True
# print(get_chart_cmd("seasickness", "hardest"))#

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == "-sv":
		msg, flag = get_chart_cmd(args[1:], "hardest")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svn":
		msg, flag = get_chart_cmd(args[1:], "n2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-sva":
		msg, flag = get_chart_cmd(args[1:], "a2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-sve":
		msg, flag = get_chart_cmd(args[1:], "e2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svm":
		msg, flag = get_chart_cmd(args[1:], "m2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svi":
		msg, flag = get_chart_cmd(args[1:], "i2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svg":
		msg, flag = get_chart_cmd(args[1:], "g2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svh":
		msg, flag = get_chart_cmd(args[1:], "h2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svv":
		msg, flag = get_chart_cmd(args[1:], "v2")
		if flag:
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)