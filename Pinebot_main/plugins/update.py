#!/usr/bin/env python3

__author__ = "Yxzh"

import json
from bs4 import BeautifulSoup
from selenium import webdriver
from nonebot import *


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument('blink-settings=imagesEnabled=false')
prefs = {
	'profile.default_content_setting_values': {
		'notifications': 2
	}
}
chrome_options.add_experimental_option('prefs', prefs)  # 禁用浏览器弹窗

# browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options = chrome_options)
browser = webdriver.Chrome("/usr/bin/chromedriver", options = chrome_options)

bot = get_bot()

@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == u"-update iidx" and len(args) == 1 and ctx["sender"]["user_id"] == 384065633:
		try:
			savePath = "./Pinebot/json/iidx_songs_list.json"
			await bot.send_group_msg(group_id = g, message = "开始更新IIDX谱面数据库。此过程耗时较长。")
			songs = []
			browser.get("https://textage.cc/score/?a011B000")
			html = browser.page_source
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

			with open(savePath, "w", encoding = "utf-8") as f:
				f.write(json.dumps(songs, ensure_ascii = False, indent = 1))

			await bot.send_group_msg(group_id = g, message = "IIDX谱面数据已更新至最新。")
		except:
			await bot.send_group_msg(group_id = g, message = "IIDX谱面数据更新失败。")
	
	if args[0] == u"-update sdvx" and len(args) == 1 and ctx["sender"]["user_id"] == 384065633:
		try:
			await bot.send_group_msg(group_id = g, message = "开始更新SDVX谱面数据。此过程耗时非常长。")
			songs = []
			for i in range(1, 21):
				url = "https://sdvx.in/sort/sort_%02d.htm" % i
				print("Form", url,"get level %d" % i)
				browser.get(url)
				songName = browser.find_elements("xpath","/html/body/center/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td[3]/div")
				fumenType = browser.find_elements("xpath","/html/body/center/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/table/tbody/tr/td//div")
				
				currentLevelSongsCount = len(songName)
				for j in range(0, currentLevelSongsCount):
					currentFumenType = fumenType[j].get_attribute("class")
					if currentFumenType == "f2":
						currentFumenType = "m2"
					currentSong = [songName[j].text, currentFumenType, fumenType[j].text, fumenType[j].find_element("xpath","..").get_attribute("href")]
					songs.append(currentSong)
					print(j, "/", currentLevelSongsCount, "\t", currentSong)
			browser.close()
			browser.quit()
			with open("./Pinebot_main/json/SDVXData.json", "w", encoding = "utf-8") as f:
				f.write(json.dumps(songs, ensure_ascii = False, indent = 1))
			await bot.send_group_msg(group_id = g, message = "SDVX谱面数据已更新至最新。")
		except:
			await bot.send_group_msg(group_id = g, message = "SDVX谱面数据更新失败。")

		