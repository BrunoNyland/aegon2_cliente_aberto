#favor manter essa linha
import dbg
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import enszxc3467hc3kokdueq as app
import Js4k2l7BrdasmVRt8Wem as chr
import grp
import wndMgr
import skill
import shop
import exchange
import safebox
import localeinfo
import background
import nonplayer
import ui
import constinfo

if app.RENDER_TARGET:
	import renderTarget

WARP_SCROLLS = [22011, 22000, 22010]

DESC_WESTERN_MAX_COLS = 35

def chop(n):
	return round(n - 0.5, 1)

def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []
	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])
			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines

class ToolTip(ui.ThinBoard):
	TOOL_TIP_WIDTH = 0
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D

	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0)

	CONDITION_COLOR = 0xffBEB47D
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB
	ITEM_VNUM_TOOLTIP_COLOR = 0xffFFFF00

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable = False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		if isPickable == False:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeinfo.UI_DEF_FONT
		self.ClearToolTip()

		if app.__COMPARE_TOOLTIP__:
			self.CompareTooltip = None
			self.IsCompare = False

	def __del__(self):
		if app.__COMPARE_TOOLTIP__ and self.CompareTooltip:
			del self.CompareTooltip

		ui.ThinBoard.__del__(self)

	def ClearToolTip(self):
		self.toolTipHeight = 12
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AppendHorizontalLine(self):
		for i in range(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(0, self.toolTipHeight)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight) = textLine.GetTextSize()

		textWidth += 30
		textHeight += 5

		if self.toolTipWidth <= textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += textHeight

		return textLine

	def SetThinBoardSize(self, width, height = 12):
		self.toolTipWidth = width 
		self.toolTipHeight = height

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True, bold = True, italic = False):
		textLine = ui.TextLine()
		textLine.SetParent(self)

		if bold:
			textLine.SetFontName("Verdana:12b")
		elif italic:
			textLine.SetFontName(self.defFontName+"i")
		else:
			textLine.SetFontName(self.defFontName)

		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.Show()

		(textWidth, textHeight) = textLine.GetTextSize()

		if self.toolTipWidth <= textWidth + 30:
			self.toolTipWidth = textWidth + 30

		if centerAlign:
			textLine.SetPosition(0, self.toolTipHeight)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		self.__AppendDescription_WesternLanguage(desc, color)

	def __AppendDescription_WesternLanguage(self, desc, color=FONT_COLOR):
		lines = SplitDescription(desc, DESC_WESTERN_MAX_COLS)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.AppendTextLine(line, color)

	def ResizeToolTip(self):
		oldWidth = self.GetWidth()
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)
		if (oldWidth < self.toolTipWidth):
			for child in self.childrenList:
				x, y = child.GetLocalPosition()
				if (x == ((oldWidth/2) - 1)):
					child.SetPosition((self.toolTipWidth/2) -1, y)
					child.SetHorizontalAlignCenter()

	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False):
		if value > 0:
			if isSpecial:
				return grp.GenerateColor(0.5, 1.0, 0.5, 1.0)
			else:
				return grp.GenerateColor(0.5, 1.0, 0.5, 1.0)

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()

		if app.__COMPARE_TOOLTIP__ and self.CompareTooltip:
			self.CompareTooltip.Hide()
			self.CompareTooltip = None

	def OnUpdate(self):
		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30
			x = mouseX - width/2
		else:
			x = self.xPos - width/2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width/2, wndMgr.GetScreenWidth() - width/2) - width/2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		if app.__COMPARE_TOOLTIP__:
			if self.IsCompare:
				return

			if self.CompareTooltip:
				val = [0] * 2
				if x < self.CompareTooltip.GetWidth():
					val[0] = self.GetWidth()
				else:
					val[0] = -self.CompareTooltip.GetWidth()
				CompareHeight = wndMgr.GetScreenHeight() - self.CompareTooltip.GetHeight()
				if y > CompareHeight:
					val[1] = CompareHeight - y
				elif y < 0:
					val[1] = 0 - y
				self.CompareTooltip.SetPosition(x + val[0], y + val[1])

		self.SetPosition(x, y)

