#favor manter essa linha
import ui
import _net as net
import _chat as chat
import _player as player
import _app as app
import localeinfo
import _ime as ime
import constinfo

from weakref import proxy

if app.ENABLE_EMOJI_SYSTEM:
	import uiemojispm

class WhisperButton(ui.Button):
	def __init__(self):
		ui.Button.__init__(self, "TOP_MOST")

	def __del__(self):
		ui.Button.__del__(self)

	def SetToolTipText(self, text, x = 0, y = 32):
		ui.Button.SetToolTipText(self, text, x, y)
		self.ToolTipText.Show()

	def SetToolTipTextWithColor(self, text, color, x = 0, y = 32):
		ui.Button.SetToolTipText(self, text, x, y)
		self.ToolTipText.SetPackedFontColor(color)
		self.ToolTipText.Show()

	def ShowToolTip(self):
		if 0 != self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if 0 != self.ToolTipText:
			self.ToolTipText.Show()

class WhisperDialog(ui.ScriptWindow):
	if app.ENABLE_EMOJI_SYSTEM:
		NEW_WIDTH = 0
		NEW_HEIGHT = 0

	class TextRenderer(ui.Window):
		def SetTargetName(self, targetName):
			self.targetName = targetName

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			chat.RenderWhisper(self.targetName, x, y)

	class ResizeButton(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)

		def __del__(self):
			ui.DragButton.__del__(self)

		def OnMouseOverIn(self):
			app.SetCursor(app.HVSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self, eventMinimize = None, eventClose = None):
		ui.ScriptWindow.__init__(self)
		self.targetName = ""

		if eventMinimize:
			self.eventMinimize = ui.__mem_func__(eventMinimize)

		if eventClose:
			self.eventClose = ui.__mem_func__(eventClose)

		self.eventAcceptTarget = None
		self.listGMName = {}
		if app.ENABLE_EMOJI_SYSTEM:
			chat.SetFontNameChat("Verdana:14")

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/whisperdialog.py")
		except BaseException:
			import exception
			exception.Abort("WhisperDialog.LoadDialog.LoadScript")

		try:
			GetObject = self.GetChild
			self.titleName = GetObject("titlename")
			self.titleNameEdit = GetObject("titlename_edit")
			self.closeButton = GetObject("closebutton")
			self.scrollBar = GetObject("scrollbar")
			self.chatLine = GetObject("chatline")
			self.negociarButton = GetObject("negociarbutton")
			self.addButton = GetObject("addbutton")
			self.minimizeButton = GetObject("minimizebutton")
			self.sendButton = GetObject("sendbutton")
			self.board = GetObject("board")
			self.editBar = GetObject("editbar")
			self.gamemasterMark = GetObject("gamemastermark")
			if app.ENABLE_EMOJI_SYSTEM:
				emojisBoard = uiemojispm.EmojisPMBoard()
				emojisBoard.SetParent(self.board)
				self.emojisBoard = emojisBoard

		except BaseException:
			import exception
			exception.Abort("DialogWindow.LoadDialog.BindObject")

		self.gamemasterMark.Hide()
		self.titleName.SetText("")
		self.titleNameEdit.SetText("")
		self.addButton.SetEvent(self.AddFriend)
		self.minimizeButton.SetEvent(self.Minimize)
		self.negociarButton.SetEvent(self.Exchange)
		self.closeButton.SetEvent(self.Close)
		self.scrollBar.SetPos(1.0)
		self.scrollBar.SetScrollEvent(self.OnScroll)
		self.SetOnRunMouseWheelEvent(self.OnRunMouseWheel)
		self.chatLine.SetReturnEvent(self.SendWhisper)
		self.chatLine.SetEscapeEvent(self.Minimize)
		self.chatLine.SetMultiLine()
		self.sendButton.SetEvent(self.SendWhisper)
		self.titleNameEdit.SetReturnEvent(self.AcceptTarget)
		self.titleNameEdit.SetEscapeEvent(self.Close)

		if app.ENABLE_EMOJI_SYSTEM:
			self.chatLine.SetFontName("Verdana:14")
			btnEmojiExpandir = ui.Button()
			btnEmojiExpandir.SetParent(self)
			btnEmojiExpandir.SetUpVisual("d:/ymir work/ui/emoji/open_norm.png")
			btnEmojiExpandir.SetOverVisual("d:/ymir work/ui/emoji/open_over.png")
			btnEmojiExpandir.SetDownVisual("d:/ymir work/ui/emoji/open_down.png")
			# btnEmojiExpandir.SetButtonScale(0.26, 0.26)
			btnEmojiExpandir.SetPosition(136, 12)
			btnEmojiExpandir.SetEvent(self.OpenEmojis)
			btnEmojiExpandir.Hide()
			self.btnEmojiExpandir = btnEmojiExpandir

			toolTipEx = ui.Ballon()
			toolTipEx.SetParent(self.btnEmojiExpandir)
			toolTipEx.SetPosition(0, -38)
			toolTipEx.SetWindowHorizontalAlignCenter()
			toolTipEx.Hide()
			toolTipEx.SetText("Selecione um Emoji")
			self.toolTipEx = toolTipEx
			self.btnEmojiExpandir.SetToolTipWindow(self.toolTipEx)

			btnEmojiRetrair = ui.Button()
			btnEmojiRetrair.SetParent(self)
			btnEmojiRetrair.SetUpVisual("d:/ymir work/ui/emoji/close_norm.png")
			btnEmojiRetrair.SetOverVisual("d:/ymir work/ui/emoji/close_over.png")
			btnEmojiRetrair.SetDownVisual("d:/ymir work/ui/emoji/close_down.png")
			# btnEmojiRetrair.SetButtonScale(0.26, 0.26)
			btnEmojiRetrair.SetPosition(136, 12)
			btnEmojiRetrair.SetEvent(self.CloseEmojis)
			btnEmojiRetrair.Hide()
			self.btnEmojiRetrair = btnEmojiRetrair

			toolTipEr = ui.Ballon()
			toolTipEr.SetParent(self.btnEmojiRetrair)
			toolTipEr.SetPosition(0, -38)
			toolTipEr.SetWindowHorizontalAlignCenter()
			toolTipEr.Hide()
			toolTipEr.SetText("Fechar Emojis")
			self.toolTipEr = toolTipEr
			self.btnEmojiRetrair.SetToolTipWindow(self.toolTipEr)

		self.textRenderer = self.TextRenderer()
		self.textRenderer.SetParent(self)
		self.textRenderer.SetPosition(20, 28)
		self.textRenderer.SetTargetName("")
		self.textRenderer.Show()

		self.resizeButton = self.ResizeButton()
		self.resizeButton.SetParent(self)
		self.resizeButton.SetSize(20, 20)
		if app.ENABLE_EMOJI_SYSTEM:
			self.resizeButton.SetPosition(390, 180)
		else:
			self.resizeButton.SetPosition(280, 180)
		self.resizeButton.SetMoveEvent(self.ResizeWhisperDialog)
		self.resizeButton.Show()

		self.ResizeWhisperDialog()

	def Destroy(self):
		self.Hide()
		self.eventMinimize = None
		self.eventClose = None
		self.eventAcceptTarget = None
		self.ClearDictionary()
		self.scrollBar.Destroy()
		self.titleName = None
		self.titleNameEdit = None
		self.closeButton = None
		self.scrollBar = None
		self.chatLine = None
		self.sendButton = None
		self.minimizeButton = None
		self.negociarButton = None
		self.textRenderer = None
		self.board = None
		self.editBar = None
		self.resizeButton = None
		self.addButton = None
		if app.ENABLE_EMOJI_SYSTEM:
			self.emojisBoard.Destroy()
			self.emojisBoard = None
			self.btnEmojiExpandir = None
			self.btnEmojiRetrair = None

	if app.ENABLE_EMOJI_SYSTEM:
		def OpenEmojis(self):
			self.NEW_WIDTH = 0
			self.NEW_HEIGHT = 240

			(xPos, yPos) = self.resizeButton.GetLocalPosition()
			self.SetWhisperDialogSize(xPos + 20, yPos + self.NEW_HEIGHT + 20)
			self.resizeButton.SetPosition(xPos, yPos + self.NEW_HEIGHT)

			self.btnEmojiExpandir.Hide()
			self.btnEmojiRetrair.Show()
			self.emojisBoard.Open(self.board)

		def CloseEmojis(self):
			self.NEW_WIDTH = 0
			self.NEW_HEIGHT = 0

			(xPos, yPos) = self.resizeButton.GetLocalPosition()
			self.SetWhisperDialogSize(xPos + 20, yPos - 240 + 20)
			self.resizeButton.SetPosition(xPos, yPos - 240)

			self.btnEmojiExpandir.Show()
			self.btnEmojiRetrair.Hide()
			self.emojisBoard.Close()

	def ResizeWhisperDialog(self):
		(xPos, yPos) = self.resizeButton.GetLocalPosition()

		if app.ENABLE_EMOJI_SYSTEM:
			if xPos < 390 + self.NEW_WIDTH:
				self.resizeButton.SetPosition(390 + self.NEW_WIDTH, yPos)
				return

			if yPos < 180 + self.NEW_HEIGHT:
				self.resizeButton.SetPosition(xPos, 180 + self.NEW_HEIGHT)
				return
		else:
			if xPos < 280:
				self.resizeButton.SetPosition(280, yPos)
				return

			if yPos < 150:
				self.resizeButton.SetPosition(xPos, 150)
				return

		self.SetWhisperDialogSize(xPos + 20, yPos + 20)

		if app.ENABLE_EMOJI_SYSTEM:
			self.emojisBoard.Refresh(self.board)

	def SetWhisperDialogSize(self, width, height):
		try:
			if app.ENABLE_EMOJI_SYSTEM:
				max = 770
			else:
				max = 200
			self.board.SetSize(width, height)
			self.scrollBar.SetPosition(width - 25, 35)
			self.scrollBar.SetScrollBarSize(height - 110 - self.NEW_HEIGHT)
			self.scrollBar.SetPos(1.0)
			self.editBar.SetScale(width - 18 - 64, 50)
			self.chatLine.SetSize(width - 18 - 5 - 64, 40)
			self.chatLine.SetLimitWidth(width - 90 - 10)
			self.SetSize(width, height)

			if 0 != self.targetName:
				chat.SetWhisperBoxSize(self.targetName, width - 50, height - 90 - self.NEW_HEIGHT)

			self.textRenderer.SetPosition(20, 28)
			self.scrollBar.SetPosition(width - 25, 35 + 7)
			self.editBar.SetPosition(15, height - 60 - self.NEW_HEIGHT)
			self.sendButton.SetPosition(width - 75, height - 60 - self.NEW_HEIGHT)
			self.negociarButton.SetPosition(width - 34 - 26*3, 8)
			self.addButton.SetPosition(width - 34 - 26*2, 8)
			self.minimizeButton.SetPosition(width - 34 - 26*1, 8)
			self.closeButton.SetPosition(width - 34, 8)
			self.SetChatLineMax(int(max))

		except BaseException:
			import exception
			exception.Abort("WhisperDialog.SetWhisperDialogSize.BindObject")

	def SetChatLineMax(self, max):
		self.chatLine.SetMax(max)

		from grpText import GetSplitingTextLine

		text = self.chatLine.GetText()
		if text:
			self.chatLine.SetText(GetSplitingTextLine(text, max, 0))

	def OpenWithTarget(self, targetName = "", loadMessages = False):
		chat.CreateWhisper(targetName)
		chat.SetWhisperBoxSize(targetName, self.GetWidth() - 60, self.GetHeight() - 90)
		self.chatLine.SetFocus()
		self.titleName.SetText(targetName)
		self.targetName = targetName
		self.textRenderer.SetTargetName(targetName)
		self.titleNameEdit.Hide()
		self.gamemasterMark.Hide()
		self.minimizeButton.Show()
		self.addButton.Show()
		self.negociarButton.Show()
		if app.ENABLE_EMOJI_SYSTEM:
			self.btnEmojiExpandir.Show()
			self.btnEmojiRetrair.Hide()
			self.ResizeWhisperDialog()

		if loadMessages:
			if constinfo.WHISPER_MESSAGES.__contains__(targetName):
				for text in constinfo.WHISPER_MESSAGES[targetName]:
					chat.AppendWhisper(text[0], targetName, text[1])

	def OpenWithoutTarget(self, event):
		if event:
			self.eventAcceptTarget = ui.__mem_func__(event)

		self.titleName.SetText("")
		self.titleNameEdit.SetText("")
		self.titleNameEdit.SetFocus()
		self.targetName = 0
		self.titleNameEdit.Show()
		self.negociarButton.Hide()
		self.addButton.Hide()
		self.minimizeButton.Hide()
		self.gamemasterMark.Hide()

	def SetGameMasterLook(self):
		self.gamemasterMark.Show()

	def Minimize(self):
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()

		if None != self.eventMinimize:
			self.eventMinimize(self.targetName)

	def Close(self):
		chat.ClearWhisper(self.targetName)
		self.titleNameEdit.KillFocus()
		self.chatLine.KillFocus()
		self.Hide()

		if None != self.eventClose:
			self.eventClose(self.targetName)

	def AddFriend(self):
		net.SendMessengerAddByNamePacket(self.targetName)

	def ReportViolentWhisper(self):
		net.SendChatPacket("/reportviolentwhisper " + self.targetName)

	def IgnoreTarget(self):
		net.SendChatPacket("/ignore " + self.targetName)

	def AcceptTarget(self):
		name = self.titleNameEdit.GetText()
		if len(name) <= 0:
			self.Close()
			return

		if None != self.eventAcceptTarget:
			self.titleNameEdit.KillFocus()
			self.eventAcceptTarget(name)

		if constinfo.WHISPER_MESSAGES.__contains__(name):
			for text in constinfo.WHISPER_MESSAGES[name]:
				chat.AppendWhisper(text[0], name, text[1])

	def OnScroll(self):
		chat.SetWhisperPosition(self.targetName, self.scrollBar.GetPos())

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()

	def Exchange(self):
		net.SendChatPacket("/exchange_remote " + self.targetName)

	def GetLinks(self, string, ret):
		import re
		links = re.findall(r"(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])", string, re.I)
		if not (hasattr(ret, "clear") and hasattr(ret, "update")):
			return False

		ret.clear()
		map(lambda link: (ret.update({link:"|cFF00C0FC|Hweb:%s|h[%s]|h|r"%(re.sub("://", "w<?", link), link)})) if link else None, links)
		return len(links) > 0

	def SendWhisper(self):
		text = self.chatLine.GetText()
		textLength = len(text)

		if textLength > 0:
			if net.IsInsultIn(text):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.CHAT_INSULT_STRING)
				return

			links = {}
			if self.GetLinks(text, links):
				for k,v in links.items():
					text = text.replace(k, v)

			net.SendWhisperPacket(self.targetName, text)

			if app.ENABLE_EMOJI_SYSTEM:
				chat.SaveEmojisChat(text)
				if self.emojisBoard:
					self.emojisBoard.RefreshCategoria(0)

			self.chatLine.SetText("")

			if not constinfo.WHISPER_MESSAGES.__contains__(self.targetName):
				constinfo.WHISPER_MESSAGES.update({self.targetName : [(1, ("{}: {}".format(player.GetName(), text)))]})
			else:
				constinfo.WHISPER_MESSAGES[self.targetName].append([1, "{}: {}".format(player.GetName(), text)])

			chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, self.targetName, player.GetName() + " : " + text)

	def OnTop(self):
		self.chatLine.SetFocus()

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)
		return True

	def OnIMETab(self):
		return False

	def OnIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self)
		if app.ENABLE_EMOJI_SYSTEM:
			if self.chatLine.GetTextSize()[0] > 200:
				ime.PasteBackspace()
		return True

# x = WhisperDialog()
# x.LoadDialog()
# x.Show()