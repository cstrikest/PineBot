#!/usr/bin/env python3

__author__ = "Yxzh"

from PIL import Image
import Pinebot_main.util.Chrome_Driver as Chrome_Driver
import json
import difflib
import requests
from Pinebot_main.util.logger import add_log
from io import BytesIO
from nonebot import *


bot = get_bot()

with open("./Pinebot_main/json/SDVXData.json", "r", encoding = "utf-8") as f:
	songs = json.load(f)

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
		print("===")
		url = song[3]
		Chrome_Driver.browser.get(url)
		bgImgUrl = Chrome_Driver.browser.find_element("xpath","/html/body/table[5]/tbody/tr[2]/td[1]/table/tbody/tr/td/img").get_attribute("src")
		chartImgUrl = Chrome_Driver.browser.find_element("xpath","/html/body/table[5]/tbody/tr[2]/td[1]/table/tbody/tr/td/p[1]/img").get_attribute("src")
		barImgUrl = Chrome_Driver.browser.find_element("xpath","/html/body/table[5]/tbody/tr[2]/td[1]/table/tbody/tr/td/p[2]/img").get_attribute("src")
		
		print("===")
		bgImg = Image.open(BytesIO(requests.get(bgImgUrl).content))
		chartImg = Image.open(BytesIO(requests.get(chartImgUrl).content))
		barImg = Image.open(BytesIO(requests.get(barImgUrl).content))
		
		print("===")
		bgImg = bgImg.convert("RGBA")
		chartImg = chartImg.convert("RGBA")
		barImg = barImg.convert("RGBA")
		
		print("===")
		resultImg = Image.alpha_composite(Image.alpha_composite(bgImg, chartImg), barImg)
		resultImg.save("./go-cqhttp/data/images/chart.png")
	except Exception as e:
		print(e)
		return song[0] + "的谱面图片暂时无法显示。", False

	return "Level " + song[2] + "\n" + song[0], True

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == "-sv":
		msg, flag = get_chart_cmd(args[1:], "hardest")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svn":
		msg, flag = get_chart_cmd(args[1:], "n2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-sva":
		msg, flag = get_chart_cmd(args[1:], "a2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-sve":
		msg, flag = get_chart_cmd(args[1:], "e2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svm":
		msg, flag = get_chart_cmd(args[1:], "m2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svi":
		msg, flag = get_chart_cmd(args[1:], "i2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svg":
		msg, flag = get_chart_cmd(args[1:], "g2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svh":
		msg, flag = get_chart_cmd(args[1:], "h2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	elif args[0] == "-svv":
		msg, flag = get_chart_cmd(args[1:], "v2")
		if flag:
			add_log(ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
