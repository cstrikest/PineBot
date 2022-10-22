#!/usr/bin/env python3

__author__ = "Yxzh"

import requests
from nonebot import *
import json
import os

GET_INFO_BY_ROOM_API_URL = """https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id="""
GET_STATUS_INFO_BY_UIDS_API_URL = """http://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?"""
bilibili_live_notification_uid_list_path = "./Pinebot_main/json/bilibili_live_notification_uid_list.json"
announce_group_list_path = "./Pinebot_main/json/announce_group_list.json"

bot = get_bot()
living_list = []
live_status = {}
with open("./Pinebot_main/json/live_notification_activate_group.json", "r") as f:
	activate_group = json.load(f)
#test dp bjm fanzhen

if not os.path.exists(bilibili_live_notification_uid_list_path):
	with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
		f.write("[]")

def get_live_status_info():
	with open(bilibili_live_notification_uid_list_path, "r", encoding = "utf-8") as f:
		user_uid_list = json.load(f)
	get_msg = ""
	for i in range(0, len(user_uid_list)):
		get_msg += "uids[{}]={}&".format(i,user_uid_list[i])
		
	result = requests.get(GET_STATUS_INFO_BY_UIDS_API_URL + get_msg)
	result = json.loads(result.text)
	return result
	
def setup_live_status_list():
	global live_status
	live_status = {}
	with open(bilibili_live_notification_uid_list_path, "r", encoding = "utf-8") as f:
		user_uid_list = json.load(f)
	for uid in user_uid_list:
		if uid in living_list:
			live_status[uid] = 1
		else:
			live_status[uid] = 0

setup_live_status_list()


# 刷新直播状态 返回是否触发，触发uid
def refresh_live_status():
	global live_status
	global living_list
	result = get_live_status_info()
	if result["data"] != []:
		print(live_status)
		for user in result["data"].values():
			try:
				# 从别的变1
				if live_status[user["uid"]] != user["live_status"]:
					if user["live_status"] == 1 and user["uid"] not in living_list:
						living_list.append(user["uid"])
						return True, user["uid"], user["uname"], user["title"], user["room_id"]
					elif user["live_status"] == 0 or user["live_status"] == 2 and user["uid"] in living_list:
						living_list.remove(user["uid"])
						return False, 0, None, None, None
			except: 
				live_status[user["uid"]] = user["live_status"]
			live_status[user["uid"]] = user["live_status"]
	return False, 0, None, None, None
	
@scheduler.scheduled_job('interval', seconds = 5)
async def _():
	global live_status
	trigger, uid, uname, title, room_id= refresh_live_status()
	if trigger:
		for group in activate_group:
			# test
			await bot.send_group_msg(group_id=group,message="{}开始直播。\n{}\nhttp://live.bilibili.com/{}".format(uname,title,room_id))
			

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
				await bot.send_group_msg(group_id = g, message = u"监控列表为空。")
				return
			for room in result["data"].values():
				msg += "\n" + room["uname"]
			await bot.send_group_msg(group_id = g, message = msg)
				
		
		if args[0] == u"-liveadd" and len(args) == 2: 
			try:
				room_id = int(args[1])
			except:
				await bot.send_group_msg(group_id = g, message = u"无效的房间号。")
				return
			try:
				result = requests.get(GET_INFO_BY_ROOM_API_URL + str(room_id))
			except:
				await bot.send_group_msg(group_id = g, message = u"网络错误")
				return
			result = json.loads(result.text)
			user_name = result["data"]["anchor_info"]["base_info"]["uname"]
			uid = result["data"]["room_info"]["uid"]
			room_name = result["data"]["room_info"]["title"]
			
			if isinstance(uid, int):
				with open(bilibili_live_notification_uid_list_path, "r", encoding = "utf-8") as f:
					user_uid_list = json.load(f)
				if uid in user_uid_list:
					await bot.send_group_msg(group_id = g, message = u"直播列表中已存在"+ user_name+"的直播间"+ room_name +"。")
					return
				user_uid_list.append(uid)
				with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
					f.write(json.dumps(user_uid_list, ensure_ascii = False, indent = 1))
				setup_live_status_list()
				await bot.send_group_msg(group_id = g, message = u"成功添加" + user_name + "的直播间" + room_name + "到监控列表。")
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
					await bot.send_group_msg(group_id = g, message = user_name+"还没有登录到直播监控列表。")
					return
				with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
					f.write(json.dumps(user_uid_list, ensure_ascii = False, indent = 1))
					
				setup_live_status_list()
				await bot.send_group_msg(group_id = g, message = u"成功从监控列表删除" + user_name + "的直播间" + room_name + "。")
			else:
				await bot.send_group_msg(group_id = g, message = u"删除失败。")
	
