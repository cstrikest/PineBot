#!/usr/bin/env python3

__author__ = "Yxzh"

import json
import time
import Pinebot_main.util.Chrome_Driver as Chrome_Driver
from bs4 import BeautifulSoup
from nonebot import *


bot = get_bot()

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	if ctx["raw_message"] == u"-update iidx" and ctx["sender"]["user_id"] == 384065633:
		try:
			await bot.send_group_msg(group_id = g, message = "开始更新IIDX谱面数据库。此过程耗时较长。")
			songs = []
			Chrome_Driver.browser.get("https://textage.cc/score/?a011B000")
			html = Chrome_Driver.browser.page_source
			soup = BeautifulSoup(html, 'html.parser')
			songsSoup = soup.body.center.find_all("table")[1].find_all("tr")[1:]
			for songSoup in songsSoup:
				infoSoup = songSoup.find_all("td")
				title = ""
				name = "?"
				gen = "0"

				for s in infoSoup[5].strings:
					title += s
				title.replace("\\n", "")

				spb = infoSoup[7].img["src"][4:].replace(".gif", "")
				spn = infoSoup[3].img["src"][4:].replace(".gif", "")
				sph = infoSoup[2].img["src"][4:].replace(".gif", "")
				spa = infoSoup[1].img["src"][4:].replace(".gif", "")
				spl = infoSoup[0].img["src"][4:].replace(".gif", "")
				dpn = infoSoup[8].img["src"][4:].replace(".gif", "")
				dph = infoSoup[9].img["src"][4:].replace(".gif", "")
				dpa = infoSoup[10].img["src"][4:].replace(".gif", "")
				dpl = infoSoup[11].img["src"][4:].replace(".gif", "")

				if spn != "0" and infoSoup[3].a != None:
					name = infoSoup[3].a["href"].split("/")[1].split(".html?")[0]
					gen = infoSoup[3].a["href"].split("/")[0]
				elif sph != "0" and infoSoup[2].a != None:
					name = infoSoup[2].a["href"].split("/")[1].split(".html?")[0]
					gen = infoSoup[2].a["href"].split("/")[0]
				elif spa != "0" and infoSoup[1].a != None:
					name = infoSoup[1].a["href"].split("/")[1].split(".html?")[0]
					gen = infoSoup[1].a["href"].split("/")[0]

				song = [title, name, gen, spb, spn, sph, spa, spl, dpn, dph, dpa, dpl]
				print(song)
				songs.append(song)

			with open("./Pinebot_main/json/iidx_songs_list.json", "w", encoding = "utf-8") as f:
				f.write(json.dumps(songs, ensure_ascii = False, indent = 1))

			await bot.send_group_msg(group_id = g, message = "IIDX谱面数据已更新至最新。")
		except Exception as e:
			print(e)
			await bot.send_group_msg(group_id = g, message = "IIDX谱面数据更新失败。")
	
	if ctx["raw_message"] == u"-update sdvx" and ctx["sender"]["user_id"] == 384065633:
		try:
			await bot.send_group_msg(group_id = g, message = "开始更新SDVX谱面数据。此过程耗时非常长。")
			songs = []
			for i in range(1, 21):
				url = "https://sdvx.in/sort/sort_%02d.htm" % i
				print("Form", url,"get level %d" % i)
				Chrome_Driver.browser.get(url)
				songName = Chrome_Driver.browser.find_elements("xpath","/html/body/center/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/div")
				fumenType = Chrome_Driver.browser.find_elements("xpath","/html/body/center/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/table/tbody/tr/td//div")
				
				currentLevelSongsCount = len(songName)
				for j in range(0, currentLevelSongsCount):
					currentFumenType = fumenType[j].get_attribute("class")
					if currentFumenType == "f2":
						currentFumenType = "m2"
					currentSong = [songName[j].text, currentFumenType, fumenType[j].text, fumenType[j].find_element("xpath","..").get_attribute("href")]
					songs.append(currentSong)
					print(j, "/", currentLevelSongsCount, "\t", currentSong)
			with open("./Pinebot_main/json/SDVXData.json", "w", encoding = "utf-8") as f:
				f.write(json.dumps(songs, ensure_ascii = False, indent = 1))
			await bot.send_group_msg(group_id = g, message = "SDVX谱面数据已更新至最新。")
		except:
			await bot.send_group_msg(group_id = g, message = "SDVX谱面数据更新失败。")
	
	if ctx["raw_message"] == u"-update bms" and ctx["sender"]["user_id"] == 384065633:
		try:
			await bot.send_group_msg(group_id = g, message = "开始更新BMS谱面数据。此过程耗时非常长。")
			
			bms_songs_h1 = []
			level = 0
			Chrome_Driver.browser.get("http://www.ribbit.xyz/bms/tables/insane.html")
			time.sleep(2)
			for tr in Chrome_Driver.browser.find_elements("xpath", "/html/body/div/div[6]/div/table/tbody/tr"):
				if "level_group" in tr.get_attribute("class").split(" "):
					level += 1
				else:
					data = tr.find_elements("xpath", "td")
					name = data[1].text
					artist = data[2].text
					url = data[4].find_element("tag name", "a").get_attribute("href")
					data = [level, name, artist, url]
					bms_songs_h1.append(data)
					print(data)
			
			with open("./Pinebot_main/json/bms_songs_h1_list.json", "w", encoding = "utf-8") as f:
				f.write(json.dumps(bms_songs_h1, ensure_ascii = False, indent = 1))		
			await bot.send_group_msg(group_id = g, message = "BMS谱面数据已更新至最新。")
			
		except Exception as e:
			print(e)
			await bot.send_group_msg(group_id = g, message = "BMS谱面数据更新失败。")
			