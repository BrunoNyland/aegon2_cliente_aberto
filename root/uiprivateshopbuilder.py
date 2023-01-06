#favor manter essa linha
import ui
import _snd as snd
import _shop as shop
import mousemodule
import _player as player
import _chr as chr
import _net as net
import uicommon
import localeinfo
import _chat as chat
import _item as item
import _settings as systemSetting
import _player as player

from weakref import proxy

g_isBuildingPrivateShop = False
g_itemPriceDict={}
g_privateShopAdvertisementBoardDict={}

def Clear():
	global g_itemPriceDict
	global g_isBuildingPrivateShop
	g_itemPriceDict={}
	g_isBuildingPrivateShop = False

def IsPrivateShopItemPriceList():
	global g_itemPriceDict
	if g_itemPriceDict:
		return True
	else:
		return False

def IsBuildingPrivateShop():
	global g_isBuildingPrivateShop
	if player.IsOpenPrivateShop() or g_isBuildingPrivateShop:
		return True
	else:
		return False

def SetPrivateShopItemPrice(itemVNum, itemPrice):
	global g_itemPriceDict
	g_itemPriceDict[int(itemVNum)]=itemPrice

def GetPrivateShopItemPrice(itemVNum):
	try:
		global g_itemPriceDict
		return g_itemPriceDict[itemVNum]
	except KeyError:
		return 0

def UpdateADBoard():
	for key in g_privateShopAdvertisementBoardDict.keys():
		g_privateShopAdvertisementBoardDict[key].Show()

def DeleteADBoard(vid):
	if not g_privateShopAdvertisementBoardDict.__contains__(vid):
		return
	del g_privateShopAdvertisementBoardDict[vid]

class PrivateShopAdvertisementBoard(ui.ThinBoard):
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
		self.textLine.Show()

	def Open(self, vid, text):
		self.vid = vid
		self.textLine.SetText(text)
		self.textLine.UpdateRect()
		(w, h) = self.textLine.GetTextSize()
		if w > 200:
			self.SetSize(w+120, 15)
		else:
			self.SetSize(200, 15)
		self.Show() 
		g_privateShopAdvertisementBoardDict[vid] = self

	def OnMouseLeftButtonUp(self):
		if not self.vid:
			return
		self.textLine.SetFontColor(0.0, 1.0, 0.8)
		net.SendOnClickPacket(self.vid)
		return True

	def OnUpdate(self):
		if not self.vid:
			return
		if systemSetting.IsShowSalesText():
			self.Show()
			x, y = chr.GetProjectPosition(self.vid, 220)
			self.SetPosition(x - self.GetWidth()/2, y - self.GetHeight()/2)
		else:
			for key in g_privateShopAdvertisementBoardDict.keys():
				if player.GetMainCharacterIndex() == key:
					g_privateShopAdvertisementBoardDict[key].Show()
					x, y = chr.GetProjectPosition(player.GetMainCharacterIndex(), 220)
					g_privateShopAdvertisementBoardDict[key].SetPosition(x - self.GetWidth()/2, y - self.GetHeight()/2)
				else:
					g_privateShopAdvertisementBoardDict[key].Hide()

