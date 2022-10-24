#!/usr/bin/env python3

__author__ = "Yxzh"

import time 


MSG_LOG_FILE_PATH = "./msg_log.log"

def add_log(ctx, msg: str):
	with open(MSG_LOG_FILE_PATH, "a", encoding = "utf-8") as f:
		f.write("[{}] QQ:{} Group: {} Group_card:{} Nickname:{} || {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ctx["sender"]["user_id"],ctx["group_id"] , ctx["sender"]["card"], ctx["sender"]["nickname"], msg))
		f.flush()