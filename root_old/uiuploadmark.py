#favor manter essa linha
import enszxc3467hc3kokdueq as app
import ui
import localeinfo

class MarkItem(ui.ListBoxEx.Item):
	def __init__(self, fileName):
		ui.ListBoxEx.Item.__init__(self)
		self.imgWidth = 0
		self.imgHeight = 0
		self.canLoad = 0
		self.textLine = self.__CreateTextLine(fileName)
		self.imgBox = self.__CreateImageBox("upload/" + fileName)

	def __del__(self):
		ui.ListBoxEx.Item.__del__(self)

	def GetText(self):
		return self.textLine.GetText()

	def SetSize(self, width, height):
		ui.ListBoxEx.Item.SetSize(self, 20 + 6*len(self.textLine.GetText()) + 4, height)

	def __CreateTextLine(self, fileName):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetPosition(20, 0)
		textLine.SetText(fileName)
		textLine.Show()
		return textLine

	def __CreateImageBox(self, fileName):
		(self.canLoad, self.imgWidth, self.imgHeight) = app.GetImageInfo(fileName)

		if 1 == self.canLoad:
			if 16 == self.imgWidth and 12 == self.imgHeight:
				imgBox = ui.ImageBox()
				imgBox.AddFlag("not_pick")
				imgBox.SetParent(self)
				imgBox.SetPosition(0, 2)
				imgBox.LoadImage(fileName)
				imgBox.Show()
				return imgBox
			else:
				return 0
		else:
			return 0

class PopupDialog(ui.ScriptWindow):
	def __init__(self, parent):
		ui.ScriptWindow.__init__(self)

		self.__Load()
		self.__Bind()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Load(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/popupdialog.py")
		except:
			import exception
			exception.Abort("PopupDialog.__Load")

	def __Bind(self):
		try:
			self.textLine = self.GetChild("message")
			self.okButton = self.GetChild("accept")
		except:
			import exception
			exception.Abort("PopupDialog.__Bind")

		self.okButton.SetEvent(self.__OnOK)

	def Open(self, msg):
		self.textLine.SetText(msg)
		self.SetCenterPosition()
		self.Show()
		self.SetTop()

	def __OnOK(self):
		self.Hide()

class MarkSelectDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.selectEvent = None
		self.isLoaded = 0

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

		if self.markListBox.IsEmpty():
			self.__PopupMessage(localeinfo.GUILDMARK_UPLOADER_ERROR_PATH)

	def Close(self):
		self.popupDialog.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SetSelectEvent(self, event):
		self.selectEvent = ui.__mem_func__(event)

	def __CreateMarkListBox(self):
		markListBox = ui.ListBoxEx()
		markListBox.SetParent(self)
		markListBox.SetPosition(15, 50)
		markListBox.Show()
		return markListBox

	def __Load(self):
		self.popupDialog = PopupDialog(self)
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/marklistwindow.py")
		except:
			import exception
			exception.Abort("MarkListBox.__Load")

		try:
			self.markListBox = self.__CreateMarkListBox()
			self.markListBox.SetScrollBar(self.GetChild("ScrollBar"))

			self.popupText = self.popupDialog.GetChild("message")
			self.popupDialog.GetChild("accept").SetEvent(self.popupDialog.Hide)

			self.board = self.GetChild("board")
			self.okButton = self.GetChild("ok")
			self.cancelButton = self.GetChild("cancel")
			self.refreshButton = self.GetChild("refresh")

		except:
			import exception
			exception.Abort("MarkListBox.__Bind")

		self.refreshButton.SetEvent(self.__OnRefresh)
		self.cancelButton.SetEvent(self.__OnCancel)
		self.okButton.SetEvent(self.__OnOK)
		self.board.SetCloseEvent(self.__OnCancel)
		self.UpdateRect()

		self.__RefreshFileList()

	def __PopupMessage(self, msg):
		self.popupDialog.Open(msg)

	def __OnOK(self):
		selItem = self.markListBox.GetSelectedItem()

		if not selItem:
			self.__PopupMessage(localeinfo.GUILDMARK_UPLOADER_ERROR_SELECT)
			return

		if selItem:
			if selItem.canLoad != 1:
				self.__PopupMessage(localeinfo.GUILDMARK_UPLOADER_ERROR_FILE_FORMAT)
			elif selItem.imgWidth != 16:
				self.__PopupMessage(localeinfo.GUILDMARK_UPLOADER_ERROR_16_WIDTH)
			elif selItem.imgHeight != 12:
				self.__PopupMessage(localeinfo.GUILDMARK_UPLOADER_ERROR_12_HEIGHT)
			else:
				self.selectEvent(selItem.GetText())
				self.Hide()

	def __OnCancel(self):
		self.Hide()

	def __OnRefresh(self):
		self.__RefreshFileList()

	def __RefreshFileList(self):
		self.__ClearFileList()
		self.__AppendFileList("png")
		self.__AppendFileList("bmp")
		self.__AppendFileList("tga")
		self.__AppendFileList("jpg")

	def __ClearFileList(self):
		self.markListBox.RemoveAllItems()

	def __AppendFileList(self, filter):
		fileNameList = app.GetFileList("upload/*." + filter)
		for fileName in fileNameList:
			self.__AppendFile(fileName)

	def __AppendFile(self, fileName):
		self.markListBox.AppendItem(MarkItem(fileName))