class PrivateShopBuilder(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__LoadWindow()
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""
		self.interface = None
		self.wndInventory = None
		self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/privateshopbuilder.py")
		except BaseException:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.LoadObject")

		try:
			GetObject = self.GetChild
			self.nameLine = GetObject("NameLine")
			self.itemSlot = GetObject("ItemSlot")
			self.btnOk = GetObject("OkButton")
			self.btnClose = GetObject("CloseButton")
			self.board = GetObject("board")
		except BaseException:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.BindObject")

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
		self.titleBar = None
		self.priceInputBoard = None
		self.interface = None
		self.wndInventory = None
		self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}

	def Open(self, title):
		self.title = title

		if len(title) > 25:
			title = title[:22] + "..."

		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.nameLine.SetText(title)
		self.SetCenterPosition()
		self.Refresh()
		self.Show()
		self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
		self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
		self.interface.RefreshMarkInventoryBag()

		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = True

	def Close(self):
		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = False

		self.title = ""
		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.Hide()
		if self.priceInputBoard:
			self.priceInputBoard.Close()
			self.priceInputBoard = None

		for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

		self.lockedItems = {i:(-1,-1) for i in range(shop.SHOP_SLOT_COUNT)}
		self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
		self.interface.RefreshMarkInventoryBag()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def Refresh(self):
		getitemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setitemVNum=self.itemSlot.SetItemSlot
		delItem=self.itemSlot.ClearSlot

		for i in range(shop.SHOP_SLOT_COUNT):

			if not self.itemStock.__contains__(i):
				delItem(i)
				continue

			pos = self.itemStock[i]

			itemCount = getItemCount(*pos)
			if itemCount <= 1:
				itemCount = 0
			setitemVNum(i, getitemVNum(*pos), itemCount)

		self.itemSlot.RefreshSlot()
		self.RefreshLockedSlot()

	def OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mousemodule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			mousemodule.mouseController.DeattachObject()
			if player.SLOT_TYPE_INVENTORY != attachedSlotType:
				return
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
				return

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				self.CantTradableItem(selectedSlotPos, attachedSlotPos)

			priceInputBoard = uicommon.PriceInputDialog()
			priceInputBoard.SetTitle(localeinfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(self.AcceptInputPrice)
			priceInputBoard.SetCancelEvent(self.CancelInputPrice)
			priceInputBoard.Open(itemVNum, itemCount)

			itemPrice=GetPrivateShopItemPrice(itemVNum)

			if itemPrice>0:
				priceInputBoard.SetValue(itemPrice)

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos
			# self.priceInputBoard.CleanAveragePrice()
			net.SendChatPacket("/price_checker shop " + str(itemVNum))

	def UpdateAveragePrice(self, price):
		if self.priceInputBoard:
			self.priceInputBoard.UpdateAveragePrice(price)

	def OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mousemodule.mouseController.isAttached()
		if isAttached:
			snd.PlaySound("sound/ui/loginfail.wav")
			mousemodule.mouseController.DeattachObject()
		else:
			if not selectedSlotPos in self.itemStock:
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			shop.DelPrivateShopItemStock(invenType, invenPos)
			snd.PlaySound("sound/ui/drop.wav")
			(itemInvenPage, itemSlotPos) = self.lockedItems[selectedSlotPos]
			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)
			self.lockedItems[selectedSlotPos] = (-1, -1)
			del self.itemStock[selectedSlotPos]
			self.Refresh()

	def AcceptInputPrice(self):
		if not self.priceInputBoard:
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
			if itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos:
				shop.DelPrivateShopItemStock(itemWindowType, itemSlotIndex)
				del self.itemStock[privatePos]

		price = int(self.priceInputBoard.GetText())

		if IsPrivateShopItemPriceList():
			SetPrivateShopItemPrice(self.priceInputBoard.itemVNum, price)

		shop.AddPrivateShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price)
		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)
		snd.PlaySound("sound/ui/drop.wav")

		self.Refresh()
		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		itemInvenPage = self.priceInputBoard.sourceSlotPos / player.INVENTORY_PAGE_SIZE
		itemSlotPos = self.priceInputBoard.sourceSlotPos - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
		if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
			self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

		self.lockedItems[self.priceInputBoard.targetSlotPos] = (-1, -1)

		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return 1

	def OnOk(self):

		if not self.title:
			return

		if 0 == len(self.itemStock):
			return

		shop.BuildPrivateShop(self.title)
		self.Close()

	def OnClose(self):
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnOverInItem(self, slotIndex):

		if self.tooltipItem:
			if self.itemStock.__contains__(slotIndex):
				self.tooltipItem.SetPrivateShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverOutItem(self):

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def CantTradableItem(self, destSlotIndex, srcSlotIndex):
		itemInvenPage = srcSlotIndex / player.INVENTORY_PAGE_SIZE
		localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
		self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)
		if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
			self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

	def RefreshLockedSlot(self):
		if self.wndInventory:
			for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

			self.wndInventory.wndItem.RefreshSlot()

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def OnTop(self):
		if self.interface:
			self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
			self.interface.RefreshMarkInventoryBag()

	def SetInven(self, wndInventory):
		from weakref import proxy
		self.wndInventory = proxy(wndInventory)
