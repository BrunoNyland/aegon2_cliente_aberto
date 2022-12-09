#favor manter essa linha
import ga3vqy6jtxqi9yf344j7 as player
import enszxc3467hc3kokdueq as app
import zn94xlgo573hf8xmddzq as net
import LURMxMaKZJqliYt2QSHG as chat
import XXjvumrgrYBZompk3PS8 as item
import Js4k2l7BrdasmVRt8Wem as chr

import snd, shop, wndMgr, ui, uicommon, uitooltip, mousemodule, localeinfo, constinfo
import exception

from _weakref import proxy

g_isEditingOfflineShop = False

def IsEditingOfflineShop():
	global g_isEditingOfflineShop
	if (g_isEditingOfflineShop):
		return True
	else:
		return False

###################################################################################################
## Offline Shop Admin Panel
class OfflineShopAdminPanelWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.RegisterWindow("UI")
		# self.isLoaded = 0
		self.wndOfflineShopAddItem = None
		self.wndOfflineShopRemoveItem = None
		self.wndOfflineShopChangePrice = None
		self.wndOfflineShopMyBank = None
		self.closeQuestionDialog = None
		self.LoadWindow()
		self.LoadOtherWindows()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.SetCenterPosition()
		self.SetTop()

	def LoadWindow(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "uiscript/offlineshopadminpanel.py")

		self.board = self.GetChild("Board")
		self.openOfflineShopButton = self.GetChild("OpenOfflineShopButton")
		self.closeOfflineShopButton = self.GetChild("CloseOfflineShopButton")
		self.addItemButton = self.GetChild("AddItemButton")
		self.removeItemButton = self.GetChild("RemoveItemButton")
		self.changePriceButton = self.GetChild("ChangePriceButton")
		self.myBankButton = self.GetChild("MyBankButton")


		self.board.SetCloseEvent(self.Close)
		self.openOfflineShopButton.SetEvent(self.ClickOpenOfflineShopButton)
		self.closeOfflineShopButton.SetEvent(self.ClickCloseOfflineShopButton)
		self.addItemButton.SetEvent(self.ClickAddItemButton)
		self.removeItemButton.SetEvent(self.ClickRemoveItemButton)
		self.changePriceButton.SetEvent(self.ClickChangePriceButton)
		self.myBankButton.SetEvent(self.ClickMyBankButton)

	def LoadOtherWindows(self):
		# OFFLINE_SHOP_ADD_ITEM
		wndOfflineShopAddItem = OfflineShopAddItemWindow()
		self.wndOfflineShopAddItem = wndOfflineShopAddItem
		# END_OF_OFFLINE_SHOP_ADD_ITEM

		# OFFLINE_SHOP_REMOVE_ITEM
		wndOfflineShopRemoveItem = OfflineShopRemoveItemWindow()
		self.wndOfflineShopRemoveItem = wndOfflineShopRemoveItem
		# END_OF_OFFLINE_SHOP_REMOVE_ITEM

		# OFFLINE_SHOP_CHANGE_PRICE
		wndOfflineShopChangePrice = OfflineShopChangePriceWindow()
		self.wndOfflineShopChangePrice = wndOfflineShopChangePrice
		# END_OF_OFFLINE_SHOP_CHANGE_PRICE

		# OFFLINE_SHOP_MY_BANK
		wndOfflineShopMyBank = OfflineShopBankDialog()
		self.wndOfflineShopMyBank = wndOfflineShopMyBank
		# END_OF_OFFLINE_SHOP_MY_BANK

	def ClickOpenOfflineShopButton(self):
		self.Close()
		net.SendChatPacket("/open_offlineshop")
		return True

	def ClickCloseOfflineShopButton(self):
		self.Close()
		closeQuestionDialog = uicommon.QuestionDialog()
		closeQuestionDialog.SetText(localeinfo.DO_YOU_WANT_TO_CLOSE_OFFLINE_SHOP)
		closeQuestionDialog.SetAcceptEvent(self.AnswerCloseOfflineShop, True)
		closeQuestionDialog.SetCancelEvent(self.AnswerCloseOfflineShop, False)
		closeQuestionDialog.Open()
		self.closeQuestionDialog = closeQuestionDialog

	def AnswerCloseOfflineShop(self, flag):
		if (flag):
			net.SendDestroyOfflineShop()
			shop.ClearOfflineShopStock()
		else:
			self.Show()

		self.closeQuestionDialog = None

	def ClickAddItemButton(self):
		self.Close()
		self.wndOfflineShopAddItem.SetTop()
		self.wndOfflineShopAddItem.SetCenterPosition()
		self.wndOfflineShopAddItem.Open(player.GetName() + "'s " + localeinfo.OFFLINE_SHOP)
		return True

	def ClickRemoveItemButton(self):
		self.Close()
		self.wndOfflineShopRemoveItem.SetTop()
		self.wndOfflineShopRemoveItem.SetCenterPosition()
		self.wndOfflineShopRemoveItem.Open(player.GetName() + "'s " + localeinfo.OFFLINE_SHOP)
		return True

	def ClickChangePriceButton(self):
		self.Close()
		self.wndOfflineShopChangePrice.SetTop()
		self.wndOfflineShopChangePrice.SetCenterPosition()
		self.wndOfflineShopChangePrice.Open(player.GetName() + "'s " + localeinfo.OFFLINE_SHOP)
		return True

	def ClickMyBankButton(self):
		self.Close()
		self.wndOfflineShopMyBank.Open()
		return True

	def BindInterfaceClass(self, interface):
		self.interface = proxy(interface)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.interface = None

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

