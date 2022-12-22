#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import enszxc3467hc3kokdueq as app
import LURMxMaKZJqliYt2QSHG as chat
import Js4k2l7BrdasmVRt8Wem as chr
import ui
import snd
import shop
import wndMgr
import uicommon
import constinfo
import localeinfo
import mousemodule
import uishopamount

from _weakref import proxy

class ShopDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.questionDialog = None
		self.popup = None
		self.itemBuyQuestionDialog = None
		self.interface = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Refresh(self):
		getItemID=shop.GetItemID
		getItemCount=shop.GetItemCount
		setItemID=self.itemSlotWindow.SetItemSlot
		for i in range(shop.SHOP_SLOT_COUNT):
			itemCount = getItemCount(i)
			if itemCount <= 1:
				itemCount = 0
			setItemID(i, getItemID(i), itemCount)
		wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetItemData(pos, itemID, itemCount, itemPrice)

	def LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/shopdialog.py")
		except BaseException:
			import exception
			exception.Abort("ShopDialog.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.itemSlotWindow = GetObject("ItemSlot")
			self.btnBuy = GetObject("BuyButton")
			self.btnSell = GetObject("SellButton")
			self.btnClose = GetObject("CloseButton")
			self.board = GetObject("board")
			self.AmountOnOff = GetObject("AmountButton")
		except BaseException:
			import exception
			exception.Abort("ShopDialog.LoadDialog.BindObject")

		self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SetButtonEvent("LEFT", "EMPTY", self.SelectEmptySlot)
		self.itemSlotWindow.SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.itemSlotWindow.SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)

		self.itemSlotWindow.SetOverInItemEvent(self.OverInItem)
		self.itemSlotWindow.SetOverOutItemEvent(self.OverOutItem)

		self.board.SetCloseEvent(self.Close)
		self.btnBuy.SetEvent(self.OnBuy)
		self.btnSell.SetEvent(self.OnSell)
		self.btnClose.SetEvent(self.AskClosePrivateShop)

		wndShopAmount = uishopamount.ShopAmountDialog()
		wndShopAmount.LoadDialog()
		wndShopAmount.Hide()
		self.wndShopAmount = wndShopAmount
		self.Refresh()

	def Destroy(self):
		self.Close(True)
		self.interface = None
		self.ClearDictionary()
		self.btnBuy = 0
		self.btnSell = 0
		self.btnClose = 0
		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.board = 0
		self.AmountOnOff = 0
		self.questionDialog = None
		self.popup = None
		self.wndShopAmount.Destroy()
		self.wndShopAmount = 0

	def Open(self, vid):
		isPrivateShop = False
		isMainPlayerPrivateShop = False

		if chr.IsNPC(vid):
			# if self.interface.wndBot.IsShow() or self.interface.wndBot.PinGroupBox != None:
				# net.SendChatPacket("/make_sitdown")
			self.SetAmountOption(constinfo.GetAmountSettings())
			self.AmountOnOff.Show()
			isPrivateShop = False
		else:
			isPrivateShop = True
			self.AmountOnOff.Hide()

		if player.IsMainCharacterIndex(vid):
			isMainPlayerPrivateShop = True
			self.btnBuy.Hide()
			self.btnSell.Hide()
			self.btnClose.Show()
		else:
			isMainPlayerPrivateShop = False
			self.btnBuy.Show()
			self.btnSell.Show()
			self.btnClose.Hide()

		shop.Open(isPrivateShop, isMainPlayerPrivateShop)
		self.Refresh()
		self.SetTop()
		self.Show()

		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()
		if not isPrivateShop:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_SHOP)
			self.interface.RefreshMarkInventoryBag()

	def SetAmountOption(self, index):
		constinfo.SetAmountSetting(index)
		if index:
			self.AmountOnOff.SetEvent(self.SetAmountOption, 0)
			self.AmountOnOff.SetUpVisual("interface/controls/common/checkbox/filled_01_normal.tga")
			self.AmountOnOff.SetOverVisual("interface/controls/common/checkbox/filled_02_hover.tga")
			self.AmountOnOff.SetDownVisual("interface/controls/common/checkbox/filled_03_active.tga")
		else:
			self.AmountOnOff.SetEvent(self.SetAmountOption, 1)
			self.AmountOnOff.SetUpVisual("interface/controls/common/checkbox/empty_01_normal.tga")
			self.AmountOnOff.SetOverVisual("interface/controls/common/checkbox/empty_02_hover.tga")
			self.AmountOnOff.SetDownVisual("interface/controls/common/checkbox/empty_03_active.tga")

	def Close(self, isDestroy=False):
		self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
		if not isDestroy:
			self.interface.RefreshMarkInventoryBag()

		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
			constinfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		self.OnCloseQuestionDialog()
		shop.Close()
		net.SendShopEndPacket()
		self.CancelShopping()
		self.tooltipItem.HideToolTip()
		self.Hide()

	def AskClosePrivateShop(self):
		questionDialog = uicommon.QuestionDialog()
		questionDialog.SetText(localeinfo.PRIVATE_SHOP_CLOSE_QUESTION)
		questionDialog.SetAcceptEvent(self.OnClosePrivateShop)
		questionDialog.SetCancelEvent(self.OnCloseQuestionDialog)
		questionDialog.Open()
		self.questionDialog = questionDialog
		return True

	def OnClosePrivateShop(self):
		net.SendChatPacket("/close_shop")
		self.OnCloseQuestionDialog()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnBuy(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SHOP_BUY_INFO)
		app.SetCursor(app.BUY)
		self.btnBuy.Disable()
		self.btnSell.Enable()

	def OnSell(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SHOP_SELL_INFO)
		app.SetCursor(app.SELL)
		self.btnSell.Disable()
		self.btnBuy.Enable()

	def CancelShopping(self):
		self.btnBuy.Enable()
		self.btnSell.Enable()
		app.SetCursor(app.NORMAL)

	def __OnClosePopupDialog(self):
		self.pop = None

	def SellAttachedItem(self):
		if shop.IsPrivateShop():
			mousemodule.mouseController.DeattachObject()
			return

		attachedSlotType = mousemodule.mouseController.GetAttachedType()
		attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
		attachedCount = mousemodule.mouseController.GetAttachedItemCount()

		itemVnum = player.GetItemIndex(attachedSlotPos)
		if player.SLOT_TYPE_INVENTORY == attachedSlotType:

			itemIndex = player.GetItemIndex(attachedSlotPos)
			item.SelectItem(itemIndex)

			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uicommon.PopupDialog()
				popup.SetText(localeinfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup

			elif player.IsValuableItem(attachedSlotPos):
				itemPrice = item.GetISellItemPrice()

				if item.Is1GoldItem():
					itemPrice = attachedCount / itemPrice / 5
				else:
					itemPrice = itemPrice * max(1, attachedCount) / 5

				itemName = item.GetItemName()

				questionDialog = uicommon.ItemQuestionDialog()
				if attachedCount > 1:
					questionDialog.SetText("Deseja realmente vender estes itens pelo valor abaixo?")
				else:
					questionDialog.SetText("Deseja realmente vender este item pelo valor abaixo?")
				questionDialog.window_type = "inv"
				questionDialog.count = attachedCount
				questionDialog.SetAcceptEvent(self.OnSellItem, attachedSlotPos, attachedCount)
				questionDialog.SetCancelEvent(self.OnCloseQuestionDialog)
				questionDialog.Open(itemVnum, attachedSlotPos, itemPrice)
				self.questionDialog = questionDialog
			else:
				self.OnSellItem(attachedSlotPos, attachedCount)

		else:
			snd.PlaySound("sound/ui/loginfail.wav")

		mousemodule.mouseController.DeattachObject()

	def OnSellItem(self, slotPos, count):
		net.SendShopSellPacket(slotPos, count)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	def SelectEmptySlot(self, selectedSlotPos):
		isAttached = mousemodule.mouseController.isAttached()
		if isAttached:
			self.SellAttachedItem()

	def UnselectItemSlot(self, selectedSlotPos):
		if shop.IsPrivateShop():
			self.AskBuyItem(selectedSlotPos)
		else:
			if constinfo.GetAmountSettings():
				itemIndex = shop.GetItemID(selectedSlotPos)
				item.SelectItem(itemIndex)
				itemName = item.GetItemName()
				self.wndShopAmount.SetTitleName(itemName)
				self.wndShopAmount.SetAcceptEvent(self.OnItC)
				self.wndShopAmount.Open(200)
				self.wndShopAmount.SetMax(3) 
				self.cek = selectedSlotPos
			else:
				net.SendShopBuyPacket(selectedSlotPos)

	def OnItC(self, adet):
		n = 0
		cek = self.cek
		while n < adet:
			net.SendShopBuyPacket(cek)
			n = n + 1

	def SelectItemSlot(self, selectedSlotPos):
		isAttached = mousemodule.mouseController.isAttached()
		if isAttached:
			self.SellAttachedItem()

		else:
			if shop.IsMainPlayerPrivateShop():
				return

			curCursorNum = app.GetCursor()
			if app.BUY == curCursorNum:
				self.AskBuyItem(selectedSlotPos)

			elif app.SELL == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SHOP_SELL_INFO)

			else:
				selectedItemID = shop.GetItemID(selectedSlotPos)
				itemCount = shop.GetItemCount(selectedSlotPos)

				type = player.SLOT_TYPE_SHOP
				if shop.IsPrivateShop():
					type = player.SLOT_TYPE_PRIVATE_SHOP

				mousemodule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
				mousemodule.mouseController.SetCallBack("INVENTORY", self.DropToInventory)
				snd.PlaySound("sound/ui/pick.wav")

	def DropToInventory(self):
		attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)

	def AskBuyItem(self, slotPos):
		itemIndex = shop.GetItemID(slotPos)
		itemPrice = shop.GetItemPrice(slotPos)
		itemCount = shop.GetItemCount(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()
		itemBuyQuestionDialog = uicommon.ItemQuestionDialog()
		# itemBuyQuestionDialog.SetText(localeinfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeinfo.NumberToGoldString(itemPrice)))
		if itemCount > 1:
			itemBuyQuestionDialog.SetText("Deseja realmente comprar estes itens pelo valor abaixo?")
		else:
			itemBuyQuestionDialog.SetText("Deseja realmente comprar este item pelo valor abaixo?")
		itemBuyQuestionDialog.window_type = "shop"
		itemBuyQuestionDialog.count = itemCount
		itemBuyQuestionDialog.SetAcceptEvent(self.AnswerBuyItem, True)
		itemBuyQuestionDialog.SetCancelEvent(self.AnswerBuyItem, False)
		itemBuyQuestionDialog.Open(itemIndex, slotPos, itemPrice)
		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog

	def AnswerBuyItem(self, flag):
		if flag:
			pos = self.itemBuyQuestionDialog.pos
			net.SendShopBuyPacket(pos)

		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def OverInItem(self, slotIndex):
		if mousemodule.mouseController.isAttached():
			return

		if 0 != self.tooltipItem:
			self.tooltipItem.SetShopItem(slotIndex)

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		USE_SHOP_LIMIT_RANGE = 2000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xShopStart) > USE_SHOP_LIMIT_RANGE or abs(y - self.yShopStart) > USE_SHOP_LIMIT_RANGE:
			self.Close()

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def OnTop(self):
		if not shop.IsPrivateShop():
			self.interface.SetOnTopWindow(player.ON_TOP_WND_SHOP)
			self.interface.RefreshMarkInventoryBag()