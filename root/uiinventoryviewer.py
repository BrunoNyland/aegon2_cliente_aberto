#favor manter essa linha
import _player as player
import _app as app
import _chr as chr
import ui
import exception
import constinfo

from weakref import proxy

PAGE_EQUIPMENT = 1
PAGE_INVENTORY = 2

WEAR_MAX_NUM = 13
COSTUME_START_INDEX = 14
COSTUME_MAX_NUM = 4

class CostumeWindow(ui.ScriptWindow):
	def __init__(self, wndInventory):
		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self, "UI_BOTTOM")

		self.isLoaded = 0
		self.wndInventory = wndInventory

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/costumewindow.py")
		except BaseException:
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
		except BaseException:
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		wndEquip.SetOverInItemEvent(self.wndInventory.OverInItemEquipment)
		wndEquip.SetOverOutItemEvent(self.wndInventory.OverOutItem)

		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		for i in range(COSTUME_MAX_NUM):
			slotNumber = COSTUME_START_INDEX + i

			if not self.wndInventory.equipmentItems.__contains__(slotNumber):
				continue

			self.wndEquip.SetItemSlot(slotNumber, self.wndInventory.equipmentItems[slotNumber]["vnum"], 0)

		self.wndEquip.RefreshSlot()

class InventoryMenu(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI_BOTTOM")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/_inventorywindowmenu.py")
		except BaseException:
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