class ItemToolTip(ToolTip):

	if app.RENDER_TARGET:
		ModelPreview = None

	if app.ENABLE_SEND_TARGET_INFO:
		isStone = False
		isBook = False
		isBook2 = False

	CHARACTER_NAMES = (
		localeinfo.TOOLTIP_WARRIOR,
		localeinfo.TOOLTIP_ASSASSIN,
		localeinfo.TOOLTIP_SURA,
		localeinfo.TOOLTIP_SHAMAN,
	)

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = ( 
		localeinfo.TOOLTIP_ARMOR, 
		localeinfo.TOOLTIP_HELMET, 
		localeinfo.TOOLTIP_SHOES, 
		localeinfo.TOOLTIP_WRISTLET, 
		localeinfo.TOOLTIP_WEAPON, 
		localeinfo.TOOLTIP_NECK,
		localeinfo.TOOLTIP_EAR,
		localeinfo.TOOLTIP_UNIQUE,
		localeinfo.TOOLTIP_SHIELD,
		localeinfo.TOOLTIP_ARROW,
	)
	WEAR_COUNT = len(WEAR_NAMES)

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeinfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeinfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeinfo.TOOLTIP_CON,
		item.APPLY_INT : localeinfo.TOOLTIP_INT,
		item.APPLY_STR : localeinfo.TOOLTIP_STR,
		item.APPLY_DEX : localeinfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeinfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeinfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeinfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeinfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeinfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeinfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeinfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeinfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeinfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeinfo.TOOLTIP_APPLY_PENETRATE_PCT,
		item.APPLY_ATTBONUS_WARRIOR : localeinfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeinfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeinfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeinfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeinfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,
		item.APPLY_ATTBONUS_HUMAN : localeinfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeinfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeinfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeinfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeinfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeinfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeinfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeinfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeinfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeinfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeinfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeinfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeinfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeinfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeinfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeinfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeinfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeinfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeinfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeinfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeinfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeinfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeinfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeinfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeinfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeinfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeinfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeinfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeinfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeinfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeinfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeinfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeinfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeinfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeinfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeinfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeinfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeinfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeinfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeinfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeinfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeinfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeinfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeinfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeinfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeinfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeinfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeinfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeinfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_RESIST_WARRIOR : localeinfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeinfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeinfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeinfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeinfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeinfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeinfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeinfo.TOOLTIP_COSTUME_ATTR_BONUS,
		item.APPLY_MAGIC_ATTBONUS_PER : localeinfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeinfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeinfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeinfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeinfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeinfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeinfo.TOOLTIP_ANTI_PENETRATE_PCT,
	}

	ANTI_FLAG_DICT = {
		0:item.ITEM_ANTIFLAG_WARRIOR,
		1:item.ITEM_ANTIFLAG_ASSASSIN,
		2:item.ITEM_ANTIFLAG_SURA,
		3:item.ITEM_ANTIFLAG_SHAMAN,
	}

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.isShopItem = False
		self.isOfflineShopItem = False
		self.bCannotUseItemForceSetDisableColor = True 

	def __del__(self):
		self.ModelPreview = None
		del self.ModelPreview

		ToolTip.__del__(self)

	if app.__COMPARE_TOOLTIP__:
		def SetCompareItem(self, itemVnum):
			slotIndex = item.GetCompareIndex(itemVnum)
			if slotIndex:
				if not self.CompareTooltip:
					self.CompareTooltip = ItemToolTip()
					self.CompareTooltip.IsCompare = True

				self.CompareTooltip.SetInventoryItem(slotIndex, player.INVENTORY, False)
				self.CompareTooltip.AutoAppendTextLine("[ EQUIPADO ]", 0xffADFF2F)
				self.CompareTooltip.ResizeToolTip()
				if app.RENDER_TARGET:
					self.__ModelPreviewClose()

	if app.RENDER_TARGET:
		def CanViewRendering(self):
			if app.__COMPARE_TOOLTIP__:
				if self.IsCompare:
					return False
				if self.CompareTooltip:
					return False

			race = player.GetRace()
			job = chr.RaceToJob(race)

			if not self.ANTI_FLAG_DICT.__contains__(job):
				return False

			if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
				return False

			sex = chr.RaceToSex(race)

			MALE = 1
			FEMALE = 0

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
				return False

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
				return False

			return True

		def __ModelPreview(self, vnum, type, model):
			if not self.CanViewRendering() and model < 8:
				return

			if self.ModelPreview == None:
				self.ModelPreview = ui.RenderTarget()
				self.ModelPreview.SetParent(self)
				self.ModelPreview.SetSize(190, 190)
				self.ModelPreview.SetPosition(-185, 10)
				self.ModelPreview.SetRenderTarget(1)
				renderTarget.SetBackground(1, "interface/controls/special/decoration/image.tga")

			renderTarget.SelectModel(1, model)

			if model < 8:
				if type == 1:
					renderTarget.SetWeapon(1, player.GetItemIndex(204))
					renderTarget.SetArmor(1, player.GetItemIndex(200))
					renderTarget.SetHair(1, vnum)
				elif type == 2:
					renderTarget.SetWeapon(1, player.GetItemIndex(204))
					renderTarget.SetHair(1, chr.GetHair())
					renderTarget.SetArmor(1, vnum)
				elif type == 3:
					renderTarget.SetArmor(1, player.GetItemIndex(200))
					renderTarget.SetHair(1, chr.GetHair())
					renderTarget.SetWeapon(1, vnum)

			self.ModelPreview.Show()

		def __ModelPreviewClose(self):
			if self.ModelPreview:
				self.ModelPreview.Hide()

		def __ItemGetRace(self):
			race = 0

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
				race = 9
			elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
				race = 1
			elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN):
				race = 2
			elif item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) and item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) and item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA):
				race = 3

			sex = chr.RaceToSex(player.GetRace())
			MALE = 1
			FEMALE = 0

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
				race = player.GetRace() + 4

			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
				race = player.GetRace()

			if race == 0:
				race = player.GetRace()

			if race == 9:
				race = 0

			return race

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def CanEquip(self):
		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = player.GetRace()
		job = chr.RaceToJob(race)
		if not self.ANTI_FLAG_DICT.__contains__(job):
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if player.GetStatus(player.LEVEL) < limitValue:
					return False
		return True

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True, bold = True, italic = False):
		if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
			color = self.DISABLE_COLOR

		return ToolTip.AppendTextLine(self, text, color, centerAlign, bold, italic)

	def ClearToolTip(self):
		self.isShopItem = False
		self.isOfflineShopItem = False
		self.toolTipWidth = self.TOOL_TIP_WIDTH
		ToolTip.ClearToolTip(self)

	def SetInventoryItem(self, slotIndex, window_type = player.INVENTORY, CompareItem = True, Show_Render = True):
		itemVnum = player.GetItemIndex(window_type, slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		if shop.IsOpen():
			if not shop.IsPrivateShop() or not shop.IsOfflineShop():
				item.SelectItem(itemVnum)
				self.AppendSellingPrice(player.GetISellItemPrice(window_type, slotIndex))

		metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in range(player.ATTRIBUTE_SLOT_MAX_NUM)]

		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, 0, Show_Render)

		if app.__COMPARE_TOOLTIP__ and (app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT)) and not slotIndex >= player.EQUIPMENT_SLOT_START and CompareItem:
			self.SetCompareItem(itemVnum)

		if app.ENABLE_SOULBIND_SYSTEM:
			self.AppendSealInformation(player.INVENTORY, slotIndex)

		if app.ALUGAR_ITENS:
			self.AppendRentInformation(player.INVENTORY, slotIndex)

	def SetOfflineShopBuilderItem(self, invenType, invenPos, offlineShopIndex):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if (itemVnum == 0):
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)
		price = shop.GetOfflineShopItemPrice2(invenType, invenPos)
		self.AppendSellingPrice(shop.GetOfflineShopItemPrice2(invenType, invenPos))


	def SetOfflineShopItem(self, slotIndex):
		itemVnum = shop.GetOfflineShopItemID(slotIndex)
		if (itemVnum == 0):
			return

		self.ClearToolTip()
		self.isOfflineShopItem = True

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetOfflineShopItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetOfflineShopItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)

		price = shop.GetOfflineShopItemPrice(slotIndex)
		self.AppendPrice(price)

	if app.ENABLE_SEND_TARGET_INFO:
		def SetItemToolTipStone(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()

			itemDesc = item.GetItemDescription()
			itemSummary = item.GetItemSummary()
			attrSlot = 0

			itemName = item.GetItemName()
			realName = itemName[:itemName.find("+")]
			self.SetTitle(realName + " +0 - +4")

			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

			if item.ITEM_TYPE_METIN == itemType:
				self.AppendMetinInformation()
				self.AppendMetinWearInformation()

			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

			self.ShowToolTip()

	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True
		item.SelectItem(itemVnum)
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))
		self.AddItemData(itemVnum, metinSlot, attrSlot)
		self.AppendPrice(price)

		if app.__COMPARE_TOOLTIP__ and (app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT)) and shop.IsOpen() and not shop.IsMainPlayerPrivateShop():
			self.SetCompareItem(itemVnum)

	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))
		self.AddItemData(itemVnum, metinSlot, attrSlot)

		if app.ALUGAR_ITENS:
			self.AppendRentInformation(10, slotIndex)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))
		self.AddItemData(itemVnum, metinSlot, attrSlot)

		if app.__COMPARE_TOOLTIP__ and (app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT)):
			self.SetCompareItem(itemVnum)

		if app.ALUGAR_ITENS:
			self.AppendRentInformation(11, slotIndex)

	def SetPrivateShopBuilderItem(self, invenType, invenPos, privateShopSlotIndex):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)

		price = shop.GetPrivateShopItemPrice(invenType, invenPos)
		self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos))

	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex))

		if app.__COMPARE_TOOLTIP__ and (app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT)):
			self.SetCompareItem(itemVnum)

		if app.ENABLE_SOULBIND_SYSTEM:
			self.AppendSealInformation(player.SAFEBOX, slotIndex)

	if app.ENABLE_GUILD_SAFEBOX:
		def SetGuildSafeBoxItem(self, slotIndex):
			itemVnum = safebox.GetGuildItemID(slotIndex)
			if 0 == itemVnum:
				return

			self.ClearToolTip()
			metinSlot = []
			for i in range(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(safebox.GetGuildItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(safebox.GetGuildItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetItemToolTip(self, itemVnum):
		self.ClearToolTip()
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeinfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeinfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeinfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeinfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeinfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeinfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeinfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))

	def __AppendAttackPowerInfo(self):
		minPower = item.GetValue(3)
		maxPower = item.GetValue(4)
		addPower = item.GetValue(5)
		if maxPower > minPower:
			self.AppendTextLine(localeinfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
		else:
			self.AppendTextLine(localeinfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicAttackInfo(self):
		minMagicAttackPower = item.GetValue(1)
		maxMagicAttackPower = item.GetValue(2)
		addPower = item.GetValue(5)

		if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
			if maxMagicAttackPower > minMagicAttackPower:
				self.AppendTextLine(localeinfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower+addPower, maxMagicAttackPower+addPower), self.POSITIVE_COLOR)
			else:
				self.AppendTextLine(localeinfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower+addPower), self.POSITIVE_COLOR)

	def __AppendMagicDefenceInfo(self):
		magicDefencePower = item.GetValue(0)

		if magicDefencePower > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, self.GetChangeTextLineColor(magicDefencePower))

	def __AppendAttributeInformation(self, attrSlot):
		if 0 != attrSlot:
			attrDisp = 5

			for i in range(5):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if 0 == value:
					continue

				attrDisp -= 1

				affectString = self.__GetAffectString(type, value)
				if affectString:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)

			if (item.GetItemType() == item.ITEM_TYPE_ARMOR or (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() != item.WEAPON_ARROW)):
				if attrDisp > 0:
					self.AppendSpace(2)
					self.AppendTextLine("Voce pode adicinar +%d Bônus" % (attrDisp), self.SPECIAL_POSITIVE_COLOR)
					self.AppendSpace(2)

			rareDisp = 2
			for i in [5, 6]:
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if 0 == value:
					continue

				rareDisp -= 1

				affectString = self.__GetAffectString(type, value)
				if affectString:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)

			if (item.GetItemType() == item.ITEM_TYPE_ARMOR or (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() != item.WEAPON_ARROW)):
				if rareDisp == 1:
					self.AppendSpace(2)
					self.AppendTextLine("Pode ser adicinado +%d Bônus Raro" % (rareDisp), self.SPECIAL_POSITIVE_COLOR)
					self.AppendSpace(2)
				elif rareDisp == 2:
					self.AppendSpace(2)
					self.AppendTextLine("Podem ser adicinados +%d Bônus Raros" % (rareDisp), self.SPECIAL_POSITIVE_COLOR)
					self.AppendSpace(2)

	def __GetAttributeColor(self, index, value):
		if value > 0:
			if index >= 5:
				return self.SPECIAL_POSITIVE_COLOR2
			else:
				return self.SPECIAL_POSITIVE_COLOR
		elif value == 0:
			return self.NORMAL_COLOR
		else:
			return self.NEGATIVE_COLOR

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70106:
			return 1
		return 0

	def __SetPolymorphItemTitle(self, monsterVnum):
		itemName =nonplayer.GetMonsterName(monsterVnum)
		itemName+=" "
		itemName+=item.GetItemName()
		self.SetTitle(itemName)

	def __SetNormalItemTitle(self):
		if app.ENABLE_SEND_TARGET_INFO:
			if self.isStone:
				itemName = item.GetItemName()
				realName = itemName[:itemName.find("+")]
				self.SetTitle(realName + " +0 - +4")
			else:
				self.SetTitle(item.GetItemName())
		else:
			self.SetTitle(item.GetItemName())

	def __SetSpecialItemTitle(self):
		self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)

	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot):
		if self.__IsPolymorphItem(itemVnum):
			self.__SetPolymorphItemTitle(metinSlot[0])
		else:
			if self.__IsAttr(attrSlot):
				self.__SetSpecialItemTitle()
				return

			self.__SetNormalItemTitle()

		if itemVnum in [28887, 28888]:
			if metinSlot[1] == 0:
				self.AppendTextLine(("Sem experiência"), self.NEGATIVE_COLOR)
			else:
				self.AppendTextLine("Experiência disponível:", self.SPECIAL_TITLE_COLOR)
				self.AppendTextLine(str(metinSlot[1]), self.SPECIAL_TITLE_COLOR)

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0):
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if self.GetMetinItemIndex(metinSlotData) == constinfo.ERROR_METIN_STONE:
				metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, unbindTime = 0, cofres = 0, Show_Render = True):
		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()

		if 50026 == itemVnum:
			if 0 != metinSlot:
				name = item.GetItemName()
				if metinSlot[0] > 0:
					name += " "
					name += localeinfo.NumberToMoneyString(metinSlot[0])
				self.SetTitle(name)
				self.AppendAntiFlagInformation()
				self.ShowToolTip()
			return

		elif 50300 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeinfo.TOOLTIP_SKILLBOOK_NAME, 1)
				self.AppendAntiFlagInformation()
				self.ShowToolTip()
			return

		if cofres == 1:
			list_item =[[50300,localeinfo.TOOLTIP_SKILLBOOK_NAME],[70037,localeinfo.TOOLTIP_SKILL_FORGET_BOOK_NAME],[70055,localeinfo.TOOLTIP_SKILL_FORGET_BOOK_NAME]]
			for i in list_item:
				if itemVnum == i[0]:
					self.AppendAntiFlagInformation()
					self.ShowToolTip()

		elif 70037 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeinfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
				self.AppendDescription(item.GetItemDescription(), 26)
				self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
				self.AppendAntiFlagInformation()
				self.ShowToolTip()
			return

		elif 70055 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeinfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
				self.AppendDescription(item.GetItemDescription(), 26)
				self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
				self.AppendAntiFlagInformation()
				self.ShowToolTip()
			return

		itemDesc = item.GetItemDescription()
		itemSummary = item.GetItemSummary()

		isCostumeItem = 0
		isCostumeHair = 0
		isCostumeBody = 0

		if app.ENABLE_COSTUME_WEAPON_SYSTEM:
			isCostumeWeapon = 0

		if item.ITEM_TYPE_COSTUME == itemType:
			isCostumeItem = 1
			isCostumeHair = item.COSTUME_TYPE_HAIR == itemSubType
			isCostumeBody = item.COSTUME_TYPE_BODY == itemSubType
			if app.ENABLE_COSTUME_WEAPON_SYSTEM:
				isCostumeWeapon = item.COSTUME_TYPE_WEAPON == itemSubType

		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if app.RENDER_TARGET:
			self.__ModelPreviewClose()

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

		if item.ITEM_TYPE_WEAPON == itemType:
			self.__AppendLimitInformation()
			self.AppendSpace(5)
			if item.WEAPON_FAN == itemSubType or item.WEAPON_BELL == itemSubType:
				self.__AppendMagicAttackInfo()
				self.__AppendAttackPowerInfo()
			else:
				self.__AppendAttackPowerInfo()
				self.__AppendMagicAttackInfo()

			self.__AppendAffectInformation()
			self.AppendSpace(5)
			self.__AppendAttributeInformation(attrSlot)
			self.AppendWearableInformation()

			if itemSubType != item.WEAPON_UNLIMITED_ARROW:
				self.__AppendMetinSlotInfo(metinSlot)
			else:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if bHasRealtimeFlag == 1:
					self.AppendMallItemLastTime(metinSlot[0])

			if app.RENDER_TARGET and Show_Render:
				if item.WEAPON_SWORD == itemSubType:
					if player.GetRace() != 7 and player.GetRace() != 3:
						self.__ModelPreview(itemVnum, 3, player.GetRace())
				if item.WEAPON_DAGGER == itemSubType or item.WEAPON_BOW == itemSubType: 
					if player.GetRace() == 5 or player.GetRace() == 1:
						self.__ModelPreview(itemVnum, 3, player.GetRace())
				if item.WEAPON_TWO_HANDED == itemSubType: 
					if player.GetRace() == 0 or player.GetRace() == 4:
						self.__ModelPreview(itemVnum, 3, player.GetRace())
				if item.WEAPON_BELL == itemSubType or item.WEAPON_FAN == itemSubType: 
					if player.GetRace() == 7 or player.GetRace() == 3:
						self.__ModelPreview(itemVnum, 3, player.GetRace())

		elif item.ITEM_TYPE_ARMOR == itemType:
			self.__AppendLimitInformation()

			defGrade = item.GetValue(1)
			defBonus = item.GetValue(5)*2
			if defGrade > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeinfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus), self.GetChangeTextLineColor(defGrade))

			self.__AppendMagicDefenceInfo()
			self.__AppendAffectInformation()
			self.AppendSpace(5)
			self.__AppendAttributeInformation(attrSlot)

			self.AppendWearableInformation()

			if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				self.__AppendAccessoryMetinSlotInfo(metinSlot, constinfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType))
			else:
				self.__AppendMetinSlotInfo(metinSlot)

			if app.RENDER_TARGET:
				if itemSubType == item.ARMOR_BODY:
					if self.__ItemGetRace() == player.GetRace():
						self.__ModelPreview(itemVnum, 2, player.GetRace())

		elif item.ITEM_TYPE_BELT == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.__AppendAccessoryMetinSlotInfo(metinSlot, constinfo.GET_BELT_MATERIAL_VNUM(itemVnum))

		elif 0 != isCostumeItem:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			self.AppendWearableInformation()
			bHasRealtimeFlag = 0
			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1

			if cofres == 0:
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			if app.RENDER_TARGET:
				if itemSubType == 0:
					self.__ModelPreview(itemVnum, 2, player.GetRace())
				elif itemSubType == 1:
					self.__ModelPreview(item.GetValue(3), 1, player.GetRace())
				elif itemSubType == 3:
					self.__ModelPreview(itemVnum, 3, player.GetRace())
				elif itemSubType == 4:
					self.__ModelPreview(itemVnum, 0, item.GetValue(3))
				elif itemSubType == 5:
					self.__ModelPreview(itemVnum, 0, item.GetValue(3))

		elif item.ITEM_TYPE_ROD == itemType:
			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendRodInformation(curLevel, curEXP, maxEXP)

		elif item.ITEM_TYPE_PICK == itemType:
			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendPickInformation(curLevel, curEXP, maxEXP)

		elif item.ITEM_TYPE_LOTTERY == itemType:
			if 0 != metinSlot:

				ticketNumber = int(metinSlot[0])
				stepNumber = int(metinSlot[1])

				self.AppendSpace(5)
				self.AppendTextLine(localeinfo.TOOLTIP_LOTTERY_STEP_NUMBER % (stepNumber), self.NORMAL_COLOR)
				self.AppendTextLine(localeinfo.TOOLTIP_LOTTO_NUMBER % (ticketNumber), self.NORMAL_COLOR);

		elif item.ITEM_TYPE_METIN == itemType:
			self.AppendMetinInformation()
			self.AppendMetinWearInformation()

		elif item.ITEM_TYPE_FISH == itemType:
			if 0 != metinSlot:
				self.__AppendFishInfo(metinSlot[0])

		elif item.ITEM_TYPE_BLEND == itemType:
			self.__AppendLimitInformation()

			affectType = item.GetValue(0)
			affectValue = item.GetValue(1)
			time = item.GetValue(2)
			self.AppendSpace(5)
			affectText = self.__GetAffectString(affectType, affectValue)

			self.AppendTextLine(affectText, self.NORMAL_COLOR)

			if time > 0:
				minute = (time / 60)
				second = (time % 60)
				timeString = localeinfo.TOOLTIP_POTION_TIME

				if minute > 0:
					timeString += str(minute) + localeinfo.TOOLTIP_POTION_MIN
				if second > 0:
					timeString += " " + str(second) + localeinfo.TOOLTIP_POTION_SEC

				self.AppendTextLine(timeString)
			else:
				self.AppendTextLine("Sem limite de tempo")

		elif item.ITEM_TYPE_UNIQUE == itemType:
			if 0 != metinSlot:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

					if 1 == item.GetValue(2):
						self.AppendMallItemLastTime(time)
					else:
						self.AppendUniqueItemLastTime(time)

		elif item.ITEM_TYPE_USE == itemType:
			self.__AppendLimitInformation()

			if item.USE_POTION == itemSubType or item.USE_POTION_NODELAY == itemSubType:
				self.__AppendPotionInformation()

			elif itemSubType == 32:
				self.__AppendAffectInformation()
				self.AppendWearableInformation()
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_ABILITY_UP == itemSubType:
				self.__AppendAbilityPotionInformation()

			if 27989 == itemVnum or 76006 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeinfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount), self.NORMAL_COLOR)

			elif 50004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeinfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount), self.NORMAL_COLOR)

			elif constinfo.IS_AUTO_POTION(itemVnum):
				if 0 != metinSlot:
					isActivated = int(metinSlot[0])
					usedAmount = float(metinSlot[1])
					totalAmount = float(metinSlot[2])

					if 0 == totalAmount:
						totalAmount = 1

					self.AppendSpace(5)

					if 0 != isActivated:
						self.AppendTextLine("(%s)" % (localeinfo.TOOLTIP_AUTO_POTION_USING), self.SPECIAL_POSITIVE_COLOR)
						self.AppendSpace(5)

					self.AppendTextLine(localeinfo.TOOLTIP_AUTO_POTION_REST % (100.0 - ((usedAmount / totalAmount) * 100.0)), self.POSITIVE_COLOR)

			elif itemVnum in WARP_SCROLLS:
				if 0 != metinSlot:
					xPos = int(metinSlot[0])
					yPos = int(metinSlot[1])

					if xPos != 0 and yPos != 0:
						(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)
						localeMapName = localeinfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")

						self.AppendSpace(5)

						if localeMapName != "":
							self.AppendTextLine(localeinfo.TOOLTIP_MEMORIZED_POSITION % (localeMapName, int(xPos-xBase)/100, int(yPos-yBase)/100), self.NORMAL_COLOR)
							self.AppendMapImage(mapName, int(xPos-xBase)/100, int(yPos-yBase)/100)
						else:
							self.AppendTextLine(localeinfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (int(xPos)/100, int(yPos)/100), self.NORMAL_COLOR)
							dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)

			if item.USE_SPECIAL == itemSubType:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					if 0 != metinSlot:
						time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

						if 1 == item.GetValue(2):
							self.AppendMallItemLastTime(time)

			elif item.USE_TIME_CHARGE_PER == itemSubType:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeinfo.TOOLTIP_TIME_CHARGER_PER(metinSlot[2]))
				else:
					self.AppendTextLine(localeinfo.TOOLTIP_TIME_CHARGER_PER(item.GetValue(0)))

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_TIME_CHARGE_FIX == itemSubType:
				bHasRealtimeFlag = 0
				for i in range(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeinfo.TOOLTIP_TIME_CHARGER_FIX(metinSlot[2]))
				else:
					self.AppendTextLine(localeinfo.TOOLTIP_TIME_CHARGER_FIX(item.GetValue(0)))

				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_QUEST == itemType:
			for i in range(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					self.AppendMallItemLastTime(metinSlot[0])
		else:
			self.__AppendLimitInformation()

		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if cofres == 0:
				if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)
				elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					self.AppendTimerBasedOnWearLastTime(metinSlot)

			elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
				self.AppendTimerBasedOnWearLastTime(metinSlot)

		if chr.IsGameMaster(player.GetMainCharacterIndex()):
			self.AppendTextLine(localeinfo.ITEM_VNUM_TOOLTIP % (int(itemVnum)), self.ITEM_VNUM_TOOLTIP_COLOR)

		self.AppendAntiFlagInformation()
		self.ShowToolTip()

	def AppendMapImage(self, mapName, xPos, yPos):
		mapImage = ui.ImageBox()
		mapImage.SetParent(self)
		mapImage.Show()
		mapImage.LoadImage("d:/ymir work/ui/atlas/%s/atlas.sub" % (mapName))
		if mapImage.GetWidth() + 40 > self.toolTipWidth:
			self.toolTipWidth = mapImage.GetWidth() + 40
		mapImage.SetPosition(0, self.toolTipHeight)
		mapImage.SetWindowHorizontalAlignCenter()

		mapSizeDict = {
			"metin2_map_a1"					: [4, 5],
			"metin2_map_b1"					: [4, 5],
			"metin2_map_c1"					: [4, 5],
			"metin2_map_a3" 				: [4, 4],
			"metin2_map_b3" 				: [4, 4],
			"metin2_map_c3" 				: [4, 4],
			"metin2_map_trent"				: [2, 2],
			"metin2_map_trent02"			: [3, 3],
			"metin2_map_skipia_dungeon_02"	: [6, 6],
			"map_n_snowm_01"				: [6, 6],
			"map_n_threeway"				: [6, 6],
			"metin2_map_milgyo"				: [4, 4],
			"metin2_map_spiderdungeon"		: [3, 3],
			"metin2_map_spiderdungeon_02"	: [4, 4],
		}

		if mapName in mapSizeDict:
			pointImageX = (xPos / float(mapSizeDict[mapName][0] * (128 * 200)) * float(mapImage.GetWidth())) * 100 - 15.0
			pointImageY = (yPos / float(mapSizeDict[mapName][1] * (128 * 200)) * float(mapImage.GetHeight())) * 100 - 15.0

			pointImage = ui.AniImageBox()
			pointImage.SetParent(mapImage)
			pointImage.SetDelay(6)
			for i in range(1, 13):
				pointImage.AppendImage("d:/ymir work/ui/minimap/mini_waypoint%02d.sub" % i)
			pointImage.SetPosition(pointImageX, pointImageY)
			pointImage.Show()

		self.toolTipHeight += mapImage.GetHeight()
		self.childrenList.append(mapImage)
		if mapName in mapSizeDict:
			self.childrenList.append(pointImage)
		self.ResizeToolTip()

	def __IsHair(self, itemVnum):
		return (self.__IsOldHair(itemVnum) or self.__IsNewHair(itemVnum) or self.__IsNewHair2(itemVnum) or self.__IsNewHair3(itemVnum) or self.__IsCostumeHair(itemVnum))

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74522) or
			(74762 < itemVnum and itemVnum < 74772) or
			(45000 < itemVnum and itemVnum < 47000))

	def __IsCostumeHair(self, itemVnum):
		self.__IsNewHair3(itemVnum - 100000)

	def __AppendHairIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		if self.__IsOldHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum)+".tga")
		elif self.__IsNewHair3(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsNewHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga")
		elif self.__IsNewHair2(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsCostumeHair(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum - 100000))

		itemImage.SetPosition(itemImage.GetWidth()/2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		self.childrenList.append(itemImage)
		self.ResizeToolTip()


	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)
		if not skillName:
			return

		itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeinfo.TOOLTIP_PICK_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeinfo.TOOLTIP_PICK_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeinfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeinfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeinfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)


	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeinfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeinfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeinfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeinfo.TOOLTIP_FISHINGROD_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeinfo.TOOLTIP_FISHINGROD_UPGRADE3, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):
		appendSpace = False

		for i in range(item.LIMIT_MAX_NUM):

			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					self.AppendSpace(5)
					appendSpace = True
			else:
				continue

			if item.LIMIT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.LEVEL), limitValue)
				self.AppendTextLine(localeinfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue), color)

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	if app.ENABLE_SOULBIND_SYSTEM:
		def AppendSealInformation(self, window_type, slotIndex):
			if window_type == player.SAFEBOX:
				if safebox.GetItemBind(slotIndex) <= 1:
					itemSoulTime = safebox.GetItemBind(slotIndex)
				else:
					itemSoulTime = max(0, safebox.GetItemBind(slotIndex) - app.GetGlobalTimeStamp())
			elif window_type == player.INVENTORY:
				if player.GetItemBind(slotIndex) <= 1:
					itemSoulTime = player.GetItemBind(slotIndex)
				else:
					itemSoulTime = max(0, player.GetItemBind(slotIndex) - app.GetGlobalTimeStamp())
			else:
				return

			if itemSoulTime == 0:
				return
			elif itemSoulTime == 1:
				self.AppendSpace(5)
				self.AppendTextLine(localeinfo.TOOLTIP_SEALED, self.NEGATIVE_COLOR)
			elif itemSoulTime > 1:
				self.AppendSpace(5)
				hrs = itemSoulTime / 3600
				itemSoulTime -= 3600 * hrs
				mins = itemSoulTime / 60
				itemSoulTime -= 60 * mins
				self.AppendTextLine(localeinfo.TOOLTIP_UNSEAL_LEFT_TIME % (hrs, mins), self.NEGATIVE_COLOR)

	def __AppendAffectInformation(self):
		for i in range(item.ITEM_APPLY_MAX_NUM):

			(affectType, affectValue) = item.GetAffect(i)

			affectString = self.__GetAffectString(affectType, affectValue)
			if affectString:
				self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendWearableInformation(self):
		self.AppendSpace(5)
		self.AppendTextLine(localeinfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

		flagList = (
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN))

		characterNames = ""
		for i in range(self.CHARACTER_COUNT):
			name = self.CHARACTER_NAMES[i]
			flag = flagList[i]
			if flag:
				characterNames += " "
				characterNames += name

		if "Guerreiro Ninja Shura Shaman Lycan" in characterNames:
			characterNames = "Todas as Classes"

		textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
		textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
			textLine = self.AppendTextLine(localeinfo.FOR_FEMALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
			textLine = self.AppendTextLine(localeinfo.FOR_MALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeinfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def AppendAntiFlagInformation(self):
		flagList = [
			[item.ITEM_ANTIFLAG_GIVE, "Negociar"],
			[item.ITEM_ANTIFLAG_DROP, "Dropar"],
			[item.ITEM_ANTIFLAG_SELL, "Vender"],
			[item.ITEM_ANTIFLAG_MYSHOP, "Loja"],
			[item.ITEM_ANTIFLAG_SAFEBOX , "Armazém"],
		]

		antiflagNames = ""
		for i in range(len(flagList)):
			if item.IsAntiFlag(flagList[i][0]):
				antiflagNames += flagList[i][1]
				antiflagNames += ","

		if antiflagNames != "":
			self.AppendSpace(5)
			self.AppendTextLine("[ Impossível Descartar ]", self.DISABLE_COLOR)
			textLine = self.AppendTextLine(antiflagNames[:-1], self.DISABLE_COLOR, True)
			textLine.SetFeather()

	def __AppendAbilityPotionInformation(self):
		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)

		if abilityType == item.APPLY_ATT_SPEED:
			self.AppendTextLine(localeinfo.TOOLTIP_POTION_PLUS_ATTACK_SPEED % point, self.GetChangeTextLineColor(point))
		elif abilityType == item.APPLY_MOV_SPEED:
			self.AppendTextLine(localeinfo.TOOLTIP_POTION_PLUS_MOVING_SPEED % point, self.GetChangeTextLineColor(point))

		if time > 0:
			minute = (time / 60)
			second = (time % 60)
			timeString = localeinfo.TOOLTIP_POTION_TIME

			if minute > 0:
				timeString += str(minute) + localeinfo.TOOLTIP_POTION_MIN
			if second > 0:
				timeString += " " + str(second) + localeinfo.TOOLTIP_POTION_SEC

			self.AppendTextLine(timeString)

	def GetPriceColor(self, price):
		if price >= constinfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price >= constinfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR

	def AppendPrice(self, price):
		self.AppendSpace(5)
		if price == 0:
			self.AppendTextLine("Grátis", self.GetPriceColor(price))
		else:
			self.AppendTextLine(localeinfo.TOOLTIP_BUYPRICE  % (localeinfo.NumberToMoneyString(price)), self.GetPriceColor(price))
		self.AppendPriceDescritpion(price)

	def AppendSellingPrice(self, price):
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):
			self.AppendTextLine(localeinfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
			self.AppendSpace(5)
		else:
			self.AppendTextLine(localeinfo.TOOLTIP_SELLPRICE % (localeinfo.NumberToMoneyString(price)), self.GetPriceColor(price))
			self.AppendSpace(5)
		self.AppendPriceDescritpion(price)

	def AppendPriceDescritpion(self, price):
		mascs = int(price/100000000)
		if mascs > 1:
			self.AppendSpace(5)
			self.AppendTextLine("Apróx. " + localeinfo.NumberToMoneyString(mascs) + " Máscaras", self.MIDDLE_PRICE_COLOR)
			self.AppendSpace(5)
		elif mascs == 1:
			self.AppendSpace(5)
			self.AppendTextLine("Apróx. " + localeinfo.NumberToMoneyString(mascs) + " Máscara da Fortuna", self.MIDDLE_PRICE_COLOR)
			self.AppendSpace(5)

	def AppendMetinInformation(self):
		affectType, affectValue = item.GetAffect(0)
		affectString = self.__GetAffectString(affectType, affectValue)

		if affectString:
			self.AppendSpace(5)
			self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):
		self.AppendSpace(5)
		self.AppendTextLine(localeinfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))

		wearNames = ""
		for i in range(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += "  "
				wearNames += name

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(self.NORMAL_COLOR)
		textLine.SetText(wearNames)
		textLine.Show()
		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if player.METIN_SOCKET_TYPE_NONE == number:
			return player.METIN_SOCKET_TYPE_NONE
		elif player.METIN_SOCKET_TYPE_SILVER == number:
			return player.METIN_SOCKET_TYPE_SILVER
		elif player.METIN_SOCKET_TYPE_GOLD == number:
			return player.METIN_SOCKET_TYPE_GOLD
		else:
			item.SelectItem(number)
			if item.METIN_NORMAL == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_SILVER
			elif item.METIN_GOLD == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_GOLD
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER

		return player.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if player.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if player.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrlVnum):
		ACCESSORY_SOCKET_MAX_SIZE = 3

		cur = min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end = min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		affectType1, affectValue1 = item.GetAffect(0)
		affectList1=[0, max(1, affectValue1*10/100), max(2, affectValue1*20/100), max(3, affectValue1*40/100)]

		affectType2, affectValue2 = item.GetAffect(1)
		affectList2 = [0, max(1, affectValue2*10/100), max(2, affectValue2*20/100), max(3, affectValue2*40/100)]

		mtrlPos = 0
		mtrlList = [mtrlVnum]*cur+[player.METIN_SOCKET_TYPE_SILVER]*(end-cur)
		for mtrl in mtrlList:
			affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos+1]-affectList1[mtrlPos])
			affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos+1]-affectList2[mtrlPos])

			leftTime = 0
			if cur == mtrlPos+1:
				leftTime=metinSlot[2]

			self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, leftTime)
			mtrlPos += 1

	def __AppendMetinSlotInfo(self, metinSlot):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return

		for i in range(player.METIN_SOCKET_MAX_NUM):
			self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1

		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if 0 != self.GetMetinSocketType(metinSlotData):
				if 0 != self.GetMetinItemIndex(metinSlotData):
					return 0
		return 1

	def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString="", custumAffectString2="", leftTime=0):
		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		self.AppendSpace(5)

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.LoadImage("interface/controls/common/slot_rectangle/slot.tga")
		slotImage.Show()

		nameTextLine = ui.TextLine()
		nameTextLine.SetParent(self)
		nameTextLine.SetFontName(self.defFontName)
		nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
		nameTextLine.SetOutline()
		nameTextLine.SetFeather()
		nameTextLine.Show()

		self.childrenList.append(nameTextLine)

		self.childrenList.append(slotImage)
		slotImage.SetPosition(13, self.toolTipHeight)
		nameTextLine.SetPosition(50, self.toolTipHeight + 2)

		metinImage = ui.ImageBox()
		metinImage.SetParent(self)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:
			item.SelectItem(itemIndex)

			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except BaseException:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" % (itemIndex, item.GetIconImageFileName()))

			nameTextLine.SetText(item.GetItemName())

			affectTextLine = ui.TextLine()
			affectTextLine.SetParent(self)
			affectTextLine.SetFontName(self.defFontName)
			affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
			affectTextLine.SetOutline()
			affectTextLine.SetFeather()
			affectTextLine.Show()
			metinImage.SetPosition(13, self.toolTipHeight)
			affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

			if custumAffectString:
				affectTextLine.SetText(custumAffectString)
			elif itemIndex != constinfo.ERROR_METIN_STONE:
				affectType, affectValue = item.GetAffect(0)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
			else:
				affectTextLine.SetText(localeinfo.TOOLTIP_APPLY_NOAFFECT)
			self.childrenList.append(affectTextLine)

			if custumAffectString2:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString2)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if 0 != leftTime:
				# timeText = (localeinfo.LEFT_TIME + " : " + localeinfo.SecondToDHM(leftTime))
				timeText = "Infinito"

				timeTextLine = ui.TextLine()
				timeTextLine.SetParent(self)
				timeTextLine.SetFontName(self.defFontName)
				timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				timeTextLine.SetOutline()
				timeTextLine.SetFeather()
				timeTextLine.Show()
				timeTextLine.SetText(timeText)
				self.childrenList.append(timeTextLine)
				self.toolTipHeight += 16 + 2

		else:
			nameTextLine.SetText(localeinfo.TOOLTIP_SOCKET_EMPTY)

		self.toolTipHeight += 35
		self.ResizeToolTip()

	if app.ALUGAR_ITENS:
		def AppendRentInformation(self, window_type, slotIndex):
			if window_type == player.INVENTORY:
				if player.GetItemRentTime(slotIndex) <= 1:
					rent = player.GetItemRentTime(slotIndex)
				else:
					rent = max(0, player.GetItemRentTime(slotIndex) - app.GetGlobalTimeStamp())
			elif window_type == 10:
				if exchange.GetItemRentTimeFromSelf(slotIndex) <= 1:
					rent = exchange.GetItemRentTimeFromSelf(slotIndex)
				else:
					rent = max(0, exchange.GetItemRentTimeFromSelf(slotIndex) - app.GetGlobalTimeStamp())
			elif window_type == 11:
				if exchange.GetItemRentTimeFromTarget(slotIndex) <= 1:
					rent = exchange.GetItemRentTimeFromTarget(slotIndex)
				else:
					rent = max(0, exchange.GetItemRentTimeFromTarget(slotIndex) - app.GetGlobalTimeStamp())
			elif window_type == 20: #InventoryViwer for GMs
				if slotIndex <= 1:
					return
				else:
					rent = slotIndex - app.GetGlobalTimeStamp()

			if rent <= 0:
				return
			else:
				days = rent / 86400
				rent -= 86400 * days
				hrs = rent / 3600
				rent -= 3600 * hrs
				mins = rent / 60
				rent -= 60 * mins

				self.AppendSpace(10)
				self.AppendTextLine("[Emprestado/Alugado]", self.TITLE_COLOR)

				if days > 0:
					self.AppendTextLine("Tempo Restante: %d dias" % (days), self.NORMAL_COLOR)
				elif hrs > 0:
					self.AppendTextLine("Tempo Restante: %d horas" % (hrs), self.NORMAL_COLOR)
				else:
					self.AppendTextLine("Tempo Restante: %d minutos" % (mins), self.NORMAL_COLOR)

	def __AppendFishInfo(self, size):
		if size > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeinfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)

	def AppendUniqueItemLastTime(self, restMin):
		if restMin == 0 and shop.IsOpen() and not shop.IsPrivateShop():
			restMin = item.GetValue(0)
		restSecond = restMin * 60
		self.AppendSpace(5)
		self.AppendTextLine(localeinfo.LEFT_TIME + " : " + localeinfo.SecondToHM(restSecond), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		if endTime == 0 and shop.IsOpen() and not shop.IsPrivateShop():
			endTime = item.GetValue(0)+app.GetGlobalTimeStamp()
		leftSec = max(0, endTime - app.GetGlobalTimeStamp())
		self.AppendSpace(5)
		self.AppendTextLine(localeinfo.LEFT_TIME + " : " + localeinfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if 0 == metinSlot[0]:
			self.AppendSpace(5)
			self.AppendTextLine(localeinfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex):
		useCount = metinSlot[1]
		endTime = metinSlot[0]

		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			endTime += app.GetGlobalTimeStamp()

		self.AppendMallItemLastTime(endTime)

if app.ENABLE_FLAGS_CHAT:
	class ToolTipBallon(ui.Ballon):

		def __init__(self):
			ui.Ballon.__init__(self, "TOP_MOST")
			self.AddFlag("not_pick")
			self.AddFlag("float")

		def __del__(self):
			ui.Ballon.__del__(self)

		def AutoAppendTextLine(self, text):
			self.SetText(text)

		def ShowToolTip(self):
			self.SetTop()
			self.Show()
			self.OnUpdate()

		def HideToolTip(self):
			self.Hide()

		def OnUpdate(self):
			x = 0
			y = 0
			width = self.GetWidth()
			height = self.GetHeight()

			(mouseX, mouseY) = wndMgr.GetMousePosition()
			x = mouseX - width / 2
			y = mouseY - height - 10

			x = max(x, 0)
			y = max(y, 0)
			x = min(x + width / 2, wndMgr.GetScreenWidth() - width / 2) - width / 2
			y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

			parentWindow = self.GetParentProxy()
			if parentWindow:
				(gx, gy) = parentWindow.GetGlobalPosition()
				x -= gx
				y -= gy

			self.SetPosition(x, y)

	class HyperlinkToolTip(ToolTipBallon):

		FLAG_LANG = {
			"br" : 'Brasil',
			"hu" : 'Hungaro',
			"pl" : 'Polônia',
			"cz" : 'Theco',
			"de" : 'Alemanha',
			"ro" : 'Rom?nia',
			"tr" : 'Turquia',
			"es" : 'Espanha',
			"en" : 'Inglaterra',
			"pt" : 'Portugal',
			"it" : 'Itália',
		}

		FLAG_REINO = {
			1: 'Shinsu',
			2: 'Chunjo',
			3: 'Jinno',
		}

		FLAG_RACE = {
			0 : 'Guerreiro',
			1 : 'Ninja',
			2 : 'Shura',
			3 : 'Shaman',
			4 : 'Guerreiro',
			5 : 'Ninja',
			6 : 'Shura',
			7 : 'Shaman',
			8 : 'Lycan',
		}

		def __init__(self):
			ToolTipBallon.__init__(self)

		def __del__(self):
			ToolTipBallon.__del__(self)

		def SetHyperlink(self, tokens):
			if tokens:
				token = tokens.split(":")
				if token and len(token):
					type = token[0]
					if "lang" == type:
						self.AutoAppendTextLine(self.FLAG_LANG[str(token[1])])
					if "reino" == type:
						self.AutoAppendTextLine(self.FLAG_REINO[int(token[1])])
					if "race" == type:
						self.AutoAppendTextLine(self.FLAG_RACE[int(token[1])])
					if "msg" == type:
						self.AutoAppendTextLine("Enviar mensagem particular")
				self.ShowToolTip()

		def HideHyperlink(self):
			self.HideToolTip()
			self.Hide()

class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable = True)

	def SetHyperlinkItem(self, tokens):
		minTokenCount = 3 + player.METIN_SOCKET_MAX_NUM
		maxTokenCount = minTokenCount + 2 * player.ATTRIBUTE_SLOT_MAX_NUM
		if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
			head, vnum, flag = tokens[:3]
			itemVnum = int(vnum, 16)

			if app.ENABLE_EXTENDED_SOCKETS:
				metinSlot = [int(metin, 16) for metin in tokens[3:9]]
				rests = tokens[9:]
			else:
				metinSlot = [int(metin, 16) for metin in tokens[3:6]]
				rests = tokens[6:]

			if rests:
				attrSlot = []

				rests.reverse()
				while rests:
					key = int(rests.pop(), 16)
					if rests:
						val = int(rests.pop())
						attrSlot.append((key, val))

				attrSlot += [(0, 0)] * (player.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
			else:
				attrSlot = [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM

			self.ClearToolTip()
			self.AddItemData(itemVnum, metinSlot, attrSlot)

			ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()
		return True

class SkillToolTip(ToolTip):
	POINT_NAME_DICT = {
		player.LEVEL : localeinfo.SKILL_TOOLTIP_LEVEL,
		player.IQ : localeinfo.SKILL_TOOLTIP_INT,
	}

	SKILL_TOOL_TIP_WIDTH = 0
	PARTY_SKILL_TOOL_TIP_WIDTH = 0

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (
		( 2, 2,  10,),
		( 8, 3,  20,),
		(14, 4,  30,),
		(22, 5,  45,),
		(28, 6,  60,),
		(34, 7,  80,),
		(38, 8, 100,),
	)

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (
		( 4, 2, 1, 0,),
		(10, 3, 2, 0,),
		(16, 4, 2, 1,),
		(24, 5, 2, 2,),
	)

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (
		( 36, 3,),
		( 26, 1,),
		( 32, 2,),
	)

	SKILL_GRADE_NAME = {
		player.SKILL_GRADE_MASTER : localeinfo.SKILL_GRADE_NAME_MASTER,
		player.SKILL_GRADE_GRAND_MASTER : localeinfo.SKILL_GRADE_NAME_GRAND_MASTER,
		player.SKILL_GRADE_PERFECT_MASTER : localeinfo.SKILL_GRADE_NAME_PERFECT_MASTER,
	}

	AFFECT_NAME_DICT = {
		"HP" : localeinfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
		"ATT_GRADE" : localeinfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
		"DEF_GRADE" : localeinfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
		"ATT_SPEED" : localeinfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
		"MOV_SPEED" : localeinfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
		"DODGE" : localeinfo.TOOLTIP_SKILL_AFFECT_DODGE,
		"RESIST_NORMAL" : localeinfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
		"REFLECT_MELEE" : localeinfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
	}

	AFFECT_APPEND_TEXT_DICT = {
		"DODGE" : "%",
		"RESIST_NORMAL" : "%",
		"REFLECT_MELEE" : "%",
	}

	def __init__(self):
		ToolTip.__init__(self, self.SKILL_TOOL_TIP_WIDTH)

	def __del__(self):
		ToolTip.__del__(self)

	def SetSkill(self, skillIndex, skillLevel = -1):
		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:
			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):
		if 0 == skillIndex:
			return

		if player.SKILL_INDEX_TONGSOL == skillIndex:
			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)
		elif player.SKILL_INDEX_RIDING == skillIndex:
			slotIndex = player.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)
		elif player.SKILL_INDEX_SUMMON == skillIndex:
			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				self.AppendTextLine(localeinfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10), self.NORMAL_COLOR)
			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.NORMAL_COLOR)
				self.AppendSpace(5)
				self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)
		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):
			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()
			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)
		else:
			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)
			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)
		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if self.SKILL_GRADE_NAME.__contains__(skillGrade):
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = player.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if player.GetStatus(player.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeinfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		self.AppendSpace(5)
		self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in range(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)

		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeinfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeinfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeinfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeinfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeinfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):
		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		skillLevelUpPoint = 1
		realSkillGrade = player.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeinfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		if skillGrade != skill.SKILL_GRADE_COUNT:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeinfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeinfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew(skillIndex, skillNextPercentage, self.DISABLE_COLOR)

	def AppendSkillLevelDescriptionNew(self, skillIndex, skillPercentage, color):
		affectDataCount = skill.GetNewAffectDataCount(skillIndex)
		if affectDataCount > 0:
			for i in range(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if not self.AFFECT_NAME_DICT.__contains__(type):
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeinfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")
				self.AppendTextLine(affectText, color)
		else:
			for i in range(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)

		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_SKILL_DURATION % (duration), color)

		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):
		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		if skill.IsSkillRequirement(skillIndex):
			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeinfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:
			for i in range(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if self.POINT_NAME_DICT.__contains__(type):
					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()
					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if player.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeinfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True
		return False

	def AppendNeedHP(self, needSP, continuationSP, color):
		self.AppendTextLine(localeinfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self, needSP, continuationSP, color):
		if -1 == needSP:
			self.AppendTextLine(localeinfo.TOOLTIP_NEED_ALL_SP, color)

		else:
			self.AppendTextLine(localeinfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeinfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel =  40

		if skillLevel <= 0:
			return

		skillIndex = player.SKILL_INDEX_TONGSOL
		slotIndex = player.GetSkillSlotIndex(skillIndex)
		skillPower = player.GetSkillCurrentEfficientPercentage(slotIndex)
		k = player.GetSkillLevel(skillIndex) / 100.0
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeinfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		if skillLevel >= 10:
			self.AutoAppendTextLine(localeinfo.PARTY_SKILL_ATTACKER % chop( 10 + 60 * k ))

		if skillLevel >= 20:
			self.AutoAppendTextLine(localeinfo.PARTY_SKILL_BERSERKER % chop(1 + 5 * k))
			self.AutoAppendTextLine(localeinfo.PARTY_SKILL_TANKER % chop(50 + 1450 * k))

		if skillLevel >= 25:
			self.AutoAppendTextLine(localeinfo.PARTY_SKILL_BUFFER % chop(5 + 45 * k ))

		if skillLevel >= 35:
			self.AutoAppendTextLine(localeinfo.PARTY_SKILL_SKILL_MASTER % chop(25 + 600 * k ))

		if skillLevel >= 40:
			self.AutoAppendTextLine(localeinfo.PARTY_SKILL_DEFENDER % chop( 5 + 30 * k ))

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			self.AppendTextLine(localeinfo.SKILL_SUMMON_DESCRIPTION % (skillLevel * 10), color)
		elif 1 == skillLevel:
			self.AppendTextLine(localeinfo.SKILL_SUMMON_DESCRIPTION % (15), color)
		elif 0 == skillLevel:
			self.AppendTextLine(localeinfo.SKILL_SUMMON_DESCRIPTION % (10), color)