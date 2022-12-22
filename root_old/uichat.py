#favor manter essa linha
import LURMxMaKZJqliYt2QSHG as chat
import ga3vqy6jtxqi9yf344j7 as player
import zn94xlgo573hf8xmddzq as net
import enszxc3467hc3kokdueq as app
import ui
import grp
import wndMgr
import ime
import localeinfo
import systemSetting
import re
import exception

if app.ENABLE_EMOJI_SYSTEM:
	import uiemojis

ENABLE_LAST_SENTENCE_STACK = True

chatInputSetList = []
def InsertChatInputSetWindow(wnd):
	global chatInputSetList
	chatInputSetList.append(wnd)

def RefreshChatMode():
	global chatInputSetList
	for wnd in chatInputSetList:
		wnd.OnRefreshChatMode()

def DestroyChatInputSetWindow():
	global chatInputSetList
	chatInputSetList = []

class ChatModeButton(ui.Window):

	OUTLINE_COLOR = 0xfff8d090
	OVER_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.3)
	BUTTON_STATE_UP = 0
	BUTTON_STATE_OVER = 1
	BUTTON_STATE_DOWN = 2

	def __init__(self):
		ui.Window.__init__(self)
		self.state = None
		self.buttonText = None
		self.event = None
		self.SetWindowName("ChatModeButton")

		toolTipchatMode = ui.Ballon()
		toolTipchatMode.SetParent(self)
		toolTipchatMode.SetPosition(0, -38)
		toolTipchatMode.SetWindowHorizontalAlignCenter()
		toolTipchatMode.Hide()
		toolTipchatMode.SetText("Escolha o modo de chat")
		self.toolTipchatMode = toolTipchatMode

	def __del__(self):
		ui.Window.__del__(self)

	def SetEvent(self, event):
		self.event = ui.__mem_func__(event)

	def SetText(self, text):
		if None == self.buttonText:
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetWindowVerticalAlignCenter()
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.SetPackedFontColor(0xfff8d090)
			textLine.Show()
			self.buttonText = textLine

		self.buttonText.SetText(text)

	def SetSize(self, width, height):
		self.width = width
		self.height = height
		ui.Window.SetSize(self, width, height)

	def OnMouseOverIn(self):
		self.buttonText.SetPackedFontColor(0xffff8784)
		self.state = self.BUTTON_STATE_OVER
		self.toolTipchatMode.Show()

	def OnMouseOverOut(self):
		self.buttonText.SetPackedFontColor(0xfff8d090)
		self.state = self.BUTTON_STATE_UP
		self.toolTipchatMode.Hide()

	def OnMouseLeftButtonDown(self):
		self.state = self.BUTTON_STATE_DOWN

	def OnMouseLeftButtonUp(self):
		self.state = self.BUTTON_STATE_UP
		if self.IsIn():
			self.state = self.BUTTON_STATE_OVER

		if None != self.event:
			self.event()

	def OnRender(self):
		(x, y) = self.GetGlobalPosition()

		grp.SetColor(self.OUTLINE_COLOR)
		grp.RenderRoundBox(x, y, self.width, self.height)

		if self.state >= self.BUTTON_STATE_OVER:
			grp.RenderRoundBox(x+1, y, self.width-2, self.height)
			grp.RenderRoundBox(x, y+1, self.width, self.height-2)

			if self.BUTTON_STATE_DOWN == self.state:
				grp.SetColor(self.OVER_COLOR)
				grp.RenderBar(x+1, y+1, self.width-2, self.height-2)

