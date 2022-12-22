#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import ui
import exception
import localeinfo

class DeclareGuildWarDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

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
		self.inputValue = None
		self.DropDown = None
		self.Hide()

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/declareguildwardialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")

		self.DropDown = getObject("DropDown")

		self.DropDown.AppendItem(localeinfo.GUILDWAR_NORMAL_TITLE, 0)
		self.DropDown.AppendItem(localeinfo.GUILDWAR_WARP_TITLE, 1)
		self.DropDown.AppendItem(localeinfo.GUILDWAR_CTF_TITLE, 2)
		self.DropDown.SelectByAffectId(1)

		self.SetAcceptEvent(self.__OnOK)
		self.SetCancelEvent(self.__OnCancel)

	def __OnOK(self):
		text = self.GetText()
		type = self.GetType()

		if "" == text:
			return

		net.SendChatPacket("/war %s %d" % (text, type))
		self.Close()

		return 1

	def __OnCancel(self):
		self.Close()
		return 1

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.SetReturnEvent(event)

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.SetEscapeEvent(event)

	def GetType(self):
		return self.DropDown.GetSelectedValue()

	def GetText(self):
		return self.inputValue.GetText()

class AcceptGuildWarDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self, guildName, warType):
		self.guildName = guildName
		self.inputValue.SetText(guildName)
		self.DropDown.SelectByAffectId(warType)
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def GetGuildName(self):
		return self.guildName

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.DropDown = None
		self.Hide()

	def __CreateDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/acceptguildwardialog.py")
		except:
			exception.Abort("DeclareGuildWarWindow.__CreateDialog - LoadScript")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")

		self.inputValue.EditLine.SetPosition(0, self.inputValue.EditLine.GetTop())
		self.inputValue.EditLine.SetHorizontalAlignCenter()
		self.inputValue.EditLine.SetWindowHorizontalAlignCenter()

		self.DropDown = getObject("DropDown")

		self.DropDown.AppendItem(localeinfo.GUILDWAR_NORMAL_TITLE, 0)
		self.DropDown.AppendItem(localeinfo.GUILDWAR_WARP_TITLE, 1)
		self.DropDown.AppendItem(localeinfo.GUILDWAR_CTF_TITLE, 2)
		self.DropDown.Block()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.SetIMEUpdateEvent(event)

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.SetEscapeEvent(event)

	def GetType(self):
		return self.DropDown.GetSelectedValue()

	def GetText(self):
		return self.inputValue.GetText()

# a = DeclareGuildWarDialog()
# a.Open()

# a = AcceptGuildWarDialog()
# a.Open("Fuckers", 1)