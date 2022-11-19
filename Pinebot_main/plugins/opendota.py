#!/usr/bin/env python3

__author__ = "Yxzh"


import requests
from nonebot import *
from Pinebot_main.util.logger import *
import json
import os

bot = get_bot()
registered_user = {}
opendota_user_list_path = "./Pinebot_main/json/opendota_user_list.json"

if not os.path.exists(opendota_user_list_path):
	with open(opendota_user_list_path, "w", encoding = "utf-8") as f:
		f.write("{}")

def reload_list():
	global registered_user
	registered_user = {}
	with open(opendota_user_list_path, "r", encoding = "utf-8") as f:
		registered_user = json.load(f)

def bind_user(steamid: int, qqid: int):
	global registered_user
	try:
		result = requests.get("https://api.opendota.com/api/players/" + str(steamid))
	except:
		return "获取失败。"
	try:
		result = json.loads(result.text)
	except:
		return "数据处理失败。"
	if result.get("profile") is None:
		return "steam账号无dota数据。"
	else:
		if registered_user.get(qqid) is not None:
			return "您的qq已绑定dota账号，新绑定前请先使用-dotaunbind解绑。。"
		name = str(result["profile"]["personaname"])
		registered_user[qqid] = steamid
		with open(opendota_user_list_path, "w", encoding = "utf-8") as f:
			f.write(json.dumps(registered_user, ensure_ascii = False, indent = 1))
		reload_list()
		return "已绑定 {}。".format(name)
		
def unbind_user(qqid: int):
	qqid = str(qqid)
	if registered_user.get(qqid) is None:
		return "您的qq还没有绑定dota账号。请使用\n-dotabind <dota好友id>绑定。"
	else:
		registered_user.pop(qqid)
		with open(opendota_user_list_path, "w", encoding = "utf-8") as f:
			f.write(json.dumps(registered_user, ensure_ascii = False, indent = 1))
		reload_list()
		return "已解除绑定dota账号。"
	
def get_solo_competitive_rank(qqid: int):
	qqid = str(qqid)
	if registered_user.get(qqid) is None:
		return "您的qq还没有绑定dota账号。请使用\n-dotabind <dota好友id>绑定。"
	else:
		try:
			result = requests.get("https://api.opendota.com/api/players/" + str(registered_user[qqid]) + "/ratings")
		except:
			return "获取失败。"
		try:
			result = json.loads(result.text)
		except:
			return "数据处理失败。"
		try:
			solo_competitive_rank = result[0]["solo_competitive_rank"]
		except:
			return "无法解析单排隐藏分。"
		return "您的单排隐藏分为" + str(solo_competitive_rank) + "。"

def get_mmr(qqid: int):
	qqid = str(qqid)
	if registered_user.get(qqid) is None:
		return "您的qq还没有绑定dota账号。请使用\n-dotabind <dota好友id>绑定。"
	else:
		try:
			result = requests.get("https://api.opendota.com/api/players/" + str(registered_user[qqid]))
		except:
			return "获取失败。"
		try:
			mmr = json.loads(result.text)["mmr_estimate"]["estimate"]
		except:
			return "无法解析mmr分数。"
		return "您的mmr预测分为" + str(mmr) + "。"
reload_list()

@bot.on_message("group")
async def handle_group_message(ctx):
	global live_status
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == u"-dotabind" and len(args) == 2:
		try:
			qqid = int(ctx["sender"]["user_id"])
			steamid = int(args[1])
		except:
			await bot.send_group_msg(group_id = g, message = u"好友id格式错误。请在游戏中点击添加好友，查看自己的好友id。")
			return
		msg = bind_user(steamid, qqid)
		await bot.send_group_msg(group_id = g, message = msg)
	if args[0] == u"-dotaunbind" and len(args) == 1:
		msg = unbind_user(int(ctx["sender"]["user_id"]))
		await bot.send_group_msg(group_id = g, message = msg)
	if args[0] == u"-dotasolorating" and len(args) == 1:
		msg = get_solo_competitive_rank(int(ctx["sender"]["user_id"]))
		await bot.send_group_msg(group_id = g, message = msg)
	if args[0] == u"-dotammr" and len(args) == 1:
		msg = get_mmr(int(ctx["sender"]["user_id"]))
		await bot.send_group_msg(group_id = g, message = msg)
	if args[0] == u"-dt" and len(args) == 1:
		msg = str(registered_user)
		await bot.send_group_msg(group_id = g, message = msg)