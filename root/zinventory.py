#favor manter essa linha
import ga3vqy6jtxqi9yf344j7 as player
import zn94xlgo573hf8xmddzq as net
import enszxc3467hc3kokdueq as app
import XXjvumrgrYBZompk3PS8 as item
import LURMxMaKZJqliYt2QSHG as chat
import Js4k2l7BrdasmVRt8Wem as chr

import snd
import ime
import exception
import mousemodule

import constinfo
import localeinfo

import ui
import uicommon
import uipicketc
import uiattachmetin
import uiofflineshop
import uiofflineshopbuilder
import uiprivateshopbuilder
import wait

from _weakref import proxy

ITEM_FLAG_APPLICABLE = 1 << 13

class CostumeWindow(ui.ScriptWindow):
	def __init__(self, wndInventory):
		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self, "UI_BOTTOM")

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/_costumewindow.py")

		wndEquip = self.GetChild("CostumeSlot")
		wndEquip.SetOverInItemEvent(self.wndInventory.OverInItem)
		wndEquip.SetOverOutItemEvent(self.wndInventory.OverOutItem)
		wndEquip.SetUnselectItemSlotEvent(self.wndInventory.UseItemSlot)
		wndEquip.SetUseSlotEvent(self.wndInventory.UseItemSlot)
		wndEquip.SetSelectEmptySlotEvent(self.wndInventory.SelectEmptySlot)
		wndEquip.SetSelectItemSlotEvent(self.wndInventory.SelectItemSlot)
		self.wndEquip = wndEquip

	def RefreshCostumeSlot(self):
		getItemVNum = player.GetItemIndex

		for i in range(item.COSTUME_SLOT_COUNT):
			slotNumber = item.COSTUME_SLOT_START + i
			self.wndEquip.SetItemSlot(slotNumber, getItemVNum(slotNumber), 0)

		self.wndEquip.RefreshSlot()

class InventoryMenu(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI_BOTTOM")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/_inventorywindowmenu.py")

class InventoryWindow(ui.ScriptWindow):
	USE_TYPE_TUPLE = (
		"USE_CLEAN_SOCKET",
		"USE_CHANGE_ATTRIBUTE",
		"USE_ADD_ATTRIBUTE",
		"USE_ADD_ATTRIBUTE2",
		"USE_ADD_ACCESSORY_SOCKET",
		"USE_PUT_INTO_ACCESSORY_SOCKET",
		"USE_PUT_INTO_BELT_SOCKET",
		"USE_BIND",
		"USE_UNBIND",
	)

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	dlgPickItem = None
	interface = None
	InventoryMenu = None
	eventClickBot = None
	eventClickAtlas = None
	eventClickReturn = None

	bindWnds = []
	sellingSlotNumber = -1
	isLoaded = 0
	isOpenedCostumeWindowWhenClosingInventory = 0

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		self.uiofflineshopWnd = uiofflineshop.OfflineShopAdminPanelWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.InventoryMenu.Show()
## TROCAR FUNDO DA IMAGEM PELO SEXO
		race = net.GetMainActorRace()
		sex = chr.RaceToSex(race)
		if sex == 0:
			self.GetChild("Equipment_Base").LoadImage("interface/controls/special/inventory/inventory_w.tga")
			self.GetChild("Equipment_Base").Show()
		elif sex == 1:
			self.GetChild("Equipment_Base").LoadImage("interface/controls/special/inventory/inventory_m.tga")
			self.GetChild("Equipment_Base").Show()
## FIM TROCAR FUNDO DA IMAGEM PELO SEXO
		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def BindWindow(self, wnd):
		self.bindWnds.append(proxy(wnd))

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

## TROCAR FUNDO DA IMAGEM PELO SEXO
		race = net.GetMainActorRace()
		sex = chr.RaceToSex(race)
		if sex == 0:
			self.GetChild("Equipment_Base").LoadImage("interface/controls/special/inventory/inventory_w.tga")
			self.GetChild("Equipment_Base").Show()
		elif sex == 1:
			self.GetChild("Equipment_Base").LoadImage("interface/controls/special/inventory/inventory_m.tga")
			self.GetChild("Equipment_Base").Show()
