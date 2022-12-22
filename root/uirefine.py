#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import ui
import uitooltip
import localeinfo
import uicommon
import wait
import grp

class RefineDialogNew(ui.ScriptWindow):

	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeinfo.REFINE_APPLY_MAX_HP,
		item.APPLY_MAX_SP : localeinfo.REFINE_APPLY_MAX_SP,
		item.APPLY_CON : localeinfo.REFINE_APPLY_CON,
		item.APPLY_INT : localeinfo.REFINE_APPLY_INT,
		item.APPLY_STR : localeinfo.REFINE_APPLY_STR,
		item.APPLY_DEX : localeinfo.REFINE_APPLY_DEX,
		item.APPLY_ATT_SPEED : localeinfo.REFINE_APPLY_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeinfo.REFINE_APPLY_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeinfo.REFINE_APPLY_CAST_SPEED,
		item.APPLY_HP_REGEN : localeinfo.REFINE_APPLY_HP_REGEN,
		item.APPLY_SP_REGEN : localeinfo.REFINE_APPLY_SP_REGEN,
		item.APPLY_POISON_PCT : localeinfo.REFINE_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeinfo.REFINE_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeinfo.REFINE_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeinfo.REFINE_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeinfo.REFINE_APPLY_PENETRATE_PCT,
		item.APPLY_ATTBONUS_WARRIOR : localeinfo.REFINE_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeinfo.REFINE_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeinfo.REFINE_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeinfo.REFINE_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeinfo.REFINE_APPLY_ATTBONUS_MONSTER,
		item.APPLY_ATTBONUS_HUMAN : localeinfo.REFINE_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeinfo.REFINE_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeinfo.REFINE_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeinfo.REFINE_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeinfo.REFINE_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeinfo.REFINE_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeinfo.REFINE_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeinfo.REFINE_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeinfo.REFINE_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeinfo.REFINE_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeinfo.REFINE_APPLY_BLOCK,
		item.APPLY_DODGE : localeinfo.REFINE_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeinfo.REFINE_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeinfo.REFINE_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeinfo.REFINE_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeinfo.REFINE_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeinfo.REFINE_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeinfo.REFINE_APPLY_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeinfo.REFINE_APPLY_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeinfo.REFINE_APPLY_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeinfo.REFINE_APPLY_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeinfo.REFINE_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeinfo.REFINE_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeinfo.REFINE_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeinfo.REFINE_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeinfo.REFINE_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeinfo.REFINE_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeinfo.REFINE_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeinfo.REFINE_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeinfo.REFINE_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeinfo.REFINE_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeinfo.REFINE_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeinfo.REFINE_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeinfo.REFINE_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeinfo.REFINE_APPLY_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeinfo.REFINE_APPLY_DEF_GRADE_BONUS,
		item.APPLY_ATT_GRADE_BONUS : localeinfo.REFINE_APPLY_ATT_GRADE_BONUS,
		item.APPLY_MAGIC_ATT_GRADE : localeinfo.REFINE_APPLY_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeinfo.REFINE_APPLY_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeinfo.REFINE_APPLY_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeinfo.REFINE_APPLY_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeinfo.REFINE_APPLY_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeinfo.REFINE_APPLY_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeinfo.REFINE_APPLY_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeinfo.REFINE_APPLY_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeinfo.REFINE_APPLY_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeinfo.REFINE_APPLY_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeinfo.REFINE_APPLY_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeinfo.REFINE_APPLY_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_RESIST_WARRIOR : localeinfo.REFINE_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeinfo.REFINE_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeinfo.REFINE_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeinfo.REFINE_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeinfo.REFINE_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeinfo.REFINE_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeinfo.REFINE_APPLY_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeinfo.REFINE_APPLY_COSTUME_ATTR_BONUS,
		item.APPLY_MAGIC_ATTBONUS_PER : localeinfo.REFINE_APPLY_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeinfo.REFINE_APPLY_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeinfo.REFINE_APPLY_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeinfo.REFINE_APPLY_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeinfo.REFINE_APPLY_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeinfo.REFINE_APPLY_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeinfo.REFINE_APPLY_ANTI_PENETRATE_PCT,
		item.APPLY_RESIST_HUMAN : localeinfo.TOOLTIP_ANTI_PENETRATE_PCT,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False
		self.wndInventory = None

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.cost = 0
		self.percentage = 0
		self.type = 0
		self.lockedItem = (-1,-1)

	def __LoadScript(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		self.board = self.GetChild("Board")
		self.retrair = self.GetChild("Retrair")
		self.expandir = self.GetChild("Expandir")
		self.probText = self.GetChild("SuccessPercentage")
		self.costText = self.GetChild("Cost")
		self.successPercentage = self.GetChild("SuccessPercentage")
		self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
		self.GetChild("CancelButton").SetEvent(self.CancelRefine)

		self.successPercentage.Show()

		itemImage = self.__MakeItemImage()
		itemImage.SetParent(self.GetChild("slot_origem"))
		itemImage.SetWindowVerticalAlignCenter()
		itemImage.SetWindowHorizontalAlignCenter()
		itemImage.SetPosition(0, 0)
		self.itemImage = itemImage

		itemResultImage = self.__MakeItemImage()
		itemResultImage.SetParent(self.GetChild("slot_result"))
		itemResultImage.SetWindowVerticalAlignCenter()
		itemResultImage.SetWindowHorizontalAlignCenter()
		itemResultImage.SetPosition(0, 0)
		self.itemResultImage = itemResultImage

		toolTip = uitooltip.ItemToolTip()
		toolTip.SetParent(self.GetChild("slot_origem"))
		toolTip.SetPosition(15, 38)
		self.toolTip = toolTip
		self.GetChild("slot_origem").SetToolTipWindow(self.toolTip)
		
		toolTipResult = uitooltip.ItemToolTip()
		toolTipResult.SetParent(self.GetChild("slot_result"))
		toolTipResult.SetPosition(15, 38)
		self.toolTipResult = toolTipResult
		self.GetChild("slot_result").SetToolTipWindow(self.toolTipResult)

		self.board.SetCloseEvent(self.CancelRefine)
		self.expandir.SetEvent(self.__Expandir)
		self.retrair.SetEvent(self.__Retrair)
		self.isLoaded = True

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeItemImage(self):
		itemImage = ui.ImageBox()
		itemImage.AddFlag("not_pick")
		itemImage.Show()
		self.children.append(itemImage)
		return itemImage

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.probText = 0
		self.costText = 0
		self.toolTip = 0
		self.toolTipResult = 0
		self.index = 1
		self.successPercentage = None
		self.children = []
		self.wndInventory = None
		self.lockedItem = (-1,-1)

	def Open(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		if False == self.isLoaded:
			self.__LoadScript()
		self.__Initialize()

		for i in range(1, 6):
			self.GetChild("add"+str(i)+"_1").SetText("Sem Atributo")
			self.GetChild("add"+str(i)+"_2").SetText("0")

		self.GetChild("slot_refine1").Hide()
		self.GetChild("slot_refine2").Hide()
		self.GetChild("slot_refine3").Hide()
		self.GetChild("slot_refine4").Hide()
		self.GetChild("slot_refine5").Hide()

		self.targetItemPos = targetItemPos
		self.vnum = nextGradeItemVnum
		self.cost = cost
		self.percentage = prob
		self.type = type
		self.index = 1
		self.probText.SetText(localeinfo.REFINE_SUCCESS_PROBALITY % (self.percentage))
		self.costText.SetText(localeinfo.REFINE_COST % (self.cost))

		self.SetCantMouseEventSlot(targetItemPos)

		#TOOLTIPs
		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		attrSlot = []
		for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(targetItemPos, i))
		
		origem_vnum = player.GetItemIndex(targetItemPos)
		item.SelectItem(origem_vnum)

		self.itemImage.LoadImage(item.GetIconImageFileName())
		self.toolTip.ClearToolTip()
		self.toolTip.AddRefineItemData(origem_vnum, metinSlot, attrSlot)		

		self.toolTipResult.ClearToolTip()
		self.toolTipResult.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot)

		self.toolTip.Hide()
		self.toolTipResult.Hide()

		self.GetChild("slot_origem").SetToolTipWindow(self.toolTip)
		self.GetChild("slot_result").SetToolTipWindow(self.toolTipResult)

		item.SelectItem(nextGradeItemVnum)
		name = item.GetItemName()
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()
		self.GetChild("name_result").SetText(name)
		self.itemResultImage.LoadImage(item.GetIconImageFileName())

		# INFO DO ITEM
		NEGATIVE_COLOR = grp.GenerateColor(0.999, 0.3, 0.3, 1.0)
		POSITIVE_COLOR = grp.GenerateColor(0.5, 0.9058, 0.5, 1.0)

		# LVL DO ITEM
		lvl = self.__LevelLimitInfo()
		self.GetChild("item_lvl").SetText(str(lvl))
		if player.GetStatus(player.LEVEL) < lvl:
			self.GetChild("item_lvl").SetPackedFontColor(NEGATIVE_COLOR)
		else:
			self.GetChild("item_lvl").SetPackedFontColor(POSITIVE_COLOR)

		if item.ITEM_TYPE_WEAPON == itemType:
			if item.WEAPON_FAN == itemSubType or item.WEAPON_BELL == itemSubType:
				self.GetChild("add1_1").SetText(localeinfo.REFINE_APPLY_MAGIC_ATT_GRADE)
				self.GetChild("add1_2").SetText(self.__MagicAttackInfo(origem_vnum, nextGradeItemVnum))
				self.GetChild("add2_1").SetText(localeinfo.REFINE_APPLY_ATT_GRADE_BONUS)
				self.GetChild("add2_2").SetText(self.__AttackPowerInfo(origem_vnum, nextGradeItemVnum))
			else:
				self.GetChild("add1_1").SetText(localeinfo.REFINE_APPLY_ATT_GRADE_BONUS)
				self.GetChild("add1_2").SetText(self.__AttackPowerInfo(origem_vnum, nextGradeItemVnum))
				self.GetChild("add2_1").SetText(localeinfo.REFINE_APPLY_MAGIC_ATT_GRADE)
				self.GetChild("add2_2").SetText(self.__MagicAttackInfo(origem_vnum, nextGradeItemVnum))

		elif item.ITEM_TYPE_ARMOR == itemType:
			defGrade = item.GetValue(1)
			defBonus = item.GetValue(5)*2
			self.GetChild("add1_1").SetText(localeinfo.REFINE_APPLY_DEF_GRADE_BONUS)
			self.GetChild("add1_2").SetText(str(defGrade+defBonus))
			self.GetChild("add2_1").SetText(localeinfo.REFINE_APPLY_MAGIC_DEF_GRADE)
			self.GetChild("add2_2").SetText(str(self.__MagicDefenceInfo(origem_vnum, nextGradeItemVnum)))
			
		self.__AppendAffectInformation(origem_vnum, nextGradeItemVnum)

		# xSlotCount, ySlotCount = item.GetItemSize()

		self.SetTop()
		self.Show()

	def __AttackPowerInfo(self, origem_vnum, nextGradeItemVnum):
		item.SelectItem(nextGradeItemVnum)
		minPower = item.GetValue(3)
		maxPower = item.GetValue(4)
		addPower = item.GetValue(5)

		item.SelectItem(origem_vnum)
		minPowerOr = item.GetValue(3)
		maxPowerOr = item.GetValue(4)
		addPowerOr = item.GetValue(5)

		if maxPower > minPower:
			return (str(minPower+addPower) + "|cfff8d090(+" + str(minPower+addPower-minPowerOr-addPowerOr) + ") - |cffa08784" + str(maxPower+addPower) + "|cfff8d090(+" + str(maxPower+addPower-maxPowerOr-addPowerOr) + ")")
		else:
			return (str(minPower+addPower) + "|cfff8d090(+" + str(minPower+addPower-addPowerOr-minPowerOr) + ")")

	def __MagicAttackInfo(self, origem_vnum, nextGradeItemVnum):
		item.SelectItem(nextGradeItemVnum)
		minPower = item.GetValue(1)
		maxPower = item.GetValue(2)
		addPower = item.GetValue(5)

		item.SelectItem(origem_vnum)
		minPowerOr = item.GetValue(1)
		maxPowerOr = item.GetValue(2)
		addPowerOr = item.GetValue(5)
		if minPower > 0 or maxPower > 0:
			if maxPower > minPower:
				return (str(minPower+addPower) + "|cfff8d090(+" + str(minPower+addPower-minPowerOr-addPowerOr) + ") - |cffa08784" + str(maxPower+addPower) + "|cfff8d090(+" + str(maxPower+addPower-maxPowerOr-addPowerOr) + ")")
			else:
				return (str(minPower+addPower) + "|cfff8d090(+" + str(minPower+addPower-addPowerOr-minPowerOr) + ")")

	def __MagicDefenceInfo(self, origem_vnum, nextGradeItemVnum):
		item.SelectItem(nextGradeItemVnum)
		magicDefencePower = item.GetValue(0)

		item.SelectItem(origem_vnum)
		magicDefencePowerOr = item.GetValue(0)

		if magicDefencePower > 0:
			return (str(magicDefencePower) + "|cfff8d090(+" + str(magicDefencePower-magicDefencePowerOr) + ")")
		return "0"

	def __AppendAffectInformation(self, origem_vnum, nextGradeItemVnum):
		for i in range(3):
			item.SelectItem(nextGradeItemVnum)
			(affectType, affectValue) = item.GetAffect(i)
			affectString = self.__GetAffectString(affectType, affectValue)

			item.SelectItem(origem_vnum)
			(affectTypeOr, affectValueOr) = item.GetAffect(i)
			affectStringOr = self.__GetAffectString(affectType, affectValue)

			if (affectType == affectTypeOr):
				self.GetChild("add"+str(i+3)+"_1").SetText(affectString)
				self.GetChild("add"+str(i+3)+"_2").SetText(str(affectValue) + "|cfff8d090(+" + str(affectValue - affectValueOr) + ")")
			else:
				self.GetChild("add"+str(i+3)+"_1").SetText(affectString)
				self.GetChild("add"+str(i+3)+"_2").SetText(str(affectValue) + "|cfff8d090  (Atributo Novo!)")

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return "Sem Atributo"

		if 0 == affectValue:
			return "Sem Atributo"

		try:
			return self.AFFECT_DICT[affectType]
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __LevelLimitInfo(self):
		for i in range(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)
			if item.LIMIT_LEVEL == limitType:
				return limitValue
		return 0

	def Close(self):
		if self.dlgQuestion:
			self.dlgQuestion.Close()

		self.dlgQuestion = None
		self.Hide()
		self.index = 1
		self.lockedItem = (-1, -1)
		self.SetCanMouseEventSlot(self.targetItemPos)

	def AppendMaterial(self, vnum, count):
		self.GetChild("slot_refine"+str(self.index)).Show()
		itemImage = self.__MakeItemImage()
		itemImage.SetParent(self.GetChild("slot_refine"+str(self.index)))
		item.SelectItem(vnum)
		itemImage.LoadImage(item.GetIconImageFileName())
		itemImage.SetWindowHorizontalAlignCenter()
		itemImage.SetWindowVerticalAlignCenter()

		textLine = self.GetChild("refine"+str(self.index))
		if player.GetItemCountByVnum(vnum) < count:
			self.GetChild("state"+str(self.index)).LoadImage("interface/controls/special/refine/f.tga")
		else:
			self.GetChild("state"+str(self.index)).LoadImage("interface/controls/special/refine/v.tga")
		textLine.SetText("%s x%d|h|r" % (item.GetItemName(), count))
		textLine.Show()

		self.index += 1

	def OpenQuestionDialog(self):
		if 100 == self.percentage:
			self.Accept()
			return

		if 5 == self.type:
			self.Accept()
			return

		dlgQuestion = uicommon.QuestionDialog2()
		dlgQuestion.SetText2(localeinfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(self.Accept)
		dlgQuestion.SetCancelEvent(dlgQuestion.Close)

		if 3 == self.type:
			dlgQuestion.SetText1(localeinfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeinfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_2)
		elif 2 == self.type:
			dlgQuestion.SetText1(localeinfo.REFINE_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeinfo.REFINE_DESTROY_WARNING)

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def __Expandir(self):
		self.expandir.Hide()
		self.retrair.Show()
		if self.board.GetWidth() < 620:
			self.board.SetSize(self.board.GetWidth()+10, self.board.GetHeight())
			self.retrair.SetPosition(self.board.GetWidth()-58, 8)
			self.expandir.SetPosition(self.board.GetWidth()-58, 8)
			self.GetChild("separator").SetWidth(self.board.GetWidth()-14)
			self.probText.SetWindowHorizontalAlignCenter()
			self.costText.SetWindowHorizontalAlignCenter()
			self.successPercentage.SetWindowHorizontalAlignCenter()
			self.GetChild("line").SetWindowHorizontalAlignCenter()
			self.GetChild("AcceptButton").SetWindowHorizontalAlignCenter()
			self.GetChild("CancelButton").SetWindowHorizontalAlignCenter()
			self.safe = wait.WaitingDialog()
			self.safe.Open(0.0)
			self.safe.SetTimeOverEvent(self.__Expandir)
		else:
			self.GetChild("Atributes").Show()
			self.SetSize(self.board.GetWidth(), self.board.GetHeight())

	def __Retrair(self):
		self.expandir.Show()
		self.retrair.Hide()
		self.GetChild("Atributes").Hide()
		if self.board.GetWidth() > 460:
			self.board.SetSize(self.board.GetWidth()-10, self.board.GetHeight())
			self.retrair.SetPosition(self.board.GetWidth()-58, 8)
			self.expandir.SetPosition(self.board.GetWidth()-58, 8)
			self.GetChild("separator").SetWidth(self.board.GetWidth()-14)
			self.probText.SetWindowHorizontalAlignCenter()
			self.costText.SetWindowHorizontalAlignCenter()
			self.successPercentage.SetWindowHorizontalAlignCenter()
			self.GetChild("line").SetWindowHorizontalAlignCenter()
			self.GetChild("AcceptButton").SetWindowHorizontalAlignCenter()
			self.GetChild("CancelButton").SetWindowHorizontalAlignCenter()
			self.safe = wait.WaitingDialog()
			self.safe.Open(0.0)
			self.safe.SetTimeOverEvent(self.__Retrair)
		else:
			self.SetSize(self.board.GetWidth(), self.board.GetHeight())

	def Accept(self):
		net.SendRefinePacket(self.targetItemPos, self.type)
		self.Close()

	def CancelRefine(self):
		net.SendRefinePacket(255, 255)
		self.Close()

	def OnPressEscapeKey(self):
		self.CancelRefine()
		return True

	def SetCanMouseEventSlot(self, slotIndex):
		itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
		localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
		self.lockedItem = (-1, -1)
		if self.wndInventory:
			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCanMouseEventSlot(localSlotPos)

	def SetCantMouseEventSlot(self, slotIndex):
		itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
		localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
		self.lockedItem = (itemInvenPage, localSlotPos)
		if self.wndInventory:
			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

	def SetInven(self, wndInventory):
		from _weakref import proxy
		self.wndInventory = proxy(wndInventory)

	def RefreshLockedSlot(self):
		if self.wndInventory:
			itemInvenPage, itemSlotPos = self.lockedItem
			if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
				self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)
			self.wndInventory.wndItem.RefreshSlot()

# x = RefineDialogNew()
# x.Open(200, 360, 10052, 50, 2)