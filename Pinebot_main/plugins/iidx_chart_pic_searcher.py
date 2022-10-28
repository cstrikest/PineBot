#!/usr/bin/env python3

__author__ = "Yxzh"
from nonebot import *
from Pinebot_main.util.logger import *
import Pinebot_main.util.Chrome_Driver as Chrome_Driver
import difflib
import json


bot = get_bot()

with open("./Pinebot_main/json/iidx_songs_list.json", "r", encoding = "utf-8") as f:
	songs = json.load(f)

def get_chart_cmd(cmd, playSide, diffculty):
	# playSide  0 sp1p
	#           1 sp2p
	#           2 dp
	# diffculty 0 e
	#           1 n
	#           4 l
	
	msg = ""
	static_cmd = list(cmd)
	set = {
		"hs": "10",
		"mirror": "",
		"clip": "",
		"search_name": "",
		"format": ""
	}
	
	diffcultyLetter = ["P","N","H","A","X"]
	playSideLetter = ["1", "2", "D"]
	#  选择谱面难度
	for i in range(len(cmd)):
		if static_cmd[i] == "-hs":
			try:
				if 10 <= int(static_cmd[i + 1]) <= 50:
					set["hs"] = static_cmd[i + 1]
					cmd.remove(static_cmd[i])
					cmd.remove(static_cmd[i + 1])
					continue
			except:
				return "hs输入错误。", False
		
		if static_cmd[i] == "-m":
			set["mirror"] = "R0765432101234567"
			cmd.remove(static_cmd[i])
			continue
		
		if static_cmd[i] == "-1P" or static_cmd[i] == "-1p" :
			if playSide == 2:
				return "DP无法区分左右侧。", False
			playSide = 0
			cmd.remove(static_cmd[i])
			continue
		if static_cmd[i] == "-1P" or static_cmd[i] == "-2p" :
			if playSide == 2:
				return "DP无法区分左右侧。", False
			playSide = 1
			cmd.remove(static_cmd[i])
			continue
		
		if static_cmd[i] == "-o":
			try:
				a = int(static_cmd[i + 1])
				b = int(static_cmd[i + 2])
				if a > b or b > 300:
					return "小节数范围错误", False
				else:
					set["clip"] = "~" + static_cmd[i + 1] + "-" + static_cmd[i + 2]
					cmd.remove(static_cmd[i])
					cmd.remove(static_cmd[i + 1])
					cmd.remove(static_cmd[i + 2])
			except:
				return "小节数错误", False
	
	set["format"] = playSideLetter[playSide]
	set["format"] += diffcultyLetter[diffculty]
	set["search_name"] = "".join(cmd)
	
	try:
		int(set["hs"])
	except:
		set["hs"] = "10"
		msg += "-hs参数出现错误 默认10。"
	
	if set["mirror"] != "" and set["mirror"] != "R0765432101234567":
		set["m"] = ""
		msg += "-m参数出现错误 默认正谱。"
	
	l = []
	level = 0
	chart_type = set["format"].upper()
	search_words = set["search_name"].lower()
	try:
		for song in songs:
			l.append([difflib.SequenceMatcher(None, song[0].lower(), search_words).ratio(), song])
		song = max(l)
		print(song)
		if song[1][1] == "?":
			return song[1][0] + "暂无谱面图片。", False
		
		#  对应url格式信息
		if playSide == 0 or playSide == 1:
			level = song[1][3 + diffculty]
		elif playSide == 2:
			level = song[1][8 + diffculty - 1]
		if level == "0":
			return song[1][0] + "无对应谱面。", False
		if level == "10":
			level = "A"
		elif level == "11":
			level = "B"
		elif level == "12":
			level = "C"
		
		url = "http://textage.cc/score/" + str(song[1][2]) + "/" + song[1][1] + ".html?" + chart_type + level +"00" + set["mirror"] + "=" + set["hs"] + set["clip"]
		Chrome_Driver.browser.set_window_size(1,1)
		Chrome_Driver.browser.get(url)
		Chrome_Driver.browser.execute_script("var a = document.getElementsByTagName('input').length;for (var i = 0; i < a; i++) document.getElementsByTagName('input')[0].remove();")
		width = Chrome_Driver.browser.execute_script("return document.documentElement.scrollWidth")
		height = Chrome_Driver.browser.execute_script("return document.documentElement.scrollHeight")
		Chrome_Driver.browser.set_window_size(width, height)
		Chrome_Driver.browser.get_screenshot_as_file("./go-cqhttp/data/images/chart.png")
		
	except Exception as e:
		print(e)
		return "获取谱面图片时发生错误\n", False
	
	return song[1][0] + " (ratio:"+ str(song[0])[:5] +")\n", True
# print(get_chart_cmd(["灼热","-o","2A","-m","-c","18","30"]))

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == "-spe":
		msg, flag = get_chart_cmd(args[1:], 0, 0)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-spn":
		msg, flag = get_chart_cmd(args[1:], 0, 1)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-sph":
		msg, flag = get_chart_cmd(args[1:], 0, 2)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-spa":
		msg, flag = get_chart_cmd(args[1:], 0, 3)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-spl":
		msg, flag = get_chart_cmd(args[1:], 0, 4)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-dpn":
		msg, flag = get_chart_cmd(args[1:], 2, 1)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-dph":
		msg, flag = get_chart_cmd(args[1:], 2, 2)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-dpa":
		msg, flag = get_chart_cmd(args[1:], 2, 3)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
	
	elif args[0] == "-dpl":
		msg, flag = get_chart_cmd(args[1:], 2, 4)
		if flag:
			add_log("IIDX_PIC", ctx, ctx["raw_message"] + " => " + msg)
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + msg)
		else:
			await bot.send_group_msg(group_id = g, message = msg)
			
