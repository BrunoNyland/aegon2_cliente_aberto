#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import XXjvumrgrYBZompk3PS8 as item
import ga3vqy6jtxqi9yf344j7 as player
import enszxc3467hc3kokdueq as app
import LURMxMaKZJqliYt2QSHG as chat
import ui
import skill
import localeinfo
import wndMgr
import constinfo
import mousemodule
import guild
import os

MOUSE_SETTINGS = [0, 0]

def InitMouseButtonSettings(left, right):
	global MOUSE_SETTINGS
	MOUSE_SETTINGS = [left, right]

def SetMouseButtonSetting(dir, event):
	global MOUSE_SETTINGS
	MOUSE_SETTINGS[dir] = event

def GetMouseButtonSettings():
	global MOUSE_SETTINGS
	return MOUSE_SETTINGS

def SaveMouseButtonSettings():
	global MOUSE_SETTINGS
	open("miles/mouse.cfg", "w", "folder").write("%s\t%s" % tuple(MOUSE_SETTINGS))

def LoadMouseButtonSettings():
	global MOUSE_SETTINGS

	if not os.path.exists("miles/mouse.cfg"):
		MOUSE_SETTINGS[0] = int(5)
		MOUSE_SETTINGS[1] = int(3)
		open("miles/mouse.cfg", "w", "folder").write("5\t3")
		return

	tokens = open("miles/mouse.cfg", "r", "folder").read().split()

	if len(tokens) != 2:
		MOUSE_SETTINGS[0] = int(5)
		MOUSE_SETTINGS[1] = int(3)
		open("miles/mouse.cfg", "w", "folder").write("5\t3")
		return

	MOUSE_SETTINGS[0] = int(tokens[0])
	MOUSE_SETTINGS[1] = int(tokens[1])

