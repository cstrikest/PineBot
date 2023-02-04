# #!/usr/bin/env python3
# 
# __author__ = "Yxzh"
# 
# import requests
# from nonebot import *
# from Pinebot_main.util.logger import *
# import json
# import os
# 
# 
# GET_INFO_BY_ROOM_API_URL = """https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id="""
# GET_STATUS_INFO_BY_UIDS_API_URL = """http://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?"""
# bilibili_live_notification_uid_list_path = "./Pinebot_main/json/bilibili_live_notification_uid_list.json"
# announce_group_list_path = "./Pinebot_main/json/announce_group_list.json"
# 
# bot = get_bot()
# living_list = []  # 当前正在直播中的用户uid List， 用于
# live_status = {}  # 储存用户直播状态的Dict {uid:0 or 1 or 2} 0关闭 1直播中 2轮播
# with open("./Pinebot_main/json/live_notification_activate_group.json", "r") as f:
# 	activate_group = json.load(f)
# # test dp bjm fanzhen
# 
# if not os.path.exists(bilibili_live_notification_uid_list_path):
# 	with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
# 		f.write("[]")
# 
# # 从文件读取直播监控用户列表
# def get_uid_list_from_json(path):
# 	with open(path, "r", encoding = "utf-8") as f:
# 		return json.load(f)
# 
# # 使用bilibili API获取已添加监控用户的直播间状态
# def get_live_status_info():
# 	user_uid_list = get_uid_list_from_json(bilibili_live_notification_uid_list_path)
# 	get_msg = ""
# 	for i in range(0, len(user_uid_list)):
# 		get_msg += "uids[{}]={}&".format(i, user_uid_list[i])
# 	result = requests.get(GET_STATUS_INFO_BY_UIDS_API_URL + get_msg)
# 	result = json.loads(result.text)
# 	return result
# 
# # 添加新用户或重启机器人时初始化状态
# def init_live_status_list():
# 	global live_status
# 	global living_list
# 	live_status = {}
# 	result = get_live_status_info()
# 	if result["data"] != []:
# 		for user in result["data"].values():
# 			if user["live_status"] == 1:
# 				if user["uid"] not in living_list:
# 					living_list.append(user["uid"])
# 				live_status[user["uid"]] = 1
# 			else:
# 				live_status[user["uid"]] = 0
# 
# init_live_status_list()
# 
# # 刷新直播状态 返回是否触发，触发uid
# def refresh_live_status():
# 	global live_status
# 	global living_list
# 	result = get_live_status_info()
# 	if result["data"] != []:
# 		for user_now in result["data"].values():
# 			try:
# 				# 从别的变1
# 				if live_status[user_now["uid"]] != user_now["live_status"]:
# 					if user_now["live_status"] == 1 and user_now["uid"] not in living_list:
# 						living_list.append(user_now["uid"])
# 						return True, user_now["uid"], user_now["uname"], user_now["title"], user_now["room_id"]
# 					elif user_now["live_status"] == 0 or user_now["live_status"] == 2 and user_now[
# 						"uid"] in living_list:
# 						living_list.remove(user_now["uid"])
# 						return False, 0, None, None, None
# 			except:
# 				live_status[user_now["uid"]] = user_now["live_status"]
# 			live_status[user_now["uid"]] = user_now["live_status"]
# 	return False, 0, None, None, None
# 
# @scheduler.scheduled_job('interval', seconds = 300)
# async def _():
# 	global live_status
# 	trigger, uid, uname, title, room_id = refresh_live_status()
# 	if trigger:
# 		if "Sonic" not in uname:
# 			for group in activate_group:
# 				msg = "{} 开始直播。\n{}\nhttp://live.bilibili.com/{}".format(uname, title, room_id)
# 				add_raw_log("BILI_LIVE_START", msg.replace("\n", " "))
# 				await bot.send_group_msg(group_id = group, message = msg)
# 
# @bot.on_message("group")
# async def handle_group_message(ctx):
# 	global live_status
# 	g = ctx["group_id"]
# 	args = ctx["raw_message"].split()
# 	if g in activate_group:
# 		if args[0] == u"-livelist" and len(args) == 1:
# 			try:
# 				result = get_live_status_info()
# 			except:
# 				await bot.send_group_msg(group_id = g, message = u"网络错误")
# 				return
# 			msg = "直播监控列表：\n"
# 			if not result["data"]:
# 				await bot.send_group_msg(group_id = g, message = u"监控列表为空")
# 				return
# 			for room in result["data"].values():
# 				msg += "\n" + room["uname"]
# 			await bot.send_group_msg(group_id = g, message = msg)
# 		
# 		if args[0] == u"-liveadd" and len(args) == 2:
# 			try:
# 				room_id = int(args[1])
# 			except:
# 				await bot.send_group_msg(group_id = g, message = u"无效的房间号")
# 				return
# 			try:
# 				result = requests.get(GET_INFO_BY_ROOM_API_URL + str(room_id))
# 			except:
# 				await bot.send_group_msg(group_id = g, message = u"网络错误")
# 				return
# 			try:
# 				result = json.loads(result.text)
# 				user_name = result["data"]["anchor_info"]["base_info"]["uname"]
# 				uid = result["data"]["room_info"]["uid"]
# 				room_name = result["data"]["room_info"]["title"]
# 			except:
# 				await bot.send_group_msg(group_id = g, message = u"未找到对应直播间")
# 				return
# 			if isinstance(uid, int):
# 				with open(bilibili_live_notification_uid_list_path, "r", encoding = "utf-8") as f:
# 					user_uid_list = json.load(f)
# 				if uid in user_uid_list:
# 					await bot.send_group_msg(group_id = g,
# 					                         message = u"直播列表中已存在 " + user_name + " 的直播间 " + room_name + "。")
# 					return
# 				user_uid_list.append(uid)
# 				with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
# 					f.write(json.dumps(user_uid_list, ensure_ascii = False, indent = 1))
# 				init_live_status_list()
# 				msg = u"成功添加 " + user_name + " 的直播间 " + room_name + " 到监控列表。"
# 				add_raw_log("BILI_LIVE_ADD", msg)
# 				await bot.send_group_msg(group_id = g, message = msg)
# 			else:
# 				await bot.send_group_msg(group_id = g, message = u"添加失败。")
# 		
# 		if args[0] == u"-livedel" and len(args) == 2:
# 			try:
# 				room_id = int(args[1])
# 			except:
# 				await bot.send_group_msg(group_id = g, message = u"无效的房间号。")
# 				return
# 			try:
# 				result = requests.get(GET_INFO_BY_ROOM_API_URL + str(room_id))
# 			except:
# 				await bot.send_group_msg(group_id = g, message = u"网络错误。")
# 				return
# 			result = json.loads(result.text)
# 			uid = result["data"]["room_info"]["uid"]
# 			user_name = result["data"]["anchor_info"]["base_info"]["uname"]
# 			room_name = result["data"]["room_info"]["title"]
# 			if isinstance(uid, int):
# 				with open(bilibili_live_notification_uid_list_path, "r", encoding = "utf-8") as f:
# 					user_uid_list = json.load(f)
# 				try:
# 					user_uid_list.remove(uid)
# 				except:
# 					await bot.send_group_msg(group_id = g, message = user_name + "还没有登录到直播监控列表。")
# 					return
# 				with open(bilibili_live_notification_uid_list_path, "w", encoding = "utf-8") as f:
# 					f.write(json.dumps(user_uid_list, ensure_ascii = False, indent = 1))
# 				msg = "成功从监控列表删除 " + user_name + " 的直播间 " + room_name + "。"
# 				add_raw_log("BILI_LIVE_DEL", msg)
# 				init_live_status_list()
# 				await bot.send_group_msg(group_id = g, message = msg)
# 			else:
# 				await bot.send_group_msg(group_id = g, message = u"删除失败。")
#!/usr/bin/env python3

