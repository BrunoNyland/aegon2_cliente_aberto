#favor manter essa linha
import XXjvumrgrYBZompk3PS8 as item
import enszxc3467hc3kokdueq as app
import ga3vqy6jtxqi9yf344j7 as player
import zn94xlgo573hf8xmddzq as net
import Js4k2l7BrdasmVRt8Wem as chr
import LURMxMaKZJqliYt2QSHG as chat
import ui
import dbg
import math
import skill
import uicommon
import uitooltip
import localeinfo

class LovePointImage(ui.ExpandedImageBox):
	FILE_PATH = "/icon/affectshower/love/"
	FILE_DICT = {
		0 : FILE_PATH + "00.tga",
		1 : FILE_PATH + "01.tga",
		2 : FILE_PATH + "01.tga",
		3 : FILE_PATH + "02.tga",
		4 : FILE_PATH + "03.tga",
		5 : FILE_PATH + "04.tga",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0

		self.toolTip = uitooltip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()

	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()

	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)

		if 0 == self.lovePoint:
			loveGrade = 0
		else:
			loveGrade = self.lovePoint / 25 + 1
		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH+"00.dds")

		try:
			self.LoadImage(fileName)
		except BaseException:
			dbg.TraceError("LovePointImage.SetLoverInfo(lovePoint=%d) - LoadError %s" % (self.lovePoint, fileName))

		# self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.loverName)
		self.toolTip.AppendTextLine(localeinfo.AFF_LOVE_POINT % (self.lovePoint))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()