###################################################################################################
## Offline Shop Add Item Window
class OfflineShopAddItemWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Refresh(self):
		net.SendRefreshOfflineShop()
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			itemCount = shop.GetOfflineShopItemCount(i)
			if (itemCount <= 1):
				itemCount = 0

			self.itemSlot.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

		wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetOfflineShopItemData(pos, itemID, itemCount, itemPrice)

	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop.py")



		self.nameLine = self.GetChild("NameLine")
		self.itemSlot = self.GetChild("ItemSlot")
		self.btnOk = self.GetChild("OkButton")
		self.btnClose = self.GetChild("CloseButton")
		self.board = self.GetChild("Board")

		self.btnOk.Hide()
		self.btnClose.Hide()
		self.board.SetCloseEvent(self.Close)

		self.itemSlot.SetOverInItemEvent(self.OverInItem)
		self.itemSlot.SetOverOutItemEvent(self.OverOutItem)
		self.itemSlot.SetSelectEmptySlotEvent(self.SelectEmptySlot)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.board = None

	def Open(self, title):
		self.title = title

		if (len(title) > 25):
			self.title = title[:22] + "..."

		self.tooltipItem = uitooltip.ItemToolTip()
		self.tooltipItem.Hide()
		self.board.SetTitleName("Adicionar Item")
		self.Refresh()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.nameLine.SetText(title)
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = True

	def Close(self):
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = False

		self.title = ""
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def SelectEmptySlot(self, slotIndex):
		if (constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS() == 1):
			return

		if (mousemodule.mouseController.isAttached()):
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			mousemodule.mouseController.DeattachObject()

			if (player.SLOT_TYPE_INVENTORY != attachedSlotType):
				return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			itemVnum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVnum)

			if (item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP)):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OFFLINE_SHOP_CANNOT_SELL_ITEM)
				return

			priceInputBoard = uicommon.PriceInputDialog()
			priceInputBoard.SetAcceptEvent(self.AcceptInputPrice)
			priceInputBoard.SetCancelEvent(self.CancelInputPrice)
			priceInputBoard.Open(itemVnum, itemCount)

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.bDisplayPos = slotIndex
			self.priceInputBoard.bPos = attachedSlotPos
			net.SendChatPacket("/price_checker additem " + str(itemVnum))

	def UpdateAveragePrice(self, price):
		if self.priceInputBoard:
			self.priceInputBoard.UpdateAveragePrice(price)

	def AcceptInputPrice(self):
		if (not self.priceInputBoard):
			return True

		text = self.priceInputBoard.GetText()

		if not text:
			return True

		if not text.isdigit():
			return True

		if int(text) <= 0:
			return True

		net.SendAddOfflineShopItem(self.priceInputBoard.bPos, self.priceInputBoard.bDisplayPos, int(self.priceInputBoard.inputValue.GetText()))
		snd.PlaySound("sound/ui/drop.wav")
		self.Refresh()
		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return True

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def OverInItem(self, slotIndex):
		if (mousemodule.mouseController.isAttached()):
			return

		if (self.tooltipItem != 0):
			self.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverOutItem(self):
		if (self.tooltipItem != 0):
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			itemCount = shop.GetOfflineShopItemCount(i)
			if (itemCount <= 1):
				itemCount = 0

			self.itemSlot.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

		wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())

