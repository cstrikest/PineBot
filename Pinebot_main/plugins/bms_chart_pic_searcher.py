#!/usr/bin/env python3

__author__ = "Yxzh"

import time

from Pinebot_main.util.logger import add_log
import Pinebot_main.util.Chrome_Driver as Chrome_Driver
from PIL import Image
import io
import difflib
import json
from nonebot import *


bot = get_bot()

with open("./Pinebot_main/json/bms_songs_h1_list.json", "r", encoding = "utf-8") as f:
	bms_songs_h1 = json.load(f)

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if "-黑" in args[0]:
		if "?" in args[0] or "？" in args[0]:
			level = 26
		else:
			try:
				level = int(args[0][2:])
			except:
				await bot.send_group_msg(group_id = g, message = "等级有误")
				return
			if level > 25 or level < 1:
				await bot.send_group_msg(group_id = g, message = "发狂表1无此等级")
				return
		try:
			_2p = False
			_mir = False
			for cmd in args:
				if cmd == "-1p":
					args.remove(cmd)
				if cmd == "-2p":
					args.remove(cmd)
					_2p = True
				if "-m" in cmd:
					args.remove(cmd)
					_mir = True
			
			name = "".join(args[1:])
			l = []
			for song in [x for x in bms_songs_h1 if x[0] == level]:
				l.append([difflib.SequenceMatcher(None, song[1].lower(), name).ratio(), song])
			song = max(l)
			url = song[1][3]
			print(song)
			
			if _2p:
				url.replace("p=1", "p=2")
			if _mir:
				url += "&o=1"
			
			Chrome_Driver.browser.set_window_size(4500, 1600)
			Chrome_Driver.browser.get(url)
			time.sleep(1)
			img_png = Chrome_Driver.browser.get_screenshot_as_png()
			img_io = io.BytesIO(img_png)
			img = Image.open(img_io)
			
			y = 1500
			bound = 4490
			for x in range(10, 3000, 10):
				if img.getpixel((4500-x, y)) != (0,0,0,255):
					bound = 4500-x
					break
			
			box = (0, 0, bound + 10, 1550)
			img = img.crop(box)
			img.save("./go-cqhttp/data/images/chart.png")
			
			add_log("BMS_PIC", ctx, ctx["raw_message"] + " => " + song[1][1])
			await bot.send_group_msg(group_id = g, message = "[CQ:image,file=chart.png]" + song[1][1])
		except Exception as e:
			print(e)
			await bot.send_group_msg(group_id = g, message = "无法获取谱面图片")