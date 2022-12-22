#favor manter essa linha
import ui
import mousemodule
import ga3vqy6jtxqi9yf344j7 as player
import zn94xlgo573hf8xmddzq as net
import snd
import safebox
import LURMxMaKZJqliYt2QSHG as chat
import enszxc3467hc3kokdueq as app
import localeinfo

from _weakref import proxy

class PasswordDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.sendMessage = "/safebox_password "
		#Salvar Senha Ao abrir
		self.lastPassword = ""
		#Final Salvar Senha Ao abrir

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/passworddialog.py")
		except:
			import exception
			exception.Abort("PasswordDialog.__LoadDialog.LoadObject")

		try:
			self.passwordValue = self.GetChild("password_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")
			self.GetChild("board").SetCloseEvent(self.CloseDialog)
		except:
			import exception
			exception.Abort("PasswordDialog.__LoadDialog.BindObject")

		self.passwordValue.SetEscapeEvent(self.OnCancel)
		self.passwordValue.SetReturnEvent(self.OnAccept)
		self.acceptButton.SetEvent(self.OnAccept)
		self.cancelButton.SetEvent(self.OnCancel)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.passwordValue = None
		self.acceptButton = None
		self.cancelButton = None

	def SetTitle(self, title):
		self.GetChild("board").SetTitle(title)

	def SetSendMessage(self, msg):
		self.sendMessage = msg

	def ShowDialog(self):
		self.passwordValue.SetText("")
		self.passwordValue.SetFocus()
		self.SetCenterPosition()
		self.Show()

	def CloseDialog(self):
		self.passwordValue.KillFocus()
		self.Hide()

	#Salvar Senha Ao abrir
	# def OnAccept(self):
		# net.SendChatPacket(self.sendMessage + self.passwordValue.GetText())
		# self.CloseDialog()
		# return True
	def OnAccept(self):
		self.lastPassword = str(self.passwordValue.GetText())
		net.SendChatPacket(self.sendMessage + self.lastPassword)
		self.CloseDialog()
		return True

	def InitSafeboxPassword(self):
		self.lastPassword = ""

	def GetSafeboxPwd(self):
		return self.lastPassword
	#Final Salvar Senha Ao abrir

	def OnCancel(self):
		self.CloseDialog()
		return True

class ChangePasswordDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.dlgMessage = ui.ScriptWindow()
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgMessage, "uiscript/popupdialog.py")
			self.dlgMessage.GetChild("message").SetText(localeinfo.SAFEBOX_WRONG_PASSWORD)
			self.dlgMessage.GetChild("accept").SetEvent(self.OnCloseMessageDialog)
		except:
			import exception
			exception.Abort("SafeboxWindow.__LoadDialog.LoadObject")

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/changepassworddialog.py")

		except:
			import exception
			exception.Abort("ChangePasswordDialog.LoadDialog.LoadObject")

		try:
			self.GetChild("accept_button").SetEvent(self.OnAccept)
			self.GetChild("cancel_button").SetEvent(self.OnCancel)
			self.GetChild("board").SetCloseEvent(self.OnCancel)
			oldPassword = self.GetChild("old_password_value")
			newPassword = self.GetChild("new_password_value")
			newPasswordCheck = self.GetChild("new_password_check_value")
		except:
			import exception
			exception.Abort("ChangePasswordDialog.LoadDialog.BindObject")

		oldPassword.SetTabEvent(self.OnNextFocus, 1)
		newPassword.SetTabEvent(self.OnNextFocus, 2)
		newPasswordCheck.SetTabEvent(self.OnNextFocus, 3)
		oldPassword.SetReturnEvent(self.OnNextFocus, 1)
		newPassword.SetReturnEvent(self.OnNextFocus, 2)
		newPasswordCheck.SetReturnEvent(self.OnAccept)
		oldPassword.SetEscapeEvent(self.OnCancel)
		newPassword.SetEscapeEvent(self.OnCancel)
		newPasswordCheck.SetEscapeEvent(self.OnCancel)

		self.oldPassword = oldPassword
		self.newPassword = newPassword
		self.newPasswordCheck = newPasswordCheck

	def OnNextFocus(self, arg):
		if 1 == arg:
			self.oldPassword.KillFocus()
			self.newPassword.SetFocus()
		elif 2 == arg:
			self.newPassword.KillFocus()
			self.newPasswordCheck.SetFocus()
		elif 3 == arg:
			self.newPasswordCheck.KillFocus()
			self.oldPassword.SetFocus()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.dlgMessage.ClearDictionary()
		self.oldPassword = None
		self.newPassword = None
		self.newPasswordCheck = None

	def Open(self):
		self.oldPassword.SetText("")
		self.newPassword.SetText("")
		self.newPasswordCheck.SetText("")
		# self.oldPassword.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.oldPassword.SetText("")
		self.newPassword.SetText("")
		self.newPasswordCheck.SetText("")
		self.oldPassword.KillFocus()
		self.newPassword.KillFocus()
		self.newPasswordCheck.KillFocus()
		self.Hide()

	def OnAccept(self):
		oldPasswordText = self.oldPassword.GetText()
		newPasswordText = self.newPassword.GetText()
		newPasswordCheckText = self.newPasswordCheck.GetText()
		if newPasswordText != newPasswordCheckText:
			self.dlgMessage.SetCenterPosition()
			self.dlgMessage.SetTop()
			self.dlgMessage.Show()
			return True
		net.SendChatPacket("/safebox_change_password %s %s" % (oldPasswordText, newPasswordText))
		self.Close()
		return True

	def OnCancel(self):
		self.Close()
		return True

	def OnCloseMessageDialog(self):
		self.newPassword.SetText("")
		self.newPasswordCheck.SetText("")
		self.newPassword.SetFocus()
		self.dlgMessage.Hide()

class SafeboxWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.interface = None
		self.sellingSlotNumber = -1
		self.pageButtonList = []
		self.curPageIndex = 0
		self.isLoaded = 0
		self.xSafeBoxStart = 0
		self.ySafeBoxStart = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = None
		self.dlgChangePassword.Destroy()
		self.dlgChangePassword = None

		self.tooltipItem = None
		self.wndMoneySlot = None
		self.wndMoney = None
		self.wndBoard = None
		self.wndItem = None
		self.interface = None

		self.pageButtonList = []

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/safeboxwindow.py")

		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self)
		wndItem.SetPosition(8, 39)
		wndItem.SetSelectEmptySlotEvent(self.SelectEmptySlot)
		wndItem.SetSelectItemSlotEvent(self.SelectItemSlot)
		wndItem.SetUnselectItemSlotEvent(self.UseItemSlot)
		wndItem.SetUseSlotEvent(self.UseItemSlot)
		wndItem.SetOverInItemEvent(self.OverInItem)
		wndItem.SetOverOutItemEvent(self.OverOutItem)
		wndItem.Show()

		import uipickmoney
		dlgPickMoney = uipickmoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(self.OnPickMoney)
		dlgPickMoney.Hide()

		dlgChangePassword = ChangePasswordDialog()
		dlgChangePassword.Hide()

		self.GetChild("ChangePasswordButton").SetEvent(self.OnChangePassword)
		self.GetChild("ExitButton").SetEvent(self.Close)

		self.wndItem = wndItem
		self.dlgPickMoney = dlgPickMoney
		self.dlgChangePassword = dlgChangePassword
		self.wndBoard = self.GetChild("board")
		self.wndBoard.SetCloseEvent(self.Close)
		self.SetTableSize(3)

	def ShowWindow(self, size):
		self.interface.SetOnTopWindow(player.ON_TOP_WND_SAFEBOX)
		self.interface.RefreshMarkInventoryBag()

		(self.xSafeBoxStart, self.ySafeBoxStart, z) = player.GetMainCharacterPosition()

		self.SetTableSize(size)
		self.Show()

	def __MakePageButton(self, pageCount):
		self.curPageIndex = 0
		self.pageButtonList = []

		text = "I"
		pos = -int(float(pageCount-1)/2 * 35)
		for i in xrange(pageCount):
			button = ui.RedButton()
			button.SetParent(self)
			button.SetWidth(27)
			button.SetWindowHorizontalAlignCenter()
			button.SetWindowVerticalAlignBottom()
			button.SetPosition(pos, 85)
			button.SetText(text)
			button.SetEvent(self.SelectPage, i)
			button.Show()
			self.pageButtonList.append(button)

			pos += 35
			text += "I"

		self.pageButtonList[0].Disable()

	def SelectPage(self, index):
		self.curPageIndex = index

		for btn in self.pageButtonList:
			btn.Enable()

		self.pageButtonList[index].Disable()
		self.RefreshSafebox()

	def __LocalPosToGlobalPos(self, local):
		return self.curPageIndex*safebox.SAFEBOX_PAGE_SIZE + local

	def SetTableSize(self, size):
		pageCount = max(1, size / safebox.SAFEBOX_SLOT_Y_COUNT)
		pageCount = min(3, pageCount)
		size = safebox.SAFEBOX_SLOT_Y_COUNT

		self.__MakePageButton(pageCount)

		self.wndItem.ArrangeSlot(0, safebox.SAFEBOX_SLOT_X_COUNT, size, 32, 32, 0, 0)
		self.wndItem.RefreshSlot()
		self.wndItem.SetSlotBaseImage("interface/controls/common/slot_rectangle/slot.tga", 1.0, 1.0, 1.0, 1.0)

		wnd_height = 130 + 32 * size
		self.UpdateRect()

	def RefreshSafebox(self):
		getItemID=safebox.GetItemID
		getItemCount=safebox.GetItemCount
		setItemID=self.wndItem.SetItemSlot

		for i in xrange(safebox.SAFEBOX_PAGE_SIZE):
			slotIndex = self.__LocalPosToGlobalPos(i)
			itemCount = getItemCount(slotIndex)
			if itemCount <= 1:
				itemCount = 0
			setItemID(i, getItemID(slotIndex), itemCount)

		self.wndItem.RefreshSlot()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = proxy(tooltip)

	def Close(self):
		self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
		net.SendChatPacket("/safebox_close")

	def CommandCloseSafebox(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.dlgPickMoney.Close()
		self.dlgChangePassword.Close()
		self.Hide()
		self.interface.RefreshMarkInventoryBag()

	def SelectEmptySlot(self, selectedSlotPos):
		selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)

		if mousemodule.mouseController.isAttached():

			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()

			if player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				net.SendSafeboxItemMovePacket(attachedSlotPos, selectedSlotPos, 0)
			else:
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.RESERVED_WINDOW == attachedInvenType:
					return
				if player.ITEM_MONEY == mousemodule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxSaveMoneyPacket(mousemodule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")
				else:
					net.SendSafeboxCheckinPacket(attachedInvenType, attachedSlotPos, selectedSlotPos)

			mousemodule.mouseController.DeattachObject()

	def SelectItemSlot(self, selectedSlotPos):
		selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)
		if mousemodule.mouseController.isAttached():
			attachedSlotType = mousemodule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				if player.ITEM_MONEY == mousemodule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxSaveMoneyPacket(mousemodule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")
				else:
					attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			mousemodule.mouseController.DeattachObject()
		else:
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SAFEBOX_SELL_DISABLE_SAFEITEM)
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SHOP_BUY_INFO)
			else:
				selectedItemID = safebox.GetItemID(selectedSlotPos)
				mousemodule.mouseController.AttachObject(self, player.SLOT_TYPE_SAFEBOX, selectedSlotPos, selectedItemID)
				snd.PlaySound("sound/ui/pick.wav")

	def UseItemSlot(self, slotIndex):
		mousemodule.mouseController.DeattachObject()

	def __ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetSafeBoxItem(slotIndex)

	def OverInItem(self, slotIndex):
		slotIndex = self.__LocalPosToGlobalPos(slotIndex)
		self.wndItem.SetUsableItem(False)
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPickMoney(self, money):
		mousemodule.mouseController.AttachMoney(self, player.SLOT_TYPE_SAFEBOX, money)

	def OnChangePassword(self):
		self.dlgChangePassword.Open()

	def OnPressEscapeKey(self):
		self.Close()
		return True

