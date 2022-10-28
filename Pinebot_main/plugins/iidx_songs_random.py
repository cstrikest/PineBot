#!/usr/bin/env python3

__author__ = "Yxzh"

from nonebot import *
from Pinebot_main.util.logger import *
import json
import random


bot = get_bot()

with open("./Pinebot_main/json/iidx_songs_list.json", "r", encoding = "utf-8") as f:
	songs = json.load(f)

def getRandomIIDXSpSong(level):
	result = [x[0] + " [spe]" for x in songs if x[3] == level]
	result += [x[0] + " [spn]" for x in songs if x[4] == level]
	result += [x[0] + " [sph]" for x in songs if x[5] == level]
	result += [x[0] + " [spa]" for x in songs if x[6] == level]
	result += [x[0] + " [spl]" for x in songs if x[7] == level]
	return random.choice(result)

def getRandomIIDXDpSong(level):
	result = [x[0] + " [dpn]" for x in songs if x[8] == level]
	result += [x[0] + " [dph]" for x in songs if x[9] == level]
	result += [x[0] + " [dpa]" for x in songs if x[10] == level]
	result += [x[0] + " [dpl]" for x in songs if x[11] == level]
	return random.choice(result)

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	try:
		if args[0] == "-dxsp" and len(args) == 2:
			try:
				level = int(args[1])
				if level > 12 or level < 1:
					await bot.send_group_msg(group_id = g, message = "等级范围错误")
				else:
					msg = getRandomIIDXSpSong(args[1])
					add_log("IIDX_RANDOM", ctx, msg)
					await bot.send_group_msg(group_id = g, message = msg)
			except:
				await bot.send_group_msg(group_id = g, message = "参数错误")
		
		if args[0] == "-dxdp" and len(args) == 2:
			try:
				level = int(args[1])
				if level > 12 or level < 1:
					await bot.send_group_msg(group_id = g, message = "等级范围错误")
				else:
					msg = getRandomIIDXDpSong(args[1])
					add_log("IIDX_RANDOM", ctx, msg)
					await bot.send_group_msg(group_id = g, message = msg)
			except:
				await bot.send_group_msg(group_id = g, message = "参数错误")
		if args[0] == "-dx" and len(args) == 1:
			await bot.send_group_msg(group_id = g, message = random.choice(songs)[0])
	except:
		pass
