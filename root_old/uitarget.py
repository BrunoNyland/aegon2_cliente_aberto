#favor manter essa linha
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import zn94xlgo573hf8xmddzq as net
import enszxc3467hc3kokdueq as app
import LURMxMaKZJqliYt2QSHG as chat
import ui
import wndMgr
import messenger
import guild
import Js4k2l7BrdasmVRt8Wem as chr
import nonplayer
import localeinfo
import constinfo
import background
import uicommon
import uitooltip

#ENABLE_SEND_TARGET_INFO
if app.ENABLE_SEND_TARGET_INFO:
	def HAS_FLAG(value, flag):
		return (value & flag) == flag
#FIM ENABLE_SEND_TARGET_INFO

class TargetBoard(ui.ThinBoard):
#ENABLE_SEND_TARGET_INFO
	if app.ENABLE_SEND_TARGET_INFO:
		class InfoBoard(ui.ThinBoard):
			class ItemListBoxItem(ui.ListBoxExNew.Item):
				def __init__(self, width):
					ui.ListBoxExNew.Item.__init__(self)

					image = ui.ExpandedImageBox()
					image.SetParent(self)
					image.Show()
					self.image = image

					nameLine = ui.TextLine()
					nameLine.SetParent(self)
					nameLine.SetPosition(32 + 5, 0)
					nameLine.Show()
					self.nameLine = nameLine

					self.SetSize(width, 32)

				def LoadImage(self, image, name = None):
					self.image.LoadImage(image)
					self.SetSize(self.GetWidth(), self.image.GetHeight() + 5 * (self.image.GetHeight() / 32))
					if name != None:
						self.SetText(name)

				def SetText(self, text):
					self.nameLine.SetText(text)

				def RefreshHeight(self):
					ui.ListBoxExNew.Item.RefreshHeight(self)
					self.image.SetRenderingRect(0.0, 0.0 - float(self.removeTop) / float(self.GetHeight()), 0.0, 0.0 - float(self.removeBottom) / float(self.GetHeight()))
					self.image.SetPosition(0, - self.removeTop)

			MAX_ITEM_COUNT = 5

			EXP_BASE_LVDELTA = [
				1,  #  -15 0
				5,  #  -14 1
				10, #  -13 2
				20, #  -12 3
				30, #  -11 4
				50, #  -10 5
				70, #  -9  6
				80, #  -8  7
				85, #  -7  8
				90, #  -6  9
				92, #  -5  10
				94, #  -4  11
				96, #  -3  12
				98, #  -2  13
				100,	#  -1  14
				100,	#  0   15
				105,	#  1   16
				110,	#  2   17
				115,	#  3   18
				120,	#  4   19
				125,	#  5   20
				130,	#  6   21
				135,	#  7   22
				140,	#  8   23
				145,	#  9   24
				150,	#  10  25
				155,	#  11  26
				160,	#  12  27
				165,	#  13  28
				170,	#  14  29
				180,	#  15  30
			]

			RACE_FLAG_TO_NAME = {
				1 << 0  : localeinfo.TARGET_INFO_RACE_ANIMAL,
				1 << 1 	: localeinfo.TARGET_INFO_RACE_UNDEAD,
				1 << 2  : localeinfo.TARGET_INFO_RACE_DEVIL,
				1 << 3  : localeinfo.TARGET_INFO_RACE_HUMAN,
				1 << 4  : localeinfo.TARGET_INFO_RACE_ORC,
				1 << 5  : localeinfo.TARGET_INFO_RACE_MILGYO,
			}

			SUB_RACE_FLAG_TO_NAME = {
				1 << 11 : localeinfo.TARGET_INFO_RACE_ELEC,
				1 << 12 : localeinfo.TARGET_INFO_RACE_FIRE,
				1 << 13 : localeinfo.TARGET_INFO_RACE_ICE,
				1 << 14 : localeinfo.TARGET_INFO_RACE_WIND,
				1 << 15 : localeinfo.TARGET_INFO_RACE_EARTH,
				1 << 16 : localeinfo.TARGET_INFO_RACE_DARK,
			}

			STONE_START_VNUM = 28030
			STONE_LAST_VNUM = 28042

			BOARD_WIDTH = 250

			def __init__(self):
				ui.ThinBoard.__init__(self)

				self.HideCorners(self.LT)
				self.HideCorners(self.RT)
				self.HideLine(self.T)

				#Aviso de pedido de expressao
				self.targetName = ""
				#Fianl Aviso de pedido de expressao

				self.race = 0
				self.hasItems = False

				self.itemTooltip = uitooltip.ItemToolTip()
				self.itemTooltip.HideToolTip()

				self.stoneImg = None
				self.stoneVnum = None
				self.lastStoneVnum = 0
				self.nextStoneIconChange = 0

				self.SetSize(self.BOARD_WIDTH, 0)

			def __del__(self):
				ui.ThinBoard.__del__(self)

			def __UpdatePosition(self, targetBoard):
				self.SetPosition(targetBoard.GetLeft() + (targetBoard.GetWidth() - self.GetWidth()) / 2, targetBoard.GetBottom() - 17)

			def Open(self, targetBoard, race):
				self.__LoadInformation(race)

				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)
				self.__UpdatePosition(targetBoard)

				self.Show()

			def Refresh(self):
				self.__LoadInformation(self.race)
				self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

			def Close(self):
				self.itemTooltip.HideToolTip()
				self.Hide()

			def __LoadInformation(self, race):
				self.yPos = 7
				self.children = []
				self.race = race
				self.stoneImg = None
				self.stoneVnum = None
				self.nextStoneIconChange = 0

				self.__LoadInformation_Default(race)
				self.__LoadInformation_Race(race)
				self.__LoadInformation_Drops(race)

			def __LoadInformation_Default_GetHitRate(self, race):
				attacker_dx = nonplayer.GetMonsterDX(race)
				attacker_level = nonplayer.GetMonsterLevel(race)

				self_dx = player.GetStatus(player.DX)
				self_level = player.GetStatus(player.LEVEL)

				iARSrc = min(90, (attacker_dx * 4 + attacker_level * 2) / 6)
				iERSrc = min(90, (self_dx * 4 + self_level * 2) / 6)

				fAR = (float(iARSrc) + 210.0) / 300.0
				fER = (float(iERSrc) * 2 + 5) / (float(iERSrc) + 95) * 3.0 / 10.0

				return fAR - fER

			def __LoadInformation_Default(self, race):
				self.AppendSeperator()
				self.AppendTextLine(localeinfo.TARGET_INFO_MAX_HP % str(nonplayer.GetMonsterMaxHP(race)))

				monsterLevel = nonplayer.GetMonsterLevel(race)
				fHitRate = self.__LoadInformation_Default_GetHitRate(race)
				iDamMin, iDamMax = nonplayer.GetMonsterDamage(race)
				iDamMin = int((iDamMin + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDamMax = int((iDamMax + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
				iDef = player.GetStatus(player.DEF_GRADE) * (100 + player.GetStatus(player.DEF_BONUS)) / 100
				fDamMulti = nonplayer.GetMonsterDamageMultiply(race)
				iDamMin = int(max(0, iDamMin) * fDamMulti)
				iDamMax = int(max(0, iDamMax) * fDamMulti)
				if iDamMin < 1:
					iDamMin = 1
				if iDamMax < 5:
					iDamMax = 5
				self.AppendTextLine(localeinfo.TARGET_INFO_DAMAGE % (str(iDamMin), str(iDamMax)))

				idx = min(len(self.EXP_BASE_LVDELTA) - 1, max(0, (monsterLevel + 15) - player.GetStatus(player.LEVEL)))
				iExp = nonplayer.GetMonsterExp(race) * self.EXP_BASE_LVDELTA[idx] / 100
				self.AppendTextLine(localeinfo.TARGET_INFO_EXP % str(iExp))

			def __LoadInformation_Race(self, race):
				dwRaceFlag = nonplayer.GetMonsterRaceFlag(race)
				self.AppendSeperator()

				mainrace = ""
				subrace = ""
				for i in xrange(17):
					curFlag = 1 << i
					if HAS_FLAG(dwRaceFlag, curFlag):
						if self.RACE_FLAG_TO_NAME.has_key(curFlag):
							mainrace += self.RACE_FLAG_TO_NAME[curFlag] + ", "
						elif self.SUB_RACE_FLAG_TO_NAME.has_key(curFlag):
							subrace += self.SUB_RACE_FLAG_TO_NAME[curFlag] + ", "
				if nonplayer.IsMonsterStone(race):
					mainrace += localeinfo.TARGET_INFO_RACE_METIN + ", "
				if mainrace == "":
					mainrace = localeinfo.TARGET_INFO_NO_RACE
				else:
					mainrace = mainrace[:-2]
				if subrace == "":
					subrace = localeinfo.TARGET_INFO_NO_RACE
				else:
					subrace = subrace[:-2]

				self.AppendTextLine(localeinfo.TARGET_INFO_MAINRACE % mainrace)
				self.AppendTextLine(localeinfo.TARGET_INFO_SUBRACE % subrace)

			def __LoadInformation_Drops(self, race):
				self.AppendSeperator()

				if race in constinfo.MONSTER_INFO_DATA:
					if len(constinfo.MONSTER_INFO_DATA[race]["items"]) == 0:
						self.AppendTextLine(localeinfo.TARGET_INFO_NO_ITEM_TEXT)
					else:
						itemListBox = ui.ListBoxExNew(32 + 5, self.MAX_ITEM_COUNT)
						itemListBox.SetSize(self.GetWidth() - 15 * 2 - ui.ScrollBar.SCROLLBAR_WIDTH, (32 + 5) * self.MAX_ITEM_COUNT)
						height = 0
						for curItem in constinfo.MONSTER_INFO_DATA[race]["items"]:
							if curItem.has_key("vnum_list"):
								height += self.AppendItem(itemListBox, curItem["vnum_list"], curItem["count"])
							else:
								height += self.AppendItem(itemListBox, curItem["vnum"], curItem["count"])
						if height < itemListBox.GetHeight():
							itemListBox.SetSize(itemListBox.GetWidth(), height)
						self.AppendWindow(itemListBox, 15)
						itemListBox.SetBasePos(0)

						if len(constinfo.MONSTER_INFO_DATA[race]["items"]) > itemListBox.GetViewItemCount():
							itemScrollBar = ui.New_ScrollBar()
							itemScrollBar.SetParent(self)
							itemScrollBar.SetPosition(itemListBox.GetRight(), itemListBox.GetTop())
							itemScrollBar.SetScrollBarSize(32 * self.MAX_ITEM_COUNT + 5 * (self.MAX_ITEM_COUNT - 1))
							itemScrollBar.SetMiddleBarSize(float(self.MAX_ITEM_COUNT) / float(height / (32 + 5)))
							itemScrollBar.Show()
							itemListBox.SetScrollBar(itemScrollBar)
				else:
					self.AppendTextLine(localeinfo.TARGET_INFO_NO_ITEM_TEXT)

			def AppendTextLine(self, text):
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetWindowHorizontalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.SetText(text)
				textLine.SetPosition(0, self.yPos)
				textLine.Show()

				self.children.append(textLine)
				self.yPos += 17

			def AppendSeperator(self):
				img = ui.ImageBox()
				img.LoadImage("interface/controls/common/horizontal_bar/center.tga")
				self.AppendWindow(img)
				img.SetPosition(img.GetLeft(), img.GetTop() - 15)
				self.yPos -= 15

			def AppendItem(self, listBox, vnums, count):
				if type(vnums) == int:
					vnum = vnums
				else:
					vnum = vnums[0]

				item.SelectItem(vnum)
				itemName = item.GetItemName()
				if type(vnums) != int and len(vnums) > 1:
					vnums = sorted(vnums)
					realName = itemName[:itemName.find("+")]
					if item.GetItemType() == item.ITEM_TYPE_METIN:
						realName = localeinfo.TARGET_INFO_STONE_NAME
						itemName = realName + "+0 - +4"
					else:
						itemName = realName + "+" + str(vnums[0] % 10) + " - +" + str(vnums[len(vnums) - 1] % 10)
					vnum = vnums[len(vnums) - 1]

				myItem = self.ItemListBoxItem(listBox.GetWidth())
				myItem.LoadImage(item.GetIconImageFileName())
				if count <= 1:
					myItem.SetText(itemName)
				else:
					myItem.SetText("%dx %s" % (count, itemName))
				myItem.SAFE_SetOverInEvent(self.OnShowItemTooltip, vnum)
				myItem.SAFE_SetOverOutEvent(self.OnHideItemTooltip)
				listBox.AppendItem(myItem)

				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.stoneImg = myItem
					self.stoneVnum = vnums
					self.lastStoneVnum = self.STONE_LAST_VNUM + vnums[len(vnums) - 1] % 1000 / 100 * 100

				return myItem.GetHeight()

			def OnShowItemTooltip(self, vnum):
				item.SelectItem(vnum)
				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.itemTooltip.isStone = True
					self.itemTooltip.isBook = False
					self.itemTooltip.isBook2 = False
					self.itemTooltip.SetItemToolTip(self.lastStoneVnum)
				else:
					self.itemTooltip.isStone = False
					self.itemTooltip.isBook = True
					self.itemTooltip.isBook2 = True
					self.itemTooltip.SetItemToolTip(vnum)

			def OnHideItemTooltip(self):
				self.itemTooltip.HideToolTip()

			def AppendWindow(self, wnd, x = 0, width = 0, height = 0):
				if width == 0:
					width = wnd.GetWidth()
				if height == 0:
					height = wnd.GetHeight()

				wnd.SetParent(self)
				if x == 0:
					wnd.SetPosition((self.GetWidth() - width) / 2, self.yPos)
				else:
					wnd.SetPosition(x, self.yPos)
				wnd.Show()

				self.children.append(wnd)
				self.yPos += height + 5

			def OnUpdate(self):
				if self.stoneImg != None and self.stoneVnum != None and app.GetTime() >= self.nextStoneIconChange:
					nextImg = self.lastStoneVnum + 1
					if nextImg % 100 > self.STONE_LAST_VNUM % 100:
						nextImg -= (self.STONE_LAST_VNUM - self.STONE_START_VNUM) + 1
					self.lastStoneVnum = nextImg
					self.nextStoneIconChange = app.GetTime() + 2.5

					item.SelectItem(nextImg)
					itemName = item.GetItemName()
					realName = itemName[:itemName.find("+")]
					realName = realName + "+0 - +4"
					self.stoneImg.LoadImage(item.GetIconImageFileName(), realName)

					if self.itemTooltip.IsShow() and self.itemTooltip.isStone:
						self.itemTooltip.SetItemToolTip(nextImg)
## FIM ENABLE_SEND_TARGET_INFO

	BUTTON_NAME_LIST = [
		localeinfo.TARGET_BUTTON_WHISPER,
		localeinfo.TARGET_BUTTON_EXCHANGE,
		localeinfo.TARGET_BUTTON_FIGHT,
		localeinfo.TARGET_BUTTON_ACCEPT_FIGHT,
		localeinfo.TARGET_BUTTON_AVENGE,
		localeinfo.TARGET_BUTTON_FRIEND,
		localeinfo.TARGET_BUTTON_INVITE_PARTY,
		localeinfo.TARGET_BUTTON_LEAVE_PARTY,
		localeinfo.TARGET_BUTTON_EXCLUDE,
		localeinfo.TARGET_BUTTON_INVITE_GUILD,
		localeinfo.TARGET_BUTTON_DISMOUNT,
		localeinfo.TARGET_BUTTON_EXIT_OBSERVER,
		localeinfo.TARGET_BUTTON_VIEW_EQUIPMENT,
		localeinfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
		localeinfo.TARGET_BUTTON_EMOTION_ALLOW,
	]

	if app.ENABLE_INVENTORY_VIEWER:
		BUTTON_NAME_LIST.append(localeinfo.TARGET_BUTTON_INVENTORY_VIEW)

	GRADE_NAME = {
		nonplayer.PAWN : localeinfo.TARGET_LEVEL_PAWN,
		nonplayer.S_PAWN : localeinfo.TARGET_LEVEL_S_PAWN,
		nonplayer.KNIGHT : localeinfo.TARGET_LEVEL_KNIGHT,
		nonplayer.S_KNIGHT : localeinfo.TARGET_LEVEL_S_KNIGHT,
		nonplayer.BOSS : localeinfo.TARGET_LEVEL_BOSS,
		nonplayer.KING : localeinfo.TARGET_LEVEL_KING,
	}
	EXCHANGE_LIMIT_RANGE = 3000

	def __init__(self):
		ui.ThinBoard.__init__(self)

		hpGauge = ui.Gauge()
		hpGauge.SetParent(self)
		hpGauge.MakeGauge(130, "red")
		hpGauge.Hide()

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("interface/controls/common/board/close_normal.tga")
		closeButton.SetOverVisual("interface/controls/common/board/close_over.tga")
		closeButton.SetDownVisual("interface/controls/common/board/close_down.tga")
		closeButton.SetPosition(33, 0)
		closeButton.SetWindowVerticalAlignCenter()
		closeButton.SetWindowHorizontalAlignRight()

		if app.ENABLE_SEND_TARGET_INFO:
			infoButton = ui.Button()
			infoButton.SetParent(self)
			infoButton.SetUpVisual("interface/controls/special/targetinfo/q_mark_01.tga")
			infoButton.SetOverVisual("interface/controls/special/targetinfo/q_mark_02.tga")
			infoButton.SetDownVisual("interface/controls/special/targetinfo/q_mark_01.tga")
			infoButton.SetEvent(self.OnPressedInfoButton)
			infoButton.Hide()
			infoBoard = self.InfoBoard()
			infoBoard.Hide()
			infoButton.showWnd = infoBoard

		hpGauge.SetPosition(175, 17)
		hpGauge.SetWindowHorizontalAlignRight()

		closeButton.SetEvent(self.OnPressedCloseButton)
		closeButton.Show()

		self.buttonDict = {}
		self.showingButtonList = []

		for buttonName in self.BUTTON_NAME_LIST:
			button = ui.RedButton()
			button.SetParent(self)
			button.SetWidth(75)
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeinfo.TARGET_BUTTON_WHISPER].SetEvent(self.OnWhisper)
		self.buttonDict[localeinfo.TARGET_BUTTON_EXCHANGE].SetEvent(self.OnExchange)
		self.buttonDict[localeinfo.TARGET_BUTTON_FIGHT].SetEvent(self.OnPVP)
		self.buttonDict[localeinfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(self.OnPVP)
		self.buttonDict[localeinfo.TARGET_BUTTON_AVENGE].SetEvent(self.OnPVP)
		self.buttonDict[localeinfo.TARGET_BUTTON_FRIEND].SetEvent(self.OnAppendToMessenger)
		self.buttonDict[localeinfo.TARGET_BUTTON_FRIEND].SetEvent(self.OnAppendToMessenger)
		self.buttonDict[localeinfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(self.OnPartyInvite)
		self.buttonDict[localeinfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(self.OnPartyExit)
		self.buttonDict[localeinfo.TARGET_BUTTON_EXCLUDE].SetEvent(self.OnPartyRemove)

		self.buttonDict[localeinfo.TARGET_BUTTON_INVITE_GUILD].SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeinfo.TARGET_BUTTON_DISMOUNT].SetEvent(self.__OnDismount)
		self.buttonDict[localeinfo.TARGET_BUTTON_EXIT_OBSERVER].SetEvent(self.__OnExitObserver)
		self.buttonDict[localeinfo.TARGET_BUTTON_VIEW_EQUIPMENT].SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeinfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SetEvent(self.__OnRequestParty)
		self.buttonDict[localeinfo.TARGET_BUTTON_EMOTION_ALLOW].SetEvent(self.__OnEmotionAllow)

		if app.ENABLE_INVENTORY_VIEWER:
			self.buttonDict[localeinfo.TARGET_BUTTON_INVENTORY_VIEW].SetEvent(self.__OnRequestInventory)

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetFontColor(1.0, 1.0, 1.0)
		name.SetOutline()
		name.Show()
		self.name = name

		nameBoard = ui.ImageBox()
		nameBoard.SetParent(self)
		nameBoard.LoadImage("interface/controls/special/target/bg_name.tga")
		nameBoard.SetPosition(0, 5)
		nameBoard.SetWindowHorizontalAlignCenter()
		nameBoard.SetWindowVerticalAlignBottom()
		nameBoard.Show()
		self.nameBoard = nameBoard

		nameBoardText = ui.TextLine()
		nameBoardText.SetParent(self.nameBoard)
		nameBoardText.SetPosition(0, 3)
		nameBoardText.SetFontName(localeinfo.UI_DEF_FONT_LARGE)
		nameBoardText.SetFontColor(1.0, 1.0, 1.0)
		nameBoardText.SetWindowHorizontalAlignCenter()
		nameBoardText.SetHorizontalAlignCenter()
		nameBoardText.Show()
		self.nameBoardText = nameBoardText
		self.hpGauge = hpGauge

		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = infoButton
			self.vnum = 0

		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		self.eventWhisper = None
		self.isShowButton = False

		self.__Initialize()
		self.ResetTargetBoard()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0
		self.isShowButton = False

	def Destroy(self):
		self.Hide()
		self.eventWhisper = None
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = None
		self.closeButton = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		self.nameBoard = None
		self.nameBoardText = None
		self.hpGauge = None

	if app.ENABLE_SEND_TARGET_INFO:
		def RefreshMonsterInfoBoard(self):
			if not self.infoButton.showWnd.IsShow():
				return

			self.infoButton.showWnd.Refresh()

		def OnPressedInfoButton(self):
			net.SendTargetInfoLoad(player.GetTargetVID())
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Close()
			elif self.vnum != 0:
				self.infoButton.showWnd.Open(self, self.vnum)

	def OnPressedCloseButton(self):
		player.ClearTarget()
		self.Close()

	def Close(self):
		self.__Initialize()
		self.Hide()
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.showWnd.Close()

	def Open(self, vid, name):
		if vid:
			if not constinfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not player.IsSameEmpire(vid):
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)

			if player.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			self.__ShowButton(localeinfo.TARGET_BUTTON_WHISPER)
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()

	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():
				self.RefreshButton()

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():
			self.Refresh()

	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __ShowMainCharacterMenu(self):
		canShow = 0

		self.HideAllButton()

		if player.IsMountingHorse():
			self.__ShowButton(localeinfo.TARGET_BUTTON_DISMOUNT)
			canShow = 1

		if player.IsObserverMode():
			self.__ShowButton(localeinfo.TARGET_BUTTON_EXIT_OBSERVER)
			canShow = 1

		if canShow:
			self.__ArrangeButtonPosition()
			self.Show()
		else:
			self.Hide()

	def __ShowNameOnlyMenu(self):
		self.HideAllButton()

	def SetWhisperEvent(self, event):
		self.eventWhisper = ui.__mem_func__(event)

	def UpdatePosition(self):
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, 22)

	def ResetTargetBoard(self):
		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()
		self.name.SetParent(self)
		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()
		self.hpGauge.Hide()
		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.Hide()
			self.infoButton.showWnd.Close()
		self.SetSize(250, 38)

	def SetTargetVID(self, vid):
		self.vid = vid
		if app.ENABLE_SEND_TARGET_INFO:
			self.vnum = 0

	def SetEnemyVID(self, vid):
		self.SetTargetVID(vid)
		if app.ENABLE_SEND_TARGET_INFO:
			vnum = nonplayer.GetRaceNumByVID(vid)
		name = chr.GetNameByVID(vid)
		level = nonplayer.GetLevelByVID(vid)
		grade = nonplayer.GetGradeByVID(vid)

		nameFront = ""
		if -1 != level:
			nameFront += "Lv." + str(level) + " "
		if self.GRADE_NAME.has_key(grade):
			nameFront += "(" + self.GRADE_NAME[grade] + ") "

		self.SetTargetName(nameFront + name)

		if app.ENABLE_SEND_TARGET_INFO:
			(textWidth, textHeight) = self.name.GetTextSize()

			self.infoButton.SetPosition(textWidth + 25, 12)
			self.infoButton.SetWindowHorizontalAlignLeft()

			self.vnum = vnum
			self.infoButton.Show()

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)
		self.name.SetText(name)
		self.nameBoardText.SetText(name)

	def SetHP(self, hpPercentage):
		if not self.hpGauge.IsShow():

			self.SetSize(200 + 7*self.nameLength, self.GetHeight())
			self.name.SetPosition(23, 13)
			self.name.Show()
			self.nameBoard.Hide()
			self.name.SetWindowHorizontalAlignLeft()
			self.name.SetHorizontalAlignLeft()
			self.hpGauge.Show()
			self.UpdatePosition()

		self.hpGauge.SetPercentage(hpPercentage, 100)

	def ShowDefaultButton(self):
		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeinfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeinfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeinfo.TARGET_BUTTON_VIEW_EQUIPMENT])
		self.showingButtonList.append(self.buttonDict[localeinfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeinfo.TARGET_BUTTON_EMOTION_ALLOW])
		for button in self.showingButtonList:
			button.Show()

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []
		self.name.Show()
		self.nameBoard.Hide()

	def __ShowButton(self, name):
		if not self.buttonDict.has_key(name):
			return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):
		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		net.SendExchangeStartPacket(self.vid)


	def OnPVP(self):
		net.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		net.SendMessengerAddByVIDPacket(self.vid)

	def OnPartyInvite(self):
		net.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		net.SendPartyExitPacket()

	def OnPartyRemove(self):
		net.SendPartyRemovePacket(self.vid, 1)

	def __OnGuildAddMember(self):
		net.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		net.SendChatPacket("/unmount")

	def __OnExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		net.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		net.SendChatPacket("/party_request " + str(self.vid))

	def __OnEmotionAllow(self):
		net.SendChatPacket("/emotion_allow %d" % (self.vid))
		net.SendWhisperPacket((self.nameString), player.GetName() + " aceita ter emoções com você.")

	if app.ENABLE_INVENTORY_VIEWER:
		def __OnRequestInventory(self):
			net.SendRequestInventory(self.vid)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):
		self.HideAllButton()

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			return

		if player.IsPVPInstance(self.vid) or player.IsObserverMode():
			self.SetSize(200 + 7*self.nameLength, 38)
			self.UpdatePosition()
			return

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeinfo.TARGET_BUTTON_INVITE_GUILD)

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeinfo.TARGET_BUTTON_FRIEND)

		if player.IsPartyMember(self.vid):
			self.__HideButton(localeinfo.TARGET_BUTTON_FIGHT)

			if player.IsPartyLeader(self.vid):
				self.__ShowButton(localeinfo.TARGET_BUTTON_LEAVE_PARTY)
			elif player.IsPartyLeader(player.GetMainCharacterIndex()):
				self.__ShowButton(localeinfo.TARGET_BUTTON_EXCLUDE)
		else:
			if player.IsPartyMember(player.GetMainCharacterIndex()):
				if player.IsPartyLeader(player.GetMainCharacterIndex()):
					self.__ShowButton(localeinfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeinfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeinfo.TARGET_BUTTON_INVITE_PARTY)

			if player.IsRevengeInstance(self.vid):
				self.__HideButton(localeinfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeinfo.TARGET_BUTTON_AVENGE)
			elif player.IsChallengeInstance(self.vid):
				self.__HideButton(localeinfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeinfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif player.IsCantFightInstance(self.vid):
				self.__HideButton(localeinfo.TARGET_BUTTON_FIGHT)

			if not player.IsSameEmpire(self.vid):
				self.__HideButton(localeinfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeinfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeinfo.TARGET_BUTTON_FIGHT)

			if app.ENABLE_INVENTORY_VIEWER:
				if "[" in player.GetName():
					self.__ShowButton(localeinfo.TARGET_BUTTON_INVENTORY_VIEW)
				else:
					self.__HideButton(localeinfo.TARGET_BUTTON_INVENTORY_VIEW)

		distance = player.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeinfo.TARGET_BUTTON_EXCHANGE)
			self.__HideButton(localeinfo.TARGET_BUTTON_VIEW_EQUIPMENT)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self):
		showingButtonCount = len(self.showingButtonList)

		pos = 7
		for button in self.showingButtonList:
			button.SetPosition(pos, 0)
			button.SetWindowVerticalAlignCenter()
			pos += 75

		self.SetSize(max(150, showingButtonCount * 75) +40, 38)
		self.name.Hide()
		self.nameBoard.Show()
		self.UpdatePosition()

	def OnUpdate(self):
		if self.isShowButton:
			exchangeButton = self.buttonDict[localeinfo.TARGET_BUTTON_EXCHANGE]
			distance = player.GetCharacterDistance(self.vid)

			if distance < 0:
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()
			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

class Component:
	def TextLine(self, parent, textlineText, x, y, color):
		textline = ui.TextLine()
		if parent != None:
			textline.SetParent(parent)
		textline.SetPosition(x, y)
		if color != None:
			textline.SetFontColor(color[0], color[1], color[2])
		textline.SetText(textlineText)
		textline.Show()
		return textline

	def RGB(self, r, g, b):
		return (r*255, g*255, b*255)

	def ExpandedImage(self, parent, x, y, img):
		image = ui.ExpandedImageBox()
		if parent != None:
			image.SetParent(parent)
		image.SetPosition(x, y)
		image.LoadImage(img)
		image.Show()
		return image