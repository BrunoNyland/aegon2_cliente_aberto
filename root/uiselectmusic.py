#favor manter essa linha
import _app as app
import ui
import localeinfo

DEFAULT_THEMA = localeinfo.MUSIC_METIN2_DEFAULT_THEMA
class Item(ui.ListBoxEx.Item):
	def __init__(self, fileName):
		ui.ListBoxEx.Item.__init__(self)
		self.canLoad=0
		self.text=fileName
		self.textLine=self.__CreateTextLine(fileName[:20])

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetText(self):
		return self.text

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, 6*len(self.textLine.GetText()) + 4, height)

	def __CreateTextLine(self, fileName):
		textLine=ui.TextLine()
		textLine.SetParent(self)
		textLine.SetPosition(0, 0)

		textLine.SetText(fileName)
		textLine.Show()
		return textLine

class PopupDialog(ui.ScriptWindow):
	def __init__(self, parent):
		ui.ScriptWindow.__init__(self)

		self.__Load()
		self.__Bind()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Load(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/popupdialog.py")

	def __Bind(self):
		self.textLine = self.GetChild("message")
		self.okButton = self.GetChild("accept")
		self.okButton.SetEvent(self.__OnOK)

	def Open(self, msg):
		self.textLine.SetText(msg)
		self.SetCenterPosition()
		self.Show()
		self.SetTop()

	def __OnOK(self):
		self.Hide()

class FileListDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.selectEvent = None
		self.fileListBox = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		if self.isLoaded == 0:
			self.isLoaded = 1
			self.__Load()

		ui.ScriptWindow.Show(self)

	def Open(self):
		self.Show()

		self.SetCenterPosition()
		self.SetTop()

		if self.fileListBox.IsEmpty():
			self.__PopupMessage(localeinfo.MUSIC_EMPTY_MUSIC_LIST)

	def Close(self):
		self.popupDialog.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SetSelectEvent(self, event):
		self.selectEvent = ui.__mem_func__(event)

	def __CreateFileListBox(self):
		fileListBox = ui.ListBoxEx()
		fileListBox.SetParent(self)
		fileListBox.SetPosition(15, 50)

		fileListBox.Show()
		return fileListBox

	def __Load(self):
		self.popupDialog = PopupDialog(self)
		self.__Load_LoadScript("uiscript/musiclistwindow.py")

		self.__Load_BindObject()

		self.refreshButton.SetEvent(self.__OnRefresh)
		self.cancelButton.SetEvent(self.__OnCancel)
		self.okButton.SetEvent(self.__OnOK)
		self.board.SetCloseEvent(self.__OnCancel)

		self.UpdateRect()
		self.__RefreshFileList()

	def __Load_LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __Load_BindObject(self):
		self.fileListBox = self.__CreateFileListBox()
		self.fileListBox.SetScrollBar(self.GetChild("ScrollBar"))

		self.board = self.GetChild("board")
		self.okButton = self.GetChild("ok")
		self.cancelButton = self.GetChild("cancel")
		self.refreshButton = self.GetChild("refresh")

		self.popupText = self.popupDialog.GetChild("message")

	def __PopupMessage(self, msg):
		self.popupDialog.Open(msg)

	def __OnOK(self):
		selItem = self.fileListBox.GetSelectedItem()
		if selItem:
			if self.selectEvent:
				self.selectEvent(selItem.GetText())
			self.Hide()
		else:
			self.__PopupMessage(localeinfo.MUSIC_NOT_SELECT_MUSIC)

	def __OnCancel(self):
		self.Hide()

	def __OnRefresh(self):
		self.__RefreshFileList()

	def __RefreshFileList(self):
		self.__ClearFileList()
		self.__AppendFile(DEFAULT_THEMA)
		self.__AppendFileList("mp3")

	def __ClearFileList(self):
		self.fileListBox.RemoveAllItems()

	def __AppendFileList(self, filter):
		fileNameList = app.GetFileList("bgm/*."+filter)
		for fileName in fileNameList:
			self.__AppendFile(fileName)

	def __AppendFile(self, fileName):
		self.fileListBox.AppendItem(Item(fileName))
