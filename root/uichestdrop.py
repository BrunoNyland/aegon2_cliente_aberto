#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import ga3vqy6jtxqi9yf344j7 as player
import ui
import wndMgr
import constinfo
import mousemodule

from _weakref import proxy

class ChestDropWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.currentChest = 0
		self.currentPage = 1
		self.openAmount = 1
		self.invItemPos = -1

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "uiscript/chestdropwindow.py")

		self.openItemSlot = self.GetChild("OpenItemSlot")
		self.openCountController = self.GetChild("OpenCountController")
		self.openChestButton = self.GetChild("OpenChestButton")
		self.prevButton = self.GetChild("prev_button")
		self.nextButton = self.GetChild("next_button")
		self.currentPageBack = self.GetChild("CurrentPageBack")
		self.currentPageText = self.GetChild("CurrentPage")

		self.GetChild("board").SetCloseEvent(self.Close)
		self.openCountController.SetEvent(self.OnChangeOpenAmount)

		self.openChestButton.SetEvent(self.OnClickOpenChest)
		self.openChestButton.SetText("Abrir %d" % self.openAmount)

		self.prevButton.SetEvent(self.OnClickPrevPage)
		self.nextButton.SetEvent(self.OnClickNextPage)
		self.currentPageText.SetText(str(self.currentPage))

		wndItem = self.GetChild("ItemSlot")
		wndItem.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		wndItem.SetOverInItemEvent(self.OverInItem)
		wndItem.SetOverOutItemEvent(self.OverOutItem)
		wndItem.RefreshSlot()
		self.wndItem = wndItem

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		# self.tooltipItem = None
		# self.wndItem = None
		self.currentChest = 0
		self.currentPage = 1
		self.openAmount = 1
		self.invItemPos = -1

	def Open(self, invItemPos = -1):
		self.currentChest = 0
		self.currentPage = 1
		self.openAmount = 1
		self.SetInvItemSlot(invItemPos)
		self.SetTop()
		self.SetCenterPosition()
		self.OnChangeOpenAmount()
		self.Show()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = proxy(tooltip)

	def OnChangeOpenAmount(self):
		selectedItemVNum = player.GetItemIndex(self.invItemPos)
		itemCount = player.GetItemCountByVnum(selectedItemVNum)
		openTemp = int(self.openCountController.GetSliderPos() * itemCount)
		if openTemp == 0:
			self.openAmount = 1
		else:
			self.openAmount = openTemp

		self.openChestButton.SetText("Abrir %d" % self.openAmount)

	def OnClickOpenChest(self):
		selectedItemVNum = player.GetItemIndex(self.invItemPos)
		itemCount = player.GetItemCountByVnum(selectedItemVNum)

		if (self.openAmount == int(1)):
			net.SendItemUsePacket(self.invItemPos)
			self.Close()
			return

		x = 1
		for i in range(player.INVENTORY_PAGE_COUNT * player.INVENTORY_PAGE_SIZE):
			if (selectedItemVNum == player.GetItemIndex(i)) and (x <= self.openAmount):
				net.SendItemUsePacket(i)
				x += 1

		self.Close()
		return

	def OnClickPrevPage(self):
		if constinfo.CHEST_DROP_INFO_DATA[self.currentChest].__contains__(self.currentPage - 1):
			self.currentPage = self.currentPage - 1
			self.currentPageText.SetText(str(self.currentPage))
			self.RefreshItemSlot()

	def OnClickNextPage(self):
		if constinfo.CHEST_DROP_INFO_DATA[self.currentChest].__contains__(self.currentPage + 1):
			self.currentPage = self.currentPage + 1
			self.currentPageText.SetText(str(self.currentPage))
			self.RefreshItemSlot()

	def EnableMultiPage(self):
		self.prevButton.Show()
		self.nextButton.Show()
		self.currentPageBack.Show()

	def EnableSinglePage(self):
		self.prevButton.Hide()
		self.nextButton.Hide()
		self.currentPageBack.Hide()	

	def SetInvItemSlot(self, invItemPos):
		self.invItemPos = invItemPos
		itemVnum = player.GetItemIndex(invItemPos)
		itemCount = player.GetItemCount(invItemPos)
		if itemVnum:
			self.openItemSlot.SetItemSlot(0, itemVnum, itemCount)

	def RefreshItems(self, chestVnum):
		if chestVnum:
			self.currentChest = chestVnum
		if constinfo.CHEST_DROP_INFO_DATA[self.currentChest].__contains__(2):
			self.EnableMultiPage()
		else:
			self.EnableSinglePage()
		self.RefreshItemSlot()

	def RefreshItemSlot(self):
		for i in range(15 * 5):
			self.wndItem.ClearSlot(i)
		if not constinfo.CHEST_DROP_INFO_DATA.__contains__(self.currentChest):
			return
		if not constinfo.CHEST_DROP_INFO_DATA[self.currentChest].__contains__(self.currentPage):
			return
		for key, value in constinfo.CHEST_DROP_INFO_DATA[self.currentChest][self.currentPage].items():
			itemVnum = value[0]
			itemCount = value[1]

			if itemCount <= 1:
				itemCount = 0
			self.wndItem.SetItemSlot(key, itemVnum, itemCount)
		wndMgr.RefreshSlot(self.wndItem.GetWindowHandle())

	def OverInItem(self, slotIndex):
		if mousemodule.mouseController.isAttached():
			return
		if not constinfo.CHEST_DROP_INFO_DATA.__contains__(self.currentChest):
			return
		if not constinfo.CHEST_DROP_INFO_DATA[self.currentChest].__contains__(self.currentPage):
			return
		if 0 != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(constinfo.CHEST_DROP_INFO_DATA[self.currentChest][self.currentPage][slotIndex][0])

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True

# a = ChestDropWindow()
# a.Show()