class HorseImage(ui.ExpandedImageBox):
	FILE_PATH = "icon/affectshower/horse/"
	FILE_DICT = {
		0 : FILE_PATH + "00.tga",
		1 : FILE_PATH + "00.tga",
		2 : FILE_PATH + "00.tga",
		3 : FILE_PATH + "00.tga",
		10 : FILE_PATH + "01.tga",
		11 : FILE_PATH + "02.tga",
		12 : FILE_PATH + "03.tga",
		13 : FILE_PATH + "04.tga",
		20 : FILE_PATH + "05.tga",
		21 : FILE_PATH + "06.tga",
		22 : FILE_PATH + "07.tga",
		23 : FILE_PATH + "08.tga",
		30 : FILE_PATH + "09.tga",
		31 : FILE_PATH + "10.tga",
		32 : FILE_PATH + "11.tga",
		33 : FILE_PATH + "12.tga",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)
		self.toolTip = uitooltip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __GetHorseGrade(self, level):
		if 0 == level:
			return 0
		return (level-1)/10 + 1

	def SetState(self, level, health, battery):
		self.toolTip.ClearToolTip()

		if level > 0:
			try:
				grade = self.__GetHorseGrade(level)
				self.__AppendText(localeinfo.LEVEL_LIST[grade])
			except IndexError:
				print("HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery))
				return

			try:
				healthName=localeinfo.HEALTH_LIST[health]
				if len(healthName)>0:
					self.__AppendText(healthName)
			except IndexError:
				print("HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery))
				return

			if health > 0:
				if battery == 0:
					self.__AppendText(localeinfo.NEEFD_REST)

			try:
				fileName = self.FILE_DICT[health * 10 + battery]
			except KeyError:
				print("HorseImage.SetState(level=%d, health=%d, battery=%d) - KeyError" % (level, health, battery))

			try:
				self.LoadImage(fileName)
			except BaseException:
				print("HorseImage.SetState(level=%d, health=%d, battery=%d) - LoadError %s" % (level, health, battery, fileName))

		# self.SetScale(0.7, 0.7)

	def __AppendText(self, text):
		self.toolTip.AppendTextLine(text)
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()

class AffectImage(ui.ExpandedImageBox):
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTipText = None
		self.isSkillAffect = True
		self.description = None
		self.endTime = 0
		self.affect = None
		self.isClocked = True

		if app.ENABLE_AFFECT_POLYMORPH_REMOVE:
			self.polymorphQuestionDialog = None

		if app.ENABLE_AFFECT_BUFF_REMOVE:
			self.buffQuestionDialog = None
			self.skillIndex = None

	def SetAffect(self, affect):
		self.affect = affect

	def GetAffect(self):
		return self.affect

	def SetToolTipText(self, text, x = 0, y = -19):
		if not self.toolTipText:
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetSize(0, 0)
			textLine.SetOutline()
			textLine.Hide()
			self.toolTipText = textLine

		self.toolTipText.SetText(text)
		w, h = self.toolTipText.GetTextSize()
		self.toolTipText.SetPosition(max(0, x + self.GetWidth()/2 - w/2), y)

	def SetDescription(self, description):
		self.description = description

	def SetDuration(self, duration):
		self.endTime = 0
		if duration > 0:
			self.endTime = app.GetGlobalTimeStamp() + duration

	def UpdateAutoPotionDescription(self):
		potionType = 0
		if self.affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			potionType = player.AUTO_POTION_TYPE_HP
		else:
			potionType = player.AUTO_POTION_TYPE_SP
		isActivated, currentAmount, totalAmount, slotIndex = player.GetAutoPotionInfo(potionType)
		amountPercent = 0.0
		if int(totalAmount) == int(0):
			totalAmount = 1.0
		amountPercent = (float(currentAmount) / float(totalAmount)) * 100.0
		self.SetToolTipText(localeinfo.TOOLTIP_AUTO_POTION_REST % amountPercent, 0, 40)

	def SetClock(self, isClocked):
		self.isClocked = isClocked

	def UpdateDescription(self):
		if not self.isClocked:
			self.__UpdateDescription2()
			return
		if not self.description:
			return
		toolTip = self.description
		if self.endTime > 0:
			leftTime = localeinfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())
			toolTip += " (%s : %s)" % (localeinfo.LEFT_TIME, leftTime)
		self.SetToolTipText(toolTip, 0, 40)

	def __UpdateDescription2(self):
		if not self.description:
			return

		toolTip = self.description
		self.SetToolTipText(toolTip, 0, 40)

	if app.ENABLE_AFFECT_BUFF_REMOVE:
		def SetSkillIndex(self, skillIndex):
			self.skillIndex = skillIndex

	def SetSkillAffectFlag(self, flag):
		self.isSkillAffect = flag

	def IsSkillAffect(self):
		return self.isSkillAffect

	if app.ENABLE_AFFECT_POLYMORPH_REMOVE:
		def OnPolymorphQuestionDialog(self):
			self.polymorphQuestionDialog = uicommon.QuestionDialog()
			self.polymorphQuestionDialog.SetText(localeinfo.POLYMORPH_AFFECT_REMOVE_QUESTION)
			self.polymorphQuestionDialog.SetWidth(350)
			self.polymorphQuestionDialog.SetAcceptEvent(self.OnClosePolymorphQuestionDialog, True)
			self.polymorphQuestionDialog.SetCancelEvent(self.OnClosePolymorphQuestionDialog, False)
			self.polymorphQuestionDialog.Open()

		def OnClosePolymorphQuestionDialog(self, answer):
			if not self.polymorphQuestionDialog:
				return

			self.polymorphQuestionDialog.Close()
			self.polymorphQuestionDialog = None

			if not answer:
				return

			net.SendChatPacket("/remove_polymorph")
			return True

	if app.ENABLE_AFFECT_BUFF_REMOVE:
		def OnBuffQuestionDialog(self, skillIndex):
			self.buffQuestionDialog = uicommon.QuestionDialog()
			self.buffQuestionDialog.SetWidth(350)
			self.buffQuestionDialog.SetText("Deseja realmente desativar este buff [%s]?" % (skill.GetSkillName(skillIndex)))
			self.buffQuestionDialog.SetAcceptEvent(self.OnCloseBuffQuestionDialog, skillIndex)
			self.buffQuestionDialog.SetCancelEvent(self.OnCloseBuffQuestionDialog, 0)
			self.buffQuestionDialog.Open()

		def OnCloseBuffQuestionDialog(self, answer):
			if not self.buffQuestionDialog:
				return False

			self.buffQuestionDialog.Close()
			self.buffQuestionDialog = None

			if not answer:
				return False

			net.SendChatPacket("/remove_buff %d" % answer)
			return True

	def OnMouseOverIn(self):
		if self.toolTipText:
			self.toolTipText.Show()
		return True

	def OnMouseLeftButtonUp(self):
		if app.ENABLE_AFFECT_POLYMORPH_REMOVE:
			if self.affect == chr.NEW_AFFECT_POLYMORPH:
				self.OnPolymorphQuestionDialog()
		if app.ENABLE_AFFECT_BUFF_REMOVE:
			if self.skillIndex:
				self.OnBuffQuestionDialog(self.skillIndex)
		return True

	def OnMouseOverOut(self):
		if self.toolTipText:
			self.toolTipText.Hide()
		return True

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	BLEND_DESC_IDX_START = 2000

	IMAGE_STEP = 25

	INFINITE_AFFECT_DURATION = 0x1FFFFFFF

	AFFECT_DATA_DICT = {
			chr.AFFECT_POISON: (localeinfo.SKILL_TOXICDIE, "icon/affectshower/poison.tga"),
			chr.AFFECT_FIRE: (localeinfo.SKILL_FIRE, "icon/affectshower/burn.tga",),
			chr.AFFECT_SLOW: (localeinfo.SKILL_SLOW, "icon/affectshower/slow.tga"),
			chr.AFFECT_STUN: (localeinfo.SKILL_STUN, "icon/affectshower/stun.tga"),

			chr.AFFECT_ATT_SPEED_POTION: (localeinfo.SKILL_INC_ATKSPD, "icon/affectshower/atack_speed_bonus.tga"),
			chr.AFFECT_MOV_SPEED_POTION: (localeinfo.SKILL_INC_MOVSPD, "icon/affectshower/move_speed_bonus.tga"),
			chr.AFFECT_FISH_MIND: (localeinfo.SKILL_FISHMIND, "icon/affectshower/fish.tga"),

			chr.AFFECT_JEONGWI: (localeinfo.SKILL_JEONGWI, "icon/affectshower/furia_p.tga",),
			chr.AFFECT_GEOMGYEONG: (localeinfo.SKILL_GEOMGYEONG, "icon/affectshower/lamina_p.tga",),
			chr.AFFECT_CHEONGEUN: (localeinfo.SKILL_CHEONGEUN, "icon/affectshower/defesa_p.tga",),
			chr.AFFECT_GWIGEOM: (localeinfo.SKILL_GWIGEOM, "icon/affectshower/lamina_sombria_p.tga",),
			chr.AFFECT_GONGPO: (localeinfo.SKILL_GONGPO, "icon/affectshower/medo_p.tga",),
			chr.AFFECT_JUMAGAP: (localeinfo.SKILL_JUMAGAP, "icon/affectshower/aura_p.tga"),
			chr.AFFECT_HEUKSIN: (localeinfo.SKILL_HEUKSIN, "icon/affectshower/proteção_p.tga",),
			chr.AFFECT_MUYEONG: (localeinfo.SKILL_MUYEONG, "icon/affectshower/evocar_p.tga",),
			chr.AFFECT_PABEOP: (localeinfo.SKILL_PABEOP, "icon/affectshower/discipar_p.tga",),
			chr.AFFECT_GYEONGGONG: (localeinfo.SKILL_GYEONGGONG, "icon/affectshower/passos_p.tga",),
			chr.AFFECT_EUNHYEONG: (localeinfo.SKILL_EUNHYEONG, "icon/affectshower/esconder_p.tga",),
			chr.AFFECT_BOHO: (localeinfo.SKILL_BOHO, "icon/affectshower/escudoespelhado_p.tga",),
			chr.AFFECT_HOSIN: (localeinfo.SKILL_HOSIN, "icon/affectshower/escudo_p.tga",),
			chr.AFFECT_GICHEON: (localeinfo.SKILL_GICHEON, "icon/affectshower/olhos_p.tga",),
			chr.AFFECT_JEUNGRYEOK: (localeinfo.SKILL_JEUNGRYEOK, "icon/affectshower/encantamentos_p.tga",),
			chr.AFFECT_KWAESOK: (localeinfo.SKILL_KWAESOK, "icon/affectshower/pluma_p.tga",),
			chr.AFFECT_FALLEN_CHEONGEUN: (localeinfo.SKILL_CHEONGEUN, "icon/affectshower/defesa_p.tga",),
			chr.AFFECT_CHINA_FIREWORK: (localeinfo.SKILL_POWERFUL_STRIKE, "icon/affectshower/atordoar_bonus.tga",),

			chr.NEW_AFFECT_AUTO_HP_RECOVERY: (localeinfo.TOOLTIP_AUTO_POTION_REST, "interface/icons/auto_hpgauge/05.tga"),
			chr.NEW_AFFECT_AUTO_SP_RECOVERY: (localeinfo.TOOLTIP_AUTO_POTION_REST, "interface/icons/auto_spgauge/05.tga"),

			MALL_DESC_IDX_START + player.ATT_BONUS: (localeinfo.TOOLTIP_MALL_ATTBONUS_STATIC, "icon/affectshower/ataque_bonus.tga",),
			MALL_DESC_IDX_START + player.POINT_MALL_DEFBONUS: (localeinfo.TOOLTIP_MALL_DEFBONUS_STATIC, "icon/affectshower/defesa_bonus.tga",),
			MALL_DESC_IDX_START + player.POINT_CRITICAL_PCT: (localeinfo.TOOLTIP_APPLY_CRITICAL_PCT, "icon/affectshower/critico_bonus.tga",),
			MALL_DESC_IDX_START + player.POINT_PENETRATE_PCT: (localeinfo.TOOLTIP_APPLY_PENETRATE_PCT, "icon/affectshower/perfurar_bonus.tga",),
			MALL_DESC_IDX_START + player.POINT_MAX_HP_PCT: (localeinfo.TOOLTIP_MAX_HP_PCT, "icon/affectshower/hp_bonus.tga",),
			MALL_DESC_IDX_START + player.POINT_MAX_SP_PCT: (localeinfo.TOOLTIP_MAX_SP_PCT, "icon/affectshower/mp_bonus.tga",),
			MALL_DESC_IDX_START + player.CASTING_SPEED: (localeinfo.TOOLTIP_CAST_SPEED, "icon/affectshower/sagaz.tga",),

			BLEND_DESC_IDX_START + player.POINT_CRITICAL_PCT: (localeinfo.TOOLTIP_AFFECT_POTION_1, "icon/affectshower/50821.tga"),
			BLEND_DESC_IDX_START + player.POINT_PENETRATE_PCT: (localeinfo.TOOLTIP_AFFECT_POTION_2, "icon/affectshower/50822.tga"),
			BLEND_DESC_IDX_START + player.ATT_SPEED: (localeinfo.TOOLTIP_AFFECT_POTION_3, "icon/affectshower/50823.tga"),
			BLEND_DESC_IDX_START + 77: (localeinfo.TOOLTIP_AFFECT_POTION_4, "icon/affectshower/50824.tga"),
			BLEND_DESC_IDX_START + player.ATT_GRADE_BONUS: (localeinfo.TOOLTIP_AFFECT_POTION_5, "icon/affectshower/50825.tga"),
			BLEND_DESC_IDX_START + player.DEF_BONUS: (localeinfo.TOOLTIP_AFFECT_POTION_6, "icon/affectshower/50826.tga"),
	}

	if app.ENABLE_AFFECT_POLYMORPH_REMOVE:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_POLYMORPH] = (localeinfo.POLYMORPH_AFFECT_TOOLTIP, "icon/affectshower/polimorph.tga")

	def __init__(self):
		ui.Window.__init__(self)

		self.serverPlayTime = 0
		self.clientPlayTime = 0
		self.lastUpdateTime = 0
		self.affectImageDict = {}
		self.affectList = []
		self.horseImage = None
		self.lovePointImage = None
		self.SetPosition(4, 4)
		self.Show()

	def ClearAllAffects(self):
		self.horseImage = None
		self.lovePointImage = None
		self.affectImageDict = {}
		self.affectList = []
		self.__ArrangeImageList()

	def ClearAffects(self):
		self.living_affectImageDict = {}
		for key, image in self.affectImageDict.items():
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image

		for aff in self.affectList:
			if not self.living_affectImageDict.__contains__(aff):
				self.affectList.remove(aff)

		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, "BINARY_NEW_AddAffect: type:%d pointIdx:%d, value:%d" % (type, pointIdx, value))

		if type < 500 and not type in [chr.NEW_AFFECT_AUTO_SP_RECOVERY, chr.NEW_AFFECT_AUTO_HP_RECOVERY, chr.NEW_AFFECT_POLYMORPH]:
			return

		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		elif type == 531:
			affect = self.BLEND_DESC_IDX_START + pointIdx
		else:
			affect = type

		if self.affectImageDict.__contains__(affect):
			return

		if not self.AFFECT_DATA_DICT.__contains__(affect):
			return

		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or\
		   affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or\
		   affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]
		description = affectData[0]
		filename = affectData[1]

		if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY and not (app.ENABLE_AFFECT_POLYMORPH_REMOVE and affect == chr.NEW_AFFECT_POLYMORPH):
			try:
				description = description(float(value))
			except BaseException:
				pass

		try:
			print("Add affect %s" % affect)
			image = AffectImage()
			image.SetParent(self)
			image.LoadImage(filename)
			image.SetDuration(duration)
			image.SetAffect(affect)
			if affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or self.INFINITE_AFFECT_DURATION < duration:
				image.SetClock(False)
				image.SetDescription(description)
				image.UpdateDescription()
			elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
				image.UpdateAutoPotionDescription()
			else:
				image.SetDescription(description)
				image.UpdateDescription()

			image.SetSkillAffectFlag(False)
			image.Show()
			self.affectImageDict[affect] = image
			self.affectList.append(affect)
			self.__ArrangeImageList()

		except Exception as e:
			print("except Aff affect ", e)
			pass

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		elif type == 531:
			affect = self.BLEND_DESC_IDX_START + pointIdx
		else:
			affect = type

		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level == 0:
			self.horseImage = None
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage = image
			self.__ArrangeImageList()

	def SetPlayTime(self, playTime):
		self.serverPlayTime = playTime
		self.clientPlayTime = app.GetTime()

	def __AppendAffect(self, affect):
		if self.affectImageDict.__contains__(affect):
			return

		if not self.AFFECT_DATA_DICT.__contains__(affect):
			return

		name = self.AFFECT_DATA_DICT[affect][0]
		filename = self.AFFECT_DATA_DICT[affect][1]

		skillIndex = player.AffectIndexToSkillIndex(affect)
		if 0 != skillIndex:
			name = skill.GetSkillName(skillIndex)

		image = AffectImage()
		image.SetParent(self)
		image.SetSkillAffectFlag(True)

		if app.ENABLE_AFFECT_BUFF_REMOVE:
			image.SetSkillIndex(skillIndex)

		try:
			image.LoadImage(filename)
		except BaseException:
			pass

		image.SetToolTipText(name, 0, 40)
		image.Show()

		self.affectImageDict[affect] = image
		self.affectList.append(affect)

	def __RemoveAffect(self, affect):
		if not self.affectImageDict.__contains__(affect):
			return

		del self.affectImageDict[affect]

		if affect in self.affectList:
			self.affectList.remove(affect)

		self.__ArrangeImageList()

	def __ArrangeImageList(self):
		width = len(self.affectImageDict) * self.IMAGE_STEP
		if self.lovePointImage:
			width += self.IMAGE_STEP
		if self.horseImage:
			width += self.IMAGE_STEP

		self.SetSize(width, 26)

		xPos = 0

		if self.lovePointImage:
			if self.lovePointImage.IsShow():
				self.lovePointImage.SetPosition(xPos, 0)
				xPos += self.IMAGE_STEP

		if self.horseImage:
			self.horseImage.SetPosition(xPos, 0)
			xPos += self.IMAGE_STEP

		for aff in self.affectList:
			if self.affectImageDict.__contains__(aff):
				self.affectImageDict[aff].SetPosition(xPos, 0)
				xPos += self.IMAGE_STEP

	def OnUpdate(self):
		if app.GetGlobalTime() - self.lastUpdateTime > 1000:
			self.lastUpdateTime = app.GetGlobalTime()

			for image in self.affectImageDict.values():
				if image.GetAffect() in [chr.NEW_AFFECT_AUTO_HP_RECOVERY, chr.NEW_AFFECT_AUTO_SP_RECOVERY]:
					image.UpdateAutoPotionDescription()
				elif not image.IsSkillAffect():
					image.UpdateDescription()
