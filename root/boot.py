#favor manter essa linha

### from client binary
import _player as player
import _item as item
import _net as net
import _chat as chat
import _app as app
import _snd as snd
import _dbg as dbg
import _wnd_mgr as wndMgr
import _ime as ime
import _grp as grp

### from python3
import os

### from root
import ui
import uicommon
import mousemodule
import constinfo

from uitooltip import ItemToolTip
from weakref import proxy

WEAR_NAMES = ItemToolTip.WEAR_NAMES
AFFECT_DICT = ItemToolTip.AFFECT_DICT

###################################################################################################################################################
### CONFIGURACOES ### CONFIGURACOES ### CONFIGURACOES ### CONFIGURACOES ### CONFIGURACOES ### CONFIGURACOES ### CONFIGURACOES ### CONFIGURACOES ###
###################################################################################################################################################
SWITCH_VNUM = 71084
SWITCH_RARE_VNUM = 71052
MIN_SWITCH_DELAY = 0
MAX_SWITCH_DELAY_APPEND = 120
MAX_NUM = 7
DISTANCE_BOTTOM = 36
## Bonus select by SubType - Use if item.GetItemType() == item.ITEM_TYPE_ARMOR or item.ITEM_TYPE_WEAPON
## and item.GetItemSubType() in (item.ARMOR_BODY, item.ARMOR_HEAD, item.ARMOR_SHIELD, item.ARMOR_WRIST, item.ARMOR_FOOTS, item.ARMOR_NECK, item.ARMOR_EAR)

MAX_NUM_FOR_BONUS = {
	1:2000,
	2:80,
	3:12,
	4:12,
	5:12,
	6:12,
	7:8,
	8:20,
	9:20,
	10:50,
	11:30,
	12:8,
	13:8,
	14:8,
	15:10,
	16:10,
	17:15,
	18:20,
	19:20,
	20:20,
	21:20,
	22:20,
	23:10,
	24:10,
	25:10,
	27:15,
	28:15,
	29:15,
	30:15,
	31:15,
	32:15,
	33:15,
	34:15,
	35:15,
	36:15,
	37:15,
	38:15,
	39:10,
	41:5,
	43:20,
	44:20,
	45:20,
	48:1,
	49:1,
	53:50,
	59:15,
	60:15,
	61:15,
	62:15,
	63:10,
	71:30,
	72:60,
	78:15,
	79:15,
	80:15,
	81:15,
}


WEAPON_DS_LIST = [
	180,181,182,183,184,185,186,187,188,189,
	190,191,192,193,194,195,196,197,198,199,
	260,261,262,263,264,265,266,267,268,269,
	270,271,272,273,274,275,276,277,278,279,
	290,291,292,293,294,295,296,297,298,299,
	1170,1171,1172,1173,1174,1175,1176,1177,1178,1179,
	2150,2151,2152,2153,2154,2155,2156,2157,2158,2159,
	2170,2171,2172,2173,2174,2175,2176,2177,2178,2179,
	3160,3161,3162,3163,3164,3165,3166,3167,3168,3169,
	3210,3211,3212,3213,3214,3215,3216,3217,3218,3219,
	5110,5111,5112,5113,5114,5115,5116,5117,5118,5119,
	5120,5121,5122,5123,5124,5125,5126,5127,5128,5129,
	6010,6011,6012,6013,6014,6015,6016,6017,6018,6019,
	7160,7161,7162,7163,7164,7165,7166,7167,7168,7169,
	1130,1131,1132,1133,1134,1135,1136,1137,1138,1139,
]

BONUS_FOR_WEAPONS		= [3,4,5,6,9,12,13,14,15,16,17,18,19,20,21,22,59,60,61,62,]
BONUS_FOR_WEAPONS_DS	= [3,4,5,6,9,12,13,14,15,16,17,18,19,20,21,22,59,60,61,62,71,72,]

BONUS_BY_SUBTYPES = {
	item.ARMOR_BODY:		[1,9,23,24,29,30,31,32,33,34,35,36,37,38,39,53,78,79,80,81,],
	item.ARMOR_HEAD:		[7,10,11,12,17,18,19,20,21,22,24,28,35,36,37,38,59,60,61,62,],
	item.ARMOR_SHIELD:		[3,4,5,6,17,18,19,20,21,22,27,39,43,44,49,48,],
	item.ARMOR_WRIST:		[1,2,16,17,18,19,20,21,22,23,25,35,36,37,38,45,],
	item.ARMOR_FOOTS:		[1,2,7,8,13,14,15,28,29,30,31,32,33,34,43,44,59,60,61,62,],
	item.ARMOR_NECK:		[1,2,10,11,13,15,16,24,29,30,31,32,33,34,43,44,78,79,80,81,],
	item.ARMOR_EAR:			[8,17,18,19,20,21,22,25,29,30,31,32,33,34,41,45,],
}

BONI_AVAIL = [1,2,3,4,5,6,9,10,12,13,14,15,16,17,23,27,28,29,30,31,32,33,34,37,39,41,43,44,45,48,53,59,60,61,62,63,71,72,]
BONI_RARE_AVAIL = [1,2,3,4,5,6,7,8,15,16,53,59,60,61,62,63,78,79,80,81,]

MAX_NUM_FOR_BONUS_RARE = {
	1:500,
	2:50,
	3:5,
	4:5,
	5:5,
	6:5,
	7:2,
	8:8,
	15:5,
	16:5,
	53:50,
	59:10,
	60:10,
	61:10,
	62:10,
	63:10,
	78:5,
	79:5,
	80:5,
	81:5,
}

###################################################################################################################################################
### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES ### CORES #######
###################################################################################################################################################
# Proporção das cores do Paint.Net para converter para Metin2: [% 2,54]
COLOR_BG = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
COLOR_INACTIVE = grp.GenerateColor(1.0, 0.0, 0.0, 0.2)
COLOR_ACTIVE   = grp.GenerateColor(1.0, 0.6, 0.1, 0.2)
COLOR_FINISHED = grp.GenerateColor(0.0, 1.0, 0.0, 0.2)
COLOR_INACTIVE_RARE = grp.GenerateColor(1.0, 0.2, 0.0, 0.2)
COLOR_ACTIVE_RARE   = grp.GenerateColor(1.0, 0.7, 0.2, 0.2)
COLOR_HIGHLIGHT_RARE = grp.GenerateColor(1.0, 0.2, 0.2, 0.05)
COLOR_PIN_HINT = grp.GenerateColor(1.0, 1.0, 0.8, 0.5)
COLOR_CHECKBOX_NOT_SELECTED = grp.GenerateColor(1.0, 0.3, 0.0, 0.1)
COLOR_CHECKBOX_SELECTED = grp.GenerateColor(0.3, 1.0, 1.0, 0.3)
COLOR_NAME_SELECTED = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
COLOR_DROP_DOWN_NORMAL = 0xc0000000
COLOR_DROP_DOWN_OVER = 0xc00a0a0a
COLOR_DROP_DOWN_BOX = grp.GenerateColor(0.208, 0.142, 0.126, 1.0)
COLOR_DROP_DOWN_ITEM_SELECT = grp.GenerateColor(0.5, 0.3, 0.2, 0.3)

### CONFIGURACOES de BONUS SALVAS ###
proposals = {
	item.ITEM_TYPE_WEAPON: {
	},
	item.ITEM_TYPE_ARMOR: {
		item.ARMOR_BODY: {},
		item.ARMOR_HEAD: {},
		item.ARMOR_SHIELD: {},
		item.ARMOR_WRIST: {},
		item.ARMOR_FOOTS: {},
		item.ARMOR_NECK: {},
		item.ARMOR_EAR: {},
	},
}

def ReturnSavedOptions():
	if not os.path.exists("miles/bonus.cfg"):
		file = open("miles/bonus.cfg", "w", "file")
		file.write("")
		file.close()

	lines = open("miles/bonus.cfg", "r", "folder").readlines()
	return lines

def RemoveLine(line_to_remove):
	temp = []
	lines = ReturnSavedOptions()
	if len(lines) == 0:
		return

	for line in lines:
		if line_to_remove != line:
			temp.append(line)

	writer = open("miles/bonus.cfg", "w", "folder")
	writer.write("")
	for line in temp:
		writer.write(line)
		if (len(line) > 0 and line[-1:] != "\n") or len(line) == 0:
			writer.write("\n")
	writer.close()

def LoadSavedOptions():
	lines = ReturnSavedOptions()
	if len(lines) == 0:
		return

	for line in lines:
		data = line.split("\t")
		if len(data) != int(23):
			RemoveLine(line)
			continue
		try:
			tmp = [
				[int(data[3]), int(data[4])],
				[int(data[5]), int(data[6])],
				[int(data[7]), int(data[8])],
				[int(data[9]), int(data[10])],
				[int(data[11]), int(data[12])],
				[int(data[13]), int(data[14])],
				[int(data[15]), int(data[16])],
				[int(data[17]), int(data[18])],
				[int(data[19]), int(data[20])],
				[int(data[21]), int(data[22])],
			]
		except BaseException:
			RemoveLine(line)
			continue

		if int(data[0]) == 1:
			proposals[1][data[2]] = tmp
		elif int(data[0]) == 2:
			proposals[2][int(data[1])][data[2]] = tmp

def RemoveSavedOption(name):
	temp = []
	lines = ReturnSavedOptions()
	if len(lines) == 0:
		return

	for line in lines:
		data = line.split("\t")
		if str(data[2]) != str(name):
			temp.append(line)

	open
	writer = open("miles/bonus.cfg", "w", "folder")
	writer.write("")

	for line in temp:
		writer.write(line)
		if (len(line) > 0 and line[-1:] != "\n") or len(line) == 0:
			writer.write("\n")
	writer.close()

def AddNewOption(type, subtype, name, options):
	temp = []
	new_line = str(type) + "\t" + str(subtype) + "\t" + str(name)
	for it in options:
		new_line += "\t"
		new_line += str(it)

	lines = ReturnSavedOptions()
	writer = open("miles/bonus.cfg", "w", "folder")
	for line in lines:
		writer.write(line)
		if (len(line) > 0 and line[-1:] != "\n") or len(line) == 0:
			writer.write("\n")
	writer.write(new_line)
	writer.close()