__author__ = "Yxzh"


from nonebot import *
from Pinebot_main.util.logger import *
import json
import os
import requests


GET_INFO_BY_ROOM_API_URL = """https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id="""
# https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id=466988
# {
# 	"code": 0, "message": "0", "ttl": 1, "data": {
# 	"room_info": {
# 		"uid": 3624698, "room_id": 466988, "short_id": 0, "title": "汪美丽的直播间", "cover": "", "tags": "",
# 		"background": "", "description": "", "live_status": 0, "live_start_time": 0, "live_screen_type": 0,
# 		"lock_status": 0, "lock_time": 0, "hidden_status": 0, "hidden_time": 0, "area_id": 0, "area_name": "",
# 		"parent_area_id": 0, "parent_area_name": "", "keyframe": "", "special_type": 0, "up_session": "0",
# 		"pk_status": 0, "is_studio": false, "pendants": {"frame": {"name": "", "value": "", "desc": ""}},
# 		"on_voice_join": 0, "online": 0, "room_type": {}
# 	}, "anchor_info": {
# 		"base_info": {
# 			"uname": "汪美丽", "face": "http://i0.hdslb.com/bfs/face/member/noface.jpg", "gender": "保密",
# 			"official_info": {
# 				"role": -1, "title": "", "desc": "", "is_nft": 0,
# 				"nft_dmark": "https://i0.hdslb.com/bfs/live/9f176ff49d28c50e9c53ec1c3297bd1ee539b3d6.gif"
# 			}
# 		}, "live_info": {
# 			"level": 1, "level_color": 6406234, "score": 0, "upgrade_score": 50, "current": [0, 0], "next": [50, 50],
# 			"rank": "\u003e10000"
# 		}, "relation_info": {"attention": 0}, "medal_info": null, "gift_info": null
# 	}, "news_info": {"uid": 3624698, "ctime": "0001-01-01 00:00:00", "content": ""}, "rankdb_info": {
# 		"roomid": 466988, "rank_desc": "", "color": "", "h5_url": "", "web_url": "", "timestamp": 1675494169
# 	}, "area_rank_info": {"areaRank": {"index": 0, "rank": "\u003e1000"}, "liveRank": {"rank": "\u003e10000"}},
# 	"battle_rank_entry_info": null, "tab_info": {
# 		"list": [{
# 			         "type": "seven-rank", "desc": "高能用户", "isFirst": 1, "isEvent": 0, "eventType": "",
# 			         "listType": "", "apiPrefix": "", "rank_name": "room_7day"
# 		         }, {
# 			         "type": "guard", "desc": "大航海", "isFirst": 0, "isEvent": 0, "eventType": "",
# 			         "listType": "top-list", "apiPrefix": "", "rank_name": ""
# 		         }]
# 	}, "activity_init_info": {
# 		"eventList": [], "weekInfo": {"bannerInfo": null, "giftName": null}, "giftName": null, "lego": {
# 			"timestamp": 1675494169,
# 			"config": "[{\"name\":\"frame-mng\",\"url\":\"https:\\/\\/live.bilibili.com\\/p\\/html\\/live-web-mng\\/index.html?roomid=#roomid#\u0026arae_id=#area_id#\u0026parent_area_id=#parent_area_id#\u0026ruid=#ruid#\",\"startTime\":1559544736,\"endTime\":1877167950,\"type\":\"frame-mng\"},{\"name\":\"s10-fun\",\"target\":\"sidebar\",\"icon\":\"https:\\/\\/i0.hdslb.com\\/bfs\\/activity-plat\\/static\\/20200908\\/3435f7521efc759ae1f90eae5629a8f0\\/HpxrZ7SOT.png\",\"text\":\"\\u7545\\u73a9s10\",\"url\":\"https:\\/\\/live.bilibili.com\\/s10\\/fun\\/index.html?room_id=#roomid#\u0026width=376\u0026height=600\u0026source=sidebar\",\"color\":\"#2e6fc0\",\"startTime\":1600920000,\"endTime\":1604721600,\"parentAreaId\":2,\"areaId\":86},{\"name\":\"genshin-avatar\",\"target\":\"sidebar\",\"icon\":\"https:\\/\\/i0.hdslb.com\\/bfs\\/activity-plat\\/static\\/20210721\\/fa538c98e9e32dc98919db4f2527ad02\\/qWxN1d0ACu.jpg\",\"text\":\"\\u539f\\u77f3\\u798f\\u5229\",\"url\":\"https:\\/\\/live.bilibili.com\\/activity\\/live-activity-full\\/genshin_avatar\\/mobile.html?no-jump=1\u0026room_id=#roomid#\u0026width=376\u0026height=550#\\/\",\"color\":\"#2e6fc0\",\"frameAllowNoBg\":\"1\",\"frameAllowDrag\":\"1\",\"startTime\":1627012800,\"endTime\":1630425540,\"parentAreaId\":3,\"areaId\":321}]"
# 		}
# 	}, "voice_join_info": {
# 		"status": {
# 			"open": 0, "anchor_open": 0, "status": 0, "uid": 0, "user_name": "", "head_pic": "", "guard": 0,
# 			"start_at": 0, "current_time": 1675494169
# 		}, "icons": {
# 			"icon_close": "https://i0.hdslb.com/bfs/live/a176d879dffe8de1586a5eb54c2a08a0c7d31392.png",
# 			"icon_open": "https://i0.hdslb.com/bfs/live/70f0844c9a12d29db1e586485954290144534be9.png",
# 			"icon_wait": "https://i0.hdslb.com/bfs/live/1049bb88f1e7afd839cc1de80e13228ccd5807e8.png",
# 			"icon_starting": "https://i0.hdslb.com/bfs/live/948433d1647a0704f8216f017c406224f9fff518.gif"
# 		}, "web_share_link": "https://live.bilibili.com/h5/466988"
# 	}, "ad_banner_info": null, "skin_info": {
# 		"id": 0, "skin_name": "", "skin_config": "", "show_text": "", "skin_url": "", "start_time": 0, "end_time": 0,
# 		"current_time": 1675494169
# 	}, "web_banner_info": {
# 		"id": 0, "title": "", "left": "", "right": "", "jump_url": "", "bg_color": "", "hover_color": "",
# 		"text_bg_color": "", "text_hover_color": "", "link_text": "", "link_color": "", "input_color": "",
# 		"input_text_color": "", "input_hover_color": "", "input_border_color": "", "input_search_color": ""
# 	}, "lol_info": null, "pk_info": null, "battle_info": null,
# 	"silent_room_info": {"type": "", "level": 0, "second": 0, "expire_time": 0},
# 	"switch_info": {"close_guard": false, "close_gift": false, "close_online": false, "close_danmaku": false},
# 	"record_switch_info": null, "room_config_info": {"dm_text": "发个弹幕呗~"}, "gift_memory_info": {"list": null},
# 	"new_switch_info": {
# 		"room-socket": 1, "room-prop-send": 1, "room-sailing": 1, "room-info-popularity": 1, "room-danmaku-editor": 1,
# 		"room-effect": 1, "room-fans_medal": 1, "room-report": 1, "room-feedback": 1, "room-player-watermark": 1,
# 		"room-recommend-live_off": 1, "room-activity": 1, "room-web_banner": 1, "room-silver_seeds-box": 1,
# 		"room-wishing_bottle": 1, "room-board": 1, "room-supplication": 1, "room-hour_rank": 1, "room-week_rank": 1,
# 		"room-anchor_rank": 1, "room-info-integral": 1, "room-super-chat": 1, "room-tab": 1, "room-hot-rank": 1,
# 		"fans-medal-progress": 1, "gift-bay-screen": 1, "room-enter": 1, "room-my-idol": 1, "room-topic": 1,
# 		"fans-club": 1, "room-popular-rank": 1, "mic_user_gift": 1, "new-room-area-rank": 1
# 	}, "super_chat_info": {
# 		"status": 0,
# 		"jump_url": "https://live.bilibili.com/p/html/live-app-superchat2/index.html?is_live_half_webview=1\u0026hybrid_half_ui=1,3,100p,70p,ffffff,0,30,100,12,0;2,2,375,100p,ffffff,0,30,100,0,0;3,3,100p,70p,ffffff,0,30,100,12,0;4,2,375,100p,ffffff,0,30,100,0,0;5,3,100p,60p,ffffff,0,30,100,12,0;6,3,100p,60p,ffffff,0,30,100,12,0;7,3,100p,60p,ffffff,0,30,100,12,0",
# 		"icon": "https://i0.hdslb.com/bfs/live/0a9ebd72c76e9cbede9547386dd453475d4af6fe.png", "ranked_mark": 0,
# 		"message_list": []
# 	}, "online_gold_rank_info_v2": {"list": null},
# 	"dm_brush_info": {"min_time": 700, "brush_count": 100, "slice_count": 2, "storage_time": 3000},
# 	"dm_emoticon_info": {"is_open_emoticon": 1, "is_shield_emoticon": 0}, "dm_tag_info": {
# 		"dm_tag": 0, "platform": [], "extra": "", "dm_chronos_extra": "", "dm_mode": [], "dm_setting_switch": 0,
# 		"material_conf": null
# 	}, "topic_info": {"topic_id": 0, "topic_name": ""}, "game_info": {"game_status": 0}, "watched_show": {
# 		"switch": true, "num": 1, "text_small": "1", "text_large": "1人看过", "icon": "", "icon_location": 0,
# 		"icon_web": ""
# 	}, "topic_room_info": {"interactive_h5_url": "", "watermark": 1}, "show_reserve_status": false,
# 	"second_create_info": {"click_permission": 0, "common_permission": 0, "icon_name": "", "icon_url": "", "url": ""},
# 	"play_together_info": {
# 		"switch": 0, "icon_list": [{
# 			                           "icon": "https://i0.hdslb.com/bfs/live/1d2e891c9a6c592e17d95825366e8ffa7555c995.png",
# 			                           "title": "未申请",
# 			                           "jump_url": "https://live.bilibili.com/p/html/live-app-play-together/index.html?roomid=466988\u0026ruid=3624698\u0026hybrid_half_ui=1,3,100p,70p,0,1,0,100,10;2,2,375,100p,0,1,0,100,10;3,3,100p,70p,0,1,0,100,10;4,2,375,100p,0,1,0,100,10;5,3,100p,70p,0,1,0,100,10;6,3,100p,70p,0,1,0,100,10;7,3,100p,70p,0,1,0,100,10;8,3,100p,70p,0,1,0,100,10\u0026is_live_half_webview=1\u0026hybrid_biz=live-play-together",
# 			                           "status": 1
# 		                           }, {
# 			                           "icon": "https://i0.hdslb.com/bfs/live/63b965459ddc7ad22d715421af8aa034977bb72f.png",
# 			                           "title": "游戏中",
# 			                           "jump_url": "https://live.bilibili.com/p/html/live-app-play-together/index.html?roomid=466988\u0026ruid=3624698\u0026hybrid_half_ui=1,3,100p,70p,0,1,0,100,10;2,2,375,100p,0,1,0,100,10;3,3,100p,70p,0,1,0,100,10;4,2,375,100p,0,1,0,100,10;5,3,100p,70p,0,1,0,100,10;6,3,100p,70p,0,1,0,100,10;7,3,100p,70p,0,1,0,100,10;8,3,100p,70p,0,1,0,100,10\u0026is_live_half_webview=1\u0026hybrid_biz=live-play-together",
# 			                           "status": 3
# 		                           }, {
# 			                           "icon": "https://i0.hdslb.com/bfs/live/fa1a4d496dc5c8da95cfda353ca88e4cc1027b99.png",
# 			                           "title": "等待中",
# 			                           "jump_url": "https://live.bilibili.com/p/html/live-app-play-together/index.html?roomid=466988\u0026ruid=3624698\u0026hybrid_half_ui=1,3,100p,70p,0,1,0,100,10;2,2,375,100p,0,1,0,100,10;3,3,100p,70p,0,1,0,100,10;4,2,375,100p,0,1,0,100,10;5,3,100p,70p,0,1,0,100,10;6,3,100p,70p,0,1,0,100,10;7,3,100p,70p,0,1,0,100,10;8,3,100p,70p,0,1,0,100,10\u0026is_live_half_webview=1\u0026hybrid_biz=live-play-together",
# 			                           "status": 2
# 		                           }]
# 	}, "cloud_game_info": {"is_gaming": 0}, "like_info_v3": {
# 		"total_likes": 0, "click_block": false, "count_block": false,
# 		"guild_emo_text": "试试双击点赞 让主播被更多人看到吧～", "guild_dm_text": "点赞30次可以帮主播冲刺热门榜哦～",
# 		"like_dm_text": "谢谢你的赞，每点赞30次有概率为主播增加曝光哦～",
# 		"hand_icons": ["https://i0.hdslb.com/bfs/live/ecc2c5a2efc1c40a1125bb0d648d891e0e8cbd3b.png",
# 		               "https://i0.hdslb.com/bfs/live/391b45ed00617391b863f6441d5d040165c4d1b4.png",
# 		               "https://i0.hdslb.com/bfs/live/ad7c7adc9ee0c778cea161dea6c5a96c4ff7f845.png",
# 		               "https://i0.hdslb.com/bfs/live/c6a4781558d84838cc4963fcf94792e54beabe15.png",
# 		               "https://i0.hdslb.com/bfs/live/6920410aca21e3397f23ee7ae5ddbf8f1c625943.png",
# 		               "https://i0.hdslb.com/bfs/live/7e671e053c365f91a0a0f4837ec92ac9581977ec.png"],
# 		"dm_icons": ["https://i0.hdslb.com/bfs/live/ecc2c5a2efc1c40a1125bb0d648d891e0e8cbd3b.png",
# 		             "https://i0.hdslb.com/bfs/live/391b45ed00617391b863f6441d5d040165c4d1b4.png",
# 		             "https://i0.hdslb.com/bfs/live/ad7c7adc9ee0c778cea161dea6c5a96c4ff7f845.png",
# 		             "https://i0.hdslb.com/bfs/live/c6a4781558d84838cc4963fcf94792e54beabe15.png",
# 		             "https://i0.hdslb.com/bfs/live/6920410aca21e3397f23ee7ae5ddbf8f1c625943.png",
# 		             "https://i0.hdslb.com/bfs/live/7e671e053c365f91a0a0f4837ec92ac9581977ec.png"],
# 		"eggshells_icon": "https://i0.hdslb.com/bfs/live/ea6454847e9b9d1b6be03f04f829620b4f0a5d46.svga",
# 		"count_show_time": 15,
# 		"process_icon": "https://i0.hdslb.com/bfs/live/6d96e9de0cc5c80acf3537fe9a23d94da0ab5ff5.png",
# 		"process_color": "#4DFF6699"
# 	}, "live_play_info": {"show_widget_banner": true}, "multi_voice": {"switch_status": 2, "members": []},
# 	"popular_rank_info": {"rank": -2, "countdown": 0, "timestamp": 0, "url": "", "on_rank_name": "", "rank_name": ""},
# 	"new_area_rank_info": {"items": null, "rotation_cycle_time_web": 5}, "gift_star": {"show": true},
# 	"video_connection_info": null, "player_throttle_info": {
# 		"status": 0, "normal_sleep_time": 0, "fullscreen_sleep_time": 0, "tab_sleep_time": 0, "prompt_time": 0
# 	}, "guard_info": {"count": 0, "anchor_guard_achieve_level": 0}, "hot_rank_info": null
# }
# }
GET_STATUS_INFO_BY_UIDS_API_URL = """http://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?"""
# http://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids?uids[0]=466988&uids[1]=359680&uids[2]=28709771
# api_result = {
# 	"code": 0, "msg": "success", "message": "success", "data": {
# 		"466988": {
# 			"title": "DPBMS", "room_id": 18702, "uid": 466988, "online": 2, "live_time": 0, "live_status": 2,
# 			"short_id": 0, "area": 1, "area_name": "单机联机", "area_v2_id": 283, "area_v2_name": "独立游戏",
# 			"area_v2_parent_name": "单机游戏", "area_v2_parent_id": 6, "uname": "天国的一毛君",
# 			"face": "https://i2.hdslb.com/bfs/face/34d15a5ba9aa549ed6433c367d26476cd0524001.jpg",
# 			"tag_name": "以撒,minecraft,饥荒,彩虹六号,东方", "tags": "音游",
# 			"cover_from_user": "https://i0.hdslb.com/bfs/live/new_room_cover/37765b3251e795fd7ffb1c922361e8d5bf256fc7.jpg",
# 			"keyframe": "https://i0.hdslb.com/bfs/live-key-frame/keyframe02031925000000018702av49py.jpg",
# 			"lock_till": "0000-00-00 00:00:00", "hidden_till": "0000-00-00 00:00:00", "broadcast_type": 0
# 		}, "359680": {
# 			"title": "復讐IIDX", "room_id": 22807, "uid": 359680, "online": 9, "live_time": 0, "live_status": 0,
# 			"short_id": 0, "area": 6, "area_name": "生活娱乐", "area_v2_id": 123, "area_v2_name": "户外",
# 			"area_v2_parent_name": "娱乐", "area_v2_parent_id": 1, "uname": "炸鸡块怎么还没来",
# 			"face": "https://i1.hdslb.com/bfs/face/966ed4315b816efdb5bb062f9d030f3be1c8f31a.jpg",
# 			"tag_name": "日常,学习,萌宠,厨艺,手机直播", "tags": "",
# 			"cover_from_user": "https://i0.hdslb.com/bfs/live/new_room_cover/7c01267f5026665a06b702999800d542145144c4.jpg",
# 			"keyframe": "https://i0.hdslb.com/bfs/live-key-frame/keyframe01142254000000022807sy7nv8.jpg",
# 			"lock_till": "0000-00-00 00:00:00", "hidden_till": "0000-00-00 00:00:00", "broadcast_type": 0
# 		}, "28709771": {
# 			"title": "16k 音游 iidx DP", "room_id": 109716, "uid": 28709771, "online": 260, "live_time": 0,
# 			"live_status": 0, "short_id": 0, "area": 1, "area_name": "单机联机", "area_v2_id": 283,
# 			"area_v2_name": "独立游戏", "area_v2_parent_name": "单机游戏", "area_v2_parent_id": 6,
# 			"uname": "菠萝Official",
# 			"face": "https://i2.hdslb.com/bfs/face/551c589ede77e68eafdef5193502fba6505c025a.jpg",
# 			"tag_name": "以撒,minecraft,饥荒,彩虹六号,东方",
# 			"tags": "音乐游戏,音游,节奏大师,OSU,Beatmania,BMS,手速,触手,雷亚,arc,iidx",
# 			"cover_from_user": "https://i0.hdslb.com/bfs/live/new_room_cover/34ef0cf6e26fb462afbff90ce9bf103c9ad4c9ba.jpg",
# 			"keyframe": "https://i0.hdslb.com/bfs/live-key-frame/keyframe02040554000000109716hu6bf4.jpg",
# 			"lock_till": "0000-00-00 00:00:00", "hidden_till": "0000-00-00 00:00:00", "broadcast_type": 0
# 		}
# 	}
# }
# 储存用户直播状态的Dict {uid:0 or 1 or 2} 0关闭 1直播中 2轮播
bilibili_live_notification_list_path = "./Pinebot_main/json/bilibili_live_notification_list.json"

