#favor manter essa linha
import enszxc3467hc3kokdueq as app
import LURMxMaKZJqliYt2QSHG as chat
import XXjvumrgrYBZompk3PS8 as item
import ui
import ime
import localeinfo
import constinfo
import uitooltip
import ga3vqy6jtxqi9yf344j7 as player
import shop

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = None
		self.acceptArgs = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "uiscript/popupdialog.py")

		self.GetChild("accept").SetEvent(self.Close)

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		if self.acceptEvent:
			self.acceptEvent(* self.acceptArgs)

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.GetChild("board").SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.GetChild("message").SetText(text)

	def SetAcceptEvent(self, event, *args):
		self.acceptEvent = ui.__mem_func__(event)
		self.acceptArgs = args

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 7 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetHideSlot(self):
		self.inputSlot.Hide()

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event, *args):
		self.acceptButton.SetEvent(event, *args)
		self.inputValue.SetReturnEvent(event, *args)

	def SetCancelEvent(self, event, *args):
		self.board.SetCloseEvent(event, *args)
		self.cancelButton.SetEvent(event, *args)
		self.inputValue.SetEscapeEvent(event, *args)

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")
		self.description = getObject("Description")

	def SetDescription(self, text):
		self.description.SetText(text)
		(width, height) = self.description.GetTextSize()
		self.SetBoardWidth(width + 30)