###################################################################################################
## Offline Shop Remove Item Window
class OfflineShopRemoveItemWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.tooltipItem = None
		self.questionDialog = None
		self.title = ""

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Refresh(self):
		net.SendRefreshOfflineShop()
		iCount = 0
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			if (shop.GetOfflineShopItemID(i) == -842150451):
				iCount = iCount + 1

		if (iCount == shop.OFFLINE_SHOP_SLOT_COUNT):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Você não tem nada na loja offline no momento.")
			return

		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			itemCount = shop.GetOfflineShopItemCount(i)
			if (itemCount <= 1):
				itemCount = 0

			self.itemSlot.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

		wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetOfflineShopItemData(pos, itemID, itemCount, itemPrice)

	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop.py")
			
		self.nameLine = self.GetChild("NameLine")
		self.itemSlot = self.GetChild("ItemSlot")
		self.btnOk = self.GetChild("OkButton")
		self.btnClose = self.GetChild("CloseButton")
		self.board = self.GetChild("Board")

		self.btnOk.Hide()
		self.btnClose.Hide()
		self.board.SetCloseEvent(self.Close)

		self.itemSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlot.SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
		self.itemSlot.SetOverInItemEvent(self.OverInItem)
		self.itemSlot.SetOverOutItemEvent(self.OverOutItem)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.board = None

	def Open(self, title):
		self.title = title

		if (len(title) > 25):
			self.title = title[:22] + "..."

		self.tooltipItem = uitooltip.ItemToolTip()
		self.tooltipItem.Hide()
		self.board.SetTitleName("Remover Item")
		self.Refresh()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.nameLine.SetText(title)
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = True

	def Close(self):
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = False

		if (self.questionDialog):
			self.questionDialog.Close()
			self.questionDialog = None
			constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

		self.title = ""
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def UnselectItemSlot(self, selectedSlotPos):
		if (constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS() == 1):
			return

		itemIndex = shop.GetOfflineShopItemID(selectedSlotPos)
		itemCount = shop.GetOfflineShopItemCount(selectedSlotPos)
		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		questionDialog = uicommon.ItemQuestionDialog()
		questionDialog.window_type = "off"
		questionDialog.count = itemCount
		questionDialog.SetText(localeinfo.DO_YOU_WANT_TO_REMOVE_ITEM % (itemName))
		questionDialog.SetAcceptEvent(self.AnswerRemoveItem, True)
		questionDialog.SetCancelEvent(self.AnswerRemoveItem, False)
		questionDialog.Open(itemIndex, selectedSlotPos)
		questionDialog.pos = selectedSlotPos
		self.questionDialog = questionDialog

		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(1)

	def AnswerRemoveItem(self, flag):
		if (flag):
			pos = self.questionDialog.pos
			net.SendRemoveOfflineShopItem(pos)

		self.questionDialog.Close()
		self.questionDialog = None
		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)
		self.Refresh()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def OverInItem(self, slotIndex):
		if (mousemodule.mouseController.isAttached()):
			return

		if (self.tooltipItem != 0):
			self.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverOutItem(self):
		if (self.tooltipItem != 0):
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			itemCount = shop.GetOfflineShopItemCount(i)
			if (itemCount <= 1):
				itemCount = 0

			self.itemSlot.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

		wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())	

###################################################################################################
## Offline Shop Bank Dialog
class OfflineShopBankDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Saldo = 0
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop_bankdialog.py")

		self.Board = self.GetChild("Board")
		self.GoldAtualLine = self.GetChild("GoldAtualLine")
		self.SacarGoldLine = self.GetChild("SacarGoldLine")
		self.AceptButton = self.GetChild("acept_button")
		self.CancelButton = self.GetChild("cancel_button")
		self.CopyButton = self.GetChild("CopyPasteButton")

		self.Board.SetCloseEvent(self.Close)
		self.CancelButton.SetEvent(self.Close)
		self.AceptButton.SetEvent(self.SacarGold)
		self.CopyButton.SetEvent(self.CopyPaste)

	def Close(self):
		self.GoldAtualLine.SetText("")
		self.SacarGoldLine.SetText("")
		self.Saldo = 0
		self.Hide()

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		net.SendRefreshOfflineShopMoney()
		self.SacarGoldLine.SetText("")
		self.Show()

	def CopyPaste(self):
		self.SacarGoldLine.SetText(str(self.Saldo))

	def SacarGold(self):
		try:
			GoldAtual = player.GetCurrentOfflineShopMoney()
			SacarGold = int(self.SacarGoldLine.GetText())

			if (SacarGold > GoldAtual):
				SacarGold = GoldAtual
				self.SacarGoldLine.SetText(str(GoldAtual))
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Valor solicitado maior que o saldo. Será sacado o valor total disponível na conta.")

			if (GoldAtual <= 0):
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Sua conta no banco está sem saldo para sacar.")
				return

			if (SacarGold <= 0):
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Valor de saque inválido.")
				return

			net.SendOfflineShopWithdrawMoney(SacarGold)

		except ValueError:
			self.SacarGoldLine.SetText(str(GoldAtual))
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Valor de saque indevido. Selecionado o valor máximo de saque.")

	def UpdateMoneyString(self, value):
		self.Saldo = value
		self.GoldAtualLine.SetText(localeinfo.NumberToGoldString(value))