class TaskBar(ui.ScriptWindow):

	BUTTON_CHARACTER = 0
	BUTTON_INVENTORY = 1
	BUTTON_MESSENGER = 2
	BUTTON_SYSTEM = 3
	BUTTON_CHAT = 4
	BUTTON_PKMODE = 5

	MOUSE_BUTTON_LEFT = 0
	MOUSE_BUTTON_RIGHT = 1
	NONE = 255

	EVENT_MOVE = 0
	EVENT_ATTACK = 1
	EVENT_MOVE_AND_ATTACK = 2
	EVENT_CAMERA = 3
	EVENT_SKILL = 4
	EVENT_AUTO = 5

	QUICKPAGE_NUMBER_FILENAME = [
		"d:/ymir work/ui/game/taskbar/1.sub",
		"d:/ymir work/ui/game/taskbar/2.sub",
		"d:/ymir work/ui/game/taskbar/3.sub",
		"d:/ymir work/ui/game/taskbar/4.sub",
	]

	QUICKPAGE_NUM = ["one", "two", "three", "four"]

	interface = "interface/controls/special/taskbar/"
	CAMERA = [interface + "btn_camera_01_normal.tga", interface + "btn_camera_02_hover.tga", interface + "btn_camera_03_active.tga"]
	AUTO = [interface + "btn_attackauto_01_normal.tga", interface + "btn_attackauto_02_hover.tga", interface + "btn_attackauto_03_active.tga"]
	NORMAL = [interface + "btn_attacknormal_01_normal.tga", interface + "btn_attacknormal_02_hover.tga", interface + "btn_attacknormal_03_active.tga"]

	def __init__(self):
		ui.ScriptWindow.__init__(self, "TOP_MOST")
		self.tooltipItem = None
		self.tooltipSkill = None
		self.TaskBarWindowList = {"LEFT":ui.ScriptWindow("TOP_MOST"), "RIGHT":ui.ScriptWindow("TOP_MOST")}
		self.mouseModeButtonList = [ None, ui.ScriptWindow("TOP_MOST") ]
		self.wndPkModeList = PkModeList()
		self.lastUpdateQuickSlot = 0
		self.SetWindowName("TaskBar")

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/_taskbar.py")
		pyScrLoader.LoadScriptFile(self.TaskBarWindowList["LEFT"], "uiscript/_taskbar_left.py")
		pyScrLoader.LoadScriptFile(self.TaskBarWindowList["RIGHT"], "uiscript/_taskbar_right.py")
		self.mouseModeButtonList[0] = self.GetChild("mask_left")
		self.mouseModeButtonList[1] = self.GetChild("mask_right")

		self.quickslot = []
		self.quickslot.append(self.GetChild("quick_slot_1"))
		self.quickslot.append(self.GetChild("quick_slot_2"))
		for slot in self.quickslot:
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectEmptySlotEvent(self.SelectEmptyQuickSlot)
			slot.SetSelectItemSlotEvent(self.SelectItemQuickSlot)
			slot.SetUnselectItemSlotEvent(self.UnselectItemQuickSlot)
			slot.SetOverInItemEvent(self.OverInItem)
			slot.SetOverOutItemEvent(self.OverOutItem)

		self.TaskBarWindowList["LEFT"].Show()
		self.TaskBarWindowList["RIGHT"].Show()
		self.mouseModeButtonList[1].Hide()
		self.mouseModeButtonList[0].Hide()
		self.SetHideEvent(self.IfHideDo)
		self.SetShowEvent(self.IfShowDo)
		self.GetChild("QuickSlotNumberButton").SetEvent(self.WindowShow, self.mouseModeButtonList[1])
		self.GetChild("LeftMouseButtonNew").SetEvent(self.WindowShow, self.mouseModeButtonList[0])

		self.PageNum = []
		self.PageNum.append(self.GetChild("1"))
		self.PageNum.append(self.GetChild("2"))
		self.PageNum.append(self.GetChild("3"))
		self.PageNum.append(self.GetChild("4"))
		self.PageNum[0].SetEvent(self.__SelectPageButton, 0)
		self.PageNum[1].SetEvent(self.__SelectPageButton, 1)
		self.PageNum[2].SetEvent(self.__SelectPageButton, 2)
		self.PageNum[3].SetEvent(self.__SelectPageButton, 3)

		self.GetChild("Camera").SetEvent(self.SelectMouseButtonEventNew, self.MOUSE_BUTTON_LEFT, self.EVENT_CAMERA)
		self.GetChild("AtqNormal").SetEvent(self.SelectMouseButtonEventNew, self.MOUSE_BUTTON_LEFT, self.EVENT_MOVE_AND_ATTACK)
		self.GetChild("AtqAuto").SetEvent(self.SelectMouseButtonEventNew, self.MOUSE_BUTTON_LEFT, self.EVENT_AUTO)

		toggleButtonDict = {}
		toggleButtonDict[TaskBar.BUTTON_CHAT] = self.GetChild("ChatButton")
		toggleButtonDict[TaskBar.BUTTON_SYSTEM] = self.TaskBarWindowList["RIGHT"].GetChild("Button_Menu")

		toggleButtonDict[TaskBar.BUTTON_INVENTORY] = self.TaskBarWindowList["RIGHT"].GetChild("Button_Inventory")
		toggleButtonDict[TaskBar.BUTTON_MESSENGER] = self.TaskBarWindowList["RIGHT"].GetChild("Button_Friends")
		toggleButtonDict[TaskBar.BUTTON_CHARACTER] = self.TaskBarWindowList["RIGHT"].GetChild("Button_Player")
		toggleButtonDict[TaskBar.BUTTON_PKMODE] = self.TaskBarWindowList["RIGHT"].GetChild("Button_PKmode")
		toggleButtonDict[TaskBar.BUTTON_PKMODE].SetEvent(self.ShowPkModeList)

		self.toggleButtonDict = toggleButtonDict

		self.TaskBarWindowList["RIGHT"].GetChild("GoldSlot").SetOverInEvent(self.ShowGoldHelper)
		self.TaskBarWindowList["RIGHT"].GetChild("GoldSlot").SetOverOutEvent(self.HideGoldHelper)

		self.TaskBarWindowList["RIGHT"].GetChild("GoldSlot").Hide()

		for item in ["hp", "mp", "tp"]:
			self.TaskBarWindowList["LEFT"].GetChild(item + "_empty").SetOverInEvent(self.ShowTooltip, item)
			self.TaskBarWindowList["LEFT"].GetChild(item + "_empty").SetOverOutEvent(self.HideTooltip, item)
			self.TaskBarWindowList["LEFT"].GetChild("tooltip_" + item).OnUpdate = ui.__mem_func__(self.OnUpdateTooltip)
		self.TaskBarWindowList["RIGHT"].GetChild("tooltip_gold").OnUpdate = ui.__mem_func__(self.OnUpdateTooltipGold)

		self.quickSlotPageIndex = 0
		self.__LoadMouseSettings()
		self.RefreshStatus()
		self.RefreshQuickSlot()

	def OnUpdateTooltip(self):
		for item in ["hp", "mp", "tp"]:
			this = self.TaskBarWindowList["LEFT"].GetChild("tooltip_" + item)
			if this.IsShow():
				this.SetPosition(max(wndMgr.GetMousePosition()[0] - this.GetWidth()/2 - 4, 0), this.GetTop())

	def OnUpdateTooltipGold(self):
		this = self.TaskBarWindowList["RIGHT"].GetChild("tooltip_gold")
		if not this.IsShow():
			return
		parent = self.TaskBarWindowList["RIGHT"].GetChild("GoldSlot")
		this.SetPosition(wndMgr.GetMousePosition()[0] - parent.GetGlobalPosition()[0] - this.GetWidth()/2, this.GetTop())

	def WindowShow(self, window):
		if window.IsShow():
			window.Hide()
		else:
			window.Show()

	def ShowPkModeList(self):
		if self.wndPkModeList.IsShow:
			self.wndPkModeList.Hide()
		else:
			self.wndPkModeList.Show()

	def __LoadMouseSettings(self):
		LoadMouseButtonSettings()

		(mouseLeftButtonEvent, mouseRightButtonEvent) = GetMouseButtonSettings()
		if not self.__IsInSafeMouseButtonSettingRange(mouseLeftButtonEvent) or not self.__IsInSafeMouseButtonSettingRange(mouseRightButtonEvent):
			InitMouseButtonSettings(self.EVENT_MOVE_AND_ATTACK, self.EVENT_CAMERA)
			(mouseLeftButtonEvent, mouseRightButtonEvent) = GetMouseButtonSettings()

		self.SelectMouseButtonEventNew(self.MOUSE_BUTTON_LEFT, mouseLeftButtonEvent)

	def __IsInSafeMouseButtonSettingRange(self, arg):
		return arg >= self.EVENT_MOVE and arg <= self.EVENT_AUTO

	def Destroy(self):
		SaveMouseButtonSettings()

		self.wndPkModeList.Destroy()
		self.wndPkModeList = None

		self.ClearDictionary()

		self.expGauge = None
		self.hpGauge = None
		self.mpGauge = None
		self.stGauge = None
		self.hpRecoveryGaugeBar = None
		self.spRecoveryGaugeBar = None

		self.tooltipItem = None
		self.tooltipSkill = None
		self.quickslot = 0
		self.toggleButtonDict = 0

		self.hpGaugeBoard = 0
		self.mpGaugeBoard = 0
		self.stGaugeBoard = 0
		self.expGaugeBoard = 0

		self.quickSlotPageIndex = 0
		self.mouseModeButtonList = []
		self.TaskBarWindowList = {}

	def __SelectPageButton(self, num):
		self.quickSlotPageIndex = num
		player.SetQuickPage(num)
		self.mouseModeButtonList[1].Hide()

	def SetToggleButtonEvent(self, eButton, kEventFunc):
		self.toggleButtonDict[eButton].SetEvent(kEventFunc)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SetSkillToolTip(self, tooltipSkill):
		self.tooltipSkill = tooltipSkill

	def RefreshStatus(self):
		curHP = player.GetStatus(player.HP)
		maxHP = player.GetStatus(player.MAX_HP)
		curSP = player.GetStatus(player.SP)
		maxSP = player.GetStatus(player.MAX_SP)
		recoveryHP = player.GetStatus(player.HP_RECOVERY)
		recoverySP = player.GetStatus(player.SP_RECOVERY)
		self.RefreshStamina()

		self.SetHP(curHP, recoveryHP, maxHP)
		self.SetSP(curSP, recoverySP, maxSP)

		money = player.GetElk()
		self.TaskBarWindowList["RIGHT"].GetChild("Gold_Text").SetText(localeinfo.NumberToMoneyString(money) + " Gold")

		masc = money/100000000
		if masc < 1:
			self.TaskBarWindowList["RIGHT"].GetChild("tooltip_gold").SetText("Apróx. %d Máscara da Fortuna" % (masc))
		else:
			self.TaskBarWindowList["RIGHT"].GetChild("tooltip_gold").SetText("Apróx. %d Máscaras da Fortuna" % (masc))

	def ShowTooltip(self, abrev):
		self.TaskBarWindowList["LEFT"].GetChild("tooltip_" + abrev).Show()

	def HideTooltip(self, abrev):
		self.TaskBarWindowList["LEFT"].GetChild("tooltip_" + abrev).Hide()

	def ShowGoldHelper(self):
		self.TaskBarWindowList["RIGHT"].GetChild("tooltip_gold").Show()

	def HideGoldHelper(self):
		self.TaskBarWindowList["RIGHT"].GetChild("tooltip_gold").Hide()

	def RefreshStamina(self):
		curST = player.GetStatus(player.STAMINA)
		maxST = player.GetStatus(player.MAX_STAMINA)
		self.SetST(curST, maxST)

	def SetHP(self, curPoint, recoveryPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			percentage = max(0, int((float(curPoint)/float(maxPoint))*100))
			destPoint = min(maxPoint, curPoint + recoveryPoint)
			recovery_percentage = max(0, int((float(destPoint)/float(maxPoint))*100))
			self.TaskBarWindowList["LEFT"].GetChild("hp_full").SetPercentage(percentage, 100)
			self.TaskBarWindowList["LEFT"].GetChild("hp_mid").SetPercentage(recovery_percentage, 100)
			self.TaskBarWindowList["LEFT"].GetChild("tooltip_hp").SetText("Vida: %d de %d" % (curPoint, maxPoint))

	def SetSP(self, curPoint, recoveryPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			percentage = max(0, int((float(curPoint)/float(maxPoint))*100))
			destPoint = min(maxPoint, curPoint + recoveryPoint)
			recovery_percentage = max(0, int((float(destPoint)/float(maxPoint))*100))
			self.TaskBarWindowList["LEFT"].GetChild("mp_full").SetPercentage(percentage, 100)
			self.TaskBarWindowList["LEFT"].GetChild("mp_mid").SetPercentage(recovery_percentage, 100)
			self.TaskBarWindowList["LEFT"].GetChild("tooltip_mp").SetText("Magia: %d de %d" % (curPoint, maxPoint))

	def SetST(self, curPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		if maxPoint > 0:
			percentage = max(0, int((float(curPoint)/float(maxPoint)) * 100))
			self.TaskBarWindowList["LEFT"].GetChild("tp_full").SetPercentage(percentage, 100)
			self.TaskBarWindowList["LEFT"].GetChild("tooltip_tp").SetText("Energia: %d de %d" % (curPoint, maxPoint))

	def RefreshQuickSlot(self):
		pageNum = player.GetQuickPage()
		name = TaskBar.QUICKPAGE_NUM[pageNum]
		self.GetChild("QuickSlotNumberButton").SetUpVisual("interface/controls/special/taskbar/btn_slotpage" + name + "_01_normal.tga")
		self.GetChild("QuickSlotNumberButton").SetOverVisual("interface/controls/special/taskbar/btn_slotpage" + name + "_02_hover.tga")
		self.GetChild("QuickSlotNumberButton").SetDownVisual("interface/controls/special/taskbar/btn_slotpage" + name + "_03_active.tga")

		startNumber = 0
		for slot in self.quickslot:
			for i in range(4):
				slotNumber = i+startNumber
				(Type, Position) = player.GetLocalQuickSlot(slotNumber)
				if player.SLOT_TYPE_NONE == Type:
					slot.ClearSlot(slotNumber)
					continue

				if player.SLOT_TYPE_INVENTORY == Type:
					itemIndex = player.GetItemIndex(Position)
					itemCount = player.GetItemCount(Position)
					if itemCount <= 1:
						itemCount = 0

					if constinfo.IS_AUTO_POTION(itemIndex):
						metinSocket = [player.GetItemMetinSocket(Position, j) for j in range(player.METIN_SOCKET_MAX_NUM)]
						if 0 != int(metinSocket[0]):
							slot.ActivateSlot(slotNumber)
						else:
							slot.DeactivateSlot(slotNumber)

					if constinfo.IS_ITEM_BUG_IN_TASKBAR(itemIndex):
						slot.ClearSlot(slotNumber)
						continue
					else:
						slot.SetItemSlot(slotNumber, itemIndex, itemCount)

				elif player.SLOT_TYPE_SKILL == Type:
					skillIndex = player.GetSkillIndex(Position)
					if 0 == skillIndex:
						slot.ClearSlot(slotNumber)
						continue

					skillType = skill.GetSkillType(skillIndex)
					if skill.SKILL_TYPE_GUILD == skillType:
						skillGrade = 0
						skillLevel = guild.GetSkillLevel(Position)
					else:
						skillGrade = player.GetSkillGrade(Position)
						skillLevel = player.GetSkillLevel(Position)

					slot.SetSkillSlotNew(slotNumber, skillIndex, skillGrade, skillLevel)
					slot.SetSlotCountNew(slotNumber, skillGrade, skillLevel)
					slot.SetCoverButton(slotNumber)

					if player.IsSkillCoolTime(Position):
						(coolTime, elapsedTime) = player.GetSkillCoolTime(Position)
						slot.SetSlotCoolTime(slotNumber, coolTime, elapsedTime)

					if player.IsSkillActive(Position):
						slot.ActivateSlot(slotNumber)

				elif player.SLOT_TYPE_EMOTION == Type:
					emotionIndex = Position
					slot.SetEmotionSlot(slotNumber, emotionIndex)
					slot.SetCoverButton(slotNumber)
					slot.SetSlotCount(slotNumber, 0)

			slot.RefreshSlot()
			startNumber += 4

	def canAddQuickSlot(self, Type, slotNumber):
		if player.SLOT_TYPE_INVENTORY == Type:
			itemIndex = player.GetItemIndex(slotNumber)
			if constinfo.IS_ITEM_BUG_IN_TASKBAR(itemIndex):
				return False
			return item.CanAddToQuickSlotItem(itemIndex)
		return True

	def AddQuickSlot(self, localSlotIndex):
		AttachedSlotType = mousemodule.mouseController.GetAttachedType()
		AttachedSlotNumber = mousemodule.mouseController.GetAttachedSlotNumber()
		AttachedItemIndex = mousemodule.mouseController.GetAttachedItemIndex()

		if player.SLOT_TYPE_QUICK_SLOT == AttachedSlotType:
			player.RequestMoveGlobalQuickSlotToLocalQuickSlot(AttachedSlotNumber, localSlotIndex)

		elif player.SLOT_TYPE_EMOTION == AttachedSlotType:

			player.RequestAddLocalQuickSlot(localSlotIndex, AttachedSlotType, AttachedItemIndex)

		elif self.canAddQuickSlot(AttachedSlotType, AttachedSlotNumber):
			player.RequestAddLocalQuickSlot(localSlotIndex, AttachedSlotType, AttachedSlotNumber)

		mousemodule.mouseController.DeattachObject()
		self.RefreshQuickSlot()

	def SelectEmptyQuickSlot(self, slotIndex):
		if mousemodule.mouseController.isAttached():
			self.AddQuickSlot(slotIndex)

	def SelectItemQuickSlot(self, localQuickSlotIndex):
		if mousemodule.mouseController.isAttached():
			self.AddQuickSlot(localQuickSlotIndex)
		else:
			globalQuickSlotIndex=player.LocalQuickSlotIndexToGlobalQuickSlotIndex(localQuickSlotIndex)
			mousemodule.mouseController.AttachObject(self, player.SLOT_TYPE_QUICK_SLOT, globalQuickSlotIndex, globalQuickSlotIndex)

	def UnselectItemQuickSlot(self, localSlotIndex):
		if False == mousemodule.mouseController.isAttached():
			player.RequestUseLocalQuickSlot(localSlotIndex)
			return

		elif mousemodule.mouseController.isAttached():
			mousemodule.mouseController.DeattachObject()
			return

	if app.SKILL_COOLTIME_UPDATE:
		def SkillClearCoolTime(self, usedSlotIndex):
			QUICK_SLOT_SLOT_COUNT = 4
			slotIndex = 0
			for slotWindow in self.quickslot:
				for i in range(QUICK_SLOT_SLOT_COUNT):
					(Type, Position) = player.GetLocalQuickSlot(slotIndex)
					if Type == player.SLOT_TYPE_SKILL:
						if usedSlotIndex == Position:
							slotWindow.SetSlotCoolTime(slotIndex, 0)
							return
					slotIndex += 1

	def OnUseSkill(self, usedSlotIndex, coolTime):
		QUICK_SLOT_SLOT_COUNT = 4
		slotIndex = 0

		for slotWindow in self.quickslot:
			for i in range(QUICK_SLOT_SLOT_COUNT):
				(Type, Position) = player.GetLocalQuickSlot(slotIndex)
				if Type == player.SLOT_TYPE_SKILL:
					if usedSlotIndex == Position:
						slotWindow.SetSlotCoolTime(slotIndex, coolTime)
						return
				slotIndex += 1

	def OnActivateSkill(self, usedSlotIndex):
		slotIndex = 0
		for slotWindow in self.quickslot:
			for i in range(4):
				(Type, Position) = player.GetLocalQuickSlot(slotIndex)
				if Type == player.SLOT_TYPE_SKILL:
					if usedSlotIndex == Position:
						slotWindow.ActivateSlot(slotIndex)
						return
				slotIndex += 1

	def OnDeactivateSkill(self, usedSlotIndex):
		slotIndex = 0
		for slotWindow in self.quickslot:
			for i in range(4):
				(Type, Position) = player.GetLocalQuickSlot(slotIndex)
				if Type == player.SLOT_TYPE_SKILL:
					if usedSlotIndex == Position:
						slotWindow.DeactivateSlot(slotIndex)
						return
				slotIndex += 1

	def OverInItem(self, slotNumber):
		if mousemodule.mouseController.isAttached():
			return

		(Type, Position) = player.GetLocalQuickSlot(slotNumber)

		if player.SLOT_TYPE_INVENTORY == Type:
			self.tooltipItem.SetInventoryItem(Position)
			self.tooltipSkill.HideToolTip()

		elif player.SLOT_TYPE_SKILL == Type:

			skillIndex = player.GetSkillIndex(Position)
			skillType = skill.GetSkillType(skillIndex)

			if skill.SKILL_TYPE_GUILD == skillType:
				skillGrade = 0
				skillLevel = guild.GetSkillLevel(Position)
			else:
				skillGrade = player.GetSkillGrade(Position)
				skillLevel = player.GetSkillLevel(Position)

			self.tooltipSkill.SetSkillNew(Position, skillIndex, skillGrade, skillLevel)
			self.tooltipItem.HideToolTip()

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
		if self.tooltipSkill:
			self.tooltipSkill.HideToolTip()

	def SelectMouseButtonEventNew(self, dir, event):
		SetMouseButtonSetting(dir, event)
		self.mouseModeButtonList[0].Hide()
		button = self.GetChild("LeftMouseButtonNew")
		func = self.NONE

		if self.EVENT_AUTO == event:
			func = player.MBF_AUTO
			button.SetUpVisual(self.AUTO[0])
			button.SetOverVisual(self.AUTO[1])
			button.SetDownVisual(self.AUTO[2])
			player.SetMouseFunc(player.MBT_RIGHT, player.MBF_CAMERA)

		elif self.EVENT_MOVE_AND_ATTACK == event:
			func = player.MBF_SMART
			button.SetUpVisual(self.NORMAL[0])
			button.SetOverVisual(self.NORMAL[1])
			button.SetDownVisual(self.NORMAL[2])
			player.SetMouseFunc(player.MBT_RIGHT, player.MBF_CAMERA)

		elif self.EVENT_CAMERA == event:
			func = player.MBF_CAMERA
			button.SetUpVisual(self.CAMERA[0])
			button.SetOverVisual(self.CAMERA[1])
			button.SetDownVisual(self.CAMERA[2])
			player.SetMouseFunc(player.MBT_RIGHT, player.MBF_SMART)

		player.SetMouseFunc(player.MBT_LEFT, func)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.curSkillButton.SetSkill(skillSlotNumber)
		self.curSkillButton.Show()

	def IfHideDo(self):
		self.TaskBarWindowList["RIGHT"].Hide()
		self.TaskBarWindowList["LEFT"].Hide()
		self.mouseModeButtonList[0].Hide()
		self.mouseModeButtonList[1].Hide()

	def IfShowDo(self):
		self.TaskBarWindowList["RIGHT"].Show()
		self.TaskBarWindowList["LEFT"].Show()

class PkModeList(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self, "TOP_MOST")
		self.IsShow = False
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/_pkmode_list.py")

		self.GetChild("button1").SetMouseLeftButtonUpEvent(self.SetPkModePeace)
		self.GetChild("button2").SetMouseLeftButtonUpEvent(self.SetPkModeRevange)
		self.GetChild("button3").SetMouseLeftButtonUpEvent(self.SetPkModeGuild)
		self.GetChild("button4").SetMouseLeftButtonUpEvent(self.SetPkModeFree)

	def Destroy(self):
		self.ClearDictionary()

	def Show(self):
		self.IsShow = True
		ui.ScriptWindow.Show(self)

	def Hide(self):
		self.IsShow = False
		ui.ScriptWindow.Hide(self)

	def SetPkModePeace(self):
		net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)
		self.Hide()

	def SetPkModeRevange(self):
		net.SendChatPacket("/pkmode 1", chat.CHAT_TYPE_TALKING)
		self.Hide()

	def SetPkModeGuild(self):
		net.SendChatPacket("/pkmode 4", chat.CHAT_TYPE_TALKING)
		self.Hide()

	def SetPkModeFree(self):
		net.SendChatPacket("/pkmode 2", chat.CHAT_TYPE_TALKING)
		self.Hide()

# t = TaskBar()
# t.LoadWindow()