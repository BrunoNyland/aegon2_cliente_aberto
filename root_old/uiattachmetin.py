#favor manter essa linha
import dbg
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import zn94xlgo573hf8xmddzq as net
import snd
import ui
import uitooltip
import wndMgr

from _weakref import proxy

class AttachMetinDialog(ui.ScriptWindow):
	def __init__(self, wndInventory):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.metinItemPos = 0
		self.targetItemPos = 0
		self.wndInventory = proxy(wndInventory)
		self.lockedItems = {i:(-1,-1) for i in range(2)}

	def __LoadScript(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/attachstonedialog.py")

		self.board = self.GetChild("Board")
		self.metinImage = self.GetChild("MetinImage")
		self.GetChild("AcceptButton").SetEvent(self.Accept)
		self.GetChild("CancelButton").SetEvent(self.Close)

		newToolTip = uitooltip.ItemToolTip()
		newToolTip.SetParent(self)
		newToolTip.SetPosition(3, 34)
		newToolTip.SetFollow(False)
		newToolTip.Show()
		self.newToolTip = newToolTip

		self.board.SetCloseEvent(self.Close)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.board = 0
		self.toolTip = 0
		self.wndInventory = 0
		self.newToolTip = 0

	def CanAttachMetin(self, slot, metin):
		if item.METIN_NORMAL == metin:
			if player.METIN_SOCKET_TYPE_SILVER == slot or player.METIN_SOCKET_TYPE_GOLD == slot:
				return True
		elif item.METIN_GOLD == metin:
			if player.METIN_SOCKET_TYPE_GOLD == slot:
				return True

	def Open(self, metinItemPos, targetItemPos):
		self.metinItemPos = metinItemPos
		self.targetItemPos = targetItemPos

		metinIndex = player.GetItemIndex(metinItemPos)
		itemIndex = player.GetItemIndex(targetItemPos)

		self.newToolTip.ClearToolTip()
		item.SelectItem(metinIndex)

		item.SelectItem(metinIndex)
		metinSubType = item.GetItemSubType()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			slotData = metinSlot[i]
			if self.CanAttachMetin(slotData, metinSubType):
				metinSlot[i] = metinIndex
				break
		self.newToolTip.AddItemData(itemIndex, metinSlot)

		self.UpdateDialog()
		self.SetTop()
		self.Show()
 
		self.SetCantMouseEventSlot(0, self.metinItemPos)
		self.SetCantMouseEventSlot(1, self.targetItemPos)

	def UpdateDialog(self):
		newWidth = self.newToolTip.GetWidth() + 6
		newHeight = self.newToolTip.GetHeight() + 98
		self.GetChild("horizontalseparator").SetWidth(newWidth-14)
		self.board.SetSize(newWidth, newHeight)
		self.SetSize(newWidth, newHeight)

		xMouse, yMouse = wndMgr.GetMousePosition()
		if xMouse < wndMgr.GetScreenWidth()/2:
			self.SetPosition(min(max(0, xMouse+5), wndMgr.GetScreenWidth()-newWidth), min(max(0, yMouse-newHeight/2), wndMgr.GetScreenHeight()-newHeight-40))
		else:
			self.SetPosition(min(max(0, xMouse-newWidth-5), wndMgr.GetScreenWidth()-newWidth), min(max(0, yMouse-newHeight/2), wndMgr.GetScreenHeight()-newHeight-40))

	def Accept(self):
		net.SendItemUseToItemPacket(self.metinItemPos, self.targetItemPos)
		snd.PlaySound("sound/ui/metinstone_insert.wav")
		self.Close()

	def Close(self):
		self.Hide()
		self.SetCanMouseEventSlot(0, self.metinItemPos)
		self.SetCanMouseEventSlot(1, self.targetItemPos)

	def SetCanMouseEventSlot(self, what, slotIndex):
		itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
		localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
		self.lockedItems[what] = (-1, -1)

		if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
			self.wndInventory.wndItem.SetCanMouseEventSlot(localSlotPos)

	def SetCantMouseEventSlot(self, what, slotIndex):
		itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
		localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
		self.lockedItems[what] = (itemInvenPage, localSlotPos)

		if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
			self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

	def RefreshLockedSlot(self):
		if self.wndInventory:
			for what, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

			self.wndInventory.wndItem.RefreshSlot()

# a = AttachMetinDialog(None)
# a.Open(45, 46)