class InventoryWindow(ui.ScriptWindow):
	tooltipItem = None
	wndCostume = None
	interface = None
	InventoryMenu = None

	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.equipmentItems = {}
		self.inventoryItems = {}

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.InventoryMenu.Show()

		self.equipmentItems = {}
		self.inventoryItems = {}

		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

	def BindInterfaceClass(self, interface):
		self.interface = proxy(interface)

	def MenuUpdate(self):
		if self.GetGlobalLeft() < 50:
			self.InventoryMenu.SetPosition(self.GetGlobalLeft() + self.GetWidth() - self.InventoryMenu.GetWidth() + 36, self.GetGlobalTop()+250)
		else:
			self.InventoryMenu.SetPosition(self.GetGlobalLeft()-36, self.GetGlobalTop()+250)

	def CostumeUpdate(self):
		if self.GetGlobalLeft() < 50:
			self.wndCostume.SetPosition(self.GetGlobalLeft() + self.GetWidth() - 15, self.GetGlobalTop() + 45)
		else:
			self.wndCostume.SetPosition(self.GetGlobalLeft() - self.wndCostume.GetWidth() + 15, self.GetGlobalTop() + 45)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1

		self.InventoryMenu = InventoryMenu()
		self.InventoryMenu.OnUpdate = ui.__mem_func__(self.MenuUpdate)

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/_inventorywindow.py")
		except BaseException:
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		wndItem = self.GetChild("ItemSlot")
		wndEquip = self.GetChild("EquipmentSlot")
		self.board = self.GetChild("board")
		self.board.SetCloseEvent(self.Hide)

		self.inventoryTab = []
		self.inventoryTab.append(self.InventoryMenu.GetChild("Inventory_Tab_01"))
		self.inventoryTab.append(self.InventoryMenu.GetChild("Inventory_Tab_02"))
		self.inventoryTab.append(self.InventoryMenu.GetChild("Inventory_Tab_03"))
		self.inventoryTab.append(self.InventoryMenu.GetChild("Inventory_Tab_04"))

		self.inventoryTabR = []
		self.inventoryTabR.append(self.InventoryMenu.GetChild("Inventory_Tab_01_R"))
		self.inventoryTabR.append(self.InventoryMenu.GetChild("Inventory_Tab_02_R"))
		self.inventoryTabR.append(self.InventoryMenu.GetChild("Inventory_Tab_03_R"))
		self.inventoryTabR.append(self.InventoryMenu.GetChild("Inventory_Tab_04_R"))

		wndItem.SetOverInItemEvent(self.OverInItem)
		wndItem.SetOverOutItemEvent(self.OverOutItem)
		wndEquip.SetOverInItemEvent(self.OverInItemEquipment)
		wndEquip.SetOverOutItemEvent(self.OverOutItem)

		self.inventoryTab[0].SetEvent(self.SetInventoryPage, 0)
		self.inventoryTab[1].SetEvent(self.SetInventoryPage, 1)
		self.inventoryTab[2].SetEvent(self.SetInventoryPage, 2)
		self.inventoryTab[3].SetEvent(self.SetInventoryPage, 3)
		self.inventoryTab[0].Disable()

		self.inventoryTabR[0].SetEvent(self.SetInventoryPage, 0)
		self.inventoryTabR[1].SetEvent(self.SetInventoryPage, 1)
		self.inventoryTabR[2].SetEvent(self.SetInventoryPage, 2)
		self.inventoryTabR[3].SetEvent(self.SetInventoryPage, 3)
		self.inventoryTabR[0].Disable()

		self.wndItem = wndItem
		self.wndEquip = wndEquip

		self.GetChild("costume_button").SetEvent(self.ClickCostumeButton)
		self.GetChild("costume_button_hide").SetEvent(self.ClickCostumeButton)

		self.wndCostume = None
		self.SetInventoryPage(0)
		self.RefreshEquipSlotWindow()
		self.RefreshItemSlot()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.interface = None

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

		self.inventoryTab = []

		if self.InventoryMenu:
			self.InventoryMenu.Hide()
			self.InventoryMenu = None

		self.equipmentItems = {}
		self.inventoryItems = {}

	def Hide(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Hide()

		if self.InventoryMenu:
			self.InventoryMenu.Hide()

		ui.ScriptWindow.Hide(self)

	def Open(self, chrVid):
		self.Show()
		self.SetTop()
		self.SetCenterPosition()

		self.board.SetTitle("Itens: %s" % chr.GetNameByVID(chrVid))

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page

		for button in self.inventoryTab:
			button.Enable()
		self.inventoryTab[page].Disable()

		for button in self.inventoryTabR:
			button.Enable()
		self.inventoryTabR[page].Disable()

		self.RefreshBagSlotWindow()

	def ClickCostumeButton(self):
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.GetChild("costume_button").Show()
				self.GetChild("costume_button_hide").Hide()
				self.wndCostume.Hide()
			else:
				self.wndCostume.Show()
				self.GetChild("costume_button").Hide()
				self.GetChild("costume_button_hide").Show()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.OnUpdate = ui.__mem_func__(self.CostumeUpdate)
			self.GetChild("costume_button").Hide()
			self.GetChild("costume_button_hide").Show()
			self.wndCostume.Show()

	def AddItemInInventory(self, pageIndex, slotIndex, itemVnum, itemCount):
		tempDict = { 
			"vnum" : itemVnum,
			"count" : itemCount,
			"socket" : { 0 : 0, 1 : 0, 2 : 0 },
			"attr" : { 0 : [0, 0], 1 : [0, 0], 2 : [0, 0], 3 : [0, 0], 4 : [0, 0], 5 : [0, 0], 5 : [0, 0], 6 : [0, 0] },
			"bind" : 0,
			"renttime" : 0,
		}

		if pageIndex == 1:
			self.equipmentItems[slotIndex] = tempDict
		elif pageIndex == 2:
			self.inventoryItems[slotIndex] = tempDict

		self.RefreshEquipSlotWindow()
		self.RefreshItemSlot()

	def InventoryItemAddSocket(self, pageIndex, slotIndex, socketIndex, socketValue):
		if pageIndex == 1:
			self.equipmentItems[slotIndex]["socket"][socketIndex] = socketValue
		elif pageIndex == 2:
			self.inventoryItems[slotIndex]["socket"][socketIndex] = socketValue

	def InventoryItemAddAttr(self, pageIndex, slotIndex, attrIndex, attrType, attrValue):
		if pageIndex == 1:
			self.equipmentItems[slotIndex]["attr"][attrIndex][0] = attrType
			self.equipmentItems[slotIndex]["attr"][attrIndex][1] = attrValue
		elif pageIndex == 2:
			self.inventoryItems[slotIndex]["attr"][attrIndex][0] = attrType
			self.inventoryItems[slotIndex]["attr"][attrIndex][1] = attrValue

	if app.ENABLE_SOULBIND_SYSTEM:
		def InventoryItemAddBind(self, pageIndex, slotIndex, bind):
			if pageIndex == 1:
				self.equipmentItems[slotIndex]["bind"] = bind
			elif pageIndex == 2:
				self.inventoryItems[slotIndex]["bind"] = bind

	if app.ALUGAR_ITENS:
		def InventoryItemAddRent(self, pageIndex, slotIndex, renttime):
			if pageIndex == 1:
				self.equipmentItems[slotIndex]["renttime"] = renttime
			elif pageIndex == 2:
				self.inventoryItems[slotIndex]["renttime"] = renttime

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		return self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE + local

	def __InventoryGlobalSlotPosToLocalSlotPos(self, globalPos):
		return globalPos - self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	def RefreshBagSlotWindow(self):
		for i in range(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			if not self.inventoryItems.__contains__(slotNumber):
				continue

			itemCount = self.inventoryItems[slotNumber]["count"]

			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue

			elif 1 == itemCount:
				itemCount = 0

			self.wndItem.SetItemSlot(i, self.inventoryItems[slotNumber]["vnum"], itemCount)
			if constinfo.IS_AUTO_POTION(self.inventoryItems[slotNumber]["vnum"]):
				if self.inventoryItems[slotNumber]["socket"][0] > 0:
					self.wndItem.ActivateSlot(slotNumber)
				else:
					self.wndItem.DeactivateSlot(slotNumber)

			if app.ENABLE_ITEM_BLEND_PLUS:
				if self.inventoryItems[slotNumber]["vnum"] in [50821, 50822, 50823, 50824, 50825, 50826]:
					if self.inventoryItems[slotNumber]["socket"][5] == 1:
						self.wndItem.ActivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)
		self.wndItem.RefreshSlot()

	def RefreshEquipSlotWindow(self):
		for slotNumber in range(WEAR_MAX_NUM):
			if not self.equipmentItems.__contains__(slotNumber):
				continue

			itemCount = self.equipmentItems[slotNumber]["count"]

			if itemCount <= 1:
				itemCount = 0

			self.wndEquip.SetItemSlot(200+slotNumber, self.equipmentItems[slotNumber]["vnum"], itemCount)

		self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, slotIndex):
		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(self.inventoryItems[slotIndex]["socket"][i])

		attrSlot = []
		for j in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((self.inventoryItems[slotIndex]["attr"][j][0], self.inventoryItems[slotIndex]["attr"][j][1]))

		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(self.inventoryItems[slotIndex]["vnum"], metinSlot, attrSlot)

			if app.ENABLE_SOULBIND_SYSTEM:
				self.tooltipItem.AppendSealInformation(player.INVENTORY, self.inventoryItems[slotIndex]["bind"])

			if app.ALUGAR_ITENS:
				self.tooltipItem.AppendRentInformation(20, self.inventoryItems[slotIndex]["renttime"])

	def OverInItemEquipment(self, slotIndex):
		slotIndex -= 200
		# chat.AppendChat(chat.CHAT_TYPE_INFO, "slotIndex: %d" % (slotIndex))
		if not self.equipmentItems.__contains__(slotIndex):
			return

		metinSlot = []
		for i in range(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(self.equipmentItems[slotIndex]["socket"][i])

		attrSlot = []
		for j in range(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((self.equipmentItems[slotIndex]["attr"][j][0], self.equipmentItems[slotIndex]["attr"][j][1]))

		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(self.equipmentItems[slotIndex]["vnum"], metinSlot, attrSlot)

			if app.ENABLE_SOULBIND_SYSTEM:
				self.tooltipItem.AppendSealInformation(player.INVENTORY, self.equipmentItems[slotIndex]["bind"])

			if app.ALUGAR_ITENS:
				self.tooltipItem.AppendRentInformation(20, self.equipmentItems[slotIndex]["renttime"])

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

# x = InventoryWindow()
# x.Show()