#!/usr/bin/env python3

__author__ = "Yxzh"

from nonebot import *
import json

bot = get_bot()

with open("./Pinebot_main/json/live_notification_activate_group.json", "r") as f:
	activate_group = json.load(f)
	
msg_iidx = """IIDX谱面查询

-spa 旅人
-dpl be quiet
以此类推。
同时可附加-m查询镜像谱面，-o 开始小节数 结束小节数来指定谱面范围，-1P或-2P指定谱面左右侧等。"""

msg_sdvx = """SDVX谱面查询

查询最高难度谱面：
-sv <曲名>
查询对应难度谱面：
-svn (NOVICE)
-sva (ADVANCED)
-sve (EXHAUST)
-svm (MAXIMUM)
-svi (INFINITE)
-svg (GRAVITY)
-svh (HEAVENLY)
-svv (VIVID)
6代部分谱面暂时缺少数据。"""

msg_live = """直播监控

-livelist 直播监控列表
-liveadd <房间号>添加直播监控
-livedel <房间号>移除直播监控"""

msg_dx = """随机选曲

指定等级随机：
-dxsp 10
-dxdp 12
全曲随机：
-dx"""
msg_ex = """曲名查询为模糊搜索，请尽量按照原曲名输入完整单词进行查询。
另外这破机器人是跑在一个学校地上捡的（真的）树莓派上，速度还是慢了些。"""
@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == u"-help" and len(args) == 1:
		# await bot.send_group_msg(group_id = g, message = "[CQ:image,file=help.png]")
		await bot.send_group_msg(group_id = g, message = msg_iidx)
		await bot.send_group_msg(group_id = g, message = msg_dx)
		await bot.send_group_msg(group_id = g, message = msg_sdvx)
		# await bot.send_group_msg(group_id = g, message = msg_ex)
		if g in activate_group:
			await bot.send_group_msg(group_id = g, message = msg_live)


# {
# 'anonymous': None,
# 'font': 8159712,
# 'group_id': 176763307,
# 'message': [{'type': 'text', 'data': {'text': '-骂街'}}],
# 'message_id': 120619,
# 'message_type': 'group',
# 'post_type': 'message',
# 'raw_message': '-骂街',
# 'self_id': 3434696172,
# 'sender': {
#           'age': 0,
#           'area': '',
#           'card': '蝴蝶 KB★09-113104/BM★05-118523',
#           'level': '★★',
#           'nickname': 'MsrButterfly',
#           'role': 'member',
#           'sex': 'unknown',
#           'title': '',
#           'user_id': 1030487187
#           },
# 'sub_type': 'normal',
# 'time': 1593492424,
# 'user_id': 1030487187
# }

# {'anonymous': None, 'font': 0, 'group_id': 558351394,
#  'message': [{'type': 'text', 'data': {'text': '- '}},
#              {'type': 'at', 'data': {'qq': '3434696172'}},
#              {'type': 'text', 'data': {'text': ' '}}],
#  'message_id': 47536,
#  'message_seq': 47536,
#  'message_type': 'group',
#  'post_type': 'message',
#  'raw_message': '- [CQ:at,qq=3434696172] ',
#  'self_id': 3434696172,
#  'sender': {
# 	 'age': 0,
# 	 'area': '',
# 	 'card': '',
# 	 'level': '',
# 	 'nickname': '菠萝',
# 	 'role': 'owner',
# 	 'sex': 'unknown',
# 	 'title': '',
# 	 'user_id': 384065633
#  },
#  'sub_type': 'normal',
#  'time': 1613330482,
#  'user_id': 384065633
# }