class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")
		self.description1 = getObject("Description1")
		self.description2 = getObject("Description2")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class ItemQuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.escapeEventFunc = None
		self.escapeEventArgs = None

		self.__CreateDialog()

		self.tooltipItem = uitooltip.ItemToolTip()
		self.toolTip = uitooltip.ToolTip()

		self.window_type = 0
		self.count = 0
		self.dropType = 0
		self.dropCount = 0
		self.dropNumber = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/itemquestiondialog.py")

		self.board = self.GetChild("board")
		self.board.SetCloseEvent(self.Close)
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")
		self.separator = self.GetChild("separator")
		self.vseparator = self.GetChild("vseparator")

		self.slotList = []
		for i in range(3):
			slot = ui.ImageBox()
			slot.LoadImage("interface/controls/common/slot_rectangle/slot.tga")
			slot.SetParent(self)
			self.slotList.append(slot)

	def Open(self, vnum, slot = None, price = None):
		item.SelectItem(vnum)
		xSlotCount, ySlotCount = item.GetItemSize()

		try:
			if self.window_type == "inv":
				metinSlot = [player.GetItemMetinSocket(player.INVENTORY, slot, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
			elif self.window_type == "shop":
				metinSlot = [shop.GetItemMetinSocket(slot, i) for i in range(player.METIN_SOCKET_MAX_NUM)]
		except BaseException:
			pass

		self.board.SetTitle(item.GetItemName())

		if price != None:
			itemPrice = ui.TextLine()
			itemPrice.SetParent(self.textLine)
			itemPrice.SetFontColor(1, 0.5, 0.5)
			itemPrice.SetPosition(0, 14)
			if str(price).isdigit():
				itemPrice.SetText("Valor: |cfff8d090" + localeinfo.NumberToMoneyString(price) + " G")
			else:
				itemPrice.SetText("Valor: " + price + " G")
			itemPrice.Show()
			self.itemPrice = itemPrice

		slotGrid = ui.SlotWindow()
		slotGrid.SetParent(self)
		slotGrid.SetPosition(8, 7 + 32)
		slotGrid.AppendSlot(0, 0, 0, 32*xSlotCount, 32*ySlotCount)
		slotGrid.AddFlag("not_pick")
		slotGrid.Show()
		self.slotGrid = slotGrid

		if self.count > 1 and vnum != 1:
			self.slotGrid.SetItemSlot(0, vnum, self.count)
		else:
			self.slotGrid.SetItemSlot(0, vnum)

		self.SetSize(self.GetWidth(), 98 + 32 * ySlotCount)
		if price != None:
			self.textLine.SetPosition(self.textLine.GetLeft(), self.textLine.GetTop() + (ySlotCount - 1) * 16 - 7)
		else:
			self.textLine.SetPosition(self.textLine.GetLeft(), self.textLine.GetTop() + (ySlotCount - 1) * 16)

		for i in range(min(3, ySlotCount)):
			self.slotList[i].SetPosition(8, 7 + ySlotCount*32 - i*32)
			if vnum != 1:
				self.slotList[i].SetOverInEvent(self.OverInItem, slot)
				self.slotList[i].SetOverOutEvent(self.OverOutItem, self.tooltipItem)
			else:
				self.slotList[i].SetOverInEvent(self.OverInToolTip, localeinfo.MONETARY_UNIT0)
				self.slotList[i].SetOverOutEvent(self.OverOutToolTip)
			self.slotList[i].Show()

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

	def SetMessage(self, text):
		self.textLine.SetText(text)
		(width, height) = self.textLine.GetTextSize()
		self.SetWidth(width + 80)

	def OverInToolTip(self, arg):
		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(arg, 0xffffff00)
		self.toolTip.Show()

	def OverOutToolTip(self):
		self.toolTip.Hide()

	def OverInItem(self, slot):
		if self.window_type == "shop":
			self.tooltipItem.SetShopItem(slot)
		elif self.window_type == "off":
			self.tooltipItem.SetOfflineShopItem(slot)
		elif self.window_type == "inv":
			self.tooltipItem.SetInventoryItem(slot)

	def OverOutItem(self, tooltipItem):
		if None != tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem.ClearToolTip()

	def Close(self):
		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)
		self.ClearDictionary()
		self.slotList = []
		self.titleBar = None
		self.titleName = None
		self.itemPrice = None
		self.slotGrid = None
		self.toolTip = None
		self.tooltipItem = None
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetSize(self, width, height):
		ui.ScriptWindow.SetSize(self, width, height)
		try:
			self.UpdatePositions(width, height)
		except BaseException:
			pass

	def UpdatePositions(self, width, height):
		self.board.SetSize(width, height)
		self.cancelButton.SetPosition(50, height - 47)
		self.acceptButton.SetPosition(-50, height - 47)
		self.separator.SetPosition(7, height - 59)
		self.separator.SetWidth(width - 14)
		self.vseparator.SetHeight(height - 96)

	def SetAcceptEvent(self, event, *args):
		self.acceptButton.SetEvent(event, *args)

	def SetCancelEvent(self, event, *args):
		self.cancelButton.SetEvent(event, *args)

	def SetText(self, text):
		self.textLine.SetText(text)
		(width, height) = self.textLine.GetTextSize()
		self.SetWidth(width + 80)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		if self.escapeEventFunc:
			self.escapeEventFunc(* self.escapeEventArgs)
		self.Close()
		return True

	def SetEscapeEvent(self, func, *args):
		self.escapeEventFunc = ui.__mem_func__(func)
		self.escapeEventArgs = args

class QuestionDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.escapeEventFunc = None
		self.escapeEventArgs = None

		self.__CreateDialog()

	def __del__(self):
		self.escapeEventFunc = None
		self.escapeEventArgs = None
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetAcceptEvent(self, event, *args):
		self.acceptButton.SetEvent(event, *args)

	def SetCancelEvent(self, event, *args):
		self.cancelButton.SetEvent(event, *args)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		if self.escapeEventFunc:
			self.escapeEventFunc(* self.escapeEventArgs)
		self.Close()
		return True

	def SetEscapeEvent(self, func, *args):
		self.escapeEventFunc = ui.__mem_func__(func)
		self.escapeEventArgs = args

class QuestionDialog2(QuestionDialog):
	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.GetChild("message1").SetText(text)

	def SetText2(self, text):
		self.GetChild("message2").SetText(text)

class QuestionDialog3(QuestionDialog):
	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog3.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.textLine3 = self.GetChild("message3")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.GetChild("message1").SetText(text)

	def SetText2(self, text):
		self.GetChild("message2").SetText(text)

	def SetText3(self, text):
		self.GetChild("message3").SetText(text)

class QuestionDialogWithTimeLimit(QuestionDialog2):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0
		#TIME NO PEDIDO
		self.timeOverMsg = 0
		self.timeOverEvent = None
		self.timeOverEventArgs = None
		#FINAL TIME NO PEDIDO

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	# def Open(self, msg, timeout):
	def Open(self, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		# self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	#TIME NO PEDIDO
	def SetTimeOverEvent(self, event, *args):
		self.timeOverEvent = ui.__mem_func__(event)
		self.timeOverEventArgs = args

	def SetTimeOverMsg(self, msg):
		self.timeOverMsg = msg

	def OnTimeOver(self):
		if self.timeOverEvent:
			self.timeOverEvent(* self.timeOverEventArgs)
		if self.timeOverMsg:
			chat.AppendChat(chat.CHAT_TYPE_INFO, self.timeOverMsg)

	#FINAL TIME NO PEDIDO
	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeinfo.UI_LEFT_TIME % (leftTime))
		#TIME NO PEDIDO
		if leftTime <= 0:
			self.OnTimeOver()

class PriceInputDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.moneyHeaderText = localeinfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/priceinputdialog.py")
		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.board.SetCloseEvent(self.Close)
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		# self.inputValue.SetIMEUpdateEvent(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")
		self.GetChild("CopyPasteButton").SetEvent(self.CopyAverageValue)

	def Open(self, vnum, count):
		self.averageprice = 0
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.count = count
		item.SelectItem(vnum)
		self.GetChild("ItemIcon").LoadImage(item.GetIconImageFileName())
		height = self.GetChild("ItemIcon").GetHeight()
		if height <= 32:
			self.GetChild("ItemIcon").SetScale(1.0, 1.0)
		elif height > 64:
			self.GetChild("ItemIcon").SetScale(0.3, 0.3)
		else:
			self.GetChild("ItemIcon").SetScale(0.5, 0.5)
		self.GetChild("ItemIcon").SetWindowHorizontalAlignCenter()
		self.GetChild("ItemIcon").SetWindowVerticalAlignCenter()
		self.GetChild("ItemIcon").Show()
		self.GetChild("NameItem").SetTextLimited(str(count) + "x " + str(item.GetItemName()), 140)
		self.GetChild("AveragePrice").SetText("Carregando Informações...")

		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.count = None
		self.averageprice = None

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def UpdateAveragePrice(self, price):
		self.averageprice = price
		if price > 0:
			self.GetChild("AveragePrice").SetTextLimited(localeinfo.NumberToMoneyString(price*self.count)+" Gold", 140)
		else:
			self.GetChild("AveragePrice").SetTextLimited("Sem Informações Ainda", 140)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(13, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event, *args):
		self.acceptButton.SetEvent(event, *args)
		self.inputValue.SetReturnEvent(event, *args)

	def SetCancelEvent(self, event, *args):
		self.board.SetCloseEvent(event, *args)
		self.cancelButton.SetEvent(event, *args)
		self.inputValue.SetEscapeEvent(event, *args)

	def SetValue(self, value):
		value = str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))

	def GetText(self):
		return self.inputValue.GetText()

	def CopyAverageValue(self):
		self.inputValue.SetText(str(self.count*self.averageprice))
		self.__OnValueUpdate()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)
		text = self.inputValue.GetText()
		money = 0
		if text and text.isdigit():
			try:
				money = int(text)
			except ValueError:
				money = 199999999
		self.moneyText.SetText(localeinfo.NumberToMoneyString(money))
		return True

# x = PriceInputDialog()
# x.Open(360, 200)
# x.UpdateAveragePrice(10)

# y = ItemQuestionDialog()
# y.Open(9, 2)