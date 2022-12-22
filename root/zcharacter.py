#favor manter essa linha
import enszxc3467hc3kokdueq as app
import zn94xlgo573hf8xmddzq as net
import LURMxMaKZJqliYt2QSHG as chat
import ga3vqy6jtxqi9yf344j7 as player
import L0E5ajNEGIFdtCIFglqo as chrmgr
import Js4k2l7BrdasmVRt8Wem as chr
import playersettingmodule
import dbg
import ui
import mousemodule
import wndMgr
import skill
import quest
import localeinfo
import uitooltip
import emotion
import colorinfo
import exception
import event
import grp

from _weakref import proxy

if app.ENABLE_SKILL_COLOR_SYSTEM:
	import uiskillcolor

temp = []
def Debug(msg):
	line = ui.MakeTextLine(None)
	line.SetText(msg)
	line.SetPosition(0, -260 + len(temp)*10)
	temp.append(line)

SHOW_LIMIT_SUPPORT_SKILL_LIST = []

FACE_IMAGE_DICT = {
	playersettingmodule.RACE_WARRIOR_M		:"interface/controls/common/faces/warrior_m.tga",
	playersettingmodule.RACE_WARRIOR_W		:"interface/controls/common/faces/warrior_w.tga",
	playersettingmodule.RACE_ASSASSIN_M		:"interface/controls/common/faces/assassin_m.tga",
	playersettingmodule.RACE_ASSASSIN_W		:"interface/controls/common/faces/assassin_w.tga",
	playersettingmodule.RACE_SURA_M			:"interface/controls/common/faces/sura_m.tga",
	playersettingmodule.RACE_SURA_W			:"interface/controls/common/faces/sura_w.tga",
	playersettingmodule.RACE_SHAMAN_M		:"interface/controls/common/faces/shaman_m.tga",
	playersettingmodule.RACE_SHAMAN_W		:"interface/controls/common/faces/shaman_w.tga",
}

