#favor manter essa linha
import ui
import grp
import LURMxMaKZJqliYt2QSHG as chat
import XXjvumrgrYBZompk3PS8 as item
import ga3vqy6jtxqi9yf344j7 as player
import uitooltip
import zn94xlgo573hf8xmddzq as net
import localeinfo
import mousemodule
import wait
import playersettingmodule
import uicommon
import exception

class PartyMemberInfoBoard(ui.ScriptWindow):
	interface = "interface/controls/special/party/"
	BOARD_WIDTH = 106
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
	GAUGE_OUT_LINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.3)

	LINK_COLOR = 0xffffffff
	UNLINK_COLOR = 0xffa08784
	OFF_COLOR = 0xc99f55900

	PARTY_AFFECT_EXPERIENCE			= 0
	PARTY_AFFECT_ATTACKER			= 1
	PARTY_AFFECT_TANKER				= 2
	PARTY_AFFECT_BUFFER				= 3
	PARTY_AFFECT_SKILL_MASTER		= 4
	PARTY_AFFECT_BERSERKER			= 5
	PARTY_AFFECT_DEFENDER			= 6
	PARTY_AFFECT_INCREASE_AREA_150	= 7
	PARTY_AFFECT_INCREASE_AREA_200	= 8
	AFFECT_STRING_DICT = {	PARTY_AFFECT_EXPERIENCE : localeinfo.PARTY_BONUS_EXP,
							PARTY_AFFECT_ATTACKER : localeinfo.PARTY_BONUS_ATTACKER,
							PARTY_AFFECT_TANKER : localeinfo.PARTY_BONUS_TANKER,
							PARTY_AFFECT_BUFFER : localeinfo.PARTY_BONUS_BUFFER,
							PARTY_AFFECT_SKILL_MASTER : localeinfo.PARTY_BONUS_SKILL_MASTER,
							PARTY_AFFECT_BERSERKER : localeinfo.PARTY_BONUS_BERSERKER,
							PARTY_AFFECT_DEFENDER : localeinfo.PARTY_BONUS_DEFENDER,
							PARTY_AFFECT_INCREASE_AREA_150 : localeinfo.PARTY_INCREASE_AREA_150,
							PARTY_AFFECT_INCREASE_AREA_200 : localeinfo.PARTY_INCREASE_AREA_200, }

	PARTY_SKILL_HEAL = 1
	PARTY_SKILL_WARP = 2
	MEMBER_BUTTON_NORMAL = 10
	MEMBER_BUTTON_WARP = 11
	MEMBER_BUTTON_EXPEL = 12
	MEMBER_BUTTON_PATH = "interface/controls/special/party/"
	MEMBER_BUTTON_IMAGE_FILE_NAME_DICT = {	player.PARTY_STATE_LEADER : "party_state_leader",
											player.PARTY_STATE_ATTACKER : "party_state_attacker",
											player.PARTY_STATE_BERSERKER : "party_state_berserker",
											player.PARTY_STATE_TANKER : "party_state_tanker",
											player.PARTY_STATE_DEFENDER : "party_state_defender",
											player.PARTY_STATE_BUFFER : "party_state_buffer",
											player.PARTY_STATE_SKILL_MASTER : "party_state_skill_master",
											MEMBER_BUTTON_NORMAL : "party_state_normal",
											MEMBER_BUTTON_WARP : "party_skill_warp",
											MEMBER_BUTTON_EXPEL : "party_expel", }

	STATE_NAME_DICT =	{	player.PARTY_STATE_ATTACKER : localeinfo.PARTY_SET_ATTACKER,
							player.PARTY_STATE_BERSERKER : localeinfo.PARTY_SET_BERSERKER,
							player.PARTY_STATE_TANKER : localeinfo.PARTY_SET_TANKER,
							player.PARTY_STATE_DEFENDER : localeinfo.PARTY_SET_DEFENDER,
							player.PARTY_STATE_BUFFER : localeinfo.PARTY_SET_BUFFER,
							player.PARTY_STATE_SKILL_MASTER : localeinfo.PARTY_SET_SKILL_MASTER, }

	faces = "interface/icons/faces/medium/"
	FACE_BUTTONS = {
		playersettingmodule.RACE_WARRIOR_M		:	"icon_mwarrior.tga",
		playersettingmodule.RACE_WARRIOR_W		:	"icon_wwarrior.tga",
		playersettingmodule.RACE_ASSASSIN_M		:	"icon_mninja.tga",
		playersettingmodule.RACE_ASSASSIN_W		:	"icon_wninja.tga",
		playersettingmodule.RACE_SURA_M			:	"icon_msura.tga",
		playersettingmodule.RACE_SURA_W			:	"icon_wsura.tga",
		playersettingmodule.RACE_SHAMAN_M		:	"icon_mshaman.tga",
		playersettingmodule.RACE_SHAMAN_W		:	"icon_wshaman.tga",
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.eventWhisper = None
		self.pid = None
		self.vid = None
		self.race = None
		self.online = None
		self.IsLeader = False
		self.partyAffectImageList = []
		self.stateButtonDict = {}
		self.affectValueDict = {}
		self.state = -1
		self.isShowStateButton = False

		self.__LoadBoard()
		self.__CreateAffectToolTip()
		self.__CreateStateButton()
		self.Show()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadBoard(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/partymemberinfoboardnew.py")
		except BaseException:
			exception.Abort("PartyMemberInfoBoard.__LoadBoard.LoadScript")

		try:
			self.nameTextLine = self.GetChild("NamePrint")
			self.gauge = self.GetChild("Gauge")
			self.stateButton = self.GetChild("StateButton")
			self.partyAffectImageList.append(self.GetChild("ExperienceImage"))
			self.partyAffectImageList.append(self.GetChild("AttackerImage"))
			self.partyAffectImageList.append(self.GetChild("DefenderImage"))
			self.partyAffectImageList.append(self.GetChild("BufferImage"))
			self.partyAffectImageList.append(self.GetChild("SkillMasterImage"))
			self.partyAffectImageList.append(self.GetChild("TimeBonusImage"))
			self.partyAffectImageList.append(self.GetChild("RegenBonus"))
			self.partyAffectImageList.append(self.GetChild("IncreaseArea150"))
			self.partyAffectImageList.append(self.GetChild("IncreaseArea200"))
			self.stateButton.SetEvent(self.OnMouseLeftButtonDown)
		except BaseException:
			exception.Abort("PartyMemberInfoBoard.__LoadBoard.BindObject")

		self.__SetAffectsMouseEvent()
		self.__HideAllAffects()
		self.SetMouseLeftButtonDoubleClickEvent(self.OnWhisper)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.nameTextLine = None
		self.eventWhisper = None
		self.gauge = None
		self.stateButton = None
		self.partyAffectImageList = []
		self.stateButtonDict = {}

		self.leaderButton = None
		self.attackerButton = None
		self.tankerButton = None

		self.Hide()

	def __SetAffectsMouseEvent(self):
		for i in range(len(self.partyAffectImageList)):
			self.partyAffectImageList[i].SetOverInEvent(self.OnAffectOverIn, i)
		for i in range(len(self.partyAffectImageList)):
			self.partyAffectImageList[i].SetOverOutEvent(self.OnAffectOverOut, i)

	def __HideAllAffects(self):
		for img in self.partyAffectImageList:
			img.Hide()

	def __CreateAffectToolTip(self):
		affectToolTip = uitooltip.ToolTip(200)
		affectToolTip.Hide()
		self.affectToolTip = affectToolTip

	def __CreateStateButton(self):
		for key, name in self.MEMBER_BUTTON_IMAGE_FILE_NAME_DICT.items():
			if key == player.PARTY_STATE_LEADER:
				self.IsLeader == True
				continue
			button = ui.Button()
			button.SetUpVisual(self.MEMBER_BUTTON_PATH + name + "_01.tga")
			button.SetOverVisual(self.MEMBER_BUTTON_PATH + name + "_02.tga")
			button.SetDownVisual(self.MEMBER_BUTTON_PATH + name + "_03.tga")
			button.Hide()
			self.stateButtonDict[key] = button

		for state, name in self.STATE_NAME_DICT.items():
			button = self.stateButtonDict[state]
			button.SetToolTipText(name)
			button.SetEvent(self.OnSelectState, state)

		self.stateButtonDict[self.MEMBER_BUTTON_NORMAL].SetEvent(self.OnSelectState, -1)
		self.stateButtonDict[self.MEMBER_BUTTON_NORMAL].SetToolTipText(localeinfo.PARTY_SET_NORMAL)
		self.stateButtonDict[self.MEMBER_BUTTON_WARP].SetEvent(self.OnWarp)
		self.stateButtonDict[self.MEMBER_BUTTON_WARP].SetToolTipText(localeinfo.PARTY_RECALL_MEMBER)
		self.stateButtonDict[self.MEMBER_BUTTON_EXPEL].SetToolTipText(localeinfo.TARGET_BUTTON_EXCLUDE)
		self.stateButtonDict[self.MEMBER_BUTTON_EXPEL].SetEvent(self.OnExpel)

	def __GetPartySkillLevel(self):
		slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_TONGSOL)
		skillGrade = player.GetSkillGrade(slotIndex)
		skillLevel = player.GetSkillLevel(slotIndex)
		return skillLevel + skillGrade*20

	def __AppendStateButton(self, x, y, state):
		if state == self.state:
			button = self.stateButtonDict[self.MEMBER_BUTTON_NORMAL]
		else:
			button = self.stateButtonDict[state]

		button.SetPosition(x, y)
		button.Show()

	def __ShowStateButton(self):
		self.isShowStateButton = True

		(x, y) = self.GetGlobalPosition()
		xPos = x + 110
		yPos = y + 2

		skillLevel = self.__GetPartySkillLevel()

		## Tanker
		if skillLevel >= 10:
			self.__AppendStateButton(xPos, yPos, player.PARTY_STATE_ATTACKER)
			xPos += 23

		## Attacker
		if skillLevel >= 20:
			self.__AppendStateButton(xPos, yPos, player.PARTY_STATE_BERSERKER)
			xPos += 23

		## Tanker
		if skillLevel >= 20:
			self.__AppendStateButton(xPos, yPos, player.PARTY_STATE_TANKER)
			xPos += 23

		## Buffer
		if skillLevel >= 25:
			self.__AppendStateButton(xPos, yPos, player.PARTY_STATE_BUFFER)
			xPos += 23

		## Skill Master
		if skillLevel >= 35:
			self.__AppendStateButton(xPos, yPos, player.PARTY_STATE_SKILL_MASTER)
			xPos += 23

		## Defender
		if skillLevel >= 40:
			self.__AppendStateButton(xPos, yPos, player.PARTY_STATE_DEFENDER)
			xPos += 23

		if self.stateButtonDict.__contains__(self.MEMBER_BUTTON_EXPEL):
			button = self.stateButtonDict[self.MEMBER_BUTTON_EXPEL]
			button.SetPosition(xPos, yPos)
			button.Show()
			xPos += 23

	def __HideStateButton(self):
		self.isShowStateButton = False
		for button in self.stateButtonDict.values():
			button.Hide()

	def __GetAffectNumber(self, img):
		for i in range(self.partyAffectImageList):
			if img == self.partyAffectImageList[i]:
				return i

		return -1

	def SetCharacterName(self, name):
		self.nameTextLine.SetText(name)
		x, y = self.nameTextLine.GetTextSize()
		if x > 40:
			self.GetChild("NameSlotFill").SetScale(float(x + 5), 1.0)
			self.GetChild("NameSlotRight").SetWindowHorizontalAlignRight()
		else:
			self.GetChild("NameSlotFill").SetScale(40.0, 1.0)
			self.GetChild("NameSlotRight").SetWindowHorizontalAlignRight()

	def GetCharacterName(self):
		return self.nameTextLine.GetText()

	def SetCharacterPID(self, pid):
		self.pid = pid

	def SetOnline(self, online):
		self.online = online

	def SetCharacterVID(self, vid):
		self.vid = vid

	def SetWhisperEvent(self, event):
		self.eventWhisper = ui.__mem_func__(event)

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.GetCharacterName())

	def GetCharacterPID(self):
		return self.pid

	def GetCharacterVID(self):
		return self.vid

	def SetCharacterHP(self, hpPercentage):
		hpPercentage = max(0, hpPercentage)
		self.gauge.SetPercentageNew(hpPercentage)

	def SetCharacterState(self, state):

		if self.state == state:
			return

		self.state = state
		self.stateButton.Show()
		if state == player.PARTY_STATE_LEADER:
			self.GetChild("leader").Show()
		else:
			self.GetChild("leader").Hide()

		name = self.MEMBER_BUTTON_IMAGE_FILE_NAME_DICT[self.MEMBER_BUTTON_NORMAL]
		if self.MEMBER_BUTTON_IMAGE_FILE_NAME_DICT.__contains__(state):
			name = self.MEMBER_BUTTON_IMAGE_FILE_NAME_DICT[state]
		
		self.stateButton.SetUpVisual(self.MEMBER_BUTTON_PATH + name + "_01.tga")
		self.stateButton.SetOverVisual(self.MEMBER_BUTTON_PATH + name + "_02.tga")
		self.stateButton.SetDownVisual(self.MEMBER_BUTTON_PATH + name + "_03.tga")

	def SetAffect(self, affectSlotIndex, affectValue):
		if affectSlotIndex >= len(self.partyAffectImageList):
			return

		if affectValue > 0:
			self.partyAffectImageList[affectSlotIndex].Show()
		else:
			self.partyAffectImageList[affectSlotIndex].Hide()

		self.affectValueDict[affectSlotIndex] = affectValue

	def HideButton(self):
		self.isShowStateButton = False
		for button in self.stateButtonDict.values():
			button.Hide()

	def Link(self):
		self.nameTextLine.SetPackedFontColor(self.LINK_COLOR)
		self.GetChild("HP_Gauge_Base").Show()
		self.gauge.Show()

	def Unlink(self):
		self.vid = None
		if self.online:
			self.nameTextLine.SetPackedFontColor(self.UNLINK_COLOR)
		else:
			self.nameTextLine.SetPackedFontColor(self.OFF_COLOR)
		self.gauge.Hide()
		self.GetChild("HP_Gauge_Base").Hide()
		self.__HideAllAffects()

	def OnSelectState(self, state):

		self.__HideStateButton()
		if state <= 0:
			net.SendPartySetStatePacket(self.pid, self.state, False)

		else:

			if self.state <= 0:
				net.SendPartySetStatePacket(self.pid, state, True)

			else:
				net.SendPartySetStatePacket(self.pid, self.state, False)
				net.SendPartySetStatePacket(self.pid, state, True)

	def OnWarp(self):
		self.__HideStateButton()

		if self.vid:
			net.SendPartyUseSkillPacket(self.PARTY_SKILL_WARP, self.vid)

	def OnExpel(self):
		self.__HideStateButton()

		if not self.pid:
			return

		net.SendPartyRemovePacket(self.pid, 0)

	def OnMouseLeftButtonDown(self):
		if self.vid:
			player.SetTarget(self.vid)
			player.OpenCharacterMenu(self.vid)

			if mousemodule.mouseController.isAttached():
				attachedSlotType = mousemodule.mouseController.GetAttachedType()
				if (player.SLOT_TYPE_INVENTORY == attachedSlotType):
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
					SrcSlotNumber = mousemodule.mouseController.GetAttachedSlotNumber()
					itemID = player.GetItemIndex(attachedInvenType, SrcSlotNumber)
					item.SelectItem(itemID)
					if item.IsAntiFlag(item.ANTIFLAG_GIVE):
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.EXCHANGE_CANNOT_GIVE)
						mousemodule.mouseController.DeattachObject()
						return
					net.SendExchangeStartPacket(self.vid)
					net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, 0)
				mousemodule.mouseController.DeattachObject()
				return

		if player.IsPartyLeader(player.GetMainCharacterIndex()):
			if player.PARTY_STATE_LEADER != self.state:
				if self.isShowStateButton:
					self.__HideStateButton()
				else:
					self.__ShowStateButton()

	def OnMouseLeftButtonUp(self):
		if self.vid:
			player.SetTarget(self.vid)
			player.OpenCharacterMenu(self.vid)

	def OnMouseRightButtonDown(self):
		self.OnMouseLeftButtonDown()

	def OnAffectOverIn(self, index):
		if index:
			self.partyAffectImageList[index].LoadImage(self.interface + "bonus_over.tga")
		if not self.AFFECT_STRING_DICT.__contains__(index):
			return
		if not self.affectValueDict.__contains__(index):
			return

		(x, y) = self.GetGlobalPosition()

		self.affectToolTip.ClearToolTip()
		self.affectToolTip.SetTitle(self.AFFECT_STRING_DICT[index](self.affectValueDict[index]))
		self.affectToolTip.SetToolTipPosition(x + 200, y + 50)
		self.affectToolTip.ShowToolTip()

	def OnAffectOverOut(self, index):
		if index:
			self.partyAffectImageList[index].LoadImage(self.interface + "bonus.tga")
		self.affectToolTip.HideToolTip()