bot = get_bot()
living_list = []  # 当前正在直播中的用户uid List，
unactivate_group = []   # 非通知群

if not os.path.exists(bilibili_live_notification_list_path):
	with open(bilibili_live_notification_list_path, "w", encoding = "utf-8") as f:
		f.write("{}")

# 群和用户的等级直播监控信息
f = open(bilibili_live_notification_list_path, "r", encoding = "utf-8")
data_dic = json.load(f)
f.flush()
f.close()

# 使用bilibili API获取已添加监控用户的直播间状态 错误返回0
def get_live_status_info():
	get_msg = ""
	for group, uid_list_in_group in data_dic.items():
		for i in range(0, len(uid_list_in_group)):
			get_msg += "uids[{}]={}&".format(i, uid_list_in_group[i])
	try:
		result = requests.get(GET_STATUS_INFO_BY_UIDS_API_URL + get_msg)
	except:
		print("更新直播信息错误。")
		return 0
	try:
		result = json.loads(result.text)
	except:
		print("直播信息json分析错误。")
		return 0
	return result

# 添加新用户或重启机器人时初始化 正在直播 列表，不发送提醒信息
def init_living_list():
	global living_list
	living_list = []
	api_result = get_live_status_info()
	# 如果api返回不为空
	if api_result["data"] != []:
		# 循环每个api返回的uid直播信息
		for user in api_result["data"].values():
			# 判断是否在直播
			if user["live_status"] == 1:
				# 在的话 加入正在直播列表
				living_list.append(user["uid"])

