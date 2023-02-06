#!/usr/bin/env python3

__author__ = "Yxzh"

from nonebot import *
from Pinebot_main.util.logger import *

bot = get_bot()

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == u"-help" and len(args) == 1:
		add_log("HELP", ctx, "Show help msg.")
		await bot.send_group_msg(group_id = g, message = "[CQ:image,file=help.png]")

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
