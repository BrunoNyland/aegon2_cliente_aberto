#favor manter essa linha
import _player as player
import _app as app
import _net as net
import _chat as chat
import _item as item
import _chr as chr
import _chr_mgr as chrmgr
import _snd as snd
import _shop as shop
import _settings as systemSetting

import ui, mousemodule, uicommon, localeinfo, exception

from weakref import proxy

g_isBuildingOfflineShop = False
g_itemPriceDict = {}
g_offlineShopAdvertisementBoardDict = {}

def Clear():
	global g_itemPriceDict
	global g_isBuildingOfflineShop
	g_itemPriceDict = {}
	g_isBuildingOfflineShop = False

def IsOfflineShopItemPriceList():
	global g_itemPriceDict
	if (g_itemPriceDict):
		return True
	else:
		return False

def IsBuildingOfflineShop():
	global g_isBuildingOfflineShop
	if (g_isBuildingOfflineShop):
		return True
	else:
		return False

def SetOfflineShopItemPrice(itemVnum, itemPrice):
	global g_itemPriceDict
	g_itemPriceDict[int(itemVnum)] = itemPrice

def GetOfflineShopItemPrice(itemVnum):
	try:
		global g_itemPriceDict
		return g_itemPriceDict[itemVnum]
	except KeyError:
		return 0

def UpdateADBoard():
	for key in g_offlineShopAdvertisementBoardDict.keys():
		g_offlineShopAdvertisementBoardDict[key].Show()

def DeleteADBoard(vid):
	if (not g_offlineShopAdvertisementBoardDict.__contains__(vid)):
		return
	del g_offlineShopAdvertisementBoardDict[vid]

class OfflineShopBuilder(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadWindow()
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/offlineshopbuilder.py")

		self.nameLine = self.GetChild("NameLine")
		self.itemSlot = self.GetChild("ItemSlot")
		self.btnOk = self.GetChild("OkButton")
		self.btnClose = self.GetChild("CloseButton")
		self.board = self.GetChild("Board")


		self.btnOk.SetEvent(self.OnOk)
		self.btnClose.SetEvent(self.OnClose)
		self.board.SetCloseEvent(self.OnClose)
		self.itemSlot.SetSelectEmptySlotEvent(self.OnSelectEmptySlot)
		self.itemSlot.SetSelectItemSlotEvent(self.OnSelectItemSlot)
		self.itemSlot.SetOverInItemEvent(self.OnOverInItem)
		self.itemSlot.SetOverOutItemEvent(self.OnOverOutItem)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.board = None
		self.priceInputBoard = None

	def Open(self, title):
		self.title = title
		self.itemStock = {}
		shop.ClearOfflineShopStock()
		self.nameLine.SetTextLimited(title, 140)
		self.SetCenterPosition()
		self.Refresh()
		self.Show()

		global g_isBuildingOfflineShop
		g_isBuildingOfflineShop = True

	def Close(self):
		global g_isBuildingOfflineShop
		g_isBuildingOfflineShop = False
		self.title = ""
		shop.ClearOfflineShopStock()
		self.Hide()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def Refresh(self):
		for i in range(shop.OFFLINE_SHOP_SLOT_COUNT):
			if (not self.itemStock.__contains__(i)):
				self.itemSlot.ClearSlot(i)
				continue
			pos = self.itemStock[i]
			itemCount = player.GetItemCount(*pos)
			if (itemCount <= 1):
				itemCount = 0
			self.itemSlot.SetItemSlot(i, player.GetItemIndex(*pos), itemCount)
		self.itemSlot.RefreshSlot()

	def OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mousemodule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			mousemodule.mouseController.DeattachObject()
			if (player.SLOT_TYPE_INVENTORY != attachedSlotType):
				return
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OFFLINE_SHOP_CANNOT_SELL_ITEM)
				return

			priceInputBoard = uicommon.PriceInputDialog()
			priceInputBoard.SetTitle(localeinfo.OFFLINE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(self.AcceptInputPrice)
			priceInputBoard.SetCancelEvent(self.CancelInputPrice)
			priceInputBoard.Open(itemVNum, itemCount)

			itemPrice = GetOfflineShopItemPrice(itemVNum)
			if (itemPrice > 0):
				priceInputBoard.SetValue(itemPrice)

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos
			# self.priceInputBoard.CleanAveragePrice()
			net.SendChatPacket("/price_checker shopoff " + str(itemVNum))

	def UpdateAveragePrice(self, price):
		if self.priceInputBoard:
			self.priceInputBoard.UpdateAveragePrice(price)

	def OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mousemodule.mouseController.isAttached()
		if (isAttached):
			snd.PlaySound("sound/ui/loginfail.wav")
			mousemodule.mouseController.DeattachObject()
		else:
			if (not selectedSlotPos in self.itemStock):
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			shop.DelOfflineShopItemStock(invenType, invenPos)
			snd.PlaySound("sound/ui/drop.wav")
			del self.itemStock[selectedSlotPos]
			self.Refresh()

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

		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos

		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			if (itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos):
				shop.DelOfflineShopItemStock(itemWindowType, itemSlotIndex)
				del self.itemStock[privatePos]


		price = int(self.priceInputBoard.GetText())
		if (IsOfflineShopItemPriceList()):
			SetOfflineShopItemPrice(self.priceInputBoard.itemVNum, price)

		shop.AddOfflineShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price)
		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)
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
		
	def OnOk(self):
		if (not self.title):
			return

		if (len(self.itemStock) == 0):
			return

		shop.BuildOfflineShop(self.title)
		self.Close()

	def OnClose(self):
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnOverInItem(self, slotIndex):
		if (self.tooltipItem):
			if (self.itemStock.__contains__(slotIndex)):
				self.tooltipItem.SetOfflineShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverOutItem(self):
		if (self.tooltipItem):
			self.tooltipItem.HideToolTip()

class OfflineShopAdvertisementBoard(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self, "UI_BOTTOM")
		self.vid = None
		self.__MakeTextLine()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def __MakeTextLine(self):
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.SetPosition(0,-2)
		self.textLine.Show()

	def Open(self, vid, text):
		self.vid = vid
		self.textLine.SetText(text)
		self.textLine.UpdateRect()
		(w, h) = self.textLine.GetTextSize()
		if w > 200:
			self.SetSize(w+120)
		else:
			self.SetSize(200)
		self.Show()
		g_offlineShopAdvertisementBoardDict[vid] = self

	def OnMouseLeftButtonUp(self):
		if (not self.vid):
			return
		self.textLine.SetFontColor(0.0, 1.0, 0.8)
		net.SendOnClickPacket(self.vid)
		return True

	def OnUpdate(self):
		if (not self.vid):
			return
		if (systemSetting.IsShowSalesText()):
			self.Show()
			(x, y) = chr.GetProjectPosition(self.vid, 220)
			self.SetPosition(x - self.GetWidth() / 2, y - self.GetHeight() / 2)
		else:
			for key in g_offlineShopAdvertisementBoardDict.keys():
				g_offlineShopAdvertisementBoardDict[key].Hide()

# x = OfflineShopBuilder()
# x.Open("Bruno Mauricio Nyland Bruno Mauricio Nyland")