class CharacterWindow(ui.ScriptWindow):

	ACTIVE_PAGE_SLOT_COUNT = 8
	SUPPORT_PAGE_SLOT_COUNT = 12

	PAGE_SLOT_COUNT = 6
	PAGE_HORSE = 2

	SKILL_GROUP_NAME_DICT = {
		playersettingmodule.JOB_WARRIOR		:{ 1 : localeinfo.SKILL_GROUP_WARRIOR_1,	2 : localeinfo.SKILL_GROUP_WARRIOR_2,	},
		playersettingmodule.JOB_ASSASSIN	:{ 1 : localeinfo.SKILL_GROUP_ASSASSIN_1,	2 : localeinfo.SKILL_GROUP_ASSASSIN_2,	},
		playersettingmodule.JOB_SURA		:{ 1 : localeinfo.SKILL_GROUP_SURA_1,		2 : localeinfo.SKILL_GROUP_SURA_2,		},
		playersettingmodule.JOB_SHAMAN		:{ 1 : localeinfo.SKILL_GROUP_SHAMAN_1,		2 : localeinfo.SKILL_GROUP_SHAMAN_2,	},
	}

	STAT_DESCRIPTION = {
		"HTH" : localeinfo.STAT_TOOLTIP_CON,
		"INT" : localeinfo.STAT_TOOLTIP_INT,
		"STR" : localeinfo.STAT_TOOLTIP_STR,
		"DEX" : localeinfo.STAT_TOOLTIP_DEX,
	}

	STAT_MINUS_DESCRIPTION = localeinfo.STAT_MINUS_DESCRIPTION

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.state = "STATUS"

		self.toolTipSkill = 0
		self.__Initialize()
		self.__LoadWindow()

		self.statusPlusCommandDict={
			"HTH" : "/stat ht",
			"INT" : "/stat iq",
			"STR" : "/stat st",
			"DEX" : "/stat dx",
		}

		self.statusMinusCommandDict={
			"HTH-" : "/stat- ht",
			"INT-" : "/stat- iq",
			"STR-" : "/stat- st",
			"DEX-" : "/stat- dx",
		}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.state = "STATUS"
		self.curSelectedSkillGroup = 0
		self.canUseHorseSkill = -1

		self.toolTip = None
		self.toolTipAlignment = None
		self.toolTipSkill = None

		self.faceImage = None
		self.statusPlusValue = None
		self.activeSlot = None
		self.tabDict = None
		self.tabButtonDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.statusPlusButtonDict = None
		self.statusMinusButtonDict = None

		self.skillPageDict = None
		self.questShowingStartIndex = 0
		self.questScrollBar = None
		self.questSlot = None
		self.questHeaderList = None
		self.questNameList = None
		self.questLastTimeList = None
		self.questLastCountList = None
		# self.skillGroupButton = ()

		self.activeSlot = None
		self.activeSkillPointValue = None
		# self.skillGroupButton1 = None
		# self.skillGroupButton2 = None
		# self.activeSkillGroupName = None

		self.guildNameSlot = None
		self.guildNameValue = None
		self.characterNameSlot = None
		self.characterNameValue = None

		self.emotionToolTip = None
		self.soloEmotionSlot = None
		self.dualEmotionSlot = None

		if app.ENABLE_EXPRESSING_EMOTION:
			self.specialEmotionSlot = None

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			self.skillColorWnd = None
			self.skillColorButton = []

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.board.Show()

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __LoadWindow(self):
		try:
			self.__LoadScript("uiscript/_characterwindow.py")
			self.__BindObject()
			self.__BindEvent()
			self.Refreshing()
		except BaseException:
			exception.Abort("CharacterWindow.__LoadWindow")

		self.SetState("STATUS")

	def Refreshing(self):
		self.RefreshStatus()
		self.RefreshCharacter()
		self.RefreshSkill()

	def Destroy(self):
		self.Hide()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd and self.skillColorWnd.IsShow():
				self.skillColorWnd.Hide()

		self.ClearDictionary()
		self.__Initialize()

	def Close(self):
		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if self.skillColorWnd and self.skillColorWnd.IsShow():
				self.skillColorWnd.Hide()
		self.state = "STATUS"
		self.Hide()

	def __BindObject(self):
		self.toolTip = uitooltip.ToolTip()
		self.toolTipAlignment = uitooltip.ToolTip()

		self.faceImage = self.GetChild("Face_Image")

		faceSlot = self.GetChild("Face_Slot")
		self.statusPlusValue = self.GetChild("Status_Plus_Value")
		self.board = self.GetChild("board")
		self.board.SetCloseEvent(self.Close)
		self.characterNameSlot = self.GetChild("Character_Name_Slot")
		self.characterNameValue = self.GetChild("Character_Name")
		self.guildNameSlot = self.GetChild("Guild_Name_Slot")
		self.guildNameValue = self.GetChild("Guild_Name")
		self.characterNameSlot.SetOverInEvent(self.__ShowAlignmentToolTip)
		self.characterNameSlot.SetOverOutEvent(self.__HideAlignmentToolTip)
		self.activeSlot = self.GetChild("Skill_Active_Slot")
		self.activeSkillPointValue = self.GetChild("Active_Skill_Point_Value")

		self.statusPlusButtonDict = {
			"HTH"		: self.GetChild("HTH_Plus"),
			"INT"		: self.GetChild("INT_Plus"),
			"STR"		: self.GetChild("STR_Plus"),
			"DEX"		: self.GetChild("DEX_Plus"),
		}

		self.statusMinusButtonDict = {
			"HTH-"		: self.GetChild("HTH_Minus"),
			"INT-"		: self.GetChild("INT_Minus"),
			"STR-"		: self.GetChild("STR_Minus"),
			"DEX-"		: self.GetChild("DEX_Minus"),
		}

		self.skillPageDict = {
			"ACTIVE" : self.GetChild("Skill_Active_Slot"),
			"SUPPORT" : self.GetChild("Skill_ETC_Slot"),
			"HORSE" : self.GetChild("Skill_Active_Slot"),
		}

		self.skillPageStatDict = {
			"SUPPORT"	: player.SKILL_SUPPORT,
			"ACTIVE"	: player.SKILL_ACTIVE,
			"HORSE"		: player.SKILL_HORSE,
		}

		self.soloEmotionSlot = self.GetChild("SoloEmotionSlot")
		self.dualEmotionSlot = self.GetChild("DualEmotionSlot")
		if app.ENABLE_EXPRESSING_EMOTION:
			self.specialEmotionSlot = self.GetChild("SpecialEmotionSlot")

		self.__SetEmotionSlot()

		self.questShowingStartIndex = 0
		self.questScrollBar = self.GetChild("Quest_ScrollBar")
		self.questScrollBar.SetScrollEvent(self.OnQuestScroll)
		self.questSlot = self.GetChild("Quest_Slot")
		for i in range(6):
			self.questSlot.HideSlotBaseImage(i)
			self.questSlot.SetCoverButton(i,\
											"interface/icons/special/quest_closed.tga",\
											"interface/icons/special/quest_open.tga",\
											"interface/icons/special/quest_open.tga",\
											"interface/icons/special/quest_open.tga", True)
		self.questHeaderList = []
		self.questNameList = []
		self.questLastTimeList = []
		self.questLastCountList = []
		for i in range(6):
			self.questHeaderList.append(self.GetChild("Quest_Header_0" + str(i)))
			self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
			self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
			self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))

		self.tabNameStringDict = {
			"STATUS"		: "Status do Personagem",
			"SKILL"			: "Habilidades",
			"EMOTICON"		: "Emoções",
			"QUEST"			: "Quests",
			"BONUS"			: "Página de Bônus",
			"RANKING"		: "Classificação Geral",
		}

		self.tabButtonDict = {
			"STATUS"		: self.GetChild("Tab_Button_01"),
			"SKILL"			: self.GetChild("Tab_Button_02"),
			"EMOTICON"		: self.GetChild("Tab_Button_03"),
			"QUEST"			: self.GetChild("Tab_Button_04"),
			"BONUS"			: self.GetChild("Tab_Button_05"),
			"RANKING"		: self.GetChild("Tab_Button_06"),
		}

		self.pageDict = {
			"STATUS"		: self.GetChild("Character_Page"),
			"SKILL"			: self.GetChild("Skill_Page"),
			"EMOTICON"		: self.GetChild("Emoticon_Page"),
			"QUEST"			: self.GetChild("Quest_Page"),
			"BONUS"			: self.GetChild("Bonus_Page"),
			"RANKING"		: self.GetChild("Ranking_Page"),
		}

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(self.__OnClickTabButton, tabKey)

		self.Make_Bonus_Page()
		self.Make_Ranking_Page()

	def SetGuildNameSlotEvent(self, event):
		self.guildNameSlot.SetMouseLeftButtonDownEvent(event)

	def __SetEmotionSlot(self):
		self.emotionToolTip = uitooltip.ToolTip()
		slots_new = None
		if app.ENABLE_EXPRESSING_EMOTION:
			slots_new = (self.soloEmotionSlot, self.dualEmotionSlot, self.specialEmotionSlot)
		else:
			slots_new = (self.soloEmotionSlot, self.dualEmotionSlot)

		for slot in slots_new:
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectItemSlotEvent(self.__SelectEmotion)
			slot.SetUnselectItemSlotEvent(self.__ClickEmotionSlot)
			slot.SetUseSlotEvent(self.__ClickEmotionSlot)
			slot.SetOverInItemEvent(self.__OverInEmotion)
			slot.SetOverOutItemEvent(self.__OverOutEmotion)

		for slotIdx, datadict in emotion.EMOTION_DICT.items():
			emotionIdx = slotIdx

			slot = self.soloEmotionSlot
			if app.ENABLE_EXPRESSING_EMOTION:
				if slotIdx > 50 and slotIdx < 54:
					slot = self.dualEmotionSlot
			else:
				if slotIdx > 50:
					slot = self.dualEmotionSlot

			slot.SetEmotionSlot(slotIdx, emotionIdx)
			slot.SetCoverButton(slotIdx)

		if app.ENABLE_EXPRESSING_EMOTION:
			for i in range(0, 17):
				slotIdx = app.SLOT_EMOTION_START + i
				emotionIdx = slotIdx

				if slotIdx >= app.SLOT_EMOTION_START:
					slot = self.specialEmotionSlot

				slot.SetEmotionSlot(slotIdx, emotionIdx)
				slot.SetCoverButton(slotIdx)

	def __SelectEmotion(self, slotIndex):
		if app.ENABLE_EXPRESSING_EMOTION:
			if not slotIndex in emotion.EMOTION_DICT and slotIndex < app.SLOT_EMOTION_START:
				return
		else:
			if not slotIndex in emotion.EMOTION_DICT:
				return

		if app.IsPressed(app.DIK_LCONTROL):
			player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_EMOTION, slotIndex)
			return

		mousemodule.mouseController.AttachObject(self, player.SLOT_TYPE_EMOTION, slotIndex, slotIndex)

	def __ClickEmotionSlot(self, slotIndex):
		print("click emotion")

		if app.ENABLE_EXPRESSING_EMOTION:
			if not slotIndex in emotion.EMOTION_DICT and slotIndex < app.SLOT_EMOTION_START:
				return
		else:
			if not slotIndex in emotion.EMOTION_DICT:
				return

		print("check acting")
		if player.IsActingEmotion():
			return

		if app.ENABLE_EXPRESSING_EMOTION:
			command = ""
			if slotIndex < app.SLOT_EMOTION_START:
				command = emotion.EMOTION_DICT[slotIndex]["command"]
			print("command", command)
		else:
			command = emotion.EMOTION_DICT[slotIndex]["command"]
			print("command", command)

		if app.ENABLE_EXPRESSING_EMOTION:
			if slotIndex > 50 and slotIndex < 54:
				vid = player.GetTargetVID()
				if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.EMOTION_CHOOSE_ONE)
					return
				command += " " + chr.GetNameByVID(vid)
		else:
			if slotIndex > 50:
				vid = player.GetTargetVID()
				if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.EMOTION_CHOOSE_ONE)
					return
				command += " " + chr.GetNameByVID(vid)

		if app.ENABLE_EXPRESSING_EMOTION:
			if slotIndex >= app.SLOT_EMOTION_START:
				emotionIdx = slotIndex

				if emotionIdx >= app.SLOT_EMOTION_START:
					command = emotion.command_emotion[emotionIdx]["command"]

				if emotionIdx > app.SLOT_EMOTION_START+4:
					command = int(emotion.command_emotion[emotionIdx]["command"])
					num = command+1

					if(chrmgr.IsPossibleEmoticon(-1)):
						chrmgr.SetEmoticon(-1,int(num)-1)
						net.SendEmoticon(int(num)-1)
				else:
					print("send_command", command)
					net.SendChatPacket(command)
			else:
				print("send_command", command)
				net.SendChatPacket(command)
		else:
			print("send_command", command)
			net.SendChatPacket(command)

	def ActEmotion(self, emotionIndex):
		if not player.IsSitting():
			self.__ClickEmotionSlot(emotionIndex)

	def __OverInEmotion(self, slotIndex):
		if self.emotionToolTip:
			if app.ENABLE_EXPRESSING_EMOTION:
				if not slotIndex in emotion.EMOTION_DICT and slotIndex < app.SLOT_EMOTION_START:
					return
			else:
				if not slotIndex in emotion.EMOTION_DICT:
					return

			self.emotionToolTip.ClearToolTip()

			if app.ENABLE_EXPRESSING_EMOTION:
				if slotIndex < app.SLOT_EMOTION_START:
					self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
				else:
					self.emotionToolTip.SetTitle(emotion.command_emotion[slotIndex]["name"])
			else:
				self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])

			self.emotionToolTip.ShowToolTip()

	def __OverOutEmotion(self):
		if self.emotionToolTip:
			self.emotionToolTip.HideToolTip()

