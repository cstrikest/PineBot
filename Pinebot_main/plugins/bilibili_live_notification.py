#!/usr/bin/env python3

__author__ = "Yxzh"

import requests
from nonebot import *
from Pinebot_main.util.logger import *
import json
import os


GET_INFO_BY_ROOM_API_URL = """https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id="""
GET_STATUS_INFO_BY_UIDS_API_URL = """http://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?"""
bilibili_live_notification_uid_list_path = "./Pinebot_main/json/bilibili_live_notification_uid_list.json"
announce_group_list_path = "./Pinebot_main/json/announce_group_list.json"

bot = get_bot()
living_list = []  # 当前正在直播中的用户uid List， 用于
live_status = {}  # 储存用户直播状态的Dict {uid:0 or 1 or 2} 0关闭 1直播中 2轮播
with open("./Pinebot_main/json/live_notification_activate_group.json", "r") as f:
	activate_group = json.load(f)
# test dp bjm fanzhen

if not os.path.exists(bilibili_live_notification_uid_list_path):
	with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
		f.write("[]")

# 从文件读取直播监控用户列表
def get_uid_list_from_json(path):
	with open(path, "r", encoding = "utf-8") as f:
		return json.load(f)

# 使用bilibili API获取已添加监控用户的直播间状态
def get_live_status_info():
	user_uid_list = get_uid_list_from_json(bilibili_live_notification_uid_list_path)
	get_msg = ""
	for i in range(0, len(user_uid_list)):
		get_msg += "uids[{}]={}&".format(i, user_uid_list[i])
	result = requests.get(GET_STATUS_INFO_BY_UIDS_API_URL + get_msg)
	result = json.loads(result.text)
	return result

# 添加新用户或重启机器人时初始化状态
def init_live_status_list():
	global live_status
	global living_list
	live_status = {}
	result = get_live_status_info()
	if result["data"] != []:
		for user in result["data"].values():
			if user["live_status"] == 1:
				if user["uid"] not in living_list:
					living_list.append(user["uid"])
				live_status[user["uid"]] = 1
			else:
				live_status[user["uid"]] = 0

init_live_status_list()

# 刷新直播状态 返回是否触发，触发uid
def refresh_live_status():
	global live_status
	global living_list
	result = get_live_status_info()
	if result["data"] != []:
		for user_now in result["data"].values():
			try:
				# 从别的变1
				if live_status[user_now["uid"]] != user_now["live_status"]:
					if user_now["live_status"] == 1 and user_now["uid"] not in living_list:
						living_list.append(user_now["uid"])
						return True, user_now["uid"], user_now["uname"], user_now["title"], user_now["room_id"]
					elif user_now["live_status"] == 0 or user_now["live_status"] == 2 and user_now[
						"uid"] in living_list:
						living_list.remove(user_now["uid"])
						return False, 0, None, None, None
			except:
				live_status[user_now["uid"]] = user_now["live_status"]
			live_status[user_now["uid"]] = user_now["live_status"]
	return False, 0, None, None, None

@scheduler.scheduled_job('interval', seconds = 300)
async def _():
	global live_status
	trigger, uid, uname, title, room_id = refresh_live_status()
	if trigger:
		if "Sonic" not in uname:
			for group in activate_group:
				msg = "{} 开始直播。\n{}\nhttp://live.bilibili.com/{}".format(uname, title, room_id)
				add_raw_log("BILI_LIVE_START", msg.replace("\n", " "))
				await bot.send_group_msg(group_id = group, message = msg)

@bot.on_message("group")
async def handle_group_message(ctx):
	global live_status
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if g in activate_group:
		if args[0] == u"-livelist" and len(args) == 1:
			try:
				result = get_live_status_info()
			except:
				await bot.send_group_msg(group_id = g, message = u"网络错误")
				return
			msg = "直播监控列表：\n"
			if not result["data"]:
				await bot.send_group_msg(group_id = g, message = u"监控列表为空")
				return
			for room in result["data"].values():
				msg += "\n" + room["uname"]
			await bot.send_group_msg(group_id = g, message = msg)
		
		if args[0] == u"-liveadd" and len(args) == 2:
			try:
				room_id = int(args[1])
			except:
				await bot.send_group_msg(group_id = g, message = u"无效的房间号")
				return
			try:
				result = requests.get(GET_INFO_BY_ROOM_API_URL + str(room_id))
			except:
				await bot.send_group_msg(group_id = g, message = u"网络错误")
				return
			try:
				result = json.loads(result.text)
				user_name = result["data"]["anchor_info"]["base_info"]["uname"]
				uid = result["data"]["room_info"]["uid"]
				room_name = result["data"]["room_info"]["title"]
			except:
				await bot.send_group_msg(group_id = g, message = u"未找到对应直播间")
				return
			if isinstance(uid, int):
				with open(bilibili_live_notification_uid_list_path, "r", encoding = "utf-8") as f:
					user_uid_list = json.load(f)
				if uid in user_uid_list:
					await bot.send_group_msg(group_id = g,
					                         message = u"直播列表中已存在 " + user_name + " 的直播间 " + room_name + "。")
					return
				user_uid_list.append(uid)
				with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
					f.write(json.dumps(user_uid_list, ensure_ascii = False, indent = 1))
				init_live_status_list()
				msg = u"成功添加 " + user_name + " 的直播间 " + room_name + " 到监控列表。"
				add_raw_log("BILI_LIVE_ADD", msg)
				await bot.send_group_msg(group_id = g, message = msg)
			else:
				await bot.send_group_msg(group_id = g, message = u"添加失败。")
		
		if args[0] == u"-livedel" and len(args) == 2:
			try:
				room_id = int(args[1])
			except:
				await bot.send_group_msg(group_id = g, message = u"无效的房间号。")
				return
			try:
				result = requests.get(GET_INFO_BY_ROOM_API_URL + str(room_id))
			except:
				await bot.send_group_msg(group_id = g, message = u"网络错误。")
				return
			result = json.loads(result.text)
			uid = result["data"]["room_info"]["uid"]
			user_name = result["data"]["anchor_info"]["base_info"]["uname"]
			room_name = result["data"]["room_info"]["title"]
			if isinstance(uid, int):
				with open(bilibili_live_notification_uid_list_path, "r", encoding = "utf-8") as f:
					user_uid_list = json.load(f)
				try:
					user_uid_list.remove(uid)
				except:
					await bot.send_group_msg(group_id = g, message = user_name + "还没有登录到直播监控列表。")
					return
				with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
					f.write(json.dumps(user_uid_list, ensure_ascii = False, indent = 1))
				msg = "成功从监控列表删除 " + user_name + " 的直播间 " + room_name + "。"
				add_raw_log("BILI_LIVE_DEL", msg)
				init_live_status_list()
				await bot.send_group_msg(group_id = g, message = msg)
			else:
				await bot.send_group_msg(group_id = g, message = u"删除失败。")