class BonusSelector(ui.Window):
	def Activate(self):
		self.sub_parent.resetSwitch()
		self.sub_parent.StatusBar.SetColor(COLOR_ACTIVE)
		self.sub_parent.StatusText.SetText("Ativo")
		self.Starter.SetText("Slot ("+str(self.index+1)+") Parar")
		self.sub_parent.boni_active = 1
		self.Starter.SetEvent(self.Deactivate)
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.swib_normal.SetColor(COLOR_ACTIVE)

	def Deactivate(self):
		self.sub_parent.resetSwitch()
		self.sub_parent.StatusBar.SetColor(COLOR_INACTIVE)
		self.sub_parent.StatusText.SetText("Inativo")
		self.Starter.SetText("Slot ("+str(self.index+1)+") Iniciar")
		self.sub_parent.boni_active = 0
		self.Starter.SetEvent(self.Activate)
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.swib_normal.SetColor(COLOR_INACTIVE)

	def Activate_rare(self):
		self.sub_parent.resetSwitch_rare()
		self.sub_parent.StatusBar_rare.SetColor(COLOR_ACTIVE_RARE)
		self.sub_parent.StatusText_rare.SetText("Ativo")
		self.Starter_rare_boni.SetText("Parar (6-7)")
		self.sub_parent.boni_rare_active = 1
		self.Starter_rare_boni.SetEvent(self.Deactivate_rare)
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.swib_rare.SetColor(COLOR_ACTIVE_RARE)

	def Deactivate_rare(self):
		self.sub_parent.resetSwitch_rare()
		self.sub_parent.StatusBar_rare.SetColor(COLOR_INACTIVE_RARE)
		self.sub_parent.StatusText_rare.SetText("Inativo")
		self.Starter_rare_boni.SetText("Iniciar (6-7)")
		self.sub_parent.boni_rare_active = 0
		self.Starter_rare_boni.SetEvent(self.Activate_rare)
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.swib_rare.SetColor(COLOR_INACTIVE_RARE)

	def Finish(self):
		self.sub_parent.StatusBar.SetColor(COLOR_FINISHED)
		self.sub_parent.StatusText.SetText("Pronto")
		self.Starter.SetText("Slot ("+str(self.index+1)+") Iniciar")
		self.sub_parent.boni_active = 0
		self.Starter.SetEvent(self.Activate)
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.swib_normal.SetColor(COLOR_FINISHED)

	def Finish_rare(self):
		self.sub_parent.StatusBar_rare.SetColor(COLOR_FINISHED)
		self.sub_parent.StatusText_rare.SetText("Pronto")
		self.Starter_rare_boni.SetText("Inicar (6-7)")
		self.sub_parent.boni_rare_active = 0
		self.Starter_rare_boni.SetEvent(self.Activate_rare)
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.swib_rare.SetColor(COLOR_FINISHED)

	def Block(self):
		self.BlockBar.Show()
		self.BlockBar.sub.Show()
		self.Starter.Hide()

	def Unblock(self):
		self.BlockBar.sub.Hide()
		self.BlockBar.Hide()
		self.Starter.Show()

	def enable_rare_boni(self):
		self.sub_parent.StatusBar_rare.Show()
		self.Block3.Hide()
		self.Starter.SetWidth(145)
		self.Starter_rare_boni.Show()
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.Enable_rare(1)

	def disable_rare_boni(self):
		self.sub_parent.StatusBar_rare.Hide()
		self.Block3.Show()
		self.Starter.SetWidth(245)
		self.Starter_rare_boni.Hide()
		self.Deactivate_rare()
		if self.sub_parent.parentWindow.parentWindow.wndInventory != None:
			self.sub_parent.blockBar.Enable_rare(0)

	def enable_extra(self):
		self.Block2.Hide()

	def disable_extra(self):
		self.Block2.Show()

	def __init__(self, sub_parent, main):
		ui.Window.__init__(self, "UI")
		self.sub_parent = sub_parent
		self.index = sub_parent.index
		self.main = main
		self.SetSize(500, 255)
		self.boni = {}
		self.boni_extra = {}

		self.Box1 = ui.MakeImageBox(self, "interface/controls/special/boot/box.tga", 8, 6)
		self.Box2 = ui.MakeImageBox(self, "interface/controls/special/boot/box.tga", 8 + 241 + 2, 6)
		self.Box3 = ui.MakeImageBox(self, "interface/controls/special/boot/box2.tga", 8, 6 + 150 + 2)
		self.Box4 = ui.MakeImageBox(self, "interface/controls/special/boot/box3.tga", 8 + 241 + 2, 6 + 150 + 2 + 28)

		self.EnableRareBoni = MakeCheckBox("Ativar 6º e 7º Bônus", self.Box3, 1, 1, self.disable_rare_boni, self.enable_rare_boni)
		self.EnableSecondOption = MakeCheckBox("Ativar 2º Opção de Bônus", self.Box2, 1, 1, self.disable_extra, self.enable_extra)

		self.but_propose = DropDown(self, "Opções Salvas")
		self.but_propose.SetParent(self)
		self.but_propose.SetPosition(self.Box4.GetLeft() + 7, self.Box4.GetTop() + 13)
		self.but_propose.OnChange = ui.__mem_func__(self.change_boni)
		self.but_propose.AppendItem("Limpar", [])
		self.but_propose.SetSize(150, 20)
		self.but_propose.Show()

		self.SaveButton = ui.RedButton()
		self.SaveButton.SetParent(self)
		self.SaveButton.SetPosition(self.but_propose.GetRight() + 6, self.but_propose.GetTop()-3)
		self.SaveButton.SetWidth(58)
		self.SaveButton.SetText("Salvar")
		self.SaveButton.Show()
		self.SaveButton.SetEvent(self.Save_Pre)

		self.DelButton = ui.RedButton()
		self.DelButton.SetParent(self)
		self.DelButton.SetPosition(self.but_propose.GetRight() + 6, self.but_propose.GetTop()-3)
		self.DelButton.SetWidth(58)
		self.DelButton.SetText("Deletar")
		self.DelButton.Hide()
		self.DelButton.SetEvent(self.Delete_Pre)

		self.Starter_rare_boni = ui.RedButton()
		self.Starter_rare_boni.SetParent(self)
		self.Starter_rare_boni.SetPosition(249+145, 158)
		self.Starter_rare_boni.SetWidth(100)
		self.Starter_rare_boni.SetText("Iniciar (6-7)")
		self.Starter_rare_boni.SetEvent(self.Activate_rare)
		self.Starter_rare_boni.Hide()

		self.Starter = ui.RedButton()
		self.Starter.SetParent(self)
		self.Starter.SetPosition(249, 158)
		self.Starter.SetWidth(245)
		self.Starter.SetText("Iniciar o Bot")
		self.Starter.SetEvent(self.Activate)
		self.Starter.Show()

		for i in range(7, 5, -1):
			vas = i
			self.boni[vas] = {}
			self.boni[vas][0] = DropDown(self.Box3, "Escolha o "+ str(vas) +"º Bônus")
			self.boni[vas][0].SetPosition(7, 22 + 25 * (vas -6))
			for x in AFFECT_DICT:
				if x in BONI_RARE_AVAIL:
					self.boni[vas][0].AppendItem(str(AFFECT_DICT[x](0)),x)
			self.boni[vas][0].SetSize(180, 20)
			self.boni[vas][0].Show()
			self.boni[vas][1] = BoxNotEdit()
			self.boni[vas][1].SetParent(self.Box3)
			self.boni[vas][1].SetSize(40, 20)
			self.boni[vas][1].SetColor(0xC0000000)
			self.boni[vas][1].SetPosition(self.boni[vas][0].GetRight() + 6, 22 + 25 * (vas -6))
			self.boni[vas][0].SetEditBoxLine(self.boni[vas][1].Line)
			self.boni[vas][1].Show()

### VERIFICAR O TIPO DO ITEM ### VERIFICAR O TIPO DO ITEM ### VERIFICAR O TIPO DO ITEM ###
		vnum = player.GetItemIndex(self.index)
		item.SelectItem(vnum)
### SELCIONA OS ADDS DISPONIVEIS PARA O ITEM ### SELCIONA OS ADDS DISPONIVEIS PARA O ITEM ###
		if item.GetItemType() == item.ITEM_TYPE_WEAPON:
			if vnum in WEAPON_DS_LIST:
				BONUS_LIST = BONUS_FOR_WEAPONS_DS
			else:
				BONUS_LIST = BONUS_FOR_WEAPONS
		elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
			BONUS_LIST = BONUS_BY_SUBTYPES[item.GetItemSubType()]
		else:
			BONUS_LIST = BONI_AVAIL
### BONUS DE 1-5 ### BONUS DE 1-5 ### BONUS DE 1-5 ### BONUS DE 1-5 ### BONUS DE 1-5 ###
		for i in range(0, 5):
			vas = 5 - i
			self.boni[vas] = {}
			self.boni[vas][0] = DropDown(self.Box1, "Escolha o "+ str(vas) +"º Bônus")
			self.boni[vas][0].SetPosition(7, 22 + 25 * (vas -1))
			for x in AFFECT_DICT:
				if x in BONUS_LIST:
					self.boni[vas][0].AppendItem(str(AFFECT_DICT[x](0)), x)
			self.boni[vas][0].SetSize(180, 20)
			self.boni[vas][0].OnChange2 = ui.__mem_func__(self.OnChangeBonus)
			self.boni[vas][0].Show()
			self.boni[vas][1] = BoxEdit2("0", 4)
			self.boni[vas][1].SetColor(0xC0000000)
			self.boni[vas][1].SetParent(self.Box1)
			self.boni[vas][1].SetSize(40, 20)
			self.boni[vas][1].SetPosition(self.boni[vas][0].GetRight() + 6, 22 + 25 * (vas -1))
			self.boni[vas][0].SetEditBoxLine(self.boni[vas][1].Line)
			self.boni[vas][1].Show()

		self.boni[5][1].Line.SetNextTab(self.boni[1][1].Line)
		for i in range(1, 5):
			self.boni[i][1].Line.SetNextTab(self.boni[i+1][1].Line)