###################################################################################################
## Offline Shop Change Price
class OfflineShopChangePriceWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Refresh(self):
		net.SendRefreshOfflineShop()
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			itemCount = shop.GetOfflineShopItemCount(i)
			if (itemCount <= 1):
				itemCount = 0

			self.itemSlot.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

		wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetOfflineShopItemData(pos, itemID, itemCount, itemPrice)

	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/offlineshop.py")

		self.nameLine = self.GetChild("NameLine")
		self.itemSlot = self.GetChild("ItemSlot")
		self.btnRefresh = self.GetChild("OkButton")
		self.btnClose = self.GetChild("CloseButton")
		self.board = self.GetChild("Board")

		self.btnRefresh.SetText("Refresh")
		self.btnClose.Hide()
		self.itemSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlot.SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
		self.itemSlot.SetOverInItemEvent(self.OverInItem)
		self.itemSlot.SetOverOutItemEvent(self.OverOutItem)
		self.btnRefresh.SetEvent(self.Refresh)
		self.board.SetCloseEvent(self.Close)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.board = None
		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None

	def Open(self, title):
		self.title = title

		if (len(title) > 25):
			self.title = title[:22] + "..."

		self.tooltipItem = uitooltip.ItemToolTip()
		self.tooltipItem.Hide()
		self.board.SetTitleName(localeinfo.CHANGE_ITEM_PRICE)
		self.Refresh()
		self.Show()

		self.nameLine.SetText(title)
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = True

	def Close(self):
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = False

		self.title = ""
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def UnselectItemSlot(self, selectedSlotPos):
		if (constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS() == 1):
			return

		itemIndex = shop.GetOfflineShopItemID(selectedSlotPos)
		itemCount = shop.GetOfflineShopItemCount(selectedSlotPos)
		item.SelectItem(itemIndex)
		itemName = item.GetItemName()
		priceInputBoard = uicommon.PriceInputDialog()
		priceInputBoard.SetAcceptEvent(self.AcceptInputPrice)
		priceInputBoard.SetCancelEvent(self.CancelInputPrice)
		priceInputBoard.Open(itemIndex, itemCount)
		self.priceInputBoard = priceInputBoard
		self.priceInputBoard.pos = selectedSlotPos
		net.SendChatPacket("/price_checker changeprice " + str(itemIndex))

	def UpdateAveragePrice(self, price):
		if self.priceInputBoard:
			self.priceInputBoard.UpdateAveragePrice(price)

	def AcceptInputPrice(self):
		if (not self.priceInputBoard):
			return True

		text = self.priceInputBoard.GetText()

		if not text:
			return True

		if not text.isdigit():
			return True

		if int(text) <= 0:
			return True

		pos = self.priceInputBoard.pos
		price = int(self.priceInputBoard.inputValue.GetText())
		net.SendChangePriceOfflineShopItem(pos, price)
		net.SendRefreshOfflineShop()
		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return True

	def OverInItem(self, slotIndex):
		if (mousemodule.mouseController.isAttached()):
			return

		if (self.tooltipItem != 0):
			self.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverOutItem(self):
		if (self.tooltipItem != 0):
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
			itemCount = shop.GetOfflineShopItemCount(i)
			if (itemCount <= 1):
				itemCount = 0

			self.itemSlot.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)

		wndMgr.RefreshSlot(self.itemSlot.GetWindowHandle())

###################################################################################################
## Offline Shop Input
class OfflineShopInputDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "uiscript/offlineshopinputdialog.py")

		self.acceptButton = self.GetChild("AgreeButton")
		self.cancelButton = self.GetChild("CancelButton")
		self.inputSlot = self.GetChild("InputSlot")
		self.inputValue = self.GetChild("InputValue")
		self.board = self.GetChild("board")
		self.board.SetCloseEvent(self.Close)
		self.GetChild("InputSlot").SetMouseLeftButtonDownEvent(self.inputValue.SetFocus)

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.SetReturnEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)
		self.inputValue.SetEscapeEvent(event)

	def GetTitle(self):
		return self.inputValue.GetText()