# Sem Limite Armazem #
	def OnUpdate(self):
		USE_SAFEBOX_LIMIT_RANGE = 1000
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xSafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE or abs(y - self.ySafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE:
			self.Close()
# Sem Limite Armazem #

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def OnTop(self):
		self.interface.SetOnTopWindow(player.ON_TOP_WND_SAFEBOX)
		self.interface.RefreshMarkInventoryBag()

class MallWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.pageButtonList = []
		self.curPageIndex = 0
		self.isLoaded = 0
		self.xSafeBoxStart = 0
		self.ySafeBoxStart = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndBoard = None
		self.wndItem = None
		self.pageButtonList = []

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/mallwindow.py")

		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self)
		wndItem.SetPosition(8, 39)
		wndItem.SetSelectEmptySlotEvent(self.SelectEmptySlot)
		wndItem.SetSelectItemSlotEvent(self.SelectItemSlot)
		wndItem.SetUnselectItemSlotEvent(self.UseItemSlot)
		wndItem.SetUseSlotEvent(self.UseItemSlot)
		wndItem.SetOverInItemEvent(self.OverInItem)
		wndItem.SetOverOutItemEvent(self.OverOutItem)
		wndItem.Show()

		self.GetChild("board").SetCloseEvent(self.Close)
		self.GetChild("ExitButton").SetEvent(self.Close)

		self.wndItem = wndItem
		self.wndBoard = self.GetChild("board")

		self.SetTableSize(3)

	def ShowWindow(self, size):
		(self.xSafeBoxStart, self.ySafeBoxStart, z) = player.GetMainCharacterPosition()

		self.SetTableSize(size)
		self.Show()

	def SetTableSize(self, size):
		pageCount = max(1, size / safebox.SAFEBOX_SLOT_Y_COUNT)
		pageCount = min(3, pageCount)
		size = safebox.SAFEBOX_SLOT_Y_COUNT

		# self.__MakePageButton(pageCount)

		self.wndItem.ArrangeSlot(0, safebox.SAFEBOX_SLOT_X_COUNT, size, 32, 32, 0, 0)
		self.wndItem.RefreshSlot()
		self.wndItem.SetSlotBaseImage("interface/controls/common/slot_rectangle/slot.tga", 1.0, 1.0, 1.0, 1.0)

		wnd_height = 130 + 32 * size
		self.UpdateRect()

	def RefreshMall(self):
		getItemID=safebox.GetMallItemID
		getItemCount=safebox.GetMallItemCount
		setItemID=self.wndItem.SetItemSlot

		for i in xrange(safebox.GetMallSize()):
			itemID = getItemID(i)
			itemCount = getItemCount(i)
			if itemCount <= 1:
				itemCount = 0
			setItemID(i, itemID, itemCount)

		self.wndItem.RefreshSlot()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = proxy(tooltip)

	def Close(self):
		net.SendChatPacket("/mall_close")
		self.Hide()

	def CommandCloseMall(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.Hide()

	def SelectEmptySlot(self, selectedSlotPos):
		if mousemodule.mouseController.isAttached():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.MALL_CANNOT_INSERT)
			mousemodule.mouseController.DeattachObject()

	def SelectItemSlot(self, selectedSlotPos):
		if mousemodule.mouseController.isAttached():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.MALL_CANNOT_INSERT)
			mousemodule.mouseController.DeattachObject()
		else:
			curCursorNum = app.GetCursor()
			selectedItemID = safebox.GetMallItemID(selectedSlotPos)
			mousemodule.mouseController.AttachObject(self, player.SLOT_TYPE_MALL, selectedSlotPos, selectedItemID)
			snd.PlaySound("sound/ui/pick.wav")

	def UseItemSlot(self, slotIndex):
		mousemodule.mouseController.DeattachObject()

	def __ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetMallItem(slotIndex)

	def OverInItem(self, slotIndex):
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):
		USE_SAFEBOX_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xSafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE or abs(y - self.ySafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE:
			self.Close()

# x = MallWindow()
# x.Show()

# x = ChangePasswordDialog()
# x.Show()

# x = PasswordDialog()
# x.Show()