#!/usr/bin/env python3

__author__ = "Yxzh"

from nonebot import *
from Pinebot_main.util.logger import *
import json
import difflib

with open("./Pinebot_main/json/ereter.json", "r", encoding = "utf-8") as f:
	songs = json.load(f)
	
bot = get_bot()

def get_ereter_result(search_words: str, difficulty: int):
	name = ""
	for word in search_words:
		name += word
	l = []
	# try:
	tmpsongs = [x for x in songs if x[2] == difficulty]
	print(len(tmpsongs))
	for song in tmpsongs:
		l.append([difflib.SequenceMatcher(None, song[1].lower(), name.lower()).ratio(), song])
	song = max(l)[1]
	print(song)
	msg = "{}\n难度: {}\nec推定: {}\nhc推定: {}\nexhc推定: {}".format(song[1],song[0], song[3], song[4], song[5])
		
	# except Exception as e:
	# 	print(e)
	# 	return "解析ereter站数据时发生错误\n", False
	return msg, True

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == u"-h" and len(args) > 1:
		msg, flag = get_ereter_result(args[1:], 1)
		await bot.send_group_msg(group_id = g, message = msg)
		if flag:
			add_log("ERETER_SEARCH", ctx, ctx["raw_message"] + " => " + msg)
	elif args[0] == u"-a" and len(args) > 1:
		msg, flag = get_ereter_result(args[1:], 2)
		await bot.send_group_msg(group_id = g, message = msg)
		if flag:
			add_log("ERETER_SEARCH", ctx, ctx["raw_message"] + " => " + msg)
	elif args[0] == u"-l" and len(args) > 1:
		msg, flag = get_ereter_result(args[1:], 3)
		await bot.send_group_msg(group_id = g, message = msg)
		if flag:
			add_log("ERETER_SEARCH", ctx, ctx["raw_message"] + " => " + msg)