## FIM TROCAR FUNDO DA IMAGEM PELO SEXO

		wndItem.SetSelectEmptySlotEvent(self.SelectEmptySlot)
		wndItem.SetSelectItemSlotEvent(self.SelectItemSlot)
		wndItem.SetUnselectItemSlotEvent(self.UseItemSlot)
		wndItem.SetUseSlotEvent(self.UseItemSlot)
		wndItem.SetOverInItemEvent(self.OverInItem)
		wndItem.SetOverOutItemEvent(self.OverOutItem)

		wndEquip.SetSelectEmptySlotEvent(self.SelectEmptySlot)
		wndEquip.SetSelectItemSlotEvent(self.SelectItemSlot)
		wndEquip.SetUnselectItemSlotEvent(self.UseItemSlot)
		wndEquip.SetUseSlotEvent(self.UseItemSlot)
		wndEquip.SetOverInItemEvent(self.OverInItem)
		wndEquip.SetOverOutItemEvent(self.OverOutItem)

		dlgPickItem = uipicketc.PickEtcDialog()
		dlgPickItem.LoadDialog()
		dlgPickItem.Hide()

		self.attachMetinDialog = uiattachmetin.AttachMetinDialog(self)
		self.BindWindow(self.attachMetinDialog)
		self.attachMetinDialog.Hide()

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

		if app.ALUGAR_ITENS:
			self.InventoryMenu.GetChild("Rent").SetEvent(self.GetRentItems)
			self.InventoryMenu.GetChild("Rent_R").SetEvent(self.GetRentItems)

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickItem = dlgPickItem

		self.GetChild("costume_button").SetEvent(self.ClickCostumeButton)
		self.GetChild("costume_button_hide").SetEvent(self.ClickCostumeButton)

		self.InventoryMenu.GetChild("Trash").SetMouseLeftButtonDownEvent(self.Add_Item)
		self.InventoryMenu.GetChild("Trash").SetOverInEvent(self.OverBorrarIn)
		self.InventoryMenu.GetChild("Trash").SetOverOutEvent(self.OverBorrarOut)

		self.InventoryMenu.GetChild("Trash_R").SetMouseLeftButtonDownEvent(self.Add_Item)
		self.InventoryMenu.GetChild("Trash_R").SetOverInEvent(self.OverBorrarIn)
		self.InventoryMenu.GetChild("Trash_R").SetOverOutEvent(self.OverBorrarOut)

		self.wndCostume = None
		self.movedSlot = -1
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		self.media = float((380 - 260)/10)

		self.SetOnRunMouseWheelEvent(self.OnRunMouseWheel)

		self.Delay = None

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

		self.bindWnds = []

		self.dlgPickItem.Destroy()
		self.dlgPickItem = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickItem = 0
		self.questionDialog = None
		self.interface = None

		eventClickBot = None
		eventClickAtlas = None
		eventClickReturn = None

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

		if self.uiofflineshopWnd:
			self.uiofflineshopWnd.Hide()
			self.uiofflineshopWnd = None

		self.inventoryTab = []

		if self.InventoryMenu:
			self.InventoryMenu.Hide()
			self.InventoryMenu = None

		self.Delay = None

	def Hide(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()
 
		self.OnCloseQuestionDialog()

		if self.dlgPickItem:
			self.dlgPickItem.Close()

		if self.InventoryMenu:
			self.InventoryMenu.Hide()

		ui.ScriptWindow.Hide(self)

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.SetInventoryPage(max(0, self.inventoryPageIndex - 1))
		else:
			self.SetInventoryPage(min(3, self.inventoryPageIndex + 1))

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

	if app.ALUGAR_ITENS:
		def GetRentItems(self):
			if self.Delay == None:
				net.SendChatPacket("/get_rent_items")
				self.Delay = wait.WaitingDialog()
				self.Delay.Open(30.0)
				self.Delay.SetTimeOverEvent(self.EnableGetRentItems)
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Voce nao possui nenhum item para resgatar neste momento.")

		def EnableGetRentItems(self):
			self.Delay = None

	def SetEventClickBot(self, event = None):
		if event:
			self.eventClickBot = ui.__mem_func__(event)
		else:
			self.eventClickBot = None

	def SetEventClickAtlas(self, event = None):
		if event:
			self.eventClickAtlas = ui.__mem_func__(event)
		else:
			self.eventClickAtlas = None

	def SetEventClickReturn(self, event = None):
		if event:
			self.eventClickReturn = ui.__mem_func__(event)
		else:
			self.eventClickReturn = None

	def ClickOfflineShopButton(self):
		self.uiofflineshopWnd.Show()

	def OverBorrarIn(self):
		if mousemodule.mouseController.isAttached():
			self.InventoryMenu.GetChild("Trash").LoadImage("interface/controls/special/inventory/trash_over.tga")
			self.InventoryMenu.GetChild("Trash").Show()
			self.InventoryMenu.GetChild("Trash_R").LoadImage("interface/controls/special/inventory/trash_over.tga")
			self.InventoryMenu.GetChild("Trash_R").Show()
		else:
			self.InventoryMenu.GetChild("Trash").LoadImage("interface/controls/special/inventory/trash_over.tga")
			self.InventoryMenu.GetChild("Trash").Show()
			self.InventoryMenu.GetChild("Trash_R").LoadImage("interface/controls/special/inventory/trash_over.tga")
			self.InventoryMenu.GetChild("Trash_R").Show()

	def OverBorrarOut(self):
		self.InventoryMenu.GetChild("Trash").LoadImage("interface/controls/special/inventory/trash_normal.tga")
		self.InventoryMenu.GetChild("Trash").Show()
		self.InventoryMenu.GetChild("Trash_R").LoadImage("interface/controls/special/inventory/trash_normal.tga")
		self.InventoryMenu.GetChild("Trash_R").Show()

	def Add_Item(self):
		if mousemodule.mouseController.isAttached():
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			attachedSlotVnum = mousemodule.mouseController.GetAttachedItemIndex()
			itemCount = player.GetItemCount(attachedSlotPos)
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(1)
				item.SelectItem(attachedSlotVnum)
				self.RemoveQuestion = uicommon.ItemQuestionDialog()
				self.RemoveQuestion.window_type = "inv"
				self.RemoveQuestion.count = itemCount
				self.RemoveQuestion.SetCancelEvent(self.Borrar_cancel)
				self.RemoveQuestion.SetAcceptEvent(self.Borrar_Item, attachedSlotPos)
				self.RemoveQuestion.SetText("Deseja remover este item permanentemente do seu inventário?")
				self.RemoveQuestion.Open(attachedSlotVnum, attachedSlotPos)
			mousemodule.mouseController.DeattachObject()
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Arraste um item para a lixeira caso queira deletar.")

	def Borrar_Item(self, arg):
		net.SendChatPacket("/deleteitem " + str(arg))
		self.RemoveQuestion.Close()
		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

	def Borrar_cancel(self):
		self.RemoveQuestion.Close()
		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickItem.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(itemSlotIndex)
		mousemodule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local):
			return local
		return self.inventoryPageIndex * player.INVENTORY_PAGE_SIZE + local

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	def RefreshMarkSlots(self, localIndex = None):
		if not self.interface:
			return

		onTopWnd = self.interface.GetOnTopWindow()
		if localIndex:
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(localIndex)
			if onTopWnd == player.ON_TOP_WND_NONE:
				self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

			elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
					self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)
			return

		for i in range(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			if onTopWnd == player.ON_TOP_WND_NONE:
				self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
				if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

			elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
				if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
					self.wndItem.SetUnusableSlotOnTopWnd(i)
				else:
					self.wndItem.SetUsableSlotOnTopWnd(i)

	def RefreshGold(self):
		money = player.GetElk()
		self.GetChild("Money").SetText(localeinfo.NumberToMoneyString(money) + " Gold")

		# masc = money/100000000
		# if masc < 1:
		# 	self.GetChild("tooltip_gold").SetText("Apróx. %d Máscara da Fortuna" % (masc))
		# else:
		# 	self.GetChild("tooltip_gold").SetText("Apróx. %d Máscaras da Fortuna" % (masc))

	def RefreshBagSlotWindow(self):
		is_activated = 0
		getItemVNum = player.GetItemIndex
		getItemCount = player.GetItemCount
		setItemVNum = self.wndItem.SetItemSlot

		for i in range(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)

			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue

			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			setItemVNum(i, itemVnum, itemCount)
			self.wndItem.EnableCoverButton(i)

			if constinfo.IS_AUTO_POTION(itemVnum):
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in range(player.METIN_SOCKET_MAX_NUM)]

				if slotNumber >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					slotNumber -= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex

				isActivated = 0 != metinSocket[0]

				if isActivated:
					self.wndItem.ActivateSlot(slotNumber)
					potionType = 0;
					if constinfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constinfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP
					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])
					player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
				else:
					self.wndItem.DeactivateSlot(slotNumber)

			if app.ENABLE_ITEM_BLEND_PLUS:
				if itemVnum in [50821, 50822, 50823, 50824, 50825, 50826]:
					if player.GetItemMetinSocket(slotNumber, 5) == 1:
						self.wndItem.ActivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)

			self.RefreshMarkSlots(i)

		self.wndItem.RefreshSlot()

		to_delete = []
		for wnd in self.bindWnds:
			try:
				wnd.RefreshLockedSlot()
			except BaseException:
				to_delete.append(wnd)

		for wnd in to_delete:
			self.bindWnds.remove(wnd)

	def RefreshEquipSlotWindow(self):
		getItemVNum = player.GetItemIndex
		getItemCount = player.GetItemCount
		setItemVNum = self.wndEquip.SetItemSlot
		for i in range(player.EQUIPMENT_SLOT_START, player.EQUIPMENT_SLOT_START+16):
			slotNumber = i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

		self.wndEquip.RefreshSlot()

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def SellItem(self):
		net.SendShopSellPacket(self.sellingSlotNumber, self.questionDialog.count)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	def SelectEmptySlot(self, selectedSlotPos):
		if constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS():
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mousemodule.mouseController.isAttached():
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mousemodule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mousemodule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mousemodule.mouseController.GetAttachedItemCount()
				self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mousemodule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_OFFLINE_SHOP == attachedSlotType:
				mousemodule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mousemodule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")
				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif app.ENABLE_GUILD_SAFEBOX and player.SLOT_TYPE_GUILD_SAFEBOX == attachedSlotType:
				net.SendGuildSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			mousemodule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS():
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if mousemodule.mouseController.isAttached():
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mousemodule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedSlotPos, itemSlotIndex)
			mousemodule.mouseController.DeattachObject()
		else:
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SHOP_BUY_INFO)
			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)
			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(itemSlotIndex)
				if itemCount > 1:
					self.dlgPickItem.SetTitleName(localeinfo.PICK_ITEM_TITLE)
					self.dlgPickItem.SetAcceptEvent(self.OnPickItem)
					self.dlgPickItem.Open(itemCount)
					self.dlgPickItem.itemGlobalSlotIndex = itemSlotIndex
			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)
				if item.CanAddToQuickSlotItem(itemIndex) and not constinfo.IS_ITEM_BUG_IN_TASKBAR(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.QUICKSLOT_REGISTER_DISABLE_ITEM)
			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mousemodule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)
				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if srcItemSlotPos == dstItemSlotPos:
			return
		elif srcItemVID == player.GetItemIndex(dstItemSlotPos):
			self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
			return

		if app.ENABLE_SOULBIND_SYSTEM:
			SrcItemVNum = player.GetItemIndex(srcItemSlotPos)
			DstItemVNum = player.GetItemIndex(dstItemSlotPos)
			item.SelectItem(SrcItemVNum)
			SrcSubType = item.GetItemSubType()
			if SrcSubType == item.USE_BIND or SrcSubType == item.USE_UNBIND:
				item.SelectItem(DstItemVNum)
				if item.IsAntiFlag(item.ANTIFLAG_BIND):
					return
				else:
					if SrcSubType == item.USE_BIND and player.GetItemBind(dstItemSlotPos) > 1:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SOULBIND_ALERT3)
					elif SrcSubType == item.USE_BIND and player.GetItemBind(dstItemSlotPos) == 1:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SOULBIND_ALERT2)
					elif SrcSubType == item.USE_UNBIND and player.GetItemBind(dstItemSlotPos) > 1:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SOULBIND_ALERT3)
					elif SrcSubType == item.USE_UNBIND and player.GetItemBind(dstItemSlotPos) != 1:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SOULBIND_ALERT1)
					else:
						action = "bind"
						if SrcSubType == item.USE_UNBIND:
							action = "unbind"
						self.__SoulBindItem(srcItemSlotPos, dstItemSlotPos, action)
					return
			else:
				if item.IsRefineScroll(srcItemVID):
					self.RefineItem(srcItemSlotPos, dstItemSlotPos)
					self.wndItem.SetUseMode(False)
				elif item.IsMetin(srcItemVID):
					self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)
				elif item.IsDetachScroll(srcItemVID):
					self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)
				elif item.IsKey(srcItemVID):
					self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
				elif (srcItemVID == 71052 or srcItemVID == 71051 or srcItemVID == 70070 or srcItemVID == 70069 or srcItemVID == 79904 or srcItemVID == 79903):
					self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
				elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
					self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
				elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
					self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
				else:
					if player.IsEquipmentSlot(dstItemSlotPos):
						if item.IsEquipmentVID(srcItemVID):
							self.__UseItem(srcItemSlotPos)
					else:
						self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
		else:
			if item.IsRefineScroll(srcItemVID):
				self.RefineItem(srcItemSlotPos, dstItemSlotPos)
				self.wndItem.SetUseMode(False)
			elif item.IsMetin(srcItemVID):
				self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)
			elif item.IsDetachScroll(srcItemVID):
				self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)
			elif item.IsKey(srcItemVID):
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
			elif (srcItemVID == 71052 or srcItemVID == 71051 or srcItemVID == 70070 or srcItemVID == 70069 or srcItemVID == 79904 or srcItemVID == 79903):
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
			elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
			elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
				self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)
			else:
				if player.IsEquipmentSlot(dstItemSlotPos):
					if item.IsEquipmentVID(srcItemVID):
						self.__UseItem(srcItemSlotPos)
				else:
					self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(itemSlotPos)
			itemCount = player.GetItemCount(itemSlotPos)
			item.SelectItem(itemIndex)
			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice / 5
			else:
				itemPrice = itemPrice * itemCount / 5

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uicommon.ItemQuestionDialog()
			self.questionDialog.window_type = "inv"
			self.questionDialog.count = itemCount
			if itemCount > 1:
				self.questionDialog.SetText("Deseja realmente vender estes itens pelo valor abaixo?")
			else:
				self.questionDialog.SetText("Deseja realmente vender este item pelo valor abaixo?")
			self.questionDialog.SetAcceptEvent(self.SellItem)
			self.questionDialog.SetCancelEvent(self.OnCloseQuestionDialog)
			self.questionDialog.Open(itemIndex, itemSlotPos, itemPrice)

	def RefineItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_NO_MORE_SOCKET)
		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_NEED_BETTER_SCROLL)
		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)
		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)
		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_EQUIP_ITEM)
		if player.REFINE_OK != result:
			return

		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		return

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if not player.CanDetach(scrollIndex, targetSlotPos):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

		self.questionDialog = uicommon.QuestionDialog()
		self.questionDialog.SetText(localeinfo.REFINE_DO_YOU_SEPARATE_METIN)
		self.questionDialog.SetAcceptEvent(self.OnDetachMetinFromItem)
		self.questionDialog.SetCancelEvent(self.OnCloseQuestionDialog)
		self.questionDialog.Open()
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_NO_SOCKET(itemName))
		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))
		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)

	def OverOutItem(self):
		if self.wndItem:
			self.wndItem.SetUsableItem(False)
			self.wndItem.SetUsableItem2(False)

		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		slotPos = overSlotPos
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)
		self.wndItem.SetUsableItem2(False)

		if mousemodule.mouseController.isAttached():
			attachedItemType = mousemodule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mousemodule.mouseController.GetAttachedItemIndex()

				if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
					self.wndItem.SetUsableItem2(True)
					self.ShowToolTip(overSlotPos)
					return
				else:
					srcItem = player.GetItemIndex(attachedSlotPos)
					item.SelectItem(srcItem)
					item1_size = str(item.GetItemSize())
 
					dstItem = player.GetItemIndex(overSlotPos)
					item.SelectItem(dstItem)
					item2_size = str(item.GetItemSize())

					if item2_size == item1_size:
						if attachedSlotPos != overSlotPos:
							self.wndItem.SetUsableItem2(True)
							self.ShowToolTip(overSlotPos)
							return

					if item1_size == "(1, 2)":
						if attachedSlotPos != overSlotPos:
							if item2_size == "(1, 1)":
								second_item = player.GetItemIndex(overSlotPos+5)
								item.SelectItem(second_item)
								second_item_size = str(item.GetItemSize())
								if second_item_size != "(1, 2)" and second_item_size != "(1, 3)":
									self.wndItem.SetUsableItem2(True)
									self.ShowToolTip(overSlotPos)
									return

					if item1_size == "(1, 3)":
						if attachedSlotPos != overSlotPos:
							if item2_size == "(1, 1)":
								second_item = player.GetItemIndex(overSlotPos+5)
								item.SelectItem(second_item)
								second_item_size = str(item.GetItemSize())

								if second_item_size != "(1, 3)":
									third_item = player.GetItemIndex(overSlotPos+10)
									item.SelectItem(third_item)
									third_item_size = str(item.GetItemSize())

									if third_item_size != "(1, 2)" and third_item_size != "(1, 3)":
										self.wndItem.SetUsableItem2(True)
										self.ShowToolTip(overSlotPos)
										return
							elif item2_size == "(1, 2)":
								second_item = player.GetItemIndex(overSlotPos+10)
								item.SelectItem(second_item)
								second_item_size = str(item.GetItemSize())

								if second_item_size != "(1, 2)" and second_item_size != "(1, 3)":
									self.wndItem.SetUsableItem2(True)
									self.ShowToolTip(overSlotPos)
									return

		if self.wndItem and self.wndItem.IsIn():
			self.ShowToolTip(overSlotPos)
		elif self.wndEquip and self.wndEquip.IsIn():
			self.ShowToolTip(overSlotPos)
		elif self.wndCostume and self.wndCostume.wndEquip and self.wndCostume.wndEquip.IsIn():#Fix for Tooltip
			self.ShowToolTip(overSlotPos)

	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		if srcItemVNum == 71052 or srcItemVNum == 71051 or srcItemVNum == 70070 or srcItemVNum == 70069 or srcItemVNum == 79904 or srcItemVNum == 79903:
			return True

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True
		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos:
			return False

		if srcItemVNum == 71052 or srcItemVNum == 71051 or srcItemVNum == 70070 or srcItemVNum == 70069 or srcItemVNum == 79904 or srcItemVNum == 79903:
			return True

		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True

		if srcItemVNum == player.GetItemIndex(dstSlotPos):
			if player.GetItemCount(dstSlotPos) < 200:
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			useType = item.GetUseType(srcItemVNum)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVNum)
				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			elif useType == "USE_BIND" or useType == "USE_UNBIND":
				if not app.ENABLE_SOULBIND_SYSTEM:
					return False
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVNum)
				if item.IsAntiFlag(item.ANTIFLAG_BIND):
					return False
				elif useType == "USE_BIND" and player.GetItemBind(dstSlotPos) == 1:
					return False
				elif useType == "USE_BIND" and player.GetItemBind(dstSlotPos) > 1:
					return False
				elif useType == "USE_UNBIND" and player.GetItemBind(dstSlotPos) != 1:
					return False
				else:
					return True
		return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)
		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in range(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constinfo.ERROR_METIN_STONE:
				return True
		return False

	if app.ENABLE_SOULBIND_SYSTEM:
		def __SoulBindItem(self, scrollSlotPos, targetSlotPos, action = "bind"):
			DstItemVNum = player.GetItemIndex(targetSlotPos)
			item.SelectItem(DstItemVNum)
			item_name = item.GetItemName()
			self.questionDialog = uicommon.ItemQuestionDialog()
			if action == "bind":
				self.questionDialog.SetText(localeinfo.SOULBIND_ITEM % (item_name))
			else:
				self.questionDialog.SetText(localeinfo.SOULUNBIND_ITEM % (item_name))
			self.questionDialog.SetAcceptEvent(self.OnAcceptSoulBindItem)
			self.questionDialog.SetCancelEvent(self.OnCloseQuestionDialog)
			self.questionDialog.window_type = "inv"
			self.questionDialog.Open(DstItemVNum, targetSlotPos)
			self.questionDialog.sourcePos = scrollSlotPos
			self.questionDialog.targetPos = targetSlotPos

		def OnAcceptSoulBindItem(self):
			if self.questionDialog == None:
				return
			self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
			self.OnCloseQuestionDialog()

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):	 
			return False

		for i in range(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if mtrlVnum != constinfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False
		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		attrCount = 0
		for i in range(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount < 4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

		to_delete = []
		for wnd in self.bindWnds:
			try:
				wnd.RefreshLockedSlot()
			except BaseException:
				to_delete.append(wnd)

		for wnd in to_delete:
			self.bindWnds.remove(wnd)

		self.RefreshMarkSlots()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def UseItemSlot(self, slotIndex):
		if constinfo.GET_ITEM_DROP_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		self.__UseItem(slotIndex)
		mousemodule.mouseController.DeattachObject()
		self.OverOutItem()

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		ItemCount = player.GetItemCount(slotIndex)
		item.SelectItem(ItemVNum)

		if item.IsEquipmentVID(ItemVNum) and player.IsSitting():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Levante seu personagem para trocar os equipamentos.")
			return

		if ItemVNum == 70066 and self.eventClickBot != None:
			self.eventClickBot()
			return
		if ItemVNum == 70067 and self.eventClickAtlas != None:
			self.eventClickAtlas()
			return
		if ItemVNum == 70068 and self.eventClickReturn != None:
			self.eventClickReturn()
			return
		if ItemVNum == 31037:
			self.ClickOfflineShopButton()
			return

		#bloqueio do mouse para uso de pote regenerador
		if ItemVNum in [70020, 98902, 76000]:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "|cfff8d090[Aegon2] |cffff9999Utilize o Sistema de AutoPote")
			return

		#protecao anel de xp
		if (ItemVNum == 70005) and (ItemCount > 1):
			self.questionDialog = uicommon.QuestionDialog()
			self.questionDialog.SetText(localeinfo.INVENTORY_ANEL_XP)
			self.questionDialog.SetAcceptEvent(self.__UseItemQuestionDialog_OnCancel)
			self.questionDialog.SetCancelEvent(self.__UseItemQuestionDialog_OnCancel)
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex
			return

		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uicommon.QuestionDialog()
			self.questionDialog.SetText(localeinfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(self.__UseItemQuestionDialog_OnAccept)
			self.questionDialog.SetCancelEvent(self.__UseItemQuestionDialog_OnCancel)
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex
			return

		if app.ENABLE_DROP_COFRE:
			if player.GetItemTypeBySlot(slotIndex) == item.ITEM_TYPE_GIFTBOX:
				if self.interface:
					if self.interface.dlgChestDrop:
						if not self.interface.dlgChestDrop.IsShow():
							self.interface.dlgChestDrop.Open(slotIndex)
							net.SendChestDropInfo(slotIndex)
							return

		self.__SendUseItemPacket(slotIndex)

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		if uiprivateshopbuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if (uiofflineshopbuilder.IsBuildingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if (uiofflineshop.IsEditingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
			return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		if uiprivateshopbuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if (uiofflineshopbuilder.IsBuildingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if (uiofflineshop.IsEditingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.USE_ITEM_FAILURE_OFFLINE_SHOP)
			return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if uiprivateshopbuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if (uiofflineshopbuilder.IsBuildingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.MOVE_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if (uiofflineshop.IsEditingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.MOVE_ITEM_FAILURE_OFFLINE_SHOP)
			return

		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

# b = InventoryMenu()
# b.Show()

# a = InventoryWindow()
# a.Show()