init_living_list()
# data_list = {11111: [1, 28709771, 13816323, 4, 5, 6], 22222: [13816323, 2, 3, 4, 5, 6, 359680, 8, 9]}

# 使用api请求直播状态 有直播就发消息
@scheduler.scheduled_job('interval', seconds = 200)
async def _():
	global living_list
	group_id_to_sent = []
	# 获取直播信息结果
	api_result = get_live_status_info()
	# 如果api返回不为空
	if api_result["data"] != []:
		# 循环每个api返回的uid直播信息
		for user in api_result["data"].values():
			# 如果正在直播 判断是否刚上播
			if user["live_status"] == 1:
				# 如果不在 正在直播 列表，则确定为开始直播， 发送消息， 添加进 正在直播 列表
				if user["uid"] not in living_list:
					living_list.append(user["uid"])
					# 找这个uid在哪个群添加了直播监控
					for group_id, group_uid_list in data_dic.items():
						if user["uid"] in group_uid_list:
							# 添加到消息发送群列表
							group_id_to_sent.append(int(group_id))
					# 抓取直播图片
					url = user["keyframe"]
					req = requests.get(url)
					with open("./go-cqhttp/data/images/live_pic.png", 'wb') as f:
						f.write(req.content)
					# 发送消息
					msg = ""
					for i in group_id_to_sent:
						msg = "{} 开始直播。\n{}\nhttp://live.bilibili.com/{}\n[CQ:image,file=live_pic.png]".format(
							user["uname"], user["title"], user["room_id"])
						await bot.send_group_msg(group_id = int(i), message = msg)
					add_raw_log("BILI_LIVE_START", str(group_id_to_sent) + msg)
			
			# 如果不在直播 判断是否刚下播
			elif user["live_status"] == 0 or user["live_status"] == 2:
				# 如果在 正在直播 列表，则判定下播，从 正在直播 列表除去
				if user["uid"] in living_list:
					living_list.remove(user["uid"])