### BONUS EXTRA 1-5 ### BONUS EXTRA 1-5 ### BONUS EXTRA 1-5 ### BONUS EXTRA 1-5 ### BONUS EXTRA 1-5 ###
		for i in range(0, 5):
			vas = 5 - i
			self.boni_extra[vas] = {}
			self.boni_extra[vas][0] = DropDown(self.Box2, "Escolha o "+ str(vas) +"º Bônus")
			self.boni_extra[vas][0].SetPosition(7, 22 + 25 * (vas -1))
			for x in AFFECT_DICT:
				if x in BONUS_LIST:
					self.boni_extra[vas][0].AppendItem(str(AFFECT_DICT[x](0)), x)
			self.boni_extra[vas][0].SetSize(180, 20)
			self.boni_extra[vas][0].OnChange2 = ui.__mem_func__(self.OnChangeBonus)
			self.boni_extra[vas][0].Show()
			self.boni_extra[vas][1] = BoxEdit2("0", 4)
			self.boni_extra[vas][1].SetColor(0xC0000000)
			self.boni_extra[vas][1].SetParent(self.Box2)
			self.boni_extra[vas][1].SetSize(40, 20)
			self.boni_extra[vas][1].SetPosition(self.boni_extra[vas][0].GetRight() + 6, 22 + 25 * (vas -1))
			self.boni_extra[vas][0].SetEditBoxLine(self.boni_extra[vas][1].Line)
			self.boni_extra[vas][1].Show()

		self.boni_extra[5][1].Line.SetNextTab(self.boni_extra[1][1].Line)
		for i in range(1, 5):
			self.boni_extra[i][1].Line.SetNextTab(self.boni_extra[i+1][1].Line)

		self.BlockBar = ui.Bar()
		self.BlockBar.SetParent(self)
		self.BlockBar.SetColor(COLOR_INACTIVE)
		self.BlockBar.SetPosition(0, 5)
		self.BlockBar.SetSize(500, 170 - 5 + 35 + 2)
		self.BlockBar.Hide()

		self.BlockBar.sub = ui.Bar()
		self.BlockBar.sub.SetParent(self)
		self.BlockBar.sub.SetColor(COLOR_INACTIVE)
		self.BlockBar.sub.SetPosition(500 - 122, 5 + 170 - 5 + 35 + 2)
		self.BlockBar.sub.SetSize(122, 30)
		self.BlockBar.sub.Hide()

		self.BlockText = ui.TextLine()
		self.BlockText.SetParent(self.BlockBar)
		self.BlockText.SetWindowHorizontalAlignCenter()
		self.BlockText.SetHorizontalAlignCenter()
		self.BlockText.SetPosition(0, 140)
		self.BlockText.SetText("Este item não pode ser melhorado.")
		self.BlockText.Show()

		self.Block2 = ui.Bar()
		self.Block2.SetParent(self.Box2)
		self.Block2.SetColor(grp.GenerateColor(1.0, 0.1, 0.1, 0.1))
		self.Block2.SetSize(237, 131)
		self.Block2.SetPosition(2, 17)
		self.Block2.Show()

		self.Block3 = ui.Bar()
		self.Block3.SetParent(self.Box3)
		self.Block3.SetColor(grp.GenerateColor(1.0, 0.1, 0.1, 0.1))
		self.Block3.SetSize(237, 55)
		self.Block3.SetPosition(2, 17)
		self.Block3.Show()

		if self.main.configs[2].checked == 1:
			self.EnableSecondOption.Toggle()

		self.SetHideEvent(self.HideEvent)
		self.prepare_propose()

	def Delete_Pre(self):
		question_dialog = uicommon.QuestionDialog()
		question_dialog.SetText("Tem certeza que deseja excluir essa opção?")
		question_dialog.SetAcceptEvent(self.DeleteOption, True)
		question_dialog.SetCancelEvent(self.DeleteOption, False)
		question_dialog.Open()
		self.Dialog = question_dialog

	def DeleteOption(self, arg):
		self.Dialog.Hide()
		self.Dialog = None
		if arg:
			RemoveSavedOption(self.but_propose.GetText())
			self.but_propose.DropList.RemoveItem(self.but_propose.DropList.GetSelectedItem())
			self.but_propose.DecreaseCountItem(1)
			self.OnChangeBonus()

	def Save_Pre(self):
		name_dialog = uicommon.InputDialog()
		name_dialog.SetTitle("Digite um Nome:")
		name_dialog.SetAcceptEvent(self.SaveOption, True)
		name_dialog.SetCancelEvent(self.SaveOption, False)
		name_dialog.Open()
		self.Dialog = name_dialog

	def SaveOption(self, arg):
		Name = self.Dialog.GetText()
		self.Dialog.Hide()
		self.Dialog = None
		if not Name:
			return
		if not arg:
			return
		try:
			item.SelectItem(self.sub_parent.vnum)
			type = item.GetItemType()
			subtype = item.GetItemSubType()
			use = proposals[type]
		except BaseException:
			type = item.ITEM_TYPE_WEAPON
			subtype = 1

		tmp = [
			[self.boni[1][0].selected.value, int(self.boni[1][1].GetText())],
			[self.boni[2][0].selected.value, int(self.boni[2][1].GetText())],
			[self.boni[3][0].selected.value, int(self.boni[3][1].GetText())],
			[self.boni[4][0].selected.value, int(self.boni[4][1].GetText())],
			[self.boni[5][0].selected.value, int(self.boni[5][1].GetText())],
			[self.boni_extra[1][0].selected.value, int(self.boni_extra[1][1].GetText())],
			[self.boni_extra[2][0].selected.value, int(self.boni_extra[2][1].GetText())],
			[self.boni_extra[3][0].selected.value, int(self.boni_extra[3][1].GetText())],
			[self.boni_extra[4][0].selected.value, int(self.boni_extra[4][1].GetText())],
			[self.boni_extra[5][0].selected.value, int(self.boni_extra[5][1].GetText())],
		]

		tmp2 = []
		for i in range(1, 6):
			tmp2.append(self.boni[i][0].selected.value)
			tmp2.append(int(self.boni[i][1].GetText()))
		for i in range(1, 6):
			tmp2.append(self.boni_extra[i][0].selected.value)
			tmp2.append(int(self.boni_extra[i][1].GetText()))

		self.but_propose.AppendItem(Name, tmp)
		self.but_propose.SetSize(150, 20)
		AddNewOption(type, subtype, Name, tmp2)

	def OnChangeBonus(self):
		self.but_propose.Drop.Hide()
		self.but_propose.SelectByAffectId(0)
		self.SaveButton.Show()
		self.DelButton.Hide()

	def HideEvent(self):
		for i in range(1, 8):
			self.boni[i][0].Drop.Hide()
		for i in range(1, 6):
			self.boni_extra[i][0].Drop.Hide()
		self.but_propose.Drop.Hide()

	def change_boni(self):
		use = self.but_propose.DropList.GetSelectedItem().GetValue()
		if use == 0:
			self.SaveButton.Show()
			self.DelButton.Hide()
			return
		bon = 1
		for x in use[:5]:
			self.boni[bon][0].SelectByAffectId(int(x[0]))
			self.boni[bon][1].SetText(str(x[1]))
			bon += 1
		if bon <= 1:
			self.OnChangeBonus()
		else:
			self.SaveButton.Hide()
			self.DelButton.Show()

		for x in range(bon, 8):
			self.boni[x][0].SelectByAffectId(0)

		bon = 1
		for x in use[5:]:
			self.boni_extra[bon][0].SelectByAffectId(int(x[0]))
			self.boni_extra[bon][1].SetText(str(x[1]))
			bon += 1
		for x in range(bon, 6):
			self.boni_extra[x][0].SelectByAffectId(0)

	def prepare_propose(self):
		LoadSavedOptions()
		self.but_propose.DropList.RemoveAllItems()
		self.but_propose.SetCountItem(1)
		self.but_propose.AppendItemAndSelect("Opções Salvas")
		self.but_propose.AppendItem("Limpar", [])

		try:
			item.SelectItem(self.sub_parent.vnum)
			type = item.GetItemType()
			use = proposals[type]
		except BaseException:
			type = item.ITEM_TYPE_WEAPON

		if type == item.ITEM_TYPE_ARMOR:
			use = use[item.GetItemSubType()]
			for prop in use:
				self.but_propose.AppendItem(prop, use[prop])
		else:
			use = proposals[item.ITEM_TYPE_WEAPON]
			for prop in use:
				self.but_propose.AppendItem(prop, use[prop])
		self.but_propose.SetSize(150, 20)