### SKILLS ### SKILLS ### SKILLS ### SKILLS ### SKILLS ### SKILLS ### SKILLS ### SKILLS ### SKILLS ### SKILLS ### SKILLS ###
	def __SetSkillSlotEvent(self):
		place = "interface/controls/common/button_status/"
		for skillPageValue in self.skillPageDict.values():
			skillPageValue.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			skillPageValue.SetSelectItemSlotEvent(self.SelectSkill)
			skillPageValue.SetSelectEmptySlotEvent(self.SelectEmptySlot)
			skillPageValue.SetUnselectItemSlotEvent(self.ClickSkillSlot)
			skillPageValue.SetUseSlotEvent(self.ClickSkillSlot)
			skillPageValue.SetOverInItemEvent(self.OverInItem)
			skillPageValue.SetOverOutItemEvent(self.OverOutItem)
			skillPageValue.SetPressedSlotButtonEvent(self.OnPressedSlotButton)
			skillPageValue.AppendSlotButton(place + "plus_n.tga", place + "plus_h.tga", place + "plus_a.tga")

	def __BindEvent(self):
		self.RefreshQuest()

		for (statusPlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.SetEvent(self.__OnClickStatusPlusButton, statusPlusKey)

		for (statusMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.SetEvent(self.__OnClickStatusMinusButton, statusMinusKey)

		self.questSlot.SetSelectItemSlotEvent(self.__SelectQuest)

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = proxy(toolTipSkill)

	def __OnClickStatusPlusButton(self, statusKey):
		try:
			statusPlusCommand = self.statusPlusCommandDict[statusKey]
			net.SendChatPacket(statusPlusCommand)
		except KeyError as msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusPlusButton KeyError: %s", msg)

	def __OnClickStatusMinusButton(self, statusKey):
		try:
			statusMinusCommand = self.statusMinusCommandDict[statusKey]
			net.SendChatPacket(statusMinusCommand)
		except KeyError as msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusMinusButton KeyError: %s", msg)

	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def SetState(self, stateKey):
		self.state = stateKey

		for pageValue in self.pageDict.values():
			pageValue.Hide()
		self.pageDict[stateKey].Show()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.Enable()
		self.tabButtonDict[stateKey].Disable()
		self.board.SetTitle(self.tabNameStringDict[stateKey])

	def GetState(self):
		return self.state

	def __GetTotalAtkText(self):
		minAtk = player.GetStatus(player.ATT_MIN)
		maxAtk = player.GetStatus(player.ATT_MAX)
		atkBonus = player.GetStatus(player.ATT_BONUS)
		attackerBonus = player.GetStatus(player.ATTACKER_BONUS)

		if minAtk == maxAtk:
			return "%d" % (minAtk + atkBonus + attackerBonus)
		else:
			return "%d-%d" % (minAtk + atkBonus + attackerBonus, maxAtk + atkBonus + attackerBonus)

	def __GetTotalMagAtkText(self):
		minMagAtk = player.GetStatus(player.MAG_ATT) + player.GetStatus(player.MIN_MAGIC_WEP)
		maxMagAtk = player.GetStatus(player.MAG_ATT) + player.GetStatus(player.MAX_MAGIC_WEP)

		if minMagAtk == maxMagAtk:
			return "%d" % (minMagAtk)
		else:
			return "%d-%d" % (minMagAtk, maxMagAtk)

	def __GetTotalDefText(self):
		defValue = player.GetStatus(player.DEF_GRADE)
		return "%d" % (defValue)

	def RefreshStatus(self):
		self.UpdateRankingPoints()
		curEXP = player.GetStatus(player.EXP)
		nextEXP = max(1, player.GetStatus(player.NEXT_EXP))

		if player.GetStatus(player.LEVEL) == 120:
			self.GetChild("ExpImgFull").SetPercentage(1, 1)
		else:
			self.GetChild("ExpImgFull").SetPercentage(curEXP, nextEXP)

		percent = str((float(curEXP)/float(max(1, nextEXP)))*100)

		if len(percent) > 4:
			percent_limited = percent[:4]
		else:
			percent_limited = percent

		self.GetChild("Level_Value").SetText("lv. "+str(player.GetStatus(player.LEVEL)))
		self.GetChild("Exp_Value").SetText(str(player.GetEXP())+" de "+str(int(player.GetStatus(player.NEXT_EXP))))
		self.GetChild("PercentExp").SetText(percent_limited+"%")

		self.GetChild("HP_Value").SetText("Vida Máxima [HP]: |cffB74646" + str(player.GetStatus(player.MAX_HP)))
		self.GetChild("SP_Value").SetText("Mágia Máxima [MP]: |cff4150CD" + str(player.GetStatus(player.MAX_SP)))

		self.GetChild("STR_Value").SetText("Força: |cff42f456" + str(player.GetStatus(player.ST)))
		self.GetChild("DEX_Value").SetText("Destresa: |cff42f456" + str(player.GetStatus(player.DX)))
		self.GetChild("HTH_Value").SetText("Vitalidade: |cffB74646" + str(player.GetStatus(player.HT)))
		self.GetChild("INT_Value").SetText("Inteligência: |cff4150CD" + str(player.GetStatus(player.IQ)))

		self.GetChild("ATT_Value").SetText("Ataque: |cff42f456" + self.__GetTotalAtkText())
		self.GetChild("DEF_Value").SetText("Defesa: |cffB74646" + self.__GetTotalDefText())

		self.GetChild("MATT_Value").SetText("Ataque Mágico: |cff4150CD" + self.__GetTotalMagAtkText())
		self.GetChild("MDEF_Value").SetText("Defesa Mágica: |cff4150CD" + str(player.GetStatus(player.MAG_DEF)))

		self.__RefreshStatusPlusButtonList()
		self.__RefreshStatusMinusButtonList()
		self.RefreshAlignment()

	def __RefreshStatusPlusButtonList(self):
		statusPlusPoint = player.GetStatus(player.STAT)

		self.statusPlusValue.SetText("Pontos Disponíveis:|cfff8d090 "+str(statusPlusPoint))
		self.statusPlusValue.Show()
		self.ShowStatusPlusButtonList()

	def __RefreshStatusMinusButtonList(self):
		self.__ShowStatusMinusButtonList()

	def RefreshAlignment(self):
		point, grade = player.GetAlignmentData()

		COLOR_DICT = {
			0 : colorinfo.TITLE_RGB_GOOD_4,
			1 : colorinfo.TITLE_RGB_GOOD_3,
			2 : colorinfo.TITLE_RGB_GOOD_2,
			3 : colorinfo.TITLE_RGB_GOOD_1,
			4 : colorinfo.TITLE_RGB_NORMAL,
			5 : colorinfo.TITLE_RGB_EVIL_1,
			6 : colorinfo.TITLE_RGB_EVIL_2,
			7 : colorinfo.TITLE_RGB_EVIL_3,
			8 : colorinfo.TITLE_RGB_EVIL_4,
		}

		colorList = COLOR_DICT.get(grade, colorinfo.TITLE_RGB_NORMAL)
		gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

		self.toolTipAlignment.ClearToolTip()
		self.toolTipAlignment.AppendTextLine(localeinfo.TITLE_NAME_LIST[grade], gradeColor)
		self.toolTipAlignment.AppendTextLine("Pontos de Honra: " + str(point))

	def __ShowStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Show()

	def __HideStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Hide()

	def ShowStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Show()

	def HideStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Hide()

	def SelectSkill(self, skillSlotIndex):
		mouseController = mousemodule.mouseController

		if not mouseController.isAttached():
			srcSlotIndex = self.__RealSkillSlotToSourceSlot(skillSlotIndex)
			selectedSkillIndex = player.GetSkillIndex(srcSlotIndex)

			if skill.CanUseSkill(selectedSkillIndex):
				if app.IsPressed(app.DIK_LCONTROL):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL, srcSlotIndex)
					return
				mouseController.AttachObject(self, player.SLOT_TYPE_SKILL, srcSlotIndex, selectedSkillIndex)
		else:
			mouseController.DeattachObject()

	def SelectEmptySlot(self, SlotIndex):
		mousemodule.mouseController.DeattachObject()

	def OverInItem(self, slotNumber):
		if mousemodule.mouseController.isAttached():
			return

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillLevel = player.GetSkillLevel(srcSlotIndex)
		skillGrade = player.GetSkillGrade(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if skill.SKILL_TYPE_ACTIVE == skillType:
			overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)

			if overInSkillGrade == skill.SKILL_GRADE_COUNT-1 and skillGrade == skill.SKILL_GRADE_COUNT:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)
			elif overInSkillGrade == skillGrade:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, overInSkillGrade, skillLevel)
			else:
				self.toolTipSkill.SetSkillOnlyName(srcSlotIndex, skillIndex, overInSkillGrade)
		else:
			self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)

	def OverOutItem(self):
		if self.toolTipSkill:
			self.toolTipSkill.HideToolTip()

	def __SelectQuest(self, slotIndex):
		questIndex = quest.GetQuestIndex(self.questShowingStartIndex+slotIndex)
		event.QuestButtonClick(-2147483648 + questIndex)

	def RefreshQuest(self):
		questCount = quest.GetQuestCount()
		questRange = range(6)
		self.questScrollBar.SetMiddleBarSize(float(6)/float(max(6, questCount)))

		for i in questRange[:questCount]:
			(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex+i)

			self.questNameList[i].SetText(questName)
			self.questHeaderList[i].Show()
			self.questNameList[i].Show()
			self.questLastCountList[i].Show()
			self.questLastTimeList[i].Show()

			if len(questCounterName) > 0:
				self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
			else:
				self.questLastCountList[i].SetText("- - -")

			self.questSlot.SetSlot(i, i, 1, 1, questIcon)

		for i in questRange[questCount:]:
			self.questHeaderList[i].Hide()
			self.questNameList[i].Hide()
			self.questLastTimeList[i].Hide()
			self.questLastCountList[i].Hide()
			self.questSlot.ClearSlot(i)
			self.questSlot.HideSlotBaseImage(i)

		self.__UpdateQuestClock()

	def __UpdateQuestClock(self):
		if "QUEST" == self.state:
			for i in range(min(quest.GetQuestCount(), 6)):
				(lastName, lastTime) = quest.GetQuestLastTime(i)

				clockText = localeinfo.QUEST_UNLIMITED_TIME
				if len(lastName) > 0:
					if lastTime <= 0:
						clockText = localeinfo.QUEST_TIMEOVER
					else:
						questLastMinute = lastTime / 60
						questLastSecond = lastTime % 60

						clockText = lastName + " : "

						if questLastMinute > 0:
							clockText += str(questLastMinute) + localeinfo.QUEST_MIN
							if questLastSecond > 0:
								clockText += " "
						if questLastSecond > 0:
							clockText += str(questLastSecond) + localeinfo.QUEST_SEC
				if self.questLastTimeList[i] != None:
					self.questLastTimeList[i].SetText("|cffa99999"+clockText)

	def __GetStatMinusPoint(self):
		POINT_STAT_RESET_COUNT = 112
		return player.GetStatus(POINT_STAT_RESET_COUNT)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __RefreshSkillPage(self, name, slotCount):
		global SHOW_LIMIT_SUPPORT_SKILL_LIST

		skillPage = self.skillPageDict[name]

		startSlotIndex = skillPage.GetStartIndex()
		if "ACTIVE" == name:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				startSlotIndex += slotCount

		getSkillType=skill.GetSkillType
		getSkillIndex=player.GetSkillIndex
		getSkillGrade=player.GetSkillGrade
		getSkillLevel=player.GetSkillLevel
		getSkillLevelUpPoint = skill.GetSkillLevelUpPoint
		getSkillMaxLevel = skill.GetSkillMaxLevel

		for i in range(slotCount + 1):
			slotIndex = i + startSlotIndex
			skillIndex = getSkillIndex(slotIndex)

			for j in range(skill.SKILL_GRADE_COUNT):
				skillPage.ClearSlot(self.__GetRealSkillSlot(j, i))

			if 0 == skillIndex:
				continue

			skillGrade = getSkillGrade(slotIndex)
			skillLevel = getSkillLevel(slotIndex)
			skillType = getSkillType(skillIndex)

			if player.SKILL_INDEX_RIDING == skillIndex:
				if 1 == skillGrade:
					skillLevel += 19
				elif 2 == skillGrade:
					skillLevel += 29
				elif 3 == skillGrade:
					skillLevel = 40

				skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel-1, 0), skillLevel)
				skillPage.SetSlotCount(slotIndex, skillLevel)

			elif skill.SKILL_TYPE_ACTIVE == skillType:
				for j in range(skill.SKILL_GRADE_COUNT):
					realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
					if not ((self.__CanUseSkillNow()) and (skillGrade != j)):
						skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
						skillPage.SetCoverButton(realSlotIndex)
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
					elif (skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT-1):
						skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
						skillPage.SetCoverButton(realSlotIndex)
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
			else:
				if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
					realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
					skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
					skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if skill.CanUseSkill(skillIndex):
						skillPage.SetCoverButton(realSlotIndex)

			skillPage.RefreshSlot()

		if app.ENABLE_SKILL_COLOR_SYSTEM:
			if "ACTIVE" == name:
				if self.PAGE_HORSE != self.curSelectedSkillGroup:
					self.__CreateSkillColorButton(skillPage)
				else:
					self.skillColorButton = []

	def __RestoreSlotCoolTime(self, skillPage):
		restoreType = skill.SKILL_TYPE_NONE
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			restoreType = skill.SKILL_TYPE_HORSE
		else:
			restoreType = skill.SKILL_TYPE_ACTIVE

		skillPage.RestoreSlotCoolTime(restoreType)

	def RefreshSkill(self):
		if self.__IsChangedHorseRidingSkillLevel():
			self.RefreshCharacter()
			return

		self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
		self.__RefreshSkillPage("SUPPORT", self.SUPPORT_PAGE_SLOT_COUNT)

		self.RefreshSkillPlusButtonList()

	def CanShowPlusButton(self, skillIndex, skillLevel, curStatPoint):
		if 0 == skillIndex:
			return False

		if not skill.CanLevelUpSkill(skillIndex, skillLevel):
			return False

		return True

	def __RefreshSkillPlusButton(self, name):
		if "SUPPORT" == name:
			return

		slotWindow = self.skillPageDict[name]
		slotWindow.HideAllSlotButton()

		slotStatType = self.skillPageStatDict[name]
		if 0 == slotStatType:
			return

		statPoint = player.GetStatus(slotStatType)
		master_skill_points = 0
		startSlotIndex = slotWindow.GetStartIndex()
		if "HORSE" == name:
			startSlotIndex += self.ACTIVE_PAGE_SLOT_COUNT

		for i in range(self.PAGE_SLOT_COUNT +1):
			slotIndex = i + startSlotIndex
			skillIndex = player.GetSkillIndex(slotIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			if skillIndex == 0:
				continue

			if skillGrade > 2:
				continue

			if skillGrade != 0:
				if master_skill_points > 0:
					slotWindow.ShowSlotButton(slotIndex)
				else:
					continue

			if statPoint > 0:
				if name == "HORSE":
					if player.GetStatus(player.LEVEL) >= skill.GetSkillLevelLimit(skillIndex):
						if skillLevel < 20:
							slotWindow.ShowSlotButton(self.__GetETCSkillRealSlotIndex(slotIndex))
				elif name == "SUPPORT":
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
								slotWindow.ShowSlotButton(slotIndex)
				else:
					if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
						slotWindow.ShowSlotButton(slotIndex)

	if app.ENABLE_SKILL_COLOR_SYSTEM:
		def __CreateSkillColorButton(self, parent):
			self.skillColorButton = []

			xPos = 35
			yPos = 0
			for idx in range(self.PAGE_SLOT_COUNT):
				skillSlot = idx
				if skillSlot < 6:
					skillIndex = player.GetSkillIndex(skillSlot + 1)
					skillMaxGrade = 3

					if len(self.skillColorButton) == skillSlot:
						self.skillColorButton.append([])
						self.skillColorButton[skillSlot] = ui.Button()
						self.skillColorButton[skillSlot].SetParent(parent)
						self.skillColorButton[skillSlot].SetUpVisual("interface/controls/special/skillcolor/skill_color_button_default.tga")
						self.skillColorButton[skillSlot].SetOverVisual("interface/controls/special/skillcolor/skill_color_button_over.tga")
						self.skillColorButton[skillSlot].SetDownVisual("interface/controls/special/skillcolor/skill_color_button_down.tga")
						self.skillColorButton[skillSlot].SetPosition(xPos, yPos)
						self.skillColorButton[skillSlot].SetEvent(self.__OnPressSkillColorButton, skillSlot, skillIndex)
						if player.GetSkillGrade(skillSlot + 1) >= skillMaxGrade:
							self.skillColorButton[skillSlot].Show()
						else:
							self.skillColorButton[skillSlot].Hide()
					else:
						self.skillColorButton[skillSlot].SetPosition(xPos, yPos)
					xPos += 41

		def __UpdateSkillColorPosition(self):
			x, y = self.GetGlobalPosition()
			self.skillColorWnd.SetPosition(x + 250, y)

		def __OnPressSkillColorButton(self, skillSlot, skillIndex):
			self.skillColorWnd = uiskillcolor.SkillColorWindow(skillSlot, skillIndex)
			if self.skillColorWnd and not self.skillColorWnd.IsShow():
				self.skillColorWnd.Show()

	def RefreshSkillPlusButtonList(self):
		self.RefreshSkillPlusPointLabel()

		if not self.__CanUseSkillNow():
			return

		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			self.__RefreshSkillPlusButton("HORSE")
		else:
			self.__RefreshSkillPlusButton("ACTIVE")

		self.__RefreshSkillPlusButton("SUPPORT")

	def RefreshSkillPlusPointLabel(self):
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			activeStatPoint = player.GetStatus(player.SKILL_HORSE)
			self.activeSkillPointValue.SetText("|cffa08784Pontos da Montaria: [|cfff8d090"+str(activeStatPoint)+"|cffa08784]")
		else:
			activeStatPoint = player.GetStatus(player.SKILL_ACTIVE)
			masterStatPoint = 0
			self.activeSkillPointValue.SetText("|cffa08784Pontos de Habilidades: [|cfff8d090"+str(activeStatPoint)+"|cffa08784]")
			self.GetChild("Master_Skill_Point_Value").SetText("|cffa08784Pontos de Habilidades Master: [|cfff8d090"+str(masterStatPoint)+"|cffa08784]")

	def OnPressedSlotButton(self, slotNumber):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber) # = return slotNumber%20

		skillIndex = player.GetSkillIndex(srcSlotIndex)
		curLevel = player.GetSkillLevel(srcSlotIndex)
		maxLevel = skill.GetSkillMaxLevel(skillIndex)

		net.SendChatPacket("/skillup " + str(skillIndex))

	def ClickSkillSlot(self, slotIndex):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotIndex)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if not self.__CanUseSkillNow():
			if skill.SKILL_TYPE_ACTIVE == skillType:
				return

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if skill.CanUseSkill(skillIndex):
					player.ClickSkillSlot(srcSlotIndex)
					return

		mousemodule.mouseController.DeattachObject()

	def OnUseSkill(self, slotIndex, coolTime):
		skillIndex = player.GetSkillIndex(slotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if skill.SKILL_TYPE_ACTIVE == skillType:
			skillGrade = player.GetSkillGrade(slotIndex)
			slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		else:
			slotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.SetSlotCoolTime(slotIndex, coolTime)
				return

	def OnActivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.ActivateSlot(slotIndex)
				return

	def OnDeactivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				return

	if app.SKILL_COOLTIME_UPDATE:
		def SkillClearCoolTime(self, slotIndex):
			slotIndex = self.__GetRealSkillSlot(player.GetSkillGrade(slotIndex), slotIndex)
			for slotWindow in self.skillPageDict.values():
				if slotWindow.HasSlot(slotIndex):
					slotWindow.SetSlotCoolTime(slotIndex, 0)


	def __ShowAlignmentToolTip(self):
		self.toolTipAlignment.ShowToolTip()

	def __HideAlignmentToolTip(self):
		self.toolTipAlignment.HideToolTip()

	def RefreshCharacter(self):
		try:
			characterName = player.GetName()
			guildName = player.GetGuildName()
			if characterName == "":
				self.characterNameValue.SetText("Sem Nome")
			else:
				self.characterNameValue.SetText(characterName)

			if guildName == "":
				self.guildNameValue.SetText("Sem Guild")
			else:
				self.guildNameValue.SetText(guildName)

		except BaseException:
			exception.Abort("CharacterWindow.RefreshCharacter.BindObject")

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()

		job = chr.RaceToJob(race)

		faceImageName = FACE_IMAGE_DICT[race]
		self.faceImage.LoadImage(faceImageName)

		if 0 == group:
			self.__SelectSkillGroup(0)
		else:
			self.__SetSkillSlotData(race, group)

			if self.__CanUseHorseSkill():
				self.__SelectSkillGroup(0)

	# def __SetSkillGroupName(self, race, group):
		# job = chr.RaceToJob(race)

		# if not self.SKILL_GROUP_NAME_DICT.__contains__(job):
			# return

		# nameList = self.SKILL_GROUP_NAME_DICT[job]

		# if 0 == group:
			# self.skillGroupButton1.SetText(nameList[1])
			# self.skillGroupButton2.SetText(nameList[2])
			# self.skillGroupButton1.Show()
			# self.skillGroupButton2.Show()
			# self.activeSkillGroupName.Hide()

		# else:
			# if self.__CanUseHorseSkill():
				# self.activeSkillGroupName.Hide()
				# self.skillGroupButton1.SetText(nameList.get(group, "Noname"))
				# self.skillGroupButton2.SetText(localeinfo.SKILL_GROUP_HORSE)
				# self.skillGroupButton1.Show()
				# self.skillGroupButton2.Show()

			# else:
				# self.activeSkillGroupName.SetText(nameList.get(group, "Noname"))
				# self.activeSkillGroupName.Show()
				# self.skillGroupButton1.Hide()
				# self.skillGroupButton2.Hide()

	def __SetSkillSlotData(self, race, group):
		playersettingmodule.RegisterSkill(race, group)
		self.__SetSkillSlotEvent()
		self.RefreshSkill()

	def __SelectSkillGroup(self, index):
		if self.__CanUseHorseSkill():
			if 0 == index:
				index = net.GetMainActorSkillGroup()-1
			elif 1 == index:
				index = self.PAGE_HORSE

		self.curSelectedSkillGroup = index
		self.__SetSkillSlotData(net.GetMainActorRace(), index + 1)

	def __CanUseSkillNow(self):
		if 0 == net.GetMainActorSkillGroup():
			return False
		return True

	def __CanUseHorseSkill(self):
		slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)

		if not slotIndex:
			return False

		grade = player.GetSkillGrade(slotIndex)
		level = player.GetSkillLevel(slotIndex)
		if level < 0:
			level *= -1
		if grade >= 1 and level >= 1:
			return True

		return False

	def __IsChangedHorseRidingSkillLevel(self):
		ret = False

		if -1 == self.canUseHorseSkill:
			self.canUseHorseSkill = self.__CanUseHorseSkill()

		if self.canUseHorseSkill != self.__CanUseHorseSkill():
			ret = True

		self.canUseHorseSkill = self.__CanUseHorseSkill()
		return ret

	def __GetRealSkillSlot(self, skillGrade, skillSlot):
		return skillSlot# + min(skill.SKILL_GRADE_COUNT-1, skillGrade)*skill.SKILL_GRADE_STEP_COUNT

	def __GetETCSkillRealSlotIndex(self, skillSlot):
		if skillSlot > 100:
			return skillSlot
		return skillSlot % self.ACTIVE_PAGE_SLOT_COUNT

	def __RealSkillSlotToSourceSlot(self, realSkillSlot): # Função aparentemente correta
		if realSkillSlot > 100:
			return realSkillSlot
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			return realSkillSlot + self.ACTIVE_PAGE_SLOT_COUNT
		return realSkillSlot % skill.SKILL_GRADE_STEP_COUNT # skill.SKILL_GRADE_STEP_COUNT = 20 -> Resto da divisão por 20

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - 6)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()