@bot.on_message("group")
async def handle_group_message(ctx):
	global living_list
	global data_dic
	g = ctx["group_id"]
	sg = str(g)
	args = ctx["raw_message"].split()
	if g not in unactivate_group:
		# 列表没有群 添加一个新的kv对
		if sg not in data_dic.keys():
			data_dic[sg] = []
			with open(bilibili_live_notification_list_path, "w", encoding = "utf-8") as f:
				f.write(json.dumps(data_dic, ensure_ascii = False, indent = 1))
		if args[0] == u"-livelist" and len(args) == 1:
			try:
				api_result = get_live_status_info()
			except:
				await bot.send_group_msg(group_id = g, message = u"网络错误")
				return
			if not api_result["data"]:
				await bot.send_group_msg(group_id = g, message = u"监控列表为空")
				return
			msg = "直播监控列表："
			for user in api_result["data"].values():
				# 如果api抓取结果在该群里有的话
				if user["uid"] in data_dic[sg]:
					msg += "\n" + user["uname"]
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
			
			# 如果已有该用户，直接提示
			if isinstance(uid, int):
				if uid in data_dic[sg]:
					await bot.send_group_msg(group_id = g,  message = u"本群直播列表中已存在 " + user_name + " 的直播间 " + room_name + "。")
					return
				# 如果没有 添加 保存 刷新
				elif uid not in data_dic[sg]:
					data_dic[sg].append(uid)
					init_living_list()
					msg = u"成功添加 " + user_name + " 的直播间 " + room_name + " 到监控列表。"
					with open(bilibili_live_notification_list_path, "w", encoding = "utf-8") as f:
						f.write(json.dumps(data_dic, ensure_ascii = False, indent = 1))
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
				# 如果未跟踪 提示
				if uid not in data_dic[sg]:
					await bot.send_group_msg(group_id = g, message = user_name + "还没有登录到本群的直播监控列表。")
					return
				# 如果该群已跟踪 则删除
				else:
					data_dic[sg].remove(uid)
					msg = "成功从监控列表删除 " + user_name + " 的直播间 " + room_name + "。"
					add_raw_log("BILI_LIVE_DEL", msg)
					with open(bilibili_live_notification_list_path, "w", encoding = "utf-8") as f:
						f.write(json.dumps(data_dic, ensure_ascii = False, indent = 1))
					init_living_list()
					await bot.send_group_msg(group_id = g, message = msg)
			else:
				await bot.send_group_msg(group_id = g, message = u"删除失败。")
