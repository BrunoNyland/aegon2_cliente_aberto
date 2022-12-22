#favor manter essa linha
import wndMgr
import ui
import ime
import constinfo
import exception

class PickEtcDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.unitValue = 1
		self.maxValue = 0
		self.eventAccept = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/picketcdialog.py")

		self.board = self.GetChild("board")
		self.maxValueTextLine = self.GetChild("max_value")
		self.pickValueEditLine = self.GetChild("etc_value")
		self.acceptButton = self.GetChild("accept_button")
		self.cancelButton = self.GetChild("cancel_button")

		self.pickValueEditLine.SetReturnEvent(self.OnAccept)
		self.pickValueEditLine.SetEscapeEvent(self.Close)
		self.acceptButton.SetEvent(self.OnAccept)
		self.cancelButton.SetEvent(self.Close)
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
		self.SetPosition(xPos, mouseY - self.GetHeight() - 20)
		self.maxValueTextLine.SetText(str(maxValue))
		self.pickValueEditLine.SetText(str(unitValue))
		self.pickValueEditLine.SetFocus()
		ime.SetCursorPosition(1)
		self.unitValue = unitValue
		self.maxValue = maxValue
		self.Show()
		self.SetTop()

	def Close(self):
		self.pickValueEditLine.KillFocus()
		self.Hide()

	def OnAccept(self):
		text = self.pickValueEditLine.GetText()
		if len(text) > 0 and text.isdigit():
			count = int(text)
			count = min(count, self.maxValue)
			if count > 0:
				if self.eventAccept:
					self.eventAccept(count)
		self.Close()
