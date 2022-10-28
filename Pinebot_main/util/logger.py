#!/usr/bin/env python3

__author__ = "Yxzh"

import time


MSG_LOG_FILE_PATH = "./msg_log.log"

def add_log(event_name: str, ctx, msg: str):
	with open(MSG_LOG_FILE_PATH, "a", encoding = "utf-8") as f:
		f.write("[{} - {}] QQ:{} Group: {} Group_card:{} Nickname:{} || {}\n".format(
			time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), event_name, ctx["sender"]["user_id"], ctx["group_id"],
			ctx["sender"]["card"], ctx["sender"]["nickname"], msg).replace("\n", "") + "\n")
		f.flush()

def add_raw_log(event_name: str, msg: str):
	with open(MSG_LOG_FILE_PATH, "a", encoding = "utf-8") as f:
		f.write("[{} - {}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), event_name, msg).replace("\n", "") + "\n")
		f.flush()