### BONUS PAGE ### BONUS PAGE ### BONUS PAGE ### BONUS PAGE ### BONUS PAGE ### BONUS PAGE ### BONUS PAGE ### BONUS PAGE ###
	def OnUpdate(self):
		# self.__UpdateQuestClock()

		if self.state != "BONUS":
			return

		Get = self.GetChild
		FINDER_ACTIVE = self.FINDER_ACTIVE
		PAGE_BONUS_ACTIVE = self.PAGE_BONUS_ACTIVE
		PAGE_INDEX = self.PAGE_INDEX

		for page in self.PAGE_BONUS:
			if Get(page + "_Bonus_Finder").IsIn() and Get(page + "_Bonus_Finder").GetWidth() < 110:
				Get(page + "_Bonus_Finder").SetLeft(Get(page + "_Bonus_Finder").GetLeft() - 10)
				Get(page + "_Bonus_Finder").SetSize(Get(page + "_Bonus_Finder").GetWidth() + 10, Get(page + "_Bonus_Finder").GetHeight())
			elif Get(page + "_Bonus_Finder").GetWidth() > 29 and FINDER_ACTIVE[page] == 0 and not Get(page + "_Bonus_Finder").IsIn():
				Get(page + "_Bonus_Finder").SetLeft(Get(page + "_Bonus_Finder").GetLeft() + 10)
				Get(page + "_Bonus_Finder").SetSize(Get(page + "_Bonus_Finder").GetWidth() - 10, Get(page + "_Bonus_Finder").GetHeight())
				Get(page + "_Bonus_Finder_Desc").Hide()
				Get(page + "_Bonus_Finder_EditLine").Hide()
			elif Get(page + "_Bonus_Finder").GetWidth() > 110 and FINDER_ACTIVE[page] == 0:
				Get(page + "_Bonus_Finder_Desc").Show()
				Get(page + "_Bonus_Finder_EditLine").Hide()

			if PAGE_BONUS_ACTIVE < PAGE_INDEX[page] and Get(page + "_Bonus").GetTop() <  (160 + 35 * PAGE_INDEX[page]):
				Get(page + "_Bonus").SetPosition(Get(page + "_Bonus").GetLeft(), Get(page + "_Bonus").GetTop() + 20)
			elif PAGE_BONUS_ACTIVE < PAGE_INDEX[page] and Get(page + "_Bonus").GetTop() == (160 + 35 * PAGE_INDEX[page]):
				Get(page + "_Bonus").SetPosition(Get(page + "_Bonus").GetLeft(), Get(page + "_Bonus").GetTop() + 13)
			elif Get(page + "_Bonus").GetTop() > 13 + 35 * PAGE_INDEX[page] and not PAGE_BONUS_ACTIVE < PAGE_INDEX[page]:
				Get(page + "_Bonus").SetPosition(Get(page + "_Bonus").GetLeft(), Get(page + "_Bonus").GetTop() - 20)
			elif Get(page + "_Bonus").GetTop() == 13 + 35 * PAGE_INDEX[page] and not PAGE_BONUS_ACTIVE < PAGE_INDEX[page]:
				Get(page + "_Bonus").SetPosition(Get(page + "_Bonus").GetLeft(), Get(page + "_Bonus").GetTop() - 13)
			else:
				Get(self.PAGE_BONUS[PAGE_BONUS_ACTIVE] + "_Bonus_Window").Show()

		self.COUNTER += 1
		if self.COUNTER > 30:
			for page in self.PAGE_BONUS:
				self.UpdateBonus(page)
			self.OnBonusScrollOffensive()
			self.OnBonusScrollDefensive()
			self.OnBonusScrollPVM()
			self.COUNTER = 0

	COUNTER = 0

	FINDER_ACTIVE = {
		"Offensive" : 0,
		"Defensive" : 0,
		"PVM" : 0,
	}

	BONUS_TEXT = {
		"Offensive" : [],
		"Defensive" : [],
		"PVM" : [],
	}

	PAGE_BONUS_ACTIVE = 2

	PAGE_BONUS = ["Offensive", "Defensive", "PVM",]
	PAGE_INDEX = {"Offensive":0, "Defensive":1, "PVM":2,}

	def Make_Bonus_Page(self):
		Get = self.GetChild

		Get("Offensive_Bonus_Finder").SetMouseLeftButtonDownEvent(self.Active_Finder, "Offensive")
		Get("Defensive_Bonus_Finder").SetMouseLeftButtonDownEvent(self.Active_Finder, "Defensive")
		Get("PVM_Bonus_Finder").SetMouseLeftButtonDownEvent(self.Active_Finder, "PVM")

		Get("Offensive_Bonus_Image").SetMouseLeftButtonDownEvent(self.Select_Bonus_Page, 0)
		Get("Defensive_Bonus_Image").SetMouseLeftButtonDownEvent(self.Select_Bonus_Page, 1)
		Get("PVM_Bonus_Image").SetMouseLeftButtonDownEvent(self.Select_Bonus_Page, 2)

		for page in self.PAGE_BONUS:
			self.UpdateBonus(page)

		Get("Offensive_ScrollBar").SetScrollEvent(self.OnBonusScrollOffensive)
		Get("Defensive_ScrollBar").SetScrollEvent(self.OnBonusScrollDefensive)
		Get("PVM_ScrollBar").SetScrollEvent(self.OnBonusScrollPVM)

		Get("Offensive_Bonus_Finder_EditLine").SetIMEUpdateEvent(self.FindTheFuckingBonusOff)
		Get("Defensive_Bonus_Finder_EditLine").SetIMEUpdateEvent(self.FindTheFuckingBonusDef)
		Get("PVM_Bonus_Finder_EditLine").SetIMEUpdateEvent(self.FindTheFuckingBonusPVM)

		Get("Offensive_Bonus_Finder_EditLine").SetEscapeEvent(self.Deactivate_Finder)
		Get("Defensive_Bonus_Finder_EditLine").SetEscapeEvent(self.Deactivate_Finder)
		Get("PVM_Bonus_Finder_EditLine").SetEscapeEvent(self.Deactivate_Finder)

		Get("Offensive_Bonus_Finder_EditLine").SetReturnEvent(self.Deactivate_Finder)
		Get("Defensive_Bonus_Finder_EditLine").SetReturnEvent(self.Deactivate_Finder)
		Get("PVM_Bonus_Finder_EditLine").SetReturnEvent(self.Deactivate_Finder)

		self.Select_Bonus_Page(0)

	def OnBonusScrollOffensive(self):
		self.OnBonusScroll("Offensive")

	def OnBonusScrollDefensive(self):
		self.OnBonusScroll("Defensive")

	def OnBonusScrollPVM(self):
		self.OnBonusScroll("PVM")

	def OnBonusScroll(self, page):
		Get = self.GetChild
		pos = int(Get(page + "_ScrollBar").GetPos() * max(0, len(BONUS_LIST[page]) - 9))
		self.ListTheFuckingBonus(page, pos)

	def SetScrollBarSize(self, page, size = 0):
		Get = self.GetChild
		if size == 0:
			Get(page + "_ScrollBar").SetMiddleBarSize(9.0/max(9.0, float(len(self.BONUS_TEXT[page]))))

	def UpdateBonus(self, page):
		self.BONUS_TEXT[page] = [] 
		for bonus in BONUS_LIST[page]:
			self.BONUS_TEXT[page].append(PLAYER_POINTS[bonus](player.GetStatus(bonus)))

	def Select_Bonus_Page_By_String(self, txt):
		tmp = {
			'Offensive': 0,
			'Defensive': 1,
			'PVM': 2,
		}

		self.Select_Bonus_Page(tmp[txt], False)

	def Select_Bonus_Page(self, num, limpar_filtros=True):
		Get = self.GetChild
		self.PAGE_BONUS_ACTIVE = num

		if limpar_filtros == True:
			self.Deactivate_Finder()

		for page in self.PAGE_BONUS:
			Get(page + "_Bonus_Window").Hide()
			Get(page + "_Bonus_Title").SetPackedFontColor(grp.GenerateColor(1.0, 0.6, 0.6, 1.0))

		Get(self.PAGE_BONUS[num] + "_Bonus_Title").SetPackedFontColor(colorinfo.COR_TEXTO_ACTIVE)

		self.ListTheFuckingBonus(self.PAGE_BONUS[num])
		self.SetScrollBarSize(self.PAGE_BONUS[num])

	def FindTheFuckingBonusOff(self):
		self.ListTheFuckingBonus("Offensive")

	def FindTheFuckingBonusDef(self):
		self.ListTheFuckingBonus("Defensive")

	def FindTheFuckingBonusPVM(self):
		self.ListTheFuckingBonus("PVM")

	def ListTheFuckingBonus(self, page, init = 0):
		Get = self.GetChild
		finder = Get(page + "_Bonus_Finder_EditLine").GetText()

		i = 0

		if finder != "":
			for bonus in self.BONUS_TEXT[page]:
				if i == 9:
					break
				if finder.lower() in bonus.lower():
					temp = bonus.split(":")
					Get(page + "_" + str(i)).SetText(temp[0] + ": |cFFF4E1C4" + temp[1])
					i += 1
		else:
			while i < 9 and init < len(self.BONUS_TEXT[page]):
				temp = self.BONUS_TEXT[page][init].split(":")
				Get(page + "_" + str(i)).SetText(temp[0] + ": |cFFF4E1C4" + temp[1])
				i += 1
				init += 1

		while i < 9:
			Get(page + "_" + str(i)).SetText("")
			i += 1

	def Active_Finder(self, finder):
		if self.FINDER_ACTIVE[finder] == 1:
			self.Deactivate_Finder()
			return

		for page in self.PAGE_BONUS:
			self.FINDER_ACTIVE[page] = 0
		self.FINDER_ACTIVE[finder] = 1

		self.Select_Bonus_Page_By_String(finder)
	
		self.GetChild(finder + "_Bonus_Finder_Desc").Hide()
		self.GetChild(finder + '_Bonus_Finder').SetColor(grp.GenerateColor(0.1, 0.1, 0.1, 1.0))
		self.GetChild(finder + "_Bonus_Finder_EditLine").Show()
		self.GetChild(finder + "_Bonus_Finder_EditLine").SetFocus()
		self.GetChild(finder + "_Bonus_Finder_EditLine").SetText("")

	def Deactivate_Finder(self):
		for page in self.PAGE_BONUS:
			self.FINDER_ACTIVE[page] = 0
		for page in self.PAGE_BONUS:
			self.GetChild(page + "_Bonus_Finder_EditLine").SetText("")
			self.GetChild(page + "_Bonus_Finder_EditLine").Hide()
			self.GetChild(page + '_Bonus_Finder').SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 1.0))
			self.GetChild(page + "_Bonus_Finder_Desc").Hide()