#################################################################################################################################
##### MENU ITENS ##### MENU ITENS ##### MENU ITENS ##### MENU ITENS ##### MENU ITENS ##### MENU ITENS ###### MENU ITENS #########
#################################################################################################################################
class ItemTabBar(ui.ScriptWindow):
	def __init__(self, parent):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.parentWindow = parent
		self.SetParent(parent)
		self.__Load_Ui_()

	def __Initialize(self):
		self.parentWindow = None
		self.tabCount = 0
		self.tabList = {}

	def __Load_Ui_(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/boot_item_tab_bar.py")

		self.plusBar = self.GetChild("Arrow")
		self.plusBar.SetWindowVerticalAlignCenter()
		self.plusBar.SetMouseLeftButtonUpEvent(self.AddTab_pre)
		self.SetMouseLeftButtonUpEvent(self.AddTab_pre)
		self.GetChild("Config_Button").SetOverInEvent(self.Config_Button_Over_In)
		self.GetChild("Config_Button").SetOverOutEvent(self.Config_Button_Over_Out)
		self.GetChild("Config_Button").SetMouseLeftButtonUpEvent(self.SelectConfig)
		self.ItemTab.width = 62
		self.ItemTab.dist = 3

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		for id in self.tabList:
			self.tabList[id].blockBar.Hide()
			self.tabList[id].blockBar.Destroy()
			self.tabList[id].Destroy()

		self.tabList = []
		self.__Initialize()

	def Config_Button_Over_In(self):
		self.GetChild("configs_text").LoadImage("interface/controls/special/boot/configurar_over.tga")

	def Config_Button_Over_Out(self):
		self.GetChild("configs_text").LoadImage("interface/controls/special/boot/configurar_normal.tga")

	def UnSelectAll(self):
		for i in self.tabList:
			self.tabList[i].UnSelect()
			self.tabList[i].bonusSelector.Hide()
		self.GetChild("Select").Hide()
		self.parentWindow.Options_Page.Hide()

	def SelectConfig(self):
		self.UnSelectAll()
		self.GetChild("Select").Show()
		self.parentWindow.Options_Page.Show()

	def DeleteTab(self, id):
		if self.parentWindow.wndInventory != None:
			self.tabList[id].blockBar.Hide()
			self.tabList[id].blockBar.Destroy()
		self.tabList[id].Destroy()
		self.tabCount = self.tabCount -1
		if self.tabCount > id and id < 5:
			for i in range(id, self.tabCount):
				self.tabList[i] = self.tabList[i+1] 
				self.tabList[i].tabnum = i
				self.tabList[i].SetPosition((self.tabList[i].width + self.tabList[i].dist) * i, 2)
			del self.tabList[self.tabCount]
		else:
			del self.tabList[id]

		if self.tabCount > 0:
			self.tabList[0].Select()
		else:
			self.GetChild("Explain").Show()

		if self.tabCount == 0:
			self.plusBar.SetPosition(10, 0)
		else:
			(x, y) = self.tabList[self.tabCount -1].GetLocalPosition()
			self.plusBar.SetPosition(x + self.ItemTab.width + self.ItemTab.dist, 0)

		if self.tabCount < 5:
			self.plusBar.Show()

	def AddTab_pre(self):
		if mousemodule.mouseController.isAttached():
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			attachedSlotVnum = mousemodule.mouseController.GetAttachedItemIndex()

			if attachedSlotPos >= (player.INVENTORY_PAGE_COUNT*player.INVENTORY_PAGE_SIZE):
				chat.AppendChat(2, "Não pode adicionar itens equipados.")
				return

			item.SelectItem(attachedSlotVnum)
			if item.GetItemType() != 1 and item.GetItemType() != 2:
				mousemodule.mouseController.DeattachObject()
				chat.AppendChat(2, "Este item não pode ser rodado.")
				return

			for a in self.tabList:
				if self.tabList[a].index == attachedSlotPos:
					mousemodule.mouseController.DeattachObject()
					chat.AppendChat(2, "Esse Slot já foi inserido!")
					return

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				self.AddTab(attachedSlotPos, attachedSlotVnum)
			mousemodule.mouseController.DeattachObject()
		else:
			self.UnSelectAll()

	def AddTab(self, id, vnum = 0):
		if self.tabCount < MAX_NUM:
			chat.AppendChat(2, "Item Adicionado!")
			self.tabList[self.tabCount] = self.ItemTab(self, self.tabCount, id, vnum)
			self.tabList[self.tabCount].Select()
			self.tabList[self.tabCount].Show()
			self.tabCount += 1
			if self.tabCount == 0:
				self.plusBar.SetPosition(20, 0)
				self.GetChild("Explain").Show()
			else:
				(x, y) = self.tabList[self.tabCount-1].GetLocalPosition()
				self.plusBar.SetPosition(x + self.ItemTab.width + self.ItemTab.dist, 0)
				self.GetChild("Explain").Hide()
		else:
			chat.AppendChat(2, "Item não adicionado. Máximo atingido.")

		if self.tabCount >= 5:
			self.plusBar.Hide()

#################################################################################################################################
#### CLASS BLOCKBAR ##### CLASS BLOCKBAR ##### CLASS BLOCKBAR ##### CLASS BLOCKBAR ##### CLASS BLOCKBAR ##### CLASS BLOCKBAR ####
#################################################################################################################################
	class BlockBar(ui.Window):
		size_res = 32
		multi = 1
		def SetSize(self, i = 1):
			self.multi = i
			ui.Window.SetSize(self, self.size_res, self.size_res * i)
			if self.rare_enabled == 1:
				self.swib_normal.SetSize(self.size_res, (self.size_res * i / 3 * 2))
				pos1 = int(self.size_res * i * 2.0 / 3.0)
				self.swib_normal.SetSize(self.size_res, pos1)
				self.swib_rare.SetSize(self.size_res, (self.size_res * i) - pos1)
				self.swib_rare.SetPosition(0, pos1)
				self.swib_rare.Show()
			else:
				self.swib_normal.SetSize(self.size_res, self.size_res * i)
				self.swib_rare.Hide()

		def Enable_rare(self, o = 1):
			self.rare_enabled = o
			self.SetSize(self.multi)

		def __init__(self):
			ui.Window.__init__(self)
			self.rare_enabled = 0
			self.swib_normal = ui.Bar()
			self.swib_normal.SetParent(self)
			self.swib_normal.SetSize(self.size_res, self.size_res * self.multi)
			self.swib_normal.SetColor(COLOR_INACTIVE)
			self.swib_normal.SetPosition(0,0)
			self.swib_normal.Show()

			self.swib_rare = ui.Bar()
			self.swib_rare.SetParent(self)
			self.swib_rare.SetSize(self.size_res, self.size_res)
			self.swib_rare.SetColor(COLOR_INACTIVE_RARE)
			self.swib_rare.SetPosition(0, 0)
			self.swib_rare.Hide()
			self.SetSize(1)

#################################################################################################################################
##### CLASS MENU ITEM ##### CLASS MENU ITEM ##### CLASS MENU ITEM ##### CLASS MENU ITEM ##### CLASS MENU ITEM ##### CLASS ITEM ##
#################################################################################################################################
	class ItemTab(ui.ScriptWindow):
		def __init__(self, parent, tabnum, index = 0, vnum = 0):
			ui.ScriptWindow.__init__(self)
			self.parentWindow = parent
			self.SetParent(parent)
			self.index = index
			self.tabnum = tabnum
			self.vnum = vnum
			self.count = 0
			self.count_rare = 0
			self.boni_active = 0
			self.boni_rare_active = 0
			self.overitem = 0
			self.tooltipItem = self.parentWindow.parentWindow.tooltipItem
			self.__Load_Ui_()

			if app.ENABLE_SWITCH_IMPROVEMENT:
				constinfo.AddItemToList(self.index)

			if self.parentWindow.parentWindow.wndInventory != None:
				self.blockBar = ItemTabBar.BlockBar()
				self.blockBar.SetParent(self.parentWindow.parentWindow.wndInventory.wndItem)
				ipi = self.parentWindow.parentWindow.wndInventory.inventoryPageIndex
				self.blockBar.swib_normal.SetOverInEvent(self.OverInItem)
				self.blockBar.swib_normal.SetOverOutEvent(self.OverOutItem)
				self.blockBar.swib_rare.SetOverInEvent(self.OverInItem)
				self.blockBar.swib_rare.SetOverOutEvent(self.OverOutItem)
				self.blockBar.Show()
				ip2 = self.index - ipi * 50
				self.blockBar.SetPosition(((ip2 - int(ip2/5) * 5) * self.blockBar.size_res), int(ip2/5) * self.blockBar.size_res)

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Destroy(self):
			self.Hide()
			self.bonusSelector.Hide()
			self.bonusSelector.Destroy()
			self.tooltipItem = None
			del self.bonusSelector
			del self

		def DeleteMe(self):
			self.parentWindow.DeleteTab(self.tabnum)

		def __Load_Ui_(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/boot_item_tab.py")

			self.ItemIcon = self.GetChild("ItemIcon")
			self.ItemIcon.SetWindowHorizontalAlignCenter()
			self.ItemIcon.SetWindowVerticalAlignCenter()
			self.ItemIcon.SetOverInEvent(self.OverInItem)
			self.ItemIcon.SetOverOutEvent(self.OverOutItem)
			self.ItemIcon.SetMouseLeftButtonDownEvent(self.Select)

			self.StatusBar = self.GetChild("StatusBar")
			self.StatusText = self.GetChild("StatusText")
			self.StatusText.SetWindowHorizontalAlignCenter()
			self.StatusText.SetWindowVerticalAlignCenter()
			self.StatusText.SetHorizontalAlignCenter()
			self.StatusText.SetVerticalAlignCenter()

			self.StatusBar_rare = self.GetChild("StatusBar_rare")
			self.StatusText_rare = self.GetChild("StatusText_rare")
			self.StatusText_rare.SetWindowHorizontalAlignCenter()
			self.StatusText_rare.SetWindowVerticalAlignCenter()
			self.StatusText_rare.SetHorizontalAlignCenter()
			self.StatusText_rare.SetVerticalAlignCenter()

			self.SlotName = self.GetChild("Slot_Name")
			self.SlotName.SetText("Slot %d" % (self.index+1))

			self.CloseBut = self.GetChild("Close_Button")
			self.CloseBut.SetEvent(self.DeleteMe)

			self.SetMouseLeftButtonDownEvent(self.Select)

			self.bonusSelector = BonusSelector(self, self.parentWindow.parentWindow)
			self.bonusSelector.SetParentProxy(self.parentWindow.parentWindow)
			self.bonusSelector.SetPosition(4, 154)
			self.bonusSelector.Hide()
			self.SetIndex(self.index)
			self.vnum = 0
			self.resetSwitch()
			self.resetSwitch_rare()

### ITEM TOOTIP ### ITEM TOOTIP ### ITEM TOOTIP ### ITEM TOOTIP ### ITEM TOOTIP ### ITEM TOOTIP ### ITEM TOOTIP ###
		def ShowToolTip(self, slotIndex):
			if self.tooltipItem != None:
				self.tooltipItem.SetInventoryItem(slotIndex, player.INVENTORY, False, False)

		def OverOutItem(self):
			self.overitem = 0
			if self.tooltipItem != None:
				self.tooltipItem.HideToolTip()

		def OverInItem(self):
			if mousemodule.mouseController.isAttached():
				return
			self.overitem = 1

		def OnUpdate(self):
			if self.overitem == 0:
				return
			self.ShowToolTip(self.index)

		def IsActive(self):
			return self.boni_active == 1

		def IsActive_rare(self):
			return self.boni_rare_active == 1

		def SetParentProxy(self, parent):
			ui.ScriptWindow.SetParentProxy(self, parent)

		def Select(self):
			self.parentWindow.UnSelectAll()
			self.bonusSelector.Show()
			self.GetChild("Select").Show()
			self.SlotName.SetPackedFontColor(0xfff8d090)
			self.StatusText.SetPackedFontColor(COLOR_NAME_SELECTED)
			self.StatusText_rare.SetPackedFontColor(COLOR_NAME_SELECTED)
			self.Update()

		def UnSelect(self):
			self.GetChild("Select").Hide()
			self.SlotName.SetPackedFontColor(0xffa08784)
			self.StatusText.SetPackedFontColor(0xffa08784)
			self.StatusText_rare.SetPackedFontColor(0xffa08784)
			self.Update()

		def Update(self):
			self.SetPosition((self.width+self.dist)*self.tabnum, 0)
			self.SlotName.SetText("Slot %d" % (self.index+1))

		def resetSwitch(self):
			self.values = [0,0,0,0,0]

		def resetSwitch_rare(self):
			self.values_rare = [0,0]

		def Switch_rare(self):
			for i in range(0, 200):
				if player.GetItemIndex(i) == SWITCH_RARE_VNUM:
					net.SendItemUseToItemPacket(i, self.index)
					if app.ENABLE_SWITCH_IMPROVEMENT:
						constinfo.SetItemSwitched(self.index)
					return

			self.bonusSelector.Deactivate_rare()
			chat.AppendChat(2,"Slot %d: 6/7 Cancelado -> Você está sem pergaminho para rodar!" % (self.index+1))

		def Switch(self):
			for i in range(0, 200):
				if player.GetItemIndex(i) == SWITCH_VNUM:
					net.SendItemUseToItemPacket(i, self.index)
					if app.ENABLE_SWITCH_IMPROVEMENT:
						constinfo.SetItemSwitched(self.index)
					return

			self.bonusSelector.Deactivate()
			chat.AppendChat(2,"Slot %d: 6/7 Cancelado -> Você está sem pergaminho para rodar!" % (self.index+1))

		def checkSwitch(self):
			if app.ENABLE_SWITCH_IMPROVEMENT:
				if not constinfo.CanSwitchItem(self.index):
					return

			self.prob = self.GetProb()
			self.StatusText.SetText("Ativo")
			if self.prob >= 90:
				self.bonusSelector.Finish()
				chat.AppendChat(1,"Slot %d: o bonus foi encontrado!" % (self.index + 1))
				if self.parentWindow.parentWindow.configs[0].checked == 1:
					app.FlashApplication()
					dbg.TrLogBox("Slot %d: o bonus foi encontrado!" % (self.index + 1))
				if self.parentWindow.parentWindow.configs[1].checked == 1:
					snd.PlaySound("sound/ui/metinstone_insert.wav")
				return

			self.Switch()

		def checkSwitch_rare(self):
			if app.ENABLE_SWITCH_IMPROVEMENT:
				if not constinfo.CanSwitchItem(self.index):
					return

			self.prob_rare = self.GetProb_rare()
			self.StatusText_rare.SetText("Ativo")
			if self.prob_rare >= 90:
				self.bonusSelector.Finish_rare()
				chat.AppendChat(1, "Slot %d: (6-7) o bonus foi encontrado!" % (self.index+1))
				if self.parentWindow.parentWindow.configs[0].checked == 1:
					dbg.TrLogBox("Slot %d: (6-7) o bonus foi encontrado!" % (self.index + 1))
					app.FlashApplication()
				if self.parentWindow.parentWindow.configs[1].checked == 1:
					snd.PlaySound("sound/ui/metinstone_insert.wav")
				return

			self.Switch_rare()

		def UpdateItem(self):
			vnum = player.GetItemIndex(self.index)
			if vnum == 0 and self.vnum != 0:
				self.resetSwitch()
				self.resetSwitch_rare()
				self.vnum = 0
				self.bonusSelector.Deactivate()
				self.bonusSelector.Block()
				self.ItemIcon.Hide()
				self.GetChild("in_process").Hide()
				if self.parentWindow.parentWindow.wndInventory != None:
					self.blockBar.SetSize(1)
				self.DeleteMe()
				return
			elif vnum != self.vnum:
				self.resetSwitch()
				self.resetSwitch_rare()
				self.vnum = vnum
				self.bonusSelector.Deactivate()
				self.bonusSelector.prepare_propose()
				item.SelectItem(self.vnum)
				if self.parentWindow.parentWindow.wndInventory != None:
					(w, h) = item.GetItemSize()
					self.blockBar.SetSize(h)
				if item.GetItemType() != 1 and item.GetItemType() != 2:
					self.bonusSelector.Block()
				else:
					self.bonusSelector.Unblock()

				#if player.GetItemAttribute(self.index, 4) == 0 and len(self.GenList()) == 5:
					#self.GetChild("warning").Show()

				self.GetChild("in_process").Hide()
				self.ItemIcon.Show()
				self.ItemIcon.LoadImage(item.GetIconImageFileName())
				return

			#if player.GetItemAttribute(self.index, 4) != 0:
				#self.GetChild("warning").Hide()

			if self.IsActive():
				self.checkSwitch()

			if self.IsActive_rare():
				self.checkSwitch_rare()

		def SetIndex(self, index):
			self.index = index
			self.bonusSelector.index = index
			self.bonusSelector.Starter.SetText("Slot ("+str(index+1)+") Iniciar")
			self.Update()
			self.UpdateItem()

		def GetProb_rare(self):
			values = [player.GetItemAttribute(self.index, i) for i in range(5, 7)]
			val2 = {}
			for i in range(0, 2):
				val2[values[i][0]] = values[i][1]
			prob = 0
			max  = 0

			yp = self.GenList_rare()
			for x in yp:
				if yp[x] in val2:
					prob += 1
				max += 1
			if max > 0:
				prozent = 100/max*prob
			else:
				prozent = 100
			return prozent

		def GetProb(self):
			values = [player.GetItemAttribute(self.index, i) for i in range(0, 5)]
			val2 = {}
			for i in range(0, 5):
				val2[values[i][0]] = values[i][1]
			prob = 0
			iter  = 0
			list_bonuses = self.GenList()

			if list_bonuses == {}:
				chat.AppendChat(1,"Slot %d: nenhum bônus selecionado na primeira opção." % (self.index + 1))
				self.bonusSelector.Deactivate()
				if self.parentWindow.parentWindow.configs[0].checked == 1:
					app.FlashApplication()
					dbg.TrLogBox("Slot %d: nenhum bônus selecionado na primeira opção." % (self.index + 1))
				if self.parentWindow.parentWindow.configs[1].checked == 1:
					snd.PlaySound("sound/ui/metinstone_insert.wav")
				return

			for index in list_bonuses:
				if list_bonuses[index] in val2 and val2[list_bonuses[index]] >= int(self.bonusSelector.boni[index][1].GetText()):
					prob = prob + 1
				iter = iter + 1
			if iter > 0:
				prozent = 100/iter*prob
			else:
				prozent = 100

			if self.bonusSelector.EnableSecondOption.checked == 0:
				return prozent

			prob = 0
			iter = 0
			list_bonuses = self.GenListExtra()

			if list_bonuses == {}:
				chat.AppendChat(1,"Slot %d: nenhum bônus selecionado na segunda opção." % (self.index + 1))
				self.bonusSelector.Deactivate()
				if self.parentWindow.parentWindow.configs[0].checked == 1:
					app.FlashApplication()
					dbg.TrLogBox("Slot %d: nenhum bônus selecionado na segunda opção." % (self.index + 1))
				if self.parentWindow.parentWindow.configs[1].checked == 1:
					snd.PlaySound("sound/ui/metinstone_insert.wav")
				return

			for index in list_bonuses:
				if list_bonuses[index] in val2 and val2[list_bonuses[index]] >= int(self.bonusSelector.boni_extra[index][1].GetText()):
					prob = prob + 1
				iter = iter + 1
			if iter > 0:
				prozent_extra = 100/iter*prob
			else:
				prozent_extra = 100

			return max(prozent, prozent_extra)

		def GenListExtra(self):
			ret = {}
			for i in range(0, 5):
				if self.bonusSelector.boni_extra[5-i][0].selected.value != int(0) and int(self.bonusSelector.boni_extra[5-i][1].GetText()) != int(0):
					ret[5-i] = self.bonusSelector.boni_extra[5-i][0].selected.value
			return ret

		def GenList(self):
			ret = {}
			for i in range(0, 5):
				if self.bonusSelector.boni[5-i][0].selected.value != int(0) and int(self.bonusSelector.boni[5-i][1].GetText()) != int(0):
					ret[5-i] = self.bonusSelector.boni[5-i][0].selected.value
			return ret

		def GenList_rare(self):
			ret = {}
			for i in range(0, 2):
				if self.bonusSelector.boni[6+i][0].selected.value != 0:
					ret[i+1] = self.bonusSelector.boni[6+i][0].selected.value
			return ret

#################################################################################################################################
##### CLASSE MAIN ##### CLASSE MAIN ##### CLASSE MAIN ##### CLASSE MAIN ##### CLASSE MAIN ##### CLASSE MAIN #####################
#################################################################################################################################
class Bot(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__LoadBoard()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Hide()
		if self.itemTabBar:
			self.itemTabBar.Destroy()

		if self.PinGroupBox:
			self.PinGroupBox.Hide()
			self.PinGroupBox = None

		self.ClearDictionary()
		self.__Initialize()

	def Show(self):
		ui.ScriptWindow.Show(self)
		if self.PinGroupBox:
			self.PinGroupBox.Hide()
			self.PinGroupBox = None

	def __Initialize(self):
		self.wndInventory = None
		self.isDragging = 0
		self.PinHint = 0
		self.PinHintState = 0
		self.PinGroupBox = None
		self.itemTabBar = None
		self.tooltipItem = None
		self.counter = 0

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def __LoadBoard(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/boot_main.py")
		except BaseException:
			pass

### Fechar ### Fechar ### Fechar ### Fechar ### Fechar ### Fechar ### Fechar ######
		self.GetChild("MainBoard").SetCloseEvent(self.Close)

		self.PinHint = ui.Bar()
		self.PinHint.SetColor(grp.GenerateColor(1.0, 0.8, 0.8, 0.2))
		self.PinHint.Show()

		self.SetMouseLeftButtonDownEvent(self.__Start_Drag)
		self.SetMouseLeftButtonUpEvent(self.__Stop_Drag)

		self.itemTabBar = ItemTabBar(self)
		self.itemTabBar.SetPosition(8, 35)
		self.itemTabBar.Show()

		self.GetChild("Button_Minimize").SetEvent(self.__PinShow, 3)
		self.GetChild("Button_Deactive_All").SetEvent(self._Deactivate_All_)
		self.GetChild("Button_Active_All").SetEvent(self._Activate_All_)
		self.SetHideEvent(self.HideEvent)

### CONFIGURACOES DO BOOT ### CONFIGURACOES DO BOOT ### CONFIGURACOES DO BOOT ###
		self.Options_Page = self.GetChild("Options_Page")
		self.but_speed = self.GetChild("slider")
		self.but_speed.SetEvent(self.On_but_speed_Move)
		self.On_but_speed_Move()

		self.configs = [
			MakeCheckBox("Ativar Notificações do Windows", self.Options_Page, 20, 20, self.ChangeConfigs, self.ChangeConfigs),
			MakeCheckBox("Ativar Aúdio e Sons", self.Options_Page, 20, 20*2, self.ChangeConfigs, self.ChangeConfigs),
			MakeCheckBox("Segunda Opção de Bônus Ativa como Padrão", self.Options_Page, 20, 20*3, self.ChangeConfigs, self.ChangeConfigs),
		]

		self.LoadConfigs()

	def On_but_speed_Move(self):
		text = str(self.but_speed.GetSliderPos()*100.0)
		self.GetChild("slider_number").SetText(text[:5]+"%")

	def MakeConfigs(self):
		file = open("miles/boot.cfg", "w", "folder")
		string = ""
		for i in range(3):
			string += "1\n"
		string += "1.0"
		file.write(string)
		file.close()

	def ReturnConfigs(self):
		if not os.path.exists("miles/boot.cfg"):
			self.MakeConfigs()
		f = open("miles/boot.cfg", "r", "folder")
		lines = f.readlines()
		f.close()
		if len(lines) != int(4):
			self.MakeConfigs()
		return lines

	def LoadConfigs(self):
		lines = self.ReturnConfigs()
		self.but_speed.SetSliderPos(float(lines[3]))
		self.but_speed.SetOverOutEvent(self.ChangeConfigs)

		i = 0
		for line in range(0, 3):
			if int(lines[i]) == 1:
				self.configs[i].ToggleDown()
			else:
				self.configs[i].ToggleUp()
			i += 1

	def ChangeConfigs(self):
		string = ""
		for checkbox in self.configs:
			if checkbox.checked == 1:
				string += "1\n"
			else:
				string += "0\n"
		string += str(self.but_speed.GetSliderPos())
		file = open("miles/boot.cfg", "w", "folder")
		file.write(string)
		file.close()

### Inventory Tweak ### Inventory Tweak ### Inventory Tweak ### Inventory Tweak ###
	def EnableInventoryTweak(self, wndInventory):
		self.wndInventory = wndInventory

		if wndInventory == None:
			return

		i = 0
		for button in self.wndInventory.inventoryTab:
			button.SetEvent(self.__SetInventoryPage, i)
			i += 1

	def __SetInventoryPage(self, arg):
		self.wndInventory.SetInventoryPage(arg)
		for a in self.itemTabBar.tabList:
			itm = self.itemTabBar.tabList[a]
			if (itm.index >= (arg * player.INVENTORY_PAGE_SIZE)) and (itm.index < ((arg + 1) * player.INVENTORY_PAGE_SIZE)):
				itm.blockBar.Show()
			else:
				itm.blockBar.Hide()

### Fechar ### Fechar ### Fechar ### Fechar ### Fechar ### Fechar ### Fechar ######
	def HideEvent(self):
		if self.itemTabBar.tabCount > 0:
			for a in self.itemTabBar.tabList:
				self.itemTabBar.tabList[a].bonusSelector.HideEvent()

	def OnPressEscapeKey(self):
		self.__PinShow(3)
		return True

	def Close(self):
		self.ChangeConfigs()
		self.Hide()
		if self.itemTabBar.tabCount > 0:
			for i in range(0, self.itemTabBar.tabCount):
				self.itemTabBar.DeleteTab(0)
		if self.PinGroupBox:
			self.PinGroupBox.Hide()
			self.PinGroupBox = None

### Arrastar ### Minimisar ### Arrastar ### Minimisar ### Arrastar ### Minimisar ###
	def __Start_Drag(self):
		self.isDragging = 1

	def __Stop_Drag(self):
		self.isDragging = 0
		if self.PinHintState > 0:
			self.__PinShow(self.PinHintState)
		self.__ShowPinHint(0)

	def __ShowPinHint(self, type):
		self.PinHintState = type
		if type == 0:
			self.PinHint.Hide()
			return
		(x,y) = self.GetGlobalPosition()
		if type == 1:
			self.PinHint.SetWindowHorizontalAlignLeft()
			self.PinHint.SetWindowVerticalAlignCenter()
			self.PinHint.SetSize(max(min(15, 15 - x), 3), wndMgr.GetScreenHeight())
			self.PinHint.SetPosition(0, 0)
		if type == 2:
			self.PinHint.SetWindowHorizontalAlignRight()
			self.PinHint.SetWindowVerticalAlignCenter()
			self.PinHint.SetSize(15, wndMgr.GetScreenHeight())
			self.PinHint.SetPosition(max(min(15, 15 - (wndMgr.GetScreenWidth() - (x + self.GetWidth()))), 3), 0)
		if type == 3:
			self.PinHint.SetWindowHorizontalAlignCenter()
			self.PinHint.SetWindowVerticalAlignTop()
			self.PinHint.SetSize(wndMgr.GetScreenWidth(), max(min(15, 15 - y), 3))
			self.PinHint.SetPosition(0, 0)
		self.PinHint.Show()

	def __PinShow(self, dir):
		self.PinGroupBox = self.PinGroup(self, dir)
		self.Hide()
		self.PinGroupBox.Show()

### Ativar/Desativar ### Ativar/Desativar ### Ativar/Desativar ### Ativar/Desativar ### Ativar/Desativar ### Ativar/Desativar 
	def _Deactivate_All_(self):
		for a in self.itemTabBar.tabList:
			self.itemTabBar.tabList[a].bonusSelector.Deactivate()
			self.itemTabBar.tabList[a].bonusSelector.Deactivate_rare()

	def _Activate_All_(self):
		for a in self.itemTabBar.tabList:
			self.itemTabBar.tabList[a].bonusSelector.Activate()

	def OnUpdate(self):
		if self.isDragging == 1:
			(x1, y1) = self.GetGlobalPosition()
			x1 = max(min(wndMgr.GetScreenWidth() - self.GetWidth(), x1), 0)
			y1 = max(min(wndMgr.GetScreenHeight() - 25 - self.GetHeight(), y1), 0)
			self.SetPosition(x1, y1)
			if x1 < 10:
				self.__ShowPinHint(1)
			elif wndMgr.GetScreenWidth()-x1-self.GetWidth() < 10:
				self.__ShowPinHint(2)
			elif y1 < 10:
				self.__ShowPinHint(3)
			else:
				self.__ShowPinHint(0)

		self.counter += 1
		if self.counter >= int(((1 - self.but_speed.GetSliderPos()) * MAX_SWITCH_DELAY_APPEND) + MIN_SWITCH_DELAY):
			self.counter = 0
			for a in self.itemTabBar.tabList:
				itm = self.itemTabBar.tabList[a]
				itm.UpdateItem()

#################################################################################################################################
##### MINIMIZED CLASS ##### MINIMIZED CLASS ##### MINIMIZED ##### MINIMIZED ##### MINIMIZED ##### MINIMIZED ####### MINIMIZED ###
#################################################################################################################################
	class PinGroup(ui.Bar):
		def OnUpdate(self):
			(x, y) = self.GetGlobalPosition()
			max_x = wndMgr.GetScreenWidth() - self.GetWidth()
			max_y = wndMgr.GetScreenHeight() - self.GetHeight() - DISTANCE_BOTTOM
			if not (x == self.pos_x)  or not (y == self.pos_y):
				old_dir = self.dir
				if self.pos_x == 0 and not self.pos_y == 0 and not self.pos_y == max_y and old_dir != 1:
					self.parse_dir(1)
				elif self.pos_x == max_x and not self.pos_y == 0 and not self.pos_y == max_y and old_dir != 2:
					self.parse_dir(2)
				elif self.pos_y == 0 and not self.pos_x == 0 and not self.pos_x == max_x and old_dir != 3:
					self.parse_dir(3)
				# elif self.pos_y == max_y and not self.pos_x == 0 and not self.pos_x == max_x and old_dir != 4:
					# self.parse_dir(4)

				max_x = wndMgr.GetScreenWidth()-self.GetWidth()
				max_y = wndMgr.GetScreenHeight()-self.GetHeight()-DISTANCE_BOTTOM

				if self.pos_x == 0 and not self.pos_y == 0 and not self.pos_y == max_y:
					x = 0
				elif self.pos_x == max_x and not self.pos_y == 0 and not self.pos_y == max_y:
					x = max_x
				elif self.pos_y == 0 and not self.pos_x == 0 and not self.pos_x == max_x:
					y = 0
				elif self.pos_y == max_y and not self.pos_x == 0 and not self.pos_x == max_x:
					y = max_y
				if ((x > 0) and (x < max_x) and (y > 0) and (y < max_y)):
					if y < int(max_y/2):
						y = 0
					else:
						y = max_y
					
					if x < int(max_x/2):
						x = 0
					else:
						x = max_x

				x = min(max(0, x), wndMgr.GetScreenWidth() - self.GetWidth())
				y = min(max(0, y), wndMgr.GetScreenHeight() - self.GetHeight() - DISTANCE_BOTTOM)
				self.SetPosition(x, y)
				self.pos_x = x
				self.pos_y = y
			self.parent.OnUpdate()
			for c in self.txtlist:
				c.SetColor(c.item.StatusBar.color)
				c.txt2.SetText("Status: %s" % c.item.StatusText.GetText())
				try:
					c.listWin2.SetColor(c.item.StatusBar_rare.color)
					c.txt3.SetText("Status: %s" % c.item.StatusText_rare.GetText())
				except BaseException:
					pass

		def ShowMainWindow(self):
			(x,y) = self.parent.GetGlobalPosition()
			x = min(max(32, x), wndMgr.GetScreenWidth() - self.parent.GetWidth() - 32)
			y = min(max(32, y), wndMgr.GetScreenHeight() - self.parent.GetHeight() - DISTANCE_BOTTOM - 32)
			self.parent.SetPosition(x, y)
			self.parent.Show()

		def CloseAll(self):
			self.parent.Close()

		def parse_dir(self, dir):
			self.dir = dir
			w = 100
			h = 50
			for listWin in self.txtlist:
				itm = listWin.item
				listWin.AddFlag("not_pick")
				if dir >= 3:
					listWin.SetPosition(w, 4)
					listWin.SetSize(90, h - 8)
					w += 92
					if itm.bonusSelector.EnableRareBoni.checked == 1:
						w += 15
						listWin.SetSize(105, 28)
						listWin.listWin2.SetSize(105, 14)
						listWin.listWin2.Show()
						listWin.txt3.Show()
				else:
					listWin.SetPosition(0, h)
					listWin.SetSize(w, 30)
					if itm.bonusSelector.EnableRareBoni.checked == 1:
						listWin.SetSize(w, 28)
						listWin.listWin2.SetSize(w, 14)
						listWin.listWin2.Show()
						listWin.txt3.Show()
						h += 12
						pass
					h += 32
			self.SetSize(w, h)

		def SetSize(self, w, h):
			ui.Window.SetSize(self, w, h)
			self.Box.SetSize(w-1, h)

		def __init__(self, parent, dir = 1):
			self.parent = parent
			self.dir = dir
			ui.Bar.__init__(self)
			self.SetColor(COLOR_BG)

			w = 100
			h = 50

			self.AddFlag("float")
			self.AddFlag("movable")

			box = ui.Box()
			box.AddFlag("not_pick")
			box.SetParent(self)
			box.SetPosition(0, 0)
			box.SetColor(0xfff8d090)
			box.Show()
			self.Box = box

			self.titleBar = ui.MakeImageBox(self, "interface/controls/special/boot/mini/titlebar.tga", 4, 4)
			self.titleBar.AddFlag("not_pick")
			self.title = ui.MakeTextLine(self.titleBar)
			self.title.SetText("M2Plus")
			self.title.SetPackedFontColor(0xffa08784)
			self.title.SetPosition(0, -1)

			self.maximise_but = ui.Button()
			self.maximise_but.SetParent(self)
			self.maximise_but.SetPosition(self.titleBar.GetRight() + 4, self.titleBar.GetTop())
			self.maximise_but.SetUpVisual("interface/controls/special/boot/mini/maxi_button.tga")
			self.maximise_but.SetOverVisual("interface/controls/special/boot/mini/maxi_button_3.tga")
			self.maximise_but.SetDownVisual("interface/controls/special/boot/mini/maxi_button_2.tga")
			self.maximise_but.SetEvent(self.ShowMainWindow)
			self.maximise_but.Show()

			self.close_but = ui.Button()
			self.close_but.SetParent(self)
			self.close_but.SetPosition(self.maximise_but.GetRight() + 4, self.maximise_but.GetTop())
			self.close_but.SetUpVisual("interface/controls/special/boot/button_close.tga")
			self.close_but.SetOverVisual("interface/controls/special/boot/button_close_3.tga")
			self.close_but.SetDownVisual("interface/controls/special/boot/button_close_2.tga")
			self.close_but.SetEvent(self.CloseAll)
			self.close_but.Show()

			self.stop_but = ui.RedButton()
			self.stop_but.SetParent(self)
			self.stop_but.SetPosition(0, 20)
			self.stop_but.SetWidth(100)
			self.stop_but.SetText("Desativar Todos")
			self.stop_but.SetEvent(self.parent._Deactivate_All_)
			self.stop_but.Show()

			self.txtlist = []
			for a in self.parent.itemTabBar.tabList:
				itm = self.parent.itemTabBar.tabList[a]

				listWin = ui.Bar()
				listWin.item = itm
				self.txtlist.append(listWin)
				listWin.SetColor(itm.StatusBar.color)
				listWin.SetParent(self)
				listWin.AddFlag("not_pick")
				listWin.Show()

				listWin.txt1 = ui.TextLine()
				listWin.txt1.SetParent(listWin)
				listWin.txt1.SetText("Slot %d:" %(itm.index+1))
				listWin.txt1.Show()
				listWin.txt1.SetPosition(4,2)

				listWin.txt2 = ui.TextLine()
				listWin.txt2.SetParent(listWin)
				listWin.txt2.SetText("Status: %s" % itm.StatusText.GetText())
				listWin.txt2.SetPosition(4,2+12)
				listWin.txt2.Show()

				listWin.listWin2 = ui.Bar()
				listWin.listWin2.AddFlag("not_pick")
				listWin.listWin2.SetColor(itm.StatusBar_rare.color)
				listWin.listWin2.SetParent(listWin)
				listWin.listWin2.SetPosition(0, 28)
				listWin.listWin2.SetSize(w, 14)
				listWin.listWin2.Hide()

				listWin.txt3 = ui.TextLine()
				listWin.txt3.SetParent(listWin.listWin2)
				listWin.txt3.SetText("Status: %s" % itm.StatusText_rare.GetText())
				listWin.txt3.SetPosition(4, 0)
				listWin.txt3.Hide()

				if dir >= 3:
					listWin.SetPosition(w, 4)
					listWin.SetSize(90, h - 8)
					w += 92
					if itm.bonusSelector.EnableRareBoni.checked == 1:
						w += 15
						listWin.SetSize(105, 28)
						listWin.listWin2.SetSize(105, 14)
						listWin.listWin2.Show()
						listWin.txt3.Show()
				else:
					listWin.SetPosition(0, h)
					listWin.SetSize(w, 30)
					
					if itm.bonusSelector.EnableRareBoni.checked == 1:
						listWin.SetSize(w, 28)
						listWin.listWin2.Show()
						listWin.txt3.Show()
						h += 12
						pass
					h += 32
			self.SetSize(w, h)
			(x, y) = self.parent.GetGlobalPosition()

			x = min(max(0, x), wndMgr.GetScreenWidth() - self.GetWidth())
			y = min(max(0, y), wndMgr.GetScreenHeight() - self.GetHeight() - DISTANCE_BOTTOM)
			if dir == 1:
				self.SetPosition(0, y)
			elif dir == 2:
				self.SetPosition(wndMgr.GetScreenWidth() - self.GetWidth(), y)
			elif dir == 3:
				self.SetPosition(x, 0)
			else:
				self.SetPosition(x, wndMgr.GetScreenHeight() - (DISTANCE_BOTTOM + h))

			(self.pos_x, self.pos_y) = self.GetGlobalPosition()

			self.parse_dir(dir)
#################################################################################################################################
### UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI UI #####
#################################################################################################################################

##################### Inicio das Classes UI - DropDown - Bar - Edit2 - CheckBox #################################################

#################################################################################################################################
##### DROPDOWN ##### DROPDOWN ##### DROPDOWN ##### DROPDOWN ##### DROPDOWN ##### DROPDOWN ####### DROPDOWN ###### DROPDOWN ######
#################################################################################################################################
class DropDown(ui.Window):
	dropped  = 0
	dropstat = 0
	last = 0
	lastS = 0
	maxh = 95

	OnChange = None
	OnChange2 = None

	class Item(ui.ListBoxEx.Item):
		def __init__(self, parent, text, value = 0):
			ui.ListBoxEx.Item.__init__(self)
			self.Bar = ui.Bar()
			self.Bar.SetParent(self)
			self.Bar.SetPosition(0, 0)
			self.Bar.SetColor(COLOR_DROP_DOWN_ITEM_SELECT)
			self.Bar.AddFlag("not_pick")
			self.Bar.Hide()
			self.textBox = ui.TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.AddFlag("not_pick")
			self.textBox.SetPosition(2, 0)
			self.textBox.SetPackedFontColor(0xffa08784)
			self.textBox.Show()
			self.value = value

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

		def SetSize(self, width, height):
			wndMgr.SetWindowSize(self.hWnd, width, height)
			self.Bar.SetSize(self.GetWidth(), self.GetHeight()+1)

		def GetValue(self):
			return self.value

		def GetValueMax(self):
			try:
				return MAX_NUM_FOR_BONUS[self.value]
			except BaseException:
				return 0

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(COLOR_DROP_DOWN_ITEM_SELECT)
			grp.RenderBar(x, y+1, self.GetWidth(), self.GetHeight()+1)

		def OnMouseOverIn(self):
			self.textBox.SetPackedFontColor(0xfff88f90)
			if self.Bar.IsShow():
				return
			self.Bar.Show()

		def OnMouseOverOut(self):
			self.textBox.SetPackedFontColor(0xffa08784)
			if self.Bar.IsShow():
				self.Bar.Hide()

	def __init__(self, parent, tt = "", down = 1):
		ui.Window.__init__(self, "TOP_MOST")
		self.down = down
		self.c = 1
		self.SetParentProxy(parent)
		self.bg = ui.Bar("TOP_MOST")
		self.bg.SetParent(self)
		self.bg.SetPosition(0, 0)
		self.bg.SetColor(COLOR_DROP_DOWN_NORMAL)
		self.bg.SetOverInEvent(self.bgMouseIn)
		self.bg.SetOverOutEvent(self.bgMouseOut)
		self.bg.SetMouseLeftButtonDownEvent(self.ExpandMe)
		self.bg.Show()

		self.EditBoxLine = None

		self.act = ui.TextLine()
		self.act.SetPackedFontColor(0xffa08784)
		self.act.SetParent(self.bg)
		self.act.SetPosition(4, 2)
		self.act.SetText(tt)
		self.act.Show()
		self.GetText = ui.__mem_func__(self.act.GetText)

		self.Drop = ui.Bar("TOP_MOST")
		self.Drop.SetParent(self.GetParentProxy().GetParentProxy())
		self.Drop.SetPosition(self.GetGlobalLeft(), self.GetGlobalTop() + self.GetHeight())
		self.Drop.SetSize(150, 0)
		self.Drop.SetColor(0xff0a0a0a)

		self.Drop.box = ui.Box()
		self.Drop.box.AddFlag("not_pick")
		self.Drop.box.SetParent(self.Drop)
		self.Drop.box.SetPosition(0, -1)
		self.Drop.box.SetColor(COLOR_DROP_DOWN_BOX)
		self.Drop.box.Show()

		self.ScrollBar = ui.New_ThinScrollBar()
		self.ScrollBar.SetParent(self.Drop)
		self.ScrollBar.SetPosition(132, 0)
		self.ScrollBar.SetScrollBarSize(0)

		self.DropList = ui.ListBoxEx()
		self.DropList.SetParent(self.Drop)
		self.DropList.itemHeight = 16
		self.DropList.itemStep = 16
		self.DropList.SetPosition(0, 0)
		self.DropList.SetSize(132, 16)
		self.DropList.SetScrollBar(self.ScrollBar)
		self.DropList.SetSelectEvent(self.SetTitle)
		self.DropList.SetViewItemCount(0)
		self.DropList.Show()
		if tt != "":
			self.AppendItemAndSelect(tt)

		self.selected = self.DropList.GetSelectedItem()

		box = ui.Box()
		box.AddFlag("not_pick")
		box.SetParent(self)
		box.SetPosition(0, 0)
		box.SetColor(COLOR_DROP_DOWN_BOX)
		box.Show()
		self.Box = box

		self.SetSize(120, 20)

	def Destroy(self):
		self.selected = None
		self.DropList.RemoveAllItems()
		self.DropList = None
		self.Box = None
		self.Drop.box = None
		self.act = None
		self.Drop = None
		self.ScrollBar = None
		self.bg = None

	def __del__(self):
		ui.Window.__del__(self)

	def SetCountItem(self, value):
		self.c = value
		self.maxh = min(200, 16 * self.c)

	def DecreaseCountItem(self, value):
		if self.c <= 0:
			return
		self.c -= 1
		self.maxh = min(200, 16 * self.c)

	def AppendItem(self, text, value = 0):
		self.c += 1
		if ":" in text:
			t = text.split(":")
			item = self.Item(self, t[0], value)
		else:
			item = self.Item(self, text, value)

		self.DropList.AppendItem(item)

		self.maxh = min(200, 16 * self.c)
		if self.c > 7:
			self.ScrollBar.Show()

	def AppendItemAndSelect(self, text, value = 0):
		self.DropList.AppendItem(self.Item(self, text, value))
		self.DropList.SelectIndex(len(self.DropList.itemList) - 1)

	def SelectByAffectId(self, id):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, str(id))
		for x in self.DropList.itemList:
			# chat.AppendChat(chat.CHAT_TYPE_INFO, str(x.GetValue()))
			if int(x.GetValue()) == int(id):
				self.DropList.SelectItem(x)
				self.SetTitle(x)
				break

	def SetTitle(self, item):
		if item.GetValue():
			self.act.SetPackedFontColor(0xfff88f90)
		else:
			self.act.SetPackedFontColor(0xffa08784)

		self.act.SetText(str(item.textBox.GetText()))
		self.last = self.DropList.basePos
		self.lastS = self.ScrollBar.GetPos()
		self.dropped = 0
		self.selected = item
		if self.EditBoxLine:
			self.EditBoxLine.SetMaxNumber(item.GetValue())
		if self.OnChange:
			self.OnChange()

	def SetEditBoxLine(self, object):
		self.EditBoxLine = proxy(object)

	def SetPosition(self, w, h):
		ui.Window.SetPosition(self, w, h)
		if self.down == 1:
			self.Drop.SetPosition(self.GetGlobalLeft(), self.GetGlobalTop() + self.GetHeight())
		else:
			self.Drop.SetPosition(w, h - self.Drop.GetHeight())

	def SetSize(self, w, h):
		ui.Window.SetSize(self, w, h)
		self.Box.SetSize(w-1, h-1)
		self.bg.SetSize(w, h)
		self.Drop.SetSize(w, 0)
		self.Drop.box.SetSize(w-1, 0)
		self.DropList.SetSize(w - 18, self.maxh)
		for x in self.DropList.itemList:
			x.SetSize(w - 18, 14)
		self.ScrollBar.SetPosition(w - 18, 0)

	def ExpandMe(self):
		if self.OnChange2:
			self.OnChange2()
		if self.dropped == 1:
			self.dropped = 0
		else:
			self.dropped = 1

	def OnUpdate(self):
		iter = 20
		if self.Drop.GetHeight() < 50:
			self.ScrollBar.Hide()
		else:
			self.ScrollBar.Show()

		if self.dropped == 0 and self.dropstat == 1:
			if self.Drop.GetHeight() <= 0:
				self.dropstat = 0
				self.Drop.SetSize(self.Drop.GetWidth(), 0)
				self.Drop.box.SetSize(self.Drop.GetWidth()-1, 0)
				self.ScrollBar.SetScrollBarSize(self.Drop.GetHeight())
				self.Drop.Hide()
			else:
				if ((self.Drop.GetHeight() - iter) < 0):
					self.Drop.SetSize(self.Drop.GetWidth(), 0)
					self.Drop.box.SetSize(self.Drop.GetWidth()-1, 0)
				else:
					self.Drop.SetSize(self.Drop.GetWidth(), self.Drop.GetHeight() - iter)
					self.Drop.box.SetSize(self.Drop.GetWidth()-1, self.Drop.GetHeight() - iter +1)
					(w, h) = self.GetLocalPosition()
					self.SetPosition(w, h)

				self.ScrollBar.SetScrollBarSize(self.Drop.GetHeight())
			self.DropList.SetViewItemCount(int(self.Drop.GetHeight()/16))
			self.DropList.SetBasePos(self.last + 1)
			self.DropList.SetBasePos(self.last)

		elif self.dropped == 1 and self.dropstat == 0:
			self.Drop.Show()
			self.SetTop()
			if self.Drop.GetHeight() >= self.maxh:
				self.Drop.SetSize(self.Drop.GetWidth(), self.maxh)
				self.Drop.box.SetSize(self.Drop.GetWidth()-1, self.maxh+1)
				self.ScrollBar.SetScrollBarSize(self.maxh)
				self.dropstat = 1
				self.DropList.SetViewItemCount(int(self.Drop.GetHeight()/16))
				self.ScrollBar.SetPos(self.lastS)
			else:
				self.ScrollBar.SetScrollBarSize(self.Drop.GetHeight() + iter)
				self.Drop.SetSize(self.Drop.GetWidth(), self.Drop.GetHeight() + iter)
				self.Drop.box.SetSize(self.Drop.GetWidth()-1, self.Drop.GetHeight() + iter +1)
				(w, h) = self.GetLocalPosition()
				self.SetPosition(w, h)
			self.DropList.SetViewItemCount(int(self.Drop.GetHeight()/16))
			self.DropList.SetBasePos(self.last + 1)
			self.DropList.SetBasePos(self.last)

		if self.dropped == 1:
			self.Drop.SetPosition(self.GetGlobalLeft(), self.GetGlobalTop() + self.GetHeight())

	def bgMouseIn(self):
		self.bg.SetColor(COLOR_DROP_DOWN_OVER)

	def bgMouseOut(self):
		self.bg.SetColor(COLOR_DROP_DOWN_NORMAL)

#################################################################################################################################
##### Edit2 ##### Edit2 ##### Edit2 ##### Edit2 ##### Edit2 ##### Edit2 ####### Edit2 ###### Edit2 ###### Edit2 ##### Edit2 #####
#################################################################################################################################
class Edit2(ui.EditLine):
	def __init__(self, main = "", ml = 4):
		ui.EditLine.__init__(self)
		self.SetText(main)
		self.main = main
		self.SetMax(ml)
		self.SetUserMax(ml)
		self.Bmax = 0
		self.Temp = ""
		self.SetReturnEvent(self.KillFocus)
		self.SetEscapeEvent(self.KillFocus)
		self.nextTab = None
		self.SetTabEvent(self.TabEvent)
		self.SetIMEUpdateEvent(self.OnTypeIMEEvent)

	def SetText(self, text):
		ui.EditLine.SetText(self, text)
		ime.SetCursorPosition(5)

	def SetMaxNumber(self, number):
		try:
			self.Bmax = MAX_NUM_FOR_BONUS[number]
			self.SetText(str(MAX_NUM_FOR_BONUS[number]))
		except BaseException:
			self.Bmax = 0
			self.SetText("0")

	def OnTypeIMEEvent(self):
		result = int(self.GetText())
		if result > self.Bmax:
			self.SetText(str(self.Bmax))
		else:
			self.SetText(str(result))

	def TabEvent(self):
		if self.nextTab:
			self.KillFocus()
			self.nextTab.SetFocus()

	def SetNextTab(self, tab):
		self.nextTab = proxy(tab)

	def GetText(self):
		res = ui.EditLine.GetText(self)
		if res == "":
			return "0"
		else:
			return res

	def __del__(self):
		ui.EditLine.__del__(self)

	def OnSetFocus(self):
		ui.EditLine.OnSetFocus(self)
		self.Temp = self.GetText()
		self.SetText("")
		ime.SetCursorPosition(5)

	def OnKillFocus(self):
		ui.EditLine.OnKillFocus(self)
		if ui.EditLine.GetText(self) == "":
			self.SetText(self.Temp)

class BoxEdit2(ui.Bar):
	def __init__(self, main = "", ml = 4):
		ui.Bar.__init__(self)
		self.Line = Edit2(main, ml)
		self.Line.SetParent(self)
		self.GetText = self.Line.GetText
		self.SetText = self.Line.SetText
		self.Line.SetNumberMode()
		self.Line.SetVerticalAlignCenter()
		self.Line.SetSize(80, 20)
		self.Line.SetPosition(4, 9)
		self.Line.SetPackedFontColor(0xffa08784)
		self.Line.Show()

		box = ui.Box()
		box.AddFlag("not_pick")
		box.SetParent(self)
		box.SetPosition(0, 0)
		box.SetColor(COLOR_DROP_DOWN_BOX)
		box.Show()
		self.Box = box

		self.Line.SetOverInEvent(self.bgMouseIn)
		self.Line.SetOverOutEvent(self.bgMouseOut)
		self.SetOverInEvent(self.bgMouseIn)
		self.SetOverInEvent(self.bgMouseOut)

	def SetSize(self, width, height):
		self.realWidth = width
		self.realHeight = height
		ui.Bar.SetSize(self, width, height)
		self.Line.SetSize(width-4, 20)
		self.Box.SetSize(width-1, height-1)

	def bgMouseIn(self):
		self.SetColor(COLOR_DROP_DOWN_OVER)
		self.Line.SetPackedFontColor(0xfff88f90)

	def bgMouseOut(self):
		self.SetColor(COLOR_DROP_DOWN_NORMAL)
		self.Line.SetPackedFontColor(0xffa08784)

class BoxNotEdit(ui.Bar):
	def __init__(self):
		ui.Bar.__init__(self)
		self.Line = ui.TextLine()
		self.Line.SetParent(self)
		self.GetText = self.Line.GetText
		self.SetText = self.Line.SetText
		self.Line.SetSize(80, 20)
		self.Line.SetPosition(4, 3)
		self.Line.SetText("0")
		self.Line.SetPackedFontColor(0xFFC8B89C)
		self.Line.Show()
		self.Line.SetMaxNumber = ui.__mem_func__(self.SetMaxNumber)

		box = ui.Box()
		box.AddFlag("not_pick")
		box.SetParent(self)
		box.SetPosition(0, 0)
		box.SetColor(COLOR_DROP_DOWN_BOX)
		box.Show()
		self.Box = box

	def SetSize(self, width, height):
		self.realWidth = width
		self.realHeight = height
		ui.Bar.SetSize(self, width, height)
		self.Line.SetSize(width-4, 20)
		self.Box.SetSize(width-1, height-1)

	def SetMaxNumber(self, number):
		try:
			self.Line.SetText(str(MAX_NUM_FOR_BONUS_RARE[number]))
		except BaseException:
			self.Line.SetText("0")

#################################################################################################################################
##### CheckBox ##### CheckBox ##### CheckBox ##### CheckBox ##### CheckBox ##### CheckBox ####### CheckBox ###### CheckBox ######
#################################################################################################################################
def MakeCheckBox(name, parent, x, y, eventUp = None, eventDown = None):
	checkbox = CheckBox(name)
	checkbox.SetParent(parent)
	checkbox.SetPosition(x, y)
	if eventUp:
		checkbox.eventUp = ui.__mem_func__(eventUp)
	if eventDown:
		checkbox.eventDown = ui.__mem_func__(eventDown)
	checkbox.Show()
	return checkbox

class CheckBox(ui.Window):
	checked = 0
	eventUp = None
	eventDown = None

	def __init__(self, cont = ""):
		ui.Window.__init__(self)
		self.BG = ui.Button()
		self.BG.SetParent(self)
		self.BG.SetPosition(0, 0)
		self.BG.SetUpVisual("interface/controls/common/checkbox/empty_01_normal.tga")
		self.BG.SetOverVisual("interface/controls/common/checkbox/empty_02_hover.tga")
		self.BG.SetDownVisual("interface/controls/common/checkbox/empty_03_active.tga")
		self.BG.Show()
		self.Title = ui.TextLine()
		self.Title.SetPackedFontColor(0xffa08784)
		self.Title.SetParent(self)
		self.Title.SetPosition(25, 0)
		self.Title.SetText(cont)
		self.Title.Show()
		self.SetSize(25 + self.Title.GetTextSize()[0] + 5, 15)

		self.BG.SetEvent(self.Toggle)
		self.SetOverInEvent(self.Title.SetPackedFontColor, 0xfff88f90)
		self.BG.SetOverInEvent(self.Title.SetPackedFontColor, 0xfff88f90)
		self.SetOverOutEvent(self.Title.SetPackedFontColor, 0xffa08784)
		self.BG.SetOverOutEvent(self.Title.SetPackedFontColor, 0xffa08784)
		self.SetMouseLeftButtonUpEvent(self.Toggle)

	def __del__(self):
		ui.Window.__del__(self)

	def Toggle(self):
		if self.checked == 1:
			self.OnToggleUp()
		else:
			self.OnToggleDown()

	def OnToggleUp(self):
		self.checked = 0
		self.BG.SetUpVisual("interface/controls/common/checkbox/empty_01_normal.tga")
		self.BG.SetOverVisual("interface/controls/common/checkbox/empty_02_hover.tga")
		self.BG.SetDownVisual("interface/controls/common/checkbox/empty_03_active.tga")
		if self.eventUp:
			self.eventUp()

	def OnToggleDown(self):
		self.checked = 1
		self.BG.SetUpVisual("interface/controls/common/checkbox/filled_01_normal.tga")
		self.BG.SetOverVisual("interface/controls/common/checkbox/filled_02_hover.tga")
		self.BG.SetDownVisual("interface/controls/common/checkbox/filled_03_active.tga")
		if self.eventDown:
			self.eventDown()

	def ToggleUp(self):
		self.checked = 0
		self.BG.SetUpVisual("interface/controls/common/checkbox/empty_01_normal.tga")
		self.BG.SetOverVisual("interface/controls/common/checkbox/empty_02_hover.tga")
		self.BG.SetDownVisual("interface/controls/common/checkbox/empty_03_active.tga")

	def ToggleDown(self):
		self.checked = 1
		self.BG.SetUpVisual("interface/controls/common/checkbox/filled_01_normal.tga")
		self.BG.SetOverVisual("interface/controls/common/checkbox/filled_02_hover.tga")
		self.BG.SetDownVisual("interface/controls/common/checkbox/filled_03_active.tga")

# a = Bot()
# a.Show()
# a.itemTabBar.AddTab(1, 0)
# a.itemTabBar.AddTab(2, 0)