class ChatLine(ui.EditLine):

	CHAT_MODE_NAME = {
		chat.CHAT_TYPE_TALKING : localeinfo.CHAT_NORMAL,
		chat.CHAT_TYPE_PARTY : localeinfo.CHAT_PARTY,
		chat.CHAT_TYPE_GUILD : localeinfo.CHAT_GUILD,
		chat.CHAT_TYPE_SHOUT : localeinfo.CHAT_SHOUT,
		chat.CHAT_TYPE_GLOBAL : localeinfo.CHAT_GLOBAL,
	}

	def __init__(self):
		ui.EditLine.__init__(self)
		self.SetWindowName("Chat Line")
		self.SetFontName("Verdana:14")
		self.SetVerticalAlignCenter()
		self.lastShoutTime = 0
		self.lastGlobalTime = 0

		self.eventEscape = None
		self.eventReturn = None
		self.eventTab = None
		self.chatMode = chat.CHAT_TYPE_TALKING
		self.bCodePage = True

		if app.ENABLE_EMOJI_SYSTEM:
			self.refreshEmojis = None

		self.overTextLine = ui.TextLine()
		self.overTextLine.SetParent(self)
		self.overTextLine.SetPosition(0, -6)
		self.overTextLine.SetFontColor(1.0, 1.0, 0.0)
		self.overTextLine.SetFontName("Verdana:14")
		self.overTextLine.SetOutline()
		self.overTextLine.Hide()

		self.lastSentenceStack = []
		self.lastSentencePos = 0

	def __del__(self):
		ui.EditLine.__del__(self)

	if app.ENABLE_EMOJI_SYSTEM:
		def SetEmojisListBoard(self, emojis):
			self.refreshEmojis = emojis

		def DelEmojisListBoard(self):
			self.refreshEmojis = None

	def SetChatMode(self, mode):
		self.chatMode = mode

	def GetChatMode(self):
		return self.chatMode

	def ChangeChatMode(self):
		if chat.CHAT_TYPE_TALKING == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_PARTY)
			self.SetText("#")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_GUILD)
			self.SetText("%")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_SHOUT)
			self.SetText("!")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_GLOBAL)
			self.SetText("&")
			self.SetEndPosition()

		elif chat.CHAT_TYPE_GLOBAL == self.GetChatMode():
			self.SetChatMode(chat.CHAT_TYPE_TALKING)
			self.SetText("")

		self.__CheckChatMark()

	def GetCurrentChatModeName(self):
		try:
			return self.CHAT_MODE_NAME[self.chatMode]
		except:
			exception.Abort("ChatLine.GetCurrentChatModeName")

	def SetEscapeEvent(self, event):
		self.eventReturn = ui.__mem_func__(event)

	def SetReturnEvent(self, event):
		self.eventEscape = ui.__mem_func__(event)

	def SetTabEvent(self, event):
		self.eventTab = ui.__mem_func__(event)

	def OpenChat(self):
		self.SetFocus()
		self.__ResetChat()

	def __ClearChat(self):
		self.SetText("")
		self.lastSentencePos = 0

	def __ResetChat(self):
		if chat.CHAT_TYPE_PARTY == self.GetChatMode():
			self.SetText("#")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_GUILD == self.GetChatMode():
			self.SetText("%")
			self.SetEndPosition()
		elif chat.CHAT_TYPE_SHOUT == self.GetChatMode():
			self.SetText("!")
			self.SetEndPosition()
		#CHAT GLOBAL
		elif chat.CHAT_TYPE_GLOBAL == self.GetChatMode():
			self.SetText("&")
			self.SetEndPosition()
		#CHAT GLOBAL
		else:
			self.__ClearChat()

		self.__CheckChatMark()

	#Link de Site in chat
	def GetLinks(self, string, ret):
		links = re.findall("(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#/%=~_|$?!:,.]*\)|[A-Z0-9+&@#/%=~_|$])", string, re.I)
		if not (hasattr(ret, "clear") and hasattr(ret, "update")):
			return False

		ret.clear()
		map(lambda link: (ret.update({link:"|cFF00C0FC|Hweb:%s|h[%s]|h|r"%(re.sub("://", "w<?", link), link)})) if link else None, links)
		return len(links) > 0
	#Final Link de Site

	def __SendChatPacket(self, text, type):
		if len(text) > int(2):
			if text[0] == '/' and text[1] == 'n'or text[1] == 'N' and text[2] == ' ':
				newtext = text.split(' ', 1)
				net.SendChatPacket(newtext[0] + " " + player.GetName() + ": " + newtext[1], type)
				return
			elif text[0] == '/' and text[1] == 'n' or text[1] == 'N' and text[2] != ' ':
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Comando inexistente")
				return

		links = {}
		if self.GetLinks(text, links):
			for k, v in links.iteritems():
				text = text.replace(k, v)

		net.SendChatPacket(text, type)

		if app.ENABLE_EMOJI_SYSTEM:
			chat.SaveEmojisChat(text)
			if self.refreshEmojis:
				self.refreshEmojis.RefreshCategoria(0)

	def __SendPartyChatPacket(self, text):
		if 1 == len(text):
			self.RunCloseEvent()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_PARTY)
		self.__ResetChat()

	def __SendGuildChatPacket(self, text):
		if 1 == len(text):
			self.RunCloseEvent()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_GUILD)
		self.__ResetChat()

	def __SendShoutChatPacket(self, text):
		if 1 == len(text):
			self.RunCloseEvent()
			return

		if app.GetTime() < self.lastShoutTime + 15:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.CHAT_SHOUT_LIMIT)
			self.__ResetChat()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_SHOUT)
		self.__ResetChat()

		self.lastShoutTime = app.GetTime()

	def __SendGlobalChatPacket(self, text):
		if 1 == len(text):
			self.RunCloseEvent()
			return

		if app.GetTime() < self.lastGlobalTime + 60:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.CHAT_GLOBAL_LIMIT)
			self.__ResetChat()
			return

		self.__SendChatPacket(text[1:], chat.CHAT_TYPE_GLOBAL)
		self.__ResetChat()

		self.lastGlobalTime = app.GetTime()

	def __SendTalkingChatPacket(self, text):
		self.__SendChatPacket(text, chat.CHAT_TYPE_TALKING)
		self.__ResetChat()

	def OnIMETab(self):
		return False

	def OnIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self)
		if self.GetTextSize()[0] > 430:
			ime.PasteBackspace()
		self.__CheckChatMark()

	def __CheckChatMark(self):
		self.overTextLine.Hide()

		text = self.GetText()
		if len(text) > 0:
			if '#' == text[0]:
				self.overTextLine.SetText("#")
				self.overTextLine.Show()
			elif '%' == text[0]:
				self.overTextLine.SetText("%")
				self.overTextLine.Show()
			elif '!' == text[0]:
				self.overTextLine.SetText("!")
				self.overTextLine.Show()
			elif '&' == text[0]:
				self.overTextLine.SetText("&")
				self.overTextLine.Show()

	def OnIMEKeyDown(self, key):
		if app.VK_UP == key:
			self.__PrevLastSentenceStack()
			return True

		if app.VK_DOWN == key:
			self.__NextLastSentenceStack()
			return True

		ui.EditLine.OnIMEKeyDown(self, key)

	def __PrevLastSentenceStack(self):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if self.lastSentenceStack and self.lastSentencePos < len(self.lastSentenceStack):
			self.lastSentencePos += 1
			lastSentence = self.lastSentenceStack[-self.lastSentencePos]
			self.SetText(lastSentence)
			self.SetEndPosition()

	def __NextLastSentenceStack(self):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if self.lastSentenceStack and self.lastSentencePos > 1:
			self.lastSentencePos -= 1
			lastSentence = self.lastSentenceStack[-self.lastSentencePos]
			self.SetText(lastSentence)
			self.SetEndPosition()

	def __PushLastSentenceStack(self, text):
		global ENABLE_LAST_SENTENCE_STACK
		if not ENABLE_LAST_SENTENCE_STACK:
			return

		if len(text) <= 0:
			return

		LAST_SENTENCE_STACK_SIZE = 32
		if len(self.lastSentenceStack) > LAST_SENTENCE_STACK_SIZE:
			self.lastSentenceStack.pop(0)

		self.lastSentenceStack.append(text)

	def OnIMEReturn(self):
		if self.GetTextSize()[0] > 430:
			return

		text = self.GetText()
		textLen = len(text)
		self.__PushLastSentenceStack(text)

		textSpaceCount = text.count(' ')

		if (textLen > 0) and (textLen != textSpaceCount):
			if '#' == text[0]:
				self.__SendPartyChatPacket(text)
			elif '%' == text[0]:
				self.__SendGuildChatPacket(text)
			elif '!' == text[0]:
				self.__SendShoutChatPacket(text)
			elif '&' == text[0]:
				self.__SendGlobalChatPacket(text)
			else:
				self.__SendTalkingChatPacket(text)
		else:
			self.__ClearChat()
			if self.eventReturn:
				self.eventReturn()

		return True

	def OnPressEscapeKey(self):
		self.__ClearChat()
		if self.eventEscape:
			self.eventEscape()
		return True

	def RunCloseEvent(self):
		if self.eventEscape:
			self.eventEscape()

	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)
		else:
			ui.EditLine.OnMouseLeftButtonDown(self)