### RANKING ###### RANKING ###### RANKING ###### RANKING ###### RANKING ###### RANKING ###### RANKING ###
	RANKING_LIST = []

	def Make_Ranking_Page(self):
		Get = self.GetChild
		Get("Ranking_ScrollBar").SetScrollEvent(self.OnRankingScroll)

	def ListTheFuckingRanking(self, init = 0):
		Get = self.GetChild

		i = 0

		while i < 15 and init < len(self.RANKING_LIST):
			temp = self.RANKING_LIST[init]
			Get("RK_" + str(i)).SetText("|cfff8d090%sº - |cffa08784%s" % (str(init + 1), str(temp[0])))
			Get("PRK_" + str(i)).SetText("|cfff8d090Pontos:|cffa08784 %s " % (str(temp[1])))
			i += 1
			init += 1

		while i < 15:
			Get("RK_" + str(i)).SetText("")
			Get("PRK_" + str(i)).SetText("")
			i += 1

	def OnRankingScroll(self):
		Get = self.GetChild
		pos = int(Get("Ranking_ScrollBar").GetPos() * max(0, len(self.RANKING_LIST) - 15))
		self.ListTheFuckingRanking(pos)

	def SetRankingScrollBarSize(self):
		Get = self.GetChild
		Get("Ranking_ScrollBar").SetMiddleBarSize(15.0/max(15.0, float(len(self.RANKING_LIST))))

	def RankingPosition(self, num):
		self.GetChild("ranking_position").SetText(str(num) + "º Lugar")

	def RankingAddPlayer(self, name, points):
		self.RANKING_LIST.append([name, points])
		self.SetRankingScrollBarSize()
		self.ListTheFuckingRanking()

	def RankingClean(self):
		self.RANKING_LIST = []
		self.SetRankingScrollBarSize()
		self.ListTheFuckingRanking()

	def UpdateRankingPoints(self):
		if int(player.GetStatus(144)) == int(1):
			self.GetChild("ranking_points").SetText("1 Ponto")
		else:
			self.GetChild("ranking_points").SetText(str(player.GetStatus(144)) + " Pontos")