###################################################################################################
## Offline Shop
class OfflineShopDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.questionDialog = None
		self.popup = None
		self.itemBuyQuestionDialog = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Refresh(self):
		try:
			for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT):
				itemCount = shop.GetOfflineShopItemCount(i)
				if (itemCount <= 1):
					itemCount = 0
				self.itemSlotWindow.SetItemSlot(i, shop.GetOfflineShopItemID(i), itemCount)
			wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())
		except:
			pass

	def LoadDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/offlineshopdialog.py")

		self.itemSlotWindow = self.GetChild("ItemSlot")
		self.board = self.GetChild("board")


		self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.itemSlotWindow.SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)

		self.itemSlotWindow.SetOverInItemEvent(self.OverInItem)
		self.itemSlotWindow.SetOverOutItemEvent(self.OverOutItem)

		self.board.SetCloseEvent(self.Close)
		self.Refresh()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.board = 0
		self.questionDialog = None
		self.popup = None

	def Open(self, vid):
		shop.Open(False, False, True)
		self.Refresh()
		self.SetTop()
		self.Show()

		self.board.SetTitle(chr.GetNameByVID(vid))

		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()

	def Close(self):
		if (self.itemBuyQuestionDialog):
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
			constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

		if (self.questionDialog):
			self.OnCloseQuestionDialog()

		shop.Close()
		net.SendOfflineShopEndPacket()
		self.CancelShopping()
		self.tooltipItem.HideToolTip()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnBuy(self):
		app.SetCursor(app.BUY)

	def CancelShopping(self):
		app.SetCursor(app.NORMAL)

	def OnCloseQuestionDialog(self):
		if (not self.questionDialog):
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

	def UnselectItemSlot(self, selectedSlotPos):
		if (constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS() == 1):
			return

		self.AskBuyItem(selectedSlotPos)

	def SelectItemSlot(self, selectedSlotPos):
		if (constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS() == 1):
			return

		isAttached = mousemodule.mouseController.isAttached()
		if (not isAttached):
			curCursorNum = app.GetCursor()
			if (app.BUY == curCursorNum):
				self.AskBuyItem(selectedSlotPos)
			else:
				selectedItemID = shop.GetOfflineShopItemID(selectedSlotPos)
				itemCount = shop.GetOfflineShopItemCount(selectedSlotPos)

				type = player.SLOT_TYPE_OFFLINE_SHOP
				mousemodule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
				mousemodule.mouseController.SetCallBack("INVENTORY", self.DropToInventory)
				snd.PlaySound("sound/ui/pick.wav")

	def DropToInventory(self):
		attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)

	def AskBuyItem(self, slotPos):
		itemIndex = shop.GetOfflineShopItemID(slotPos)
		itemPrice = shop.GetOfflineShopItemPrice(slotPos)
		itemCount = shop.GetOfflineShopItemCount(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		itemBuyQuestionDialog = uicommon.ItemQuestionDialog()
		if itemCount > 1:
			itemBuyQuestionDialog.SetText("Deseja realmente comprar estes itens pelo valor abaixo?")
		else:
			itemBuyQuestionDialog.SetText("Deseja realmente comprar este item pelo valor abaixo?")
		itemBuyQuestionDialog.window_type = "off"
		itemBuyQuestionDialog.count = itemCount
		itemBuyQuestionDialog.SetAcceptEvent(self.AnswerBuyItem, True)
		itemBuyQuestionDialog.SetCancelEvent(self.AnswerBuyItem, False)
		itemBuyQuestionDialog.Open(itemIndex, slotPos, itemPrice)
		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog

		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(1)

	def AnswerBuyItem(self, flag):
		if (flag):
			pos = self.itemBuyQuestionDialog.pos
			net.SendOfflineShopBuyPacket(pos)

		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None

		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def OverInItem(self, slotIndex):
		if (mousemodule.mouseController.isAttached()):
			return

		if (self.tooltipItem != 0):
			self.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverOutItem(self):
		if (self.tooltipItem != 0):
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xShopStart) > 1500 or abs(y - self.yShopStart) > 1500:
			self.Close()

# x = OfflineShopInputDialog()
# x = OfflineShopAdminPanelWindow()
# x.Show()