#favor manter essa linha
import _player as player
import _trade as exchange
import _net as net
import _chat as chat
import _item as item
import _wnd_mgr as wndMgr
import _snd as snd
import _app as app
import localeinfo
import constinfo
import mousemodule
import ui
import uipickmoney
import uicommon
import playersettingmodule

from weakref import proxy

class ExchangeDialog(ui.ScriptWindow):

	faces = "interface/icons/faces/medium/icon_"
	faces_on = "interface/icons/faces/medium/on/icon_"
	FACE_IMAGE_DICT = {
		playersettingmodule.RACE_WARRIOR_M		:	"mwarrior.tga",
		playersettingmodule.RACE_WARRIOR_W		:	"wwarrior.tga",
		playersettingmodule.RACE_ASSASSIN_M		:	"mninja.tga",
		playersettingmodule.RACE_ASSASSIN_W		:	"wninja.tga",
		playersettingmodule.RACE_SURA_M			:	"msura.tga",
		playersettingmodule.RACE_SURA_W			:	"wsura.tga",
		playersettingmodule.RACE_SHAMAN_M		:	"mshaman.tga",
		playersettingmodule.RACE_SHAMAN_W		:	"wshaman.tga",
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.xStart = 0
		self.yStart = 0
		self.interface = 0
		self.wndInventory = 0
		self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "uiscript/exchangedialog.py")
		self.board = self.GetChild("board")
		self.board.SetCloseEvent(self.Close)
		self.OwnerSlot = self.GetChild("Owner_Slot")
		self.OwnerSlot.SetSelectEmptySlotEvent(self.SelectOwnerEmptySlot)
		self.OwnerSlot.SetSelectItemSlotEvent(self.SelectOwnerItemSlot)
		self.OwnerSlot.SetOverInItemEvent(self.OverInOwnerItem)
		self.OwnerSlot.SetOverOutItemEvent(self.OverOutItem)
		self.OwnerMoney = self.GetChild("Owner_Money_Value")
		self.OwnerAcceptLight = self.GetChild("Owner_Accept_Light")
		self.OwnerAcceptLight.Disable()
		self.OwnerMoneyButton = self.GetChild("Owner_Money")
		self.OwnerMoneyButton.SetEvent(self.OpenPickMoneyDialog)
		self.TargetSlot = self.GetChild("Target_Slot")
		self.TargetSlot.SetOverInItemEvent(self.OverInTargetItem)
		self.TargetSlot.SetOverOutItemEvent(self.OverOutItem)
		self.TargetMoney = self.GetChild("Target_Money_Value")
		self.TargetAcceptLight = self.GetChild("Target_Accept_Light")
		self.TargetAcceptLight.Disable()

		dlgPickMoney = uipickmoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(self.OnPickMoney)
		dlgPickMoney.SetTitleName(localeinfo.EXCHANGE_MONEY)

		dlgPickMoney.SetMax(13)
		dlgPickMoney.Hide()
		self.dlgPickMoney = dlgPickMoney
		self.GetChild("Owner_Decline_Button").SetEvent(self.Close)
		self.AcceptButton = self.GetChild("Owner_Accept_Button")
		self.AcceptButton.SetEvent(self.AcceptExchange)

		characterName = player.GetName()
		guildName = player.GetGuildName()
		race = net.GetMainActorRace()
		empire = net.GetMainActorEmpire()
		try:
			self.GetChild("owner_face").SetUpVisual(self.faces + self.FACE_IMAGE_DICT[race])
			self.GetChild("owner_face").SetOverVisual(self.faces_on + self.FACE_IMAGE_DICT[race])
			self.GetChild("owner_face").SetDownVisual(self.faces_on + self.FACE_IMAGE_DICT[race])
			self.GetChild("owner_face").SetEvent(self.interface.ToggleInventoryWindow)
		except BaseException:
			pass

		if characterName == "":
			self.GetChild("owner_name").SetText("Nome: |cfff88f90"+"Sem Nome")
		else:
			self.GetChild("owner_name").SetText("Nome: |cfff88f90"+characterName)
		if guildName == "":
			self.GetChild("owner_guild").SetText("Guild: |cfff88f90"+"Sem Guild")
		else:
			self.GetChild("owner_guild").SetText("Guild: |cfff88f90"+guildName)
		self.GetChild("owner_lvl").SetText("Level: |cfff88f90"+str(player.GetStatus(player.LEVEL)))

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0
		self.OwnerSlot = 0
		self.OwnerMoney = 0
		self.OwnerAcceptLight = 0
		self.OwnerMoneyButton = 0
		self.TargetSlot = 0
		self.TargetMoney = 0
		self.TargetAcceptLight = 0
		self.AcceptButton = 0
		self.tooltipItem = 0
		self.interface = 0
		self.wndInventory = 0
		self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}

	def OpenDialog(self, level, race, guild):
		self.board.SetTitleName(localeinfo.EXCHANGE_TITLE % (exchange.GetNameFromTarget()))

		try:
			self.GetChild("target_face").SetUpVisual(self.faces + self.FACE_IMAGE_DICT[race])
			self.GetChild("target_face").SetOverVisual(self.faces_on + self.FACE_IMAGE_DICT[race])
			self.GetChild("target_face").SetDownVisual(self.faces_on + self.FACE_IMAGE_DICT[race])
		except BaseException:
			pass

		self.GetChild("target_face").SetEvent(self.interface.OpenWhisperDialog, str(exchange.GetNameFromTarget()))
		self.GetChild("target_name").SetText("Nome: |cfff88f90"+exchange.GetNameFromTarget())
		self.GetChild("target_guild").SetText("Guild: |cfff88f90"+guild)
		self.GetChild("target_lvl").SetText("Level: |cfff88f90"+str(level))

		self.AcceptButton.Enable()
		self.Show()
		self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
		self.interface.RefreshMarkInventoryBag()
		(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()

	def CloseDialog(self):
		wndMgr.OnceIgnoreMouseLeftButtonUpEvent()

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.dlgPickMoney.Close()

		self.Hide()
		for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems = {i:(-1,-1) for i in range(exchange.EXCHANGE_ITEM_MAX_NUM)}
			self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
			self.interface.RefreshMarkInventoryBag()

	def Close(self):
		self.Hide()
		net.SendExchangeExitPacket()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def OpenPickMoneyDialog(self):
		if exchange.GetElkFromSelf() > 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.EXCHANGE_CANT_EDIT_MONEY)
			return
		self.dlgPickMoney.Open(player.GetElk())

	def OnPickMoney(self, money):
		net.SendExchangeElkAddPacket(money)

	def AcceptExchange(self):
		questionDialog = uicommon.QuestionDialog3()
		questionDialog.SetText1("|cffa07970" +localeinfo.ACCEPTA_BUTON1)
		questionDialog.SetText2("|cffa07970" +localeinfo.ACCEPTA_BUTON2)
		questionDialog.SetText3("|cffa07970" +localeinfo.ACCEPTA_BUTON3)
		questionDialog.SetAcceptEvent(self.AcceptaNou)
		questionDialog.SetCancelEvent(self.RefuzaNou)
		questionDialog.Open()
		self.questionDialog = questionDialog

	def AcceptaNou(self):
		self.questionDialog.Close()
		net.SendExchangeAcceptPacket()
		self.AcceptButton.Disable()
		snd.PlaySound('sound/effect/etc/levelup_2/levelup1_2.wav')

	def RefuzaNou(self):
		self.questionDialog.Close()

	def SelectOwnerEmptySlot(self, SlotIndex):
		if not mousemodule.mouseController.isAttached():
			return

		if mousemodule.mouseController.IsAttachedMoney():
			net.SendExchangeElkAddPacket(mousemodule.mouseController.GetAttachedMoneyAmount())
		else:
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			if (player.SLOT_TYPE_INVENTORY == attachedSlotType):
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				SrcSlotNumber = mousemodule.mouseController.GetAttachedSlotNumber()
				DstSlotNumber = SlotIndex
				itemID = player.GetItemIndex(attachedInvenType, SrcSlotNumber)
				item.SelectItem(itemID)
				if item.IsAntiFlag(item.ANTIFLAG_GIVE):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.EXCHANGE_CANNOT_GIVE)
					mousemodule.mouseController.DeattachObject()
					return

				if app.ALUGAR_ITENS and (app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT)):
					self.interface.RentTimeDialog.Open(attachedInvenType, SrcSlotNumber, DstSlotNumber)
				else:
					self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
					net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)

		mousemodule.mouseController.DeattachObject()

	def SelectOwnerItemSlot(self, SlotIndex):
		if not mousemodule.mouseController.isAttached():
			net.SendExchangeItemDelPacket(SlotIndex)
			return

		if player.ITEM_MONEY == mousemodule.mouseController.GetAttachedItemIndex():
			money = mousemodule.mouseController.GetAttachedItemCount()
			net.SendExchangeElkAddPacket(money)

		mousemodule.mouseController.DeattachObject()

	def RefreshOwnerSlot(self):
		for i in range(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			itemCount = exchange.GetItemCountFromSelf(i)
			if itemCount == 1:
				itemCount = 0
			self.OwnerSlot.SetItemSlot(i, itemIndex, itemCount)
		self.OwnerSlot.RefreshSlot()

	def RefreshTargetSlot(self):
		for i in range(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			itemCount = exchange.GetItemCountFromTarget(i)
			if itemCount == 1:
				itemCount = 0
			self.TargetSlot.SetItemSlot(i, itemIndex, itemCount)
		self.TargetSlot.RefreshSlot()

	def Refresh(self):
		self.RefreshOwnerSlot()
		self.RefreshTargetSlot()
		self.RefreshLockedSlot()
		self.OwnerMoney.SetText(str(exchange.GetElkFromSelf()))
		self.TargetMoney.SetText(str(exchange.GetElkFromTarget()))
		if exchange.GetAcceptFromSelf():
			self.OwnerAcceptLight.Down()
		else:
			self.AcceptButton.Enable()
			self.OwnerAcceptLight.SetUp()

		if  exchange.GetAcceptFromTarget():
			self.TargetAcceptLight.Down()
		else:
			self.TargetAcceptLight.SetUp()

	def OverInOwnerItem(self, slotIndex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeOwnerItem(slotIndex)

	def OverInTargetItem(self, slotIndex):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeTargetItem(slotIndex)

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnTop(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.SetTop()
		if self.interface:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_EXCHANGE)
			self.interface.RefreshMarkInventoryBag()

	def OnUpdate(self):
		USE_EXCHANGE_LIMIT_RANGE = 10000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xStart) > USE_EXCHANGE_LIMIT_RANGE or abs(y - self.yStart) > USE_EXCHANGE_LIMIT_RANGE:
			(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()
			net.SendExchangeExitPacket()

	def CantTradableItem(self, destSlotIndex, srcSlotIndex):
		if exchange.GetAcceptFromTarget():
			return

		itemInvenPage = srcSlotIndex / player.INVENTORY_PAGE_SIZE
		localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
		self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)

		if self.wndInventory.GetInventoryPageIndex() == itemInvenPage and self.IsShow():
			self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

	def CanTradableItem(self, destSlotIndex):
		self.lockedItems[destSlotIndex] = (-1,-1)

	def RefreshLockedSlot(self):
		if self.wndInventory:
			for exchangePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

			self.wndInventory.wndItem.RefreshSlot()

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def SetInven(self, wndInventory):
		self.wndInventory = proxy(wndInventory)

#a=ExchangeDialog()
#a.LoadDialog()
#a.Show()