BONUS_LIST = {
	"Offensive" : [121,122,43,54,55,56,57,17,19,21,34,37,38,39,40,41,63,64,],
	"Defensive" : [59,60,61,62,69,70,71,74,72,73,32,33,67,68,77,79,80,81,123,124,],
	"PVM" : [44,45,46,47,48,53,],
}

PLAYER_POINTS = {
	6 : localeinfo.TOOLTIP_MAX_HP,
	8 : localeinfo.TOOLTIP_MAX_SP,
	12 : localeinfo.TOOLTIP_STR,
	13 : localeinfo.TOOLTIP_CON,
	14 : localeinfo.TOOLTIP_DEX,
	15 : localeinfo.TOOLTIP_INT,
	17 : localeinfo.TOOLTIP_ATT_SPEED,
	19 : localeinfo.TOOLTIP_MOV_SPEED,
	21 : localeinfo.TOOLTIP_CAST_SPEED,
	32 : localeinfo.TOOLTIP_HP_REGEN,
	33 : localeinfo.TOOLTIP_SP_REGEN,
	34 : localeinfo.TOOLTIP_BOW_DISTANCE,
	37 : localeinfo.TOOLTIP_APPLY_POISON_PCT,
	38 : localeinfo.TOOLTIP_APPLY_STUN_PCT,
	39 : localeinfo.TOOLTIP_APPLY_SLOW_PCT,
	40 : localeinfo.TOOLTIP_APPLY_CRITICAL_PCT,
	41 : localeinfo.TOOLTIP_APPLY_PENETRATE_PCT,
	43 : localeinfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
	44 : localeinfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
	45 : localeinfo.TOOLTIP_APPLY_ATTBONUS_ORC,
	46 : localeinfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
	47 : localeinfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
	48 : localeinfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
	53 : localeinfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,
	54 : localeinfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
	55 : localeinfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
	56 : localeinfo.TOOLTIP_APPLY_ATTBONUS_SURA,
	57 : localeinfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
	59 : localeinfo.TOOLTIP_APPLY_RESIST_WARRIOR,
	60 : localeinfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
	61 : localeinfo.TOOLTIP_APPLY_RESIST_SURA,
	62 : localeinfo.TOOLTIP_APPLY_RESIST_SHAMAN,
	63 : localeinfo.TOOLTIP_APPLY_STEAL_HP,
	64 : localeinfo.TOOLTIP_APPLY_STEAL_SP,
	65 : localeinfo.TOOLTIP_APPLY_MANA_BURN_PCT,
	66 : localeinfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
	67 : localeinfo.TOOLTIP_APPLY_BLOCK,
	68 : localeinfo.TOOLTIP_APPLY_DODGE,
	69 : localeinfo.TOOLTIP_APPLY_RESIST_SWORD,
	70 : localeinfo.TOOLTIP_APPLY_RESIST_TWOHAND,
	71 : localeinfo.TOOLTIP_APPLY_RESIST_DAGGER,
	72 : localeinfo.TOOLTIP_APPLY_RESIST_BELL,
	73 : localeinfo.TOOLTIP_APPLY_RESIST_FAN,
	74 : localeinfo.TOOLTIP_RESIST_BOW,
	75 : localeinfo.TOOLTIP_RESIST_FIRE,
	76 : localeinfo.TOOLTIP_RESIST_ELEC,
	77 : localeinfo.TOOLTIP_RESIST_MAGIC,
	78 : localeinfo.TOOLTIP_APPLY_RESIST_WIND,
	79 : localeinfo.TOOLTIP_APPLY_REFLECT_MELEE,
	80 : localeinfo.TOOLTIP_APPLY_REFLECT_CURSE,
	81 : localeinfo.TOOLTIP_APPLY_POISON_REDUCE,
	82 : localeinfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
	83 : localeinfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
	84 : localeinfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
	85 : localeinfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
	86 : localeinfo.TOOLTIP_APPLY_POTION_BONUS,
	87 : localeinfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
	88 : localeinfo.TOOLTIP_APPLY_IMMUNE_STUN,
	89 : localeinfo.TOOLTIP_APPLY_IMMUNE_SLOW,
	90 : localeinfo.TOOLTIP_APPLY_IMMUNE_FALL,
	119 : localeinfo.TOOLTIP_APPLY_MAX_HP_PCT,
	120 : localeinfo.TOOLTIP_APPLY_MAX_SP_PCT,
	121 : localeinfo.TOOLTIP_SKILL_DAMAGE_BONUS,
	122 : localeinfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
	123 : localeinfo.TOOLTIP_SKILL_DEFEND_BONUS,
	124 : localeinfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
	133 : localeinfo.TOOLTIP_RESIST_ICE,
	134 : localeinfo.TOOLTIP_RESIST_EARTH,
	135 : localeinfo.TOOLTIP_RESIST_DARK,
	136 : localeinfo.TOOLTIP_ANTI_CRITICAL_PCT,
	137 : localeinfo.TOOLTIP_ANTI_PENETRATE_PCT,
}

# c = CharacterWindow()
# c.Show()
# c.__RefreshSkillPage("ACTIVE", c.ACTIVE_PAGE_SLOT_COUNT)

# slotIndex = 3
# skillIndex = player.GetSkillIndex(slotIndex)
# skillGrade = player.GetSkillGrade(slotIndex)
# skillLevel = player.GetSkillLevel(slotIndex)
# chat.AppendChat(chat.CHAT_TYPE_INFO, "skillIndex: [%d] skillGrade: [%d] skillLevel: [%d]" % (skillIndex, skillGrade, skillLevel))