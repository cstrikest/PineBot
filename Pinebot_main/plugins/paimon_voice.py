#!/usr/bin/env python3

__author__ = "Yxzh"

import sys
sys.path.insert(0, './Pinebot_main/VITS_Paimon/')

from nonebot import *
import torch
import Pinebot_main.VITS_Paimon.commons as commons
import Pinebot_main.VITS_Paimon.utils as utils
from Pinebot_main.VITS_Paimon.models import SynthesizerTrn
from Pinebot_main.VITS_Paimon.text.symbols import symbols
from Pinebot_main.VITS_Paimon.text import text_to_sequence
import soundfile as sf
import gc
from Pinebot_main.util.logger import add_log

bot = get_bot()

def get_text(text, hps):
	text_norm = text_to_sequence(text, hps.data.text_cleaners)
	if hps.data.add_blank:
		text_norm = commons.intersperse(text_norm, 0)
	text_norm = torch.LongTensor(text_norm)
	return text_norm


hps = utils.get_hparams_from_file("./Pinebot_main/VITS_Paimon/configs/biaobei_base.json")
net_g = SynthesizerTrn(
	len(symbols),
	hps.data.filter_length // 2 + 1,
	hps.train.segment_size // hps.data.hop_length,
	**hps.model)
net_g.eval()

utils.load_checkpoint('./Pinebot_main/VITS_Paimon/G_1434000.pth', net_g, None)

# torch.load('./Pinebot_main/VITS_Paimon/G_1434000.pth', map_location='cpu')


def get_paimon_voice_file(text: str):
	stn_tst = get_text(text, hps)
	with torch.no_grad():
		x_tst = stn_tst.unsqueeze(0)
	x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
	audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1.5)[0][0,0].data.numpy()
	net_g.zero_grad()
	# ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate))
	sf.write("./go-cqhttp/data/voices/paimon.wav",audio,samplerate=hps.data.sampling_rate)
	
	torch.cuda.empty_cache()
	del audio
	del stn_tst
	del x_tst
	del x_tst_lengths
	gc.collect()



@bot.on_message("group")
async def handle_group_message(ctx):
	g = ctx["group_id"]
	args = ctx["raw_message"].split()
	if args[0] == u"派蒙" and len(args) > 1:
		if len(ctx["raw_message"]) < 30:
			get_paimon_voice_file(args[1:])
			add_log(ctx, ctx["raw_message"])
			await bot.send_group_msg(group_id = g, message = "[CQ:record,file=paimon.wav]")
		else:
			await bot.send_group_msg(group_id = g, message = "消息太长。")
		
		