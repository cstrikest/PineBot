#!/usr/bin/env python3

__author__ = "Yxzh"

from nonebot import *
from Pinebot_main.util.logger import *
import os

bot = get_bot()

@bot.on_message("group")
async def handle_group_message(ctx):
	if ctx["group_id"] == 368200079 and ctx["raw_message"] == "111":
		os.system("sudo /usr/local/nginx/sbin/nginx")
		add_raw_log("RTMP_PROXY", "START")
		await bot.send_group_msg(group_id = 368200079, message = "启动推流转发")
	
	if ctx["group_id"] == 368200079 and ctx["raw_message"] == "000":
		os.system("sudo /usr/local/nginx/sbin/nginx -s stop")
		add_raw_log("RTMP_PROXY", "STOP")
		await bot.send_group_msg(group_id = 368200079, message = "关闭推流转发")