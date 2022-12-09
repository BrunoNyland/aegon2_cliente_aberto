#favor manter essa linha
import ga3vqy6jtxqi9yf344j7 as player
import L0E5ajNEGIFdtCIFglqo as chrmgr
import XXjvumrgrYBZompk3PS8 as item
import enszxc3467hc3kokdueq as app
import os

NEW_TASKBAR = True
NEW_INTERFACE = True
NEW_MESSENGER = True
NEW_CHARACTER = True
NEW_GUILD = True

DETECT_LEAKING_WINDOWS = False
if DETECT_LEAKING_WINDOWS:
	WINDOW_COUNT_OBJ = False # we only want to check leaking while we are in the game phase
	WINDOW_OBJ_COUNT = 0 # number of leaking window (only counting this if window_count_obj is true)
	WINDOW_OBJ_LIST = {} # here we store the init-ed but not del-ed (so currently allocated) windows
	WINDOW_OBJ_TRACE = [] # we store the curent stackstrace here
	WINDOW_TOTAL_OBJ_COUNT = 0 # number of total allocated windows

coins = 0
blockMode = 0

WHISPER_MESSAGES = {}

if app.ENABLE_SWITCH_IMPROVEMENT:
	INVENTORY_ITENS_UPDATE = {}

	def AddItemToList(slot):
		if not INVENTORY_ITENS_UPDATE.has_key(slot):
			INVENTORY_ITENS_UPDATE.update({slot : 1})
		else:
			INVENTORY_ITENS_UPDATE[slot] = 1

	def SetItemUpdated(slot):
		if INVENTORY_ITENS_UPDATE.has_key(slot):
			INVENTORY_ITENS_UPDATE[slot] = 1

	def SetItemSwitched(slot):
		if INVENTORY_ITENS_UPDATE.has_key(slot):
			INVENTORY_ITENS_UPDATE[slot] = 0

	def CanSwitchItem(slot):
		return INVENTORY_ITENS_UPDATE[slot] == 1

if app.ENABLE_SEND_TARGET_INFO:
	MONSTER_INFO_DATA = {}

if app.ENABLE_DROP_COFRE:
	CHEST_DROP_INFO_DATA = {}

APP_TITLE_NEW = ""

PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 30

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL2
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]
NEBLINA = FOG_LEVEL

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_LONG

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT = "d:/ymir work/environment/moonlight04.msenv"

PRICE_CHECKER = 0
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960

USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
PVPMODE_PROTECTED_LEVEL = 15
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

isItemDropQuestionDialog = 0
isItemQuestionDialog = 0

INPUT = 0

RANKING_LIST = []
WAR_LIST = []
WAR_LOGS = {}
WAR_KILL = {}

#SHOP OFFLINE
def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag
#FINAL SHOP OFFLINE

def GET_ITEM_DROP_QUESTION_DIALOG_STATUS():
	global isItemDropQuestionDialog
	return isItemDropQuestionDialog

def SET_ITEM_DROP_QUESTION_DIALOG_STATUS(flag):
	global isItemDropQuestionDialog
	isItemDropQuestionDialog = flag

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

ACCESSORY_MATERIAL_LIST = [50623,50624,50625,50626,50627,50628,50629,50630,50631,50632,50633,50634,50635,50636,50637,50638]

JewelAccessoryInfos = [
	[ 50634, 83020, 16220, 17220 ],
	[ 50635, 14500, 16500, 17500 ],
	[ 50636, 14520, 16520, 17520 ],
	[ 50637, 14540, 16540, 17540 ],
	[ 50638, 14560, 16560, 17560 ],
]

def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10

	#BRACELETE OLIMPICO FIX
	if vnum == 11978:
		return 50634

	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE

	type = ret/20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) / 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	return 18900

def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:
		return 1
	elif itemVnum == 79012:
		return 1
	return 0

def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:
		return 1
	elif itemVnum == 79013:
		return 1
	elif itemVnum == 55701 or itemVnum == 55702 or itemVnum == 55703 or itemVnum == 55704:
		return 1

	return 0

def IS_ITEM_BUG_IN_TASKBAR(itemVnum):
	item_bloq = [
		71054, #Permissao de Exilio
		71099, #Anel da sucessao
		71100, #Pergaminho Troca de Forca
		71055, #Lista de Troca de Nome
		71048, #Pergaminho da Troca
		70056, #Pocao Regeneradora+
		71108, #Pocao Regeneradora+
		76000, #Pocao Regeneradora(B)
		70020, #Pocao Regeneradora
		98902, #Pocao Eterna
	]
	if itemVnum in item_bloq:
		return 1
	return 0

POTADOR = 0
DELAY_MACRO = 0.03

## CONFIGURACAO DE CAMERA
CAMERA_SETTINGS = [0.0, 0.0]

def InitCameraSettings(max_zoom, fog_distance):
	global CAMERA_SETTINGS
	CAMERA_SETTINGS = [max_zoom, fog_distance]

def SetCameraSetting(index, value):
	global CAMERA_SETTINGS
	CAMERA_SETTINGS[index] = value

def GetCameraSettings():
	global CAMERA_SETTINGS
	return CAMERA_SETTINGS

def SaveCameraSettings():
	global CAMERA_SETTINGS
	old_open("miles/camera.cfg", "w").write("%s\t%s" % tuple(CAMERA_SETTINGS))

def LoadCameraSettings():
	global CAMERA_SETTINGS

	if not os.path.exists("miles/camera.cfg"):
		old_open("miles/camera.cfg", "w").write("3500.00\t5000.00")
		CAMERA_SETTINGS[0] = 3500.00
		CAMERA_SETTINGS[1] = 5000.00
		return

	tokens = old_open("miles/camera.cfg", "r").read().split()

	if len(tokens) != 2:
		CAMERA_SETTINGS[0] = 3500.00
		CAMERA_SETTINGS[1] = 5000.00
		return

	CAMERA_SETTINGS[0] = float(tokens[0])
	CAMERA_SETTINGS[1] = float(tokens[1])

def SET_DEFAULT_FOG_LEVEL():
	global CAMERA_SETTINGS
	app.SetMinFog(CAMERA_SETTINGS[1])

def GET_FOG():
	global CAMERA_SETTINGS
	return CAMERA_SETTINGS[1]

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_SETTINGS
	app.SetCameraMaxDistance(CAMERA_SETTINGS[0])

def GET_CAMERA_MAX_DISTANCE():
	global CAMERA_SETTINGS
	return CAMERA_SETTINGS[0]

LoadCameraSettings()

AMOUNT = 0

def GetAmountSettings():
	global AMOUNT
	return AMOUNT

def SetAmountSetting(value):
	global AMOUNT
	AMOUNT = value
	SaveAmountSettings()

def SaveAmountSettings():
	global AMOUNT
	old_open("miles/amount.cfg", "w").write("%s" % AMOUNT)

def LoadShopAmountConfig():
	global AMOUNT

	if not os.path.exists("miles"):
		os.mkdir("miles")

	if not os.path.exists("miles/amount.cfg"):
		old_open("miles/amount.cfg", "w").write("1")
		AMOUNT = 1
		return

	tokens = old_open("miles/amount.cfg", "r").read().split()

	if len(tokens) != 1:
		AMOUNT = 1
		return

	AMOUNT = int(tokens[0])

LoadShopAmountConfig()