class PartyHideWindow(ui.ScriptWindow):
	interface = "interface/controls/special/party/"

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadBoard()
		self.SetPosition(-250, 52)
		self.Show()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadBoard(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/partyhide.py")
		except BaseException:
			exception.Abort("PartyHideWindow.__LoadBoard.LoadScript")

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

class PartyWindow(ui.Window):
	interface = "interface/controls/special/party/"
	BUTTON_NAME = ( "Retrair", localeinfo.PARTY_HEAL_ALL_MEMBER, localeinfo.PARTY_BREAK_UP, localeinfo.PARTY_LEAVE)
	FACE_BUTTONS = {
		playersettingmodule.RACE_WARRIOR_M		:	"icon_mwarrior.tga",
		playersettingmodule.RACE_WARRIOR_W		:	"icon_wwarrior.tga",
		playersettingmodule.RACE_ASSASSIN_M		:	"icon_mninja.tga",
		playersettingmodule.RACE_ASSASSIN_W		:	"icon_wninja.tga",
		playersettingmodule.RACE_SURA_M			:	"icon_msura.tga",
		playersettingmodule.RACE_SURA_W			:	"icon_wsura.tga",
		playersettingmodule.RACE_SHAMAN_M		:	"icon_mshaman.tga",
		playersettingmodule.RACE_SHAMAN_W		:	"icon_wshaman.tga",
	}

	def __init__(self):
		ui.Window.__init__(self)
		self.WhisperEvent = None
		self.SetPosition(5, 52)
		self.partyMemberInfoBoardList = []
		PartyBG = ui.ExpandedImageBox()
		PartyBG.SetParent(self)
		PartyBG.SetPosition(-5, 0)
		PartyBG.LoadImage(self.interface + "party_bg.tga")
		self.PartyBG = PartyBG
		MenuBG = ui.ImageBox()
		MenuBG.LoadImage(self.interface + "party_menu_bg.tga")
		MenuBG.SetParent(self)
		MenuBG.SetPosition(-5, 0)
		MenuBG.Show()
		self.MenuBG = MenuBG
		self.buttonDict = {}
		self.distributionMode = 0
		self.isLeader = False
		self.showingButtonList = []
		self.modeButtonList = {}
		self.__CreateButtons()
		self.__CreateModeButtons()
		self.HideWindow = PartyHideWindow()
		self.HideWindow.GetChild("ExpandButton").SetEvent(self.__Expandir)

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Hide()
		self.DestroyPartyMemberInfoBoard()
		self.WhisperEvent = None
		self.buttonDict = {}
		self.showingButtonList = []
		self.modeButtonList = {}
		self.HideWindow = None
		self.ExpImage = None
		self.PartyBG = None
		self.MenuBG = None

	def DestroyPartyMemberInfoBoard(self):
		for board in self.partyMemberInfoBoardList:
			board.Destroy()

		self.partyMemberInfoBoardList = []

	def AddPartyMember(self, pid, name, race, online):
		board = self.__FindPartyMemberInfoBoardByPID(pid)

		if race > 7:
			race = 1

		if None == board:
			board = PartyMemberInfoBoard()
			board.SetParent(self)
			board.SetCharacterPID(pid)
			board.GetChild("face").LoadImage("interface/icons/faces/medium/" + self.FACE_BUTTONS[race])
			self.partyMemberInfoBoardList.append(board)
			self.__ArrangePartyMemberInfoBoard()
			self.UpdateRect()

		board.SetOnline(online)

		if not name:
			name = localeinfo.PARTY_MEMBER_OFFLINE

		board.SetWhisperEvent(self.WhisperEvent)
		board.SetCharacterName(name)
		board.Unlink()

		self.Show()

	def RemovePartyMember(self, pid):
		board = self.__FindPartyMemberInfoBoardByPID(pid)

		if None == board:
			return

		vid = board.GetCharacterVID()

		if None != vid and player.IsMainCharacterIndex(vid):
			self.ExitParty()
			player.ExitParty()
		else:
			board.Destroy()
			player.RemovePartyMember(pid)
			self.partyMemberInfoBoardList.remove(board)
			self.__ArrangePartyMemberInfoBoard()
			self.UpdateRect()

	def UpdatePartyMemberInfo(self, pid):
		board = self.__FindPartyMemberInfoBoardByPID(pid)

		if None == board:
			return

		state = player.GetPartyMemberState(pid)
		hpPercentage = player.GetPartyMemberHPPercentage(pid)
		affectsList = player.GetPartyMemberAffects(pid)

		board.SetCharacterState(state)
		board.SetCharacterHP(hpPercentage)
		for i in range(len(affectsList)):
			board.SetAffect(i, affectsList[i])

		vid = board.GetCharacterVID()
		if None != vid:
			if player.IsMainCharacterIndex(vid):
				if player.PARTY_STATE_LEADER == player.GetPartyMemberState(pid):
					self.ShowLeaderButton()
				else:
					self.ShowMemberButton()

	def LinkPartyMember(self, pid, vid):
		board = self.__FindPartyMemberInfoBoardByPID(pid)

		if None == board:
			return

		board.Link()
		board.SetCharacterVID(vid)

	def UnlinkPartyMember(self, pid):
		board = self.__FindPartyMemberInfoBoardByPID(pid)

		if None == board:
			return

		board.Unlink()

	def UnlinkAllPartyMember(self):
		for board in self.partyMemberInfoBoardList:
			board.Unlink()

	def ExitParty(self):
		self.DestroyPartyMemberInfoBoard()
		self.__Expandir_sem_efeito()
		self.Hide()

	def __HideAllMembersButtons(self):
		for board in self.partyMemberInfoBoardList:
			board.HideButton()

	def __ArrangePartyMemberInfoBoard(self):
		count = 0
		newHeight = 41
		for board in self.partyMemberInfoBoardList:
			board.SetPosition(0, 41 + count * (board.GetHeight() + 2))
			count += 1
			newHeight += board.GetHeight() + 2
		newHeight -= 7
		self.SetSize(150, newHeight)
		self.PartyBG.SetScale(1, newHeight + 5)
		self.PartyBG.Show()
		(x, y) = self.GetGlobalPosition()

	def __Retrair(self):
		self.__HideAllMembersButtons()
		(x, y) = self.GetGlobalPosition()
		(hx, hy) = self.HideWindow.GetGlobalPosition()
		if x > -205:
			self.SetPosition(x-10, 52)
			self.HideWindow.SetPosition(hx+10, 52)
			self.safe = wait.WaitingDialog()
			self.safe.Open(0.0)
			self.safe.SetTimeOverEvent(self.__Retrair)
		else:
			self.SetPosition(-205, 52)
			self.HideWindow.SetPosition(0, 52)

	def __Expandir(self):
		(x, y) = self.GetGlobalPosition()
		(hx, hy) = self.HideWindow.GetGlobalPosition()
		if x < 5:
			self.SetPosition(x+10, 52)
			self.HideWindow.SetPosition(hx-10, 52)
			self.safe = wait.WaitingDialog()
			self.safe.Open(0.0)
			self.safe.SetTimeOverEvent(self.__Expandir)
		else:
			self.SetPosition(5, 52)
			self.HideWindow.SetPosition(-205, 52)

	def __Expandir_sem_efeito(self):
		self.__HideAllMembersButtons()
		self.SetPosition(5, 52)
		self.HideWindow.SetPosition(-205, 52)

	def __FindPartyMemberInfoBoardByVID(self, vid):
		for board in self.partyMemberInfoBoardList:
			if vid == board.GetCharacterVID():
				return board
		return None

	def __FindPartyMemberInfoBoardByPID(self, pid):
		for board in self.partyMemberInfoBoardList:
			if pid == board.GetCharacterPID():
				return board
		return None

	def __CreateModeButtons(self):
		self.modeButtonList = {}

		level = ui.Button()
		level.SetParent(self)
		level.SetEvent(self.OnClickEXPLevel)
		level.SetUpVisual(self.interface + "party_exp_radio_btn_level_01_normal.tga")
		level.SetOverVisual(self.interface + "party_exp_radio_btn_level_02_hover.tga")
		level.SetDownVisual(self.interface + "party_exp_radio_btn_level_03_active.tga")
		level.Show()
		self.modeButtonList[player.PARTY_EXP_NON_DISTRIBUTION] = level

		parity = ui.Button()
		parity.SetParent(self)
		parity.SetEvent(self.OnClickEXPDistributeParity)
		parity.SetUpVisual(self.interface + "party_exp_radio_btn_equal_01_normal.tga")
		parity.SetOverVisual(self.interface + "party_exp_radio_btn_equal_02_hover.tga")
		parity.SetDownVisual(self.interface + "party_exp_radio_btn_equal_03_active.tga")

		parity.Show()
		self.modeButtonList[player.PARTY_EXP_DISTRIBUTION_PARITY] = parity

		ExpImage = ui.ImageBox()
		ExpImage.SetParent(self)
		ExpImage.LoadImage(self.interface + "party_exp_radio_active.tga")
		ExpImage.Hide()
		self.ExpImage = ExpImage

		self.ChangePartyParameter(self.distributionMode)

	def __CreateButtons(self):
		QuestionDialog = uicommon.QuestionDialog()
		QuestionDialog.SetText("Deseja sair do Grupo?")
		QuestionDialog.SetAcceptText("Sim")
		QuestionDialog.SetCancelText("Não")
		QuestionDialog.SetAcceptEvent(self.__Sair)
		QuestionDialog.SetCancelEvent(QuestionDialog.Close)
		self.QuestionDialog = QuestionDialog

		for name in self.BUTTON_NAME:
			button = ui.Button()
			button.SetParent(self)
			self.buttonDict[name] = button

		self.buttonDict["Retrair"].SetUpVisual(self.interface + "party_btn_hide_01_normal.tga")
		self.buttonDict["Retrair"].SetOverVisual(self.interface + "party_btn_hide_02_hover.tga")
		self.buttonDict["Retrair"].SetDownVisual(self.interface + "party_btn_hide_03_active.tga")
		self.buttonDict["Retrair"].SetEvent(self.__Retrair)

		self.buttonDict[localeinfo.PARTY_HEAL_ALL_MEMBER].SetEvent(self.OnPartyUseSkill)
		self.buttonDict[localeinfo.PARTY_HEAL_ALL_MEMBER].SetUpVisual(self.interface + "party_btn_leave_01_normal.tga")
		self.buttonDict[localeinfo.PARTY_HEAL_ALL_MEMBER].SetOverVisual(self.interface + "party_btn_leave_02_hover.tga")
		self.buttonDict[localeinfo.PARTY_HEAL_ALL_MEMBER].SetDownVisual(self.interface + "party_btn_leave_03_active.tga")

		self.buttonDict[localeinfo.PARTY_BREAK_UP].SetEvent(self.__Sair)
		self.buttonDict[localeinfo.PARTY_BREAK_UP].SetUpVisual(self.interface + "party_btn_leave_01_normal.tga")
		self.buttonDict[localeinfo.PARTY_BREAK_UP].SetOverVisual(self.interface + "party_btn_leave_02_hover.tga")
		self.buttonDict[localeinfo.PARTY_BREAK_UP].SetDownVisual(self.interface + "party_btn_leave_03_active.tga")

		self.buttonDict[localeinfo.PARTY_LEAVE].SetEvent(self.QuestionDialog.Open)
		self.buttonDict[localeinfo.PARTY_LEAVE].SetUpVisual(self.interface + "party_btn_leave_01_normal.tga")
		self.buttonDict[localeinfo.PARTY_LEAVE].SetOverVisual(self.interface + "party_btn_leave_02_hover.tga")
		self.buttonDict[localeinfo.PARTY_LEAVE].SetDownVisual(self.interface + "party_btn_leave_03_active.tga")

	def __Sair(self):
		net.SendPartyExitPacket()
		if self.QuestionDialog:
			self.QuestionDialog.Close()

	def __ClearShowingButtons(self):
		self.showingButtonList = []

	def __ArrangeButtons(self):
		showingButtonCount = len(self.showingButtonList)
		xPos = 4

		self.buttonDict[localeinfo.PARTY_LEAVE].SetPosition(xPos, 7)
		self.buttonDict[localeinfo.PARTY_LEAVE].Show()
		xPos += 30

		for button in self.modeButtonList.values():
			button.SetPosition(xPos, 7)
			xPos += 30

		self.buttonDict["Retrair"].SetPosition(xPos, 7)
		self.buttonDict["Retrair"].Show()
		xPos += 30

		self.UpdateRect()

	def __ShowButton(self, name):
		if not self.buttonDict.__contains__(name):
			return

		self.showingButtonList.append(self.buttonDict[name])
		self.__ArrangeButtons()

	def __HideButton(self, name):
		if not self.buttonDict.__contains__(name):
			return

		searchingButton = self.buttonDict[name]
		searchingButton.Hide()
		for btn in self.showingButtonList:
			if btn == searchingButton:
				self.showingButtonList.remove(btn)

		self.__ArrangeButtons()

	def ShowLeaderButton(self):
		self.isLeader = True
		self.__ClearShowingButtons()
		self.__ShowButton(localeinfo.PARTY_BREAK_UP)

	def ShowMemberButton(self):
		self.isLeader = False
		self.__ClearShowingButtons()
		self.__ShowButton(localeinfo.PARTY_LEAVE)

	def OnPartyUseSkill(self):
		net.SendPartyUseSkillPacket(PartyMemberInfoBoard.PARTY_SKILL_HEAL, 0)
		self.__HideButton(localeinfo.PARTY_HEAL_ALL_MEMBER)

	def PartyHealReady(self):
		self.__ShowButton(localeinfo.PARTY_HEAL_ALL_MEMBER)

	def __SetModeButton(self, mode):
		(x, y) = self.modeButtonList[mode].GetLocalPosition()
		self.distributionMode = mode
		if mode == player.PARTY_EXP_NON_DISTRIBUTION:
			self.ExpImage.SetPosition(x-4, y-4)
		elif mode == player.PARTY_EXP_DISTRIBUTION_PARITY:
			self.ExpImage.SetPosition(x-4, y-4)
		self.ExpImage.Show()

	def OnClickEXPLevel(self):
		self.__SetModeButton(self.distributionMode)
		if self.isLeader:
			net.SendPartyParameterPacket(player.PARTY_EXP_NON_DISTRIBUTION)

	def OnClickEXPDistributeParity(self):
		self.__SetModeButton(self.distributionMode)
		if self.isLeader:
			net.SendPartyParameterPacket(player.PARTY_EXP_DISTRIBUTION_PARITY)

	def ChangePartyParameter(self, distributionMode):
		try:
			self.__SetModeButton(distributionMode)
		except BaseException:
			pass