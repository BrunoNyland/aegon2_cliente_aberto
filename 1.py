#favor manter essa linha
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import zn94xlgo573hf8xmddzq as net
import LURMxMaKZJqliYt2QSHG as chat
import enszxc3467hc3kokdueq as app
import Js4k2l7BrdasmVRt8Wem as chr
# import player, item, chat, net
import ui
import os
import snd
import dbg
import ime
import grp
import shop
import wndMgr
import uicommon
import mousemodule
from uitooltip import ItemToolTip
import sys

class TESTADOR(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __LoadWindow(self):
		self.__LoadScript("uiscript/inputdialogwithdescription.py")

# x = TESTADOR()
# x.Show()
# chr.Update()
# chr.PushOnceMotion(chr.MOTION_ATTRACTIVE, 0.1)