class ChatInputSet(ui.Window):

	CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	def __init__(self):
		ui.Window.__init__(self)
		self.SetWindowName("ChatInputSet")

		InsertChatInputSetWindow(self)
		self.__Create()

	def __del__(self):
		ui.Window.__del__(self)

	def __Create(self):
		chatModeButton = ChatModeButton()
		chatModeButton.SetParent(self)
		chatModeButton.SetSize(40, 17)
		chatModeButton.SetText(localeinfo.CHAT_NORMAL)
		chatModeButton.SetPosition(7, 2)
		chatModeButton.SetEvent(self.OnChangeChatMode)
		self.chatModeButton = chatModeButton

		chatLine = ChatLine()
		chatLine.SetParent(self)
		if app.ENABLE_EMOJI_SYSTEM:
			chatLine.SetMax(770)
			chatLine.SetUserMax(110)
		else:
			chatLine.SetMax(512)
			chatLine.SetUserMax(76)
		chatLine.SetText("")
		chatLine.SetTabEvent(self.OnChangeChatMode)
		chatLine.x = 0
		chatLine.y = 0
		chatLine.width = 0
		chatLine.height = 0
		self.chatLine = chatLine

		btnSend = ui.Button()
		btnSend.SetParent(self)
		btnSend.SetUpVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_01.sub")
		btnSend.SetOverVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_02.sub")
		btnSend.SetDownVisual("d:/ymir work/ui/game/taskbar/Send_Chat_Button_03.sub")
		if app.ENABLE_EMOJI_SYSTEM:
			toolTipbtnSend = ui.Ballon()
			toolTipbtnSend.SetParent(btnSend)
			toolTipbtnSend.SetPosition(0, -38)
			toolTipbtnSend.SetWindowHorizontalAlignCenter()
			toolTipbtnSend.Hide()
			toolTipbtnSend.SetText(localeinfo.CHAT_SEND_CHAT)
			self.toolTipbtnSend = toolTipbtnSend
			btnSend.SetToolTipWindow(self.toolTipbtnSend)
		else:
			btnSend.SetToolTipText(localeinfo.CHAT_SEND_CHAT)
		btnSend.SetEvent(self.chatLine.OnIMEReturn)
		self.btnSend = btnSend

	def Destroy(self):
		self.Hide()
		self.chatModeButton = None
		self.chatLine = None
		self.btnSend = None

	def Open(self):
		self.chatLine.Show()
		if app.ENABLE_EMOJI_SYSTEM:
			self.chatLine.SetPosition(77, 9)
		else:
			self.chatLine.SetPosition(57, 9)
		self.chatLine.SetFocus()
		self.chatLine.OpenChat()

		self.chatModeButton.SetPosition(7, 2)
		self.chatModeButton.Show()

		self.btnSend.Show()
		self.Show()

		self.RefreshPosition()
		return True

	def Close(self):
		self.chatLine.KillFocus()
		self.chatLine.Hide()
		self.chatModeButton.Hide()
		self.btnSend.Hide()
		self.Hide()
		return True

	def SetEscapeEvent(self, event):
		self.chatLine.SetEscapeEvent(event)

	def SetReturnEvent(self, event):
		self.chatLine.SetReturnEvent(event)

	def OnChangeChatMode(self):
		RefreshChatMode()

	def OnRefreshChatMode(self):
		self.chatLine.ChangeChatMode()
		self.chatModeButton.SetText(self.chatLine.GetCurrentChatModeName())

	def SetChatFocus(self):
		self.chatLine.SetFocus()

	def KillChatFocus(self):
		self.chatLine.KillFocus()

	def SetChatMax(self, max):
		self.chatLine.SetUserMax(max)

	def RefreshPosition(self):
		if app.ENABLE_EMOJI_SYSTEM:
			self.chatLine.SetSize(self.GetWidth() - 113, 13)
		else:
			self.chatLine.SetSize(self.GetWidth() - 93, 13)

		self.btnSend.SetPosition(self.GetWidth() - 25, 2)

		(self.chatLine.x, self.chatLine.y, self.chatLine.width, self.chatLine.height) = self.chatLine.GetRect()

	def BindInterface(self, interface):
		self.chatLine.BindInterface(interface)

	def OnRender(self):
		(x, y, width, height) = self.chatLine.GetRect()
		ui.RenderRoundBox(x - 4, y - 8, width + 7, height + 5, self.CHAT_OUTLINE_COLOR)

