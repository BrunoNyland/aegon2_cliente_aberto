import _wnd_mgr as wndMgr
import ui
import _ime as ime

class ShopAmountDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.unitValue = 1
		self.maxValue = 0
		self.eventAccept = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/shopamountdialog.py")
		except BaseException:
			import exception
			exception.Abort("ShopAmountDialog.LoadDialog.LoadScript")

		try:
			self.board = self.GetChild("board")
			self.pickValueEditLine = self.GetChild("amount_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")
			self.artiButton = self.GetChild("Plus")
			self.eksiButton = self.GetChild("Minus")
		except BaseException:
			import exception
			exception.Abort("ShopAmountDialog.LoadDialog.BindObject")

		self.pickValueEditLine.SetReturnEvent(self.OnAccept)
		self.pickValueEditLine.SetEscapeEvent(self.Close)
		self.acceptButton.SetEvent(self.OnAccept)
		self.cancelButton.SetEvent(self.Close)
		self.artiButton.SetEvent(self.Increase)
		self.eksiButton.SetEvent(self.Decrease)
		self.board.SetCloseEvent(self.Close)

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.eventAccept = 0
		self.maxValue = 0
		self.pickValueEditLine = 0
		self.acceptButton = 0
		self.cancelButton = 0
		self.board = None

	def SetTitleName(self, text):
		self.board.SetTitleName(text)

	def SetAcceptEvent(self, event):
		self.eventAccept = ui.__mem_func__(event)

	def SetMax(self, max):
		self.pickValueEditLine.SetMax(max)

	def Open(self, maxValue, unitValue=1):
		width = self.GetWidth()
		(mouseX, mouseY) = wndMgr.GetMousePosition()

		if mouseX + width/2 > wndMgr.GetScreenWidth():
			xPos = wndMgr.GetScreenWidth() - width
		elif mouseX - width/2 < 0:
			xPos = 0
		else:
			xPos = mouseX - width/2

		self.SetPosition(xPos + 40, mouseY - self.GetHeight() + 25)
		self.pickValueEditLine.SetText(str(unitValue))
		self.pickValueEditLine.SetFocus()
		self.pickValueEditLine.SetIMEUpdateEvent(self._OnIMEUpdate)
		ime.SetCursorPosition(4)
		self.unitValue = unitValue
		self.maxValue = maxValue
		self.Show()
		self.SetTop()

	def _OnIMEUpdate(self):
		input = self.pickValueEditLine.GetText()
		if input == "":
			return
		amount = int(input)
		if amount > 200:
			self.pickValueEditLine.SetText("200")

	def Close(self):
		self.pickValueEditLine.KillFocus()
		self.Hide()

	def OnAccept(self):
		text = self.pickValueEditLine.GetText()
		if len(text) > 0 and text.isdigit():
			money = int(text)
			money = min(money, self.maxValue)
			if money > 0:
				if self.eventAccept:
					self.eventAccept(money)
		self.Close()

	def Increase(self):
		input = self.pickValueEditLine.GetText()
		if input != "":
			amount = int(input)
			if amount > 199:
				self.pickValueEditLine.SetText("200")
			else:
				self.pickValueEditLine.SetText("%s" % (str(amount+1)))
		else:
			self.pickValueEditLine.SetText("1")
		ime.SetCursorPosition(4)

	def Decrease(self):
		input = self.pickValueEditLine.GetText()
		if input != "":
			amount = int(input)
			if amount == 0:
				self.pickValueEditLine.SetText("0")
			else:
				amount -= 1
				self.pickValueEditLine.SetText("%s" % (str(amount)))
		else:
			self.pickValueEditLine.SetText("0")
		ime.SetCursorPosition(4)

# x = ShopAmountDialog()
# x.LoadDialog()
# x.Open(200, 1)