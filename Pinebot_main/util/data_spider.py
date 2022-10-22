#!/usr/bin/env python3

__author__ = "Yxzh"

from bs4 import BeautifulSoup
import json
import requests
import urllib.request
import os
from selenium import webdriver


#  因为各难度表名称非常不统一，因此只能一定程度上自动同步。有问题的部分仍需手动更新调整。

optiChar = ["~", "〜", " ", "(", ")", "～", "…", ".", "！", "!", "-", "?", "？", "♥","♨","・", "∀", "Λ", "*", "-", "'", ""]
		
# 更新查找谱面数据:
#   访问url https://textage.cc/score/?a011B000
#   手动创建fumenData.html文件，运行脚本
# dp地理表
# 保存的json文件格式为
# {[曲名，url简称，代数，spb, spn, sph, spa, spl, dpn, dph, dpa, dpl]}
# 全部元素均为字符串
# url简称获取错误时默认为"?"
# 代数获取错误时默认为"0
def updateIIDXSongsList(savePath):
	print("开始从textage的谱面html中抓取歌曲信息。")
	songs = []
	browser = webdriver.Chrome("./chromedriver.exe")
	browser.get("https://textage.cc/score/?a011B000")
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')
	browser.quit()
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
		songs.append(song)
	
	print("抓取完成，正在保存。")
	with open(savePath, "w", encoding = "utf-8") as f:
		f.write(json.dumps(songs, ensure_ascii = False, indent = 1))
	
	print("保存完毕。")
	return songs

def updateCurrentVersionSongsListDataTextageOpti(htmlPath, savePath):
	print("开始从textage的谱面html中抓取歌曲信息。")
	songs = {}
	soup = BeautifulSoup(open(htmlPath, "r", encoding = "utf-8"), 'lxml')
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
		for i in range(len(optiChar)):
			title = title.replace(optiChar[i], "")
		songs[title.lower()] = [[name, gen, spb, spn, sph, spa, spl, dpn, dph, dpa, dpl], ["0", "0", "0"]]
	
	print("抓取完成，正在保存。")
	with open(savePath, "w", encoding = "utf-8") as f:
		f.write(json.dumps(songs, ensure_ascii = False, indent = 1))
	
	print("保存完毕。")
	return songs

def updateDPDiffcultyData(htmlPath, savePath, currentVersionSongsListDataTextage):
	#  错字 修改 Muzik Loverz 为 Musik LoverZ
	print("开始读取DP地力表html")
	soup = BeautifulSoup(open(htmlPath, "r", encoding = "utf-8"), 'lxml')
	songsSoup = soup.body.div.find_all("div", attrs = {"id": "main"})[0].find_all("div")
	print("成功读取DP地力表html")
	songs = currentVersionSongsListDataTextage
	optiVisionInfo = ["(BIS)", "(HSKY)", "(HERO)", "(ROOT)", "(CB)", "(SINO)", "(COP)", "(LC)", "(DJT)", "(9th)", "(EMP)", "(10th)",
	                  "(9th)", "(8th)", "(7th)", "(6th)", "(5th)", "(4th)", "(3rd)", "(2th)", "(1th)", "(0th)"]
	for songSoup in songsSoup:
		temp = songSoup.text.split("\n")
		try:
			while True:
				temp.remove("")
		except:
			pass
		diffcultyLabel = temp[0]
		print("当前难度", diffcultyLabel)
		currentDiffcultySongs = temp[1:]
		for currentDiffcultySong in currentDiffcultySongs:
			if currentDiffcultySong[-2] == "H":
				fumen = 0
			elif currentDiffcultySong[-2] == "A":
				fumen = 1
			elif currentDiffcultySong[-2] == "L":
				fumen = 2
			currentDiffcultySongNameLowerOpti = currentDiffcultySong[:-4]
			for i in range(0, len(optiVisionInfo)):
				currentDiffcultySongNameLowerOpti = currentDiffcultySongNameLowerOpti.replace(optiVisionInfo[i], "")
			for i in range(0, len(optiChar)):
				currentDiffcultySongNameLowerOpti = currentDiffcultySongNameLowerOpti.replace(optiChar[i], "")
			try:
				songs[currentDiffcultySongNameLowerOpti.lower()][1][fumen] = diffcultyLabel
			except:
				print("无法加载", currentDiffcultySong, diffcultyLabel)
			
	
	with open(savePath, "w", encoding = "utf-8") as f:
		f.write(json.dumps(songs, ensure_ascii = False, indent = 1))
	
	return songs

# fldt = updateFumenListDataTextage("./HTML/fumenListData.html", "./JSON/fumenListData.json")

def updateSDVXFumenListData(savePath):
	for level in range(1, 21):
		listURL = "https://sdvx.in/sort/sort_%02d.htm" % level
		strhtml = requests.get(listURL, params='html')
		soup = BeautifulSoup(strhtml.text, encoding = "utf-8" 'lxml')
		songsSoup = soup.body.center.table[1].tbody

# with open("./JSON/currentVersionSongList.json", "r", encoding = "utf-8") as f:
# 	cvsldtnospace = json.load(f)
# 	updateDPDiffcultyData("./HTML/dpDiffcultyData.html", "./JSON/dpDiffcultyData.json", cvsldtnospace)
# updateSDVXFumenListData("")

updateIIDXSongsList("./Pinebot/json/iidx_songs_list.json")