class ChatWindow(ui.Window):

	BOARD_START_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
	BOARD_END_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.611)
	BOARD_MIDDLE_COLOR = BOARD_END_COLOR
	CHAT_OUTLINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	if app.ENABLE_EMOJI_SYSTEM:
		LINE_HEIGHT = 0
	EDIT_LINE_HEIGHT = 85
	CHAT_WINDOW_WIDTH = 600

	class ChatBackBoard(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
		def __del__(self):
			ui.Window.__del__(self)

	class ChatButton(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("float")
			self.AddFlag("movable")
			self.AddFlag("restrict_x")
			self.topFlag = False
			self.SetWindowName("ChatWindow:ChatButton")

		def __del__(self):
			ui.DragButton.__del__(self)

		def SetOwner(self, owner):
			self.owner = owner

		def OnMouseOverIn(self):
			app.SetCursor(app.VSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

		def OnTop(self):
			if self.topFlag:
				return

			self.topFlag = True
			self.owner.SetTop()
			self.topFlag = False

	def __init__(self):
		ui.Window.__init__(self)
		self.AddFlag("float")

		self.SetWindowName("ChatWindow")

		self.boardState = chat.BOARD_STATE_VIEW
		self.chatID = chat.CreateChatSet(chat.CHAT_SET_CHAT_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_VIEW)

		if app.ENABLE_EMOJI_SYSTEM:
			chat.SetStep(self.chatID, 20)
			chat.SetFontNameChat("Verdana:14")

		self.xBar = 0
		self.yBar = 0
		self.widthBar = 0
		self.heightBar = 0
		self.curHeightBar = 0
		self.visibleLineCount = 0
		self.scrollBarPos = 1.0

		if app.ENABLE_EMOJI_SYSTEM:
			emojisBoard = uiemojis.EmojisBoard()
			emojisBoard.SetParent(self)
			self.emojisBoard = emojisBoard

		chatInputSet = ChatInputSet()
		chatInputSet.SetParent(self)
		chatInputSet.SetEscapeEvent(self.CloseChat)
		chatInputSet.SetReturnEvent(self.CloseChat)
		chatInputSet.SetSize(550, 25)
		self.chatInputSet = chatInputSet

		if app.ENABLE_EMOJI_SYSTEM:
			btnEmojiExpandir = ui.Button()
			btnEmojiExpandir.SetParent(self)
			btnEmojiExpandir.SetUpVisual("d:/ymir work/ui/emoji/open_norm.png")
			btnEmojiExpandir.SetOverVisual("d:/ymir work/ui/emoji/open_over.png")
			btnEmojiExpandir.SetDownVisual("d:/ymir work/ui/emoji/open_down.png")
			# btnEmojiExpandir.SetButtonScale(0.26, 0.26)
			btnEmojiExpandir.SetPosition(52, 3)
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
			btnEmojiRetrair.SetToolTipText("Selecione um Emoji")
			btnEmojiRetrair.SetPosition(52, 3 + 250)
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

		btnSendWhisper = ui.Button()
		btnSendWhisper.SetParent(self)
		btnSendWhisper.SetUpVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_01.sub")
		btnSendWhisper.SetOverVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_02.sub")
		btnSendWhisper.SetDownVisual("d:/ymir work/ui/game/taskbar/Send_Whisper_Button_03.sub")
		btnSendWhisper.Hide()
		if app.ENABLE_EMOJI_SYSTEM:
			toolTipSendWhisper = ui.Ballon()
			toolTipSendWhisper.SetParent(self)
			toolTipSendWhisper.SetPosition(0, -38)
			toolTipSendWhisper.SetWindowHorizontalAlignCenter()
			toolTipSendWhisper.Hide()
			toolTipSendWhisper.SetText(localeinfo.CHAT_SEND_MEMO)
			self.toolTipSendWhisper = toolTipSendWhisper
			btnSendWhisper.SetToolTipWindow(self.toolTipSendWhisper)
		else:
			btnSendWhisper.SetToolTipText(localeinfo.CHAT_SEND_MEMO)
		self.btnSendWhisper = btnSendWhisper

		btnChatLog = ui.Button()
		btnChatLog.SetParent(self)
		btnChatLog.SetUpVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_01.sub")
		btnChatLog.SetOverVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_02.sub")
		btnChatLog.SetDownVisual("d:/ymir work/ui/game/taskbar/Open_Chat_Log_Button_03.sub")
		btnChatLog.Hide()
		if app.ENABLE_EMOJI_SYSTEM:
			toolTipChatLog = ui.Ballon()
			toolTipChatLog.SetParent(self)
			toolTipChatLog.SetPosition(0, -38)
			toolTipChatLog.SetWindowHorizontalAlignCenter()
			toolTipChatLog.Hide()
			toolTipChatLog.SetText(localeinfo.CHAT_LOG)
			self.toolTipChatLog = toolTipChatLog
			btnChatLog.SetToolTipWindow(self.toolTipChatLog)
		else:
			btnChatLog.SetToolTipText(localeinfo.CHAT_LOG)
		self.btnChatLog = btnChatLog

		btnChatSizing = self.ChatButton()
		btnChatSizing.SetOwner(self)
		btnChatSizing.SetMoveEvent(self.Refresh)
		btnChatSizing.Hide()
		self.btnChatSizing = btnChatSizing

		imgChatBar = ui.ExpandedImageBox()
		imgChatBar.SetParent(self.btnChatSizing)
		imgChatBar.AddFlag("not_pick")
		imgChatBar.LoadImage("interface/controls/special/chat/bar.png")
		imgChatBar.Show()
		self.imgChatBar = imgChatBar

		scrollBar = ui.New_ThinScrollBar()
		scrollBar.AddFlag("float")
		scrollBar.SetScrollEvent(self.OnScroll)
		self.scrollBar = scrollBar

		self.Refresh()
		self.chatInputSet.RefreshPosition()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Hide()
		self.chatInputSet.Destroy()
		self.chatInputSet = None

		self.btnSendWhisper = 0
		self.btnChatLog = 0
		self.btnChatSizing = 0
		if app.ENABLE_EMOJI_SYSTEM:
			self.emojisBoard.Destroy()
			self.emojisBoard = None
			self.btnEmojiExpandir = None
			self.btnEmojiRetrair = None

	if app.ENABLE_EMOJI_SYSTEM:
		def OpenEmojis(self):
			self.LINE_HEIGHT = 250

			self.btnEmojiExpandir.Hide()
			self.btnEmojiRetrair.Show()
			self.emojisBoard.Open(self.chatInputSet.chatLine)

			self.SetSize(self.CHAT_WINDOW_WIDTH, self.EDIT_LINE_HEIGHT + 250)
			(x, y, width, height) = self.GetRect()
			self.SetPosition(x, y - 250)
			self.SetHeight(self.GetHeight() + 220)

			self.chatInputSet.SetPosition(0, 250)
			self.btnSendWhisper.SetPosition(self.GetWidth() - 50, 2 + self.LINE_HEIGHT)
			self.btnChatLog.SetPosition(self.GetWidth() - 25, 2 + self.LINE_HEIGHT)
			self.Refresh()

		def CloseEmojis(self):
			self.LINE_HEIGHT = 0

			self.btnEmojiExpandir.Show()
			self.btnEmojiRetrair.Hide()
			self.emojisBoard.Close()

			self.SetSize(self.CHAT_WINDOW_WIDTH, self.EDIT_LINE_HEIGHT)
			(x, y, width, height) = self.GetRect()
			self.SetPosition(x, y + 250)
			self.SetHeight(224)

			self.chatInputSet.SetPosition(0, 0)
			self.btnSendWhisper.SetPosition(self.GetWidth() - 50, 2 + self.LINE_HEIGHT)
			self.btnChatLog.SetPosition(self.GetWidth() - 25, 2 + self.LINE_HEIGHT)
			self.Refresh()

	def OpenChat(self):
		if app.ENABLE_EMOJI_SYSTEM:
			self.SetSize(self.CHAT_WINDOW_WIDTH, self.EDIT_LINE_HEIGHT + self.LINE_HEIGHT)
		else:
			self.SetSize(self.CHAT_WINDOW_WIDTH, self.EDIT_LINE_HEIGHT)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_EDIT)
		self.boardState = chat.BOARD_STATE_EDIT
		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()
		chat.SetPosition(self.chatID, x + 10, y)
		if app.ENABLE_EMOJI_SYSTEM:
			chat.SetHeight(self.chatID, y - btnY - (self.EDIT_LINE_HEIGHT + self.LINE_HEIGHT) + 100 - 25)
		else:
			chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT + 100)

		if self.IsShow():
			self.btnChatSizing.Show()

		self.Refresh()

		if app.ENABLE_EMOJI_SYSTEM:
			self.btnSendWhisper.SetPosition(self.GetWidth() - 50, 2 + self.LINE_HEIGHT)
		else:
			self.btnSendWhisper.SetPosition(self.GetWidth() - 50, 2)
		self.btnSendWhisper.Show()

		if app.ENABLE_EMOJI_SYSTEM:
			self.btnChatLog.SetPosition(self.GetWidth() - 25, 2 + self.LINE_HEIGHT)
		else:
			self.btnChatLog.SetPosition(self.GetWidth() - 25, 2)
		self.btnChatLog.Show()

		self.chatInputSet.Open()
		self.chatInputSet.SetTop()

		if app.ENABLE_EMOJI_SYSTEM:
			if self.LINE_HEIGHT > 0:
				self.emojisBoard.Open(self.chatInputSet.chatLine)
				self.btnEmojiExpandir.Hide()
				self.btnEmojiRetrair.Show()
			else:
				self.emojisBoard.Close()
				self.btnEmojiRetrair.Hide()
				self.btnEmojiExpandir.Show()

		self.chatInputSet.Open()
		self.chatInputSet.SetTop()
		self.SetTop()

	def CloseChat(self):
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_VIEW)
		self.boardState = chat.BOARD_STATE_VIEW
		(x, y, width, height) = self.GetRect()
		if app.ENABLE_EMOJI_SYSTEM:
			if self.LINE_HEIGHT > 0:
				self.LINE_HEIGHT = 0

				self.SetPosition(x, y + 250)
				self.SetHeight(224)

				self.chatInputSet.SetPosition(0, 0)
				self.btnSendWhisper.SetPosition(self.GetWidth() - 50, 2 + self.LINE_HEIGHT)
				self.btnChatLog.SetPosition(self.GetWidth() - 25, 2 + self.LINE_HEIGHT)
				self.Refresh()

			chat.SetPosition(self.chatID, x + 10, y + (self.EDIT_LINE_HEIGHT + self.LINE_HEIGHT))
			chat.Close()
		else:
			chat.SetPosition(self.chatID, x + 10, y + self.EDIT_LINE_HEIGHT)

		self.SetSize(self.CHAT_WINDOW_WIDTH, 0)

		self.chatInputSet.Close()
		self.btnSendWhisper.Hide()
		self.btnChatLog.Hide()
		self.btnChatSizing.Hide()
		if app.ENABLE_EMOJI_SYSTEM:
			self.emojisBoard.Close()
			self.btnEmojiExpandir.Hide()
			self.btnEmojiRetrair.Hide()

		self.Refresh()

	def SetSendWhisperEvent(self, event):
		self.btnSendWhisper.SetEvent(event)

	def SetOpenChatLogEvent(self, event):
		self.btnChatLog.SetEvent(event)

	def IsEditMode(self):
		if chat.BOARD_STATE_EDIT == self.boardState:
			return True
		return False

	def __RefreshSizingBar(self):
		(x, y, width, height) = self.GetRect()
		gxChat, gyChat = self.btnChatSizing.GetGlobalPosition()
		self.btnChatSizing.SetPosition(x, gyChat)
		self.btnChatSizing.SetSize(width, 10)
		self.imgChatBar.SetPosition(-12-7, -70+60-6)

	def SetPosition(self, x, y):
		ui.Window.SetPosition(self, x, y)
		self.__RefreshSizingBar()

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		self.__RefreshSizingBar()

	def SetHeight(self, height):
		gxChat, gyChat = self.btnChatSizing.GetGlobalPosition()
		self.btnChatSizing.SetPosition(gxChat, wndMgr.GetScreenHeight() - height)

	def Refresh(self):
		if self.boardState == chat.BOARD_STATE_EDIT:
			self.RefreshBoardEditState()
		elif self.boardState == chat.BOARD_STATE_VIEW:
			self.RefreshBoardViewState()

	def RefreshBoardEditState(self):
		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()

		self.xBar = x
		self.yBar = btnY
		self.widthBar = width
		if app.ENABLE_EMOJI_SYSTEM:
			self.heightBar = y - btnY + (self.EDIT_LINE_HEIGHT + self.LINE_HEIGHT)
		else:
			self.heightBar = y - btnY + self.EDIT_LINE_HEIGHT
		self.curHeightBar = self.heightBar
		chat.SetPosition(self.chatID, x + 10, y)

		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT - 25)
		chat.ArrangeShowingChat(self.chatID)

		if btnY > y:
			self.btnChatSizing.SetPosition(btnX, y)
			if app.ENABLE_EMOJI_SYSTEM:
				self.heightBar = (self.EDIT_LINE_HEIGHT + self.LINE_HEIGHT)
			else:
				self.heightBar = self.EDIT_LINE_HEIGHT

	def RefreshBoardViewState(self):
		(x, y, width, height) = self.GetRect()
		(btnX, btnY) = self.btnChatSizing.GetGlobalPosition()
		textAreaHeight = self.visibleLineCount * chat.GetLineStep(self.chatID) + 76
		chat.SetPosition(self.chatID, x + 10, y + self.EDIT_LINE_HEIGHT)
		chat.SetHeight(self.chatID, y - btnY - self.EDIT_LINE_HEIGHT + 100)

		if self.boardState == chat.BOARD_STATE_EDIT:
			textAreaHeight += 45
		elif self.visibleLineCount == 0:
			textAreaHeight = 0
		elif self.visibleLineCount != 0:
			textAreaHeight += 10 + 10

		self.xBar = x
		if app.ENABLE_EMOJI_SYSTEM:
			self.yBar = y + (self.EDIT_LINE_HEIGHT + self.LINE_HEIGHT) - textAreaHeight
		else:
			self.yBar = y + self.EDIT_LINE_HEIGHT - textAreaHeight
		self.widthBar = width
		self.heightBar = textAreaHeight
		self.scrollBar.Hide()

	def OnUpdate(self):
		if self.boardState == chat.BOARD_STATE_EDIT:
			chat.Update(self.chatID)
		elif self.boardState == chat.BOARD_STATE_VIEW:
			if systemSetting.IsViewChat():
				chat.Update(self.chatID)

	def OnRender(self):
		if chat.GetVisibleLineCount(self.chatID) != self.visibleLineCount:
			self.visibleLineCount = chat.GetVisibleLineCount(self.chatID)
			self.Refresh()

		if self.curHeightBar != self.heightBar:
			self.curHeightBar += (self.heightBar - self.curHeightBar) / 10

		if self.boardState == chat.BOARD_STATE_EDIT:
			grp.SetColor(self.BOARD_MIDDLE_COLOR)
			grp.RenderBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar) + 10, self.widthBar, self.curHeightBar)
			chat.Render(self.chatID)
		elif self.boardState == chat.BOARD_STATE_VIEW:
			if systemSetting.IsViewChat():
				grp.RenderGradationBar(self.xBar, self.yBar + (self.heightBar - self.curHeightBar), self.widthBar, self.curHeightBar, self.BOARD_START_COLOR, self.BOARD_END_COLOR)
				chat.Render(self.chatID)

	def OnTop(self):
		self.btnChatSizing.SetTop()
		self.scrollBar.SetTop()

	def OnScroll(self):
		self.scrollBarPos = self.scrollBar.GetPos()

		lineCount = chat.GetLineCount(self.chatID)
		visibleLineCount = chat.GetVisibleLineCount(self.chatID)
		endLine = visibleLineCount + int(float(lineCount - visibleLineCount) * self.scrollBarPos)

		chat.SetEndPos(self.chatID, self.scrollBarPos)

	def OnChangeChatMode(self):
		self.chatInputSet.OnChangeChatMode()

	def SetChatFocus(self):
		self.chatInputSet.SetChatFocus()

	def BindInterface(self, interface):
		self.chatInputSet.BindInterface(interface)

class ChatLogWindow(ui.Window):

	BLOCK_WIDTH = 32
	CHAT_MODE_NAME = ( localeinfo.CHAT_NORMAL, localeinfo.CHAT_PARTY, localeinfo.CHAT_GUILD, localeinfo.CHAT_SHOUT, localeinfo.CHAT_GLOBAL, localeinfo.CHAT_INFORMATION, localeinfo.CHAT_NOTICE, )
	CHAT_MODE_INDEX = (
		chat.CHAT_TYPE_TALKING,
		chat.CHAT_TYPE_PARTY,
		chat.CHAT_TYPE_GUILD,
		chat.CHAT_TYPE_SHOUT,
		chat.CHAT_TYPE_GLOBAL,
		chat.CHAT_TYPE_INFO,
		chat.CHAT_TYPE_NOTICE,
	)

	CHAT_LOG_WINDOW_MINIMUM_WIDTH = 450
	CHAT_LOG_WINDOW_MINIMUM_HEIGHT = 120

	class ResizeButton(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)

		def __del__(self):
			ui.DragButton.__del__(self)

		def OnMouseOverIn(self):
			app.SetCursor(app.HVSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self):
		self.allChatMode = True
		if app.ENABLE_EMOJI_SYSTEM:
			self.linhaChatLog = None
		else:
			self.chatInputSet = None

		ui.Window.__init__(self)
		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetWindowName("ChatLogWindow")
		if app.ENABLE_EMOJI_SYSTEM:
			self.__CreateLine()
		else:
			self.__CreateChatInputSet()
		self.__CreateWindow()
		self.__CreateButton()
		self.__CreateScrollBar()

		self.chatID = chat.CreateChatSet(chat.CHAT_SET_LOG_WINDOW)
		chat.SetBoardState(self.chatID, chat.BOARD_STATE_LOG)
		if app.ENABLE_EMOJI_SYSTEM:
			chat.SetStep(self.chatID, 20)
			chat.SetFontNameChat("Verdana:14")

		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)

		self.SetPosition(20, 20)
		self.SetSize(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT)
		self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH-self.btnSizing.GetWidth(), self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT-self.btnSizing.GetHeight()+2)

		self.OnResize()

	if app.ENABLE_EMOJI_SYSTEM:
		def __CreateLine(self):
			linhaChatLog = ui.Line()
			linhaChatLog.SetParent(self)
			linhaChatLog.SetColor(0xffe6d0a2)
			linhaChatLog.SetWindowVerticalAlignBottom()
			linhaChatLog.Show()
			self.linhaChatLog = linhaChatLog
	else:
		def __CreateChatInputSet(self):
			chatInputSet = ChatInputSet()
			chatInputSet.SetParent(self)
			chatInputSet.SetEscapeEvent(self.Close)
			chatInputSet.SetWindowVerticalAlignBottom()
			chatInputSet.Open()
			self.chatInputSet = chatInputSet

	def __CreateWindow(self):
		interface = "interface/controls/special/chat/"

		imgLeft = ui.ImageBox()
		imgLeft.AddFlag("not_pick")
		imgLeft.SetParent(self)

		imgCenter = ui.ExpandedImageBox()
		imgCenter.AddFlag("not_pick")
		imgCenter.SetParent(self)

		imgRight = ui.ImageBox()
		imgRight.AddFlag("not_pick")
		imgRight.SetParent(self)
		imgLeft.LoadImage(interface + "titlebar_left.tga")
		imgLeft.SetPosition(-8,-17)
		imgCenter.LoadImage(interface + "titlebar_center.tga")
		imgRight.LoadImage(interface + "titlebar_right.tga")

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		btnClose = ui.Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("interface/controls/common/button/board_close_01_normal.tga")
		btnClose.SetOverVisual("interface/controls/common/button/board_close_02_hover.tga")
		btnClose.SetDownVisual("interface/controls/common/button/board_close_03_active.tga")
		btnClose.SetToolTipText(localeinfo.UI_CLOSE, 0, -23)
		btnClose.SetEvent(self.Close)
		btnClose.Show()

		btnSizing = self.ResizeButton()
		btnSizing.SetParent(self)
		btnSizing.SetMoveEvent(self.OnResize)
		btnSizing.SetSize(16, 16)
		btnSizing.Show()

		titleName = ui.TextLine()
		titleName.SetParent(self)
		titleName.SetPosition(0, 6)
		titleName.SetHorizontalAlignCenter()
		titleName.SetPackedFontColor(0xFFCAA76F)
		titleName.SetText(localeinfo.CHAT_LOG_TITLE)
		titleName.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose
		self.btnSizing = btnSizing
		self.titleName = titleName

	def __CreateButton(self):
		interface = "interface/controls/special/chat/"

		bx = 3

		btnAll = ui.RadioButton()
		btnAll.SetParent(self)
		btnAll.SetPosition(bx, 27)
		btnAll.SetUpVisual(interface + "log_button.tga")
		btnAll.SetOverVisual(interface + "log_button_hover.tga")
		btnAll.SetDownVisual(interface + "log_button_down.tga")
		btnAll.SetText("|cfff8d090" + localeinfo.CHAT_ALL)
		btnAll.SetEvent(self.ToggleAllChatMode)
		btnAll.Down()
		btnAll.Show()
		self.btnAll = btnAll

		x = bx + 52
		i = 0

		self.modeButtonList = []
		for name in self.CHAT_MODE_NAME:
			btn = ui.ToggleButton()
			btn.SetParent(self)
			btn.SetPosition(x, 27)
			btn.SetUpVisual(interface + "log_button.tga")
			btn.SetOverVisual(interface + "log_button_hover.tga")
			btn.SetDownVisual(interface + "log_button_down.tga")
			btn.SetText("|cffa08784" + name)
			btn.Show()

			mode = self.CHAT_MODE_INDEX[i]
			btn.SetToggleUpEvent(self.ToggleUpChatMode, mode, btn, name)
			btn.SetToggleDownEvent(self.ToggleDownChatMode, mode, btn, name)
			self.modeButtonList.append(btn)

			x += 52
			i += 1

	def __CreateScrollBar(self):
		scrollBar = ui.New_ThinScrollBar()
		scrollBar.SetParent(self)
		scrollBar.Show()
		scrollBar.SetScrollEvent(self.OnScroll)
		self.scrollBar = scrollBar
		self.scrollBarPos = 1.0

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Close()
		self.imgLeft = None
		self.imgCenter = None
		self.imgRight = None
		self.btnClose = None
		self.btnSizing = None
		self.scrollBar = None
		if app.ENABLE_EMOJI_SYSTEM:
			self.linhaChatLog = None
		else:
			self.chatInputSet = None

		for btn in self.modeButtonList:
			btn.Hide()
			btn.SetToggleDownEvent(0)
			btn.SetToggleUpEvent(0)
			btn = None

		del self.modeButtonList

	def ToggleAllChatMode(self):
		if self.allChatMode:
			return
		if len(self.modeButtonList) == 0:
			return

		self.allChatMode = True

		for i in self.CHAT_MODE_INDEX:
			chat.EnableChatMode(self.chatID, i)
		for btn in self.modeButtonList:
			btn.SetUp()

		i = 0
		for name in self.CHAT_MODE_NAME:
			self.modeButtonList[i].SetText("|cffa08784" + name)
			i += 1
		self.btnAll.SetText("|cfff8d090" + localeinfo.CHAT_ALL)

	def ToggleDownChatMode(self, mode, button, name):
		if self.allChatMode:
			self.allChatMode = False
			for i in self.CHAT_MODE_INDEX:
				chat.DisableChatMode(self.chatID, i)
			chat.EnableChatMode(self.chatID, mode)
			self.btnAll.SetUp()
			self.btnAll.SetText("|cffa08784" + localeinfo.CHAT_ALL)
			button.SetText("|cfff8d090" + name)
		else:
			chat.ToggleChatMode(self.chatID, mode)
			button.SetText("|cfff8d090" + name)
			if not chat.GetChatMode(self.chatID):
				self.btnAll.Down()
				self.ToggleAllChatMode()

	def ToggleUpChatMode(self, mode, button, name):
		if self.allChatMode:
			self.allChatMode = False
			for i in self.CHAT_MODE_INDEX:
				chat.DisableChatMode(self.chatID, i)
			chat.EnableChatMode(self.chatID, mode)
			self.btnAll.SetUp()
			self.btnAll.SetText("|cffa08784" + localeinfo.CHAT_ALL)
			button.SetText("|cffa08784" + name)
		else:
			chat.ToggleChatMode(self.chatID, mode)
			button.SetText("|cffa08784" + name)
			if not chat.GetChatMode(self.chatID):
				self.btnAll.Down()
				self.ToggleAllChatMode()

	def SetSize(self, width, height):
		self.imgCenter.SetScale(float((width - self.BLOCK_WIDTH) - 46) / 32, 1)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, -17)
		self.imgRight.SetPosition(width - 46, -17)
		self.btnClose.SetPosition(width - self.btnClose.GetWidth() + 1, 1)
		self.scrollBar.SetPosition(width - 20, 60)
		self.titleName.SetPosition(width/2, 6)
		self.scrollBar.SetScrollBarSize(height - 60 - 12 -5)
		self.scrollBar.SetPos(self.scrollBarPos)
		ui.Window.SetSize(self, width, height)

	def Open(self):
		self.OnResize()
		if not app.ENABLE_EMOJI_SYSTEM:
			self.chatInputSet.SetChatFocus()
		self.Show()

	def Close(self):
		if not app.ENABLE_EMOJI_SYSTEM:
			if self.chatInputSet:
				self.chatInputSet.KillChatFocus()
		self.Hide()

	def OnResize(self):
		x, y = self.btnSizing.GetLocalPosition()
		width = self.btnSizing.GetWidth()
		height = self.btnSizing.GetHeight()

		if x < self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width:
			self.btnSizing.SetPosition(self.CHAT_LOG_WINDOW_MINIMUM_WIDTH - width, y)
			return
		if y < self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height:
			self.btnSizing.SetPosition(x, self.CHAT_LOG_WINDOW_MINIMUM_HEIGHT - height)
			return

		self.scrollBar.LockScroll()
		self.SetSize(x + width, y + height)
		self.scrollBar.UnlockScroll()

		if app.ENABLE_EMOJI_SYSTEM:
			self.linhaChatLog.SetPosition(10, 16)
			self.linhaChatLog.SetSize(self.GetWidth() - 35, 0)
		else:
			self.chatInputSet.SetPosition(0, 25)
			self.chatInputSet.SetSize(self.GetWidth() - 20, 20)
			self.chatInputSet.RefreshPosition()
			self.chatInputSet.SetChatMax(self.GetWidth() / 8)

	def OnScroll(self):
		self.scrollBarPos = self.scrollBar.GetPos()

		lineCount = chat.GetLineCount(self.chatID)
		visibleLineCount = chat.GetVisibleLineCount(self.chatID)
		endLine = visibleLineCount + int(float(lineCount - visibleLineCount) * self.scrollBarPos)

		chat.SetEndPos(self.chatID, self.scrollBarPos)

	def OnRender(self):
		(x, y, width, height) = self.GetRect()
		grp.SetColor(0x77000000)
		grp.RenderBar(x, y, width, height)
		grp.SetColor(0xff525552)
		grp.RenderBox(x, y, width-2, height)
		grp.SetColor(0xff000000)
		grp.RenderBox(x+1, y+1, width-2, height)

		grp.SetColor(0xff989898)
		grp.RenderLine(x+width-13, y+height-1, 11, -11)
		grp.RenderLine(x+width-9, y+height-1, 7, -7)
		grp.RenderLine(x+width-5, y+height-1, 3, -3)
		chat.ArrangeShowingChat(self.chatID)
		chat.SetPosition(self.chatID, x + 10, y + height - 25)

		chat.SetHeight(self.chatID, height - 45 - 25)
		chat.Update(self.chatID)
		chat.Render(self.chatID)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			if app.IsPressed(app.DIK_LALT):
				link = chat.GetLinkFromHyperlink(hyperlink)
				ime.PasteString(link)
			else:
				self.interface.MakeHyperlinkTooltip(hyperlink)