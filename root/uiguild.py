#favor manter essa linha
import _app as app
import _net as net
import _chat as chat
import _player as player
import _chr as chr
import ui
import _grp as grp
import _snd as snd
import _skill as skill
import _guild as guild
import _wnd_mgr as wndMgr
import _safebox as safebox
import uicommon
import constinfo
import exception
import localeinfo
import _background as background
import mousemodule
import uipickmoney
import uiuploadmark
import playersettingmodule

from weakref import proxy

def NumberToMoneyString(n):
	return localeinfo.NumberToMoneyString(n)

def GetGVGKey(srcGuildID, dstGuildID):
	minID = min(srcGuildID, dstGuildID)
	maxID = max(srcGuildID, dstGuildID)
	return minID*1000 + maxID

class MouseReflector(ui.Window):
	def __init__(self, parent):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.AddFlag("not_pick")
		self.width = self.height = 0
		self.isDown = False

	def Down(self):
		self.isDown = True

	def Up(self):
		self.isDown = False

	def OnRender(self):
		if self.isDown:
			grp.SetColor(ui.WHITE_COLOR)
		else:
			grp.SetColor(ui.HALF_WHITE_COLOR)

		x, y = self.GetGlobalPosition()
		grp.RenderBar(x+2, y+2, self.GetWidth()-4, self.GetHeight()-4)

class EditableTextSlot(ui.ImageBox):
	def __init__(self, parent, x, y):
		ui.ImageBox.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.LoadImage("interface/controls/special/guild/edit_grade_name.tga")

		self.mouseReflector = MouseReflector(self)
		self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())

		self.Enable = True
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetPackedFontColor(0xffffffff)
		self.textLine.SetPosition(8, 7)
		self.textLine.Show()
		self.event = None
		self.arg = 0
		self.Show()

		self.mouseReflector.UpdateRect()

	def __del__(self):
		ui.ImageBox.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetEvent(self, event, *args):
		self.event = ui.__mem_func__(event)
		self.arg = args

	def Disable(self):
		self.Enable = False

	def EnableW(self):
		self.Enable = True

	def OnMouseOverIn(self):
		if not self.Enable:
			return
		self.mouseReflector.Show()

	def OnMouseOverOut(self):
		if not self.Enable:
			return
		self.mouseReflector.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.Enable:
			return
		self.mouseReflector.Down()

	def OnMouseLeftButtonUp(self):
		if not self.Enable:
			return
		self.mouseReflector.Up()
		self.event(self.arg)

class CheckBox(ui.BarWithBox):
	def __init__(self, parent, x, y, event, *args):
		ui.BarWithBox.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.SetSize(37, 31)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.8))
		self.SetBoxColor(grp.GenerateColor(1.0, 1.0, 1.0, 0.5))
		self.SetFlashColor(ui.HALF_WHITE_COLOR)

		image = ui.MakeImageBox(self, "interface/controls/special/guild/ok.tga", 0, 0)
		image.AddFlag("not_pick")
		image.SetWindowHorizontalAlignCenter()
		image.SetWindowVerticalAlignCenter()
		image.Hide()

		self.Enable = True
		self.image = image
		self.event = ui.__mem_func__(event)
		self.args = args

		self.Show()

	def __del__(self):
		ui.BarWithBox.__del__(self)

	def SetCheck(self, flag):
		if flag:
			self.image.Show()
		else:
			self.image.Hide()

	def Disable(self):
		self.SetFlashColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.8))
		self.Enable = False

	def EnableW(self):
		self.SetFlashColor(ui.HALF_WHITE_COLOR)
		self.Enable = True

	def SetEvent(self, event, *args):
		self.event = ui.__mem_func__(event)
		self.args = args

	def OnMouseLeftButtonUp(self):
		if self.Enable:
			if self.event:
				self.event(* self.args)

class ChangeGradeNameDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def Open(self):
		self.gradeNameSlot.SetText("")
		self.gradeNameSlot.SetFocus()
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.SetPosition(xMouse - self.GetWidth()/2, yMouse + 20)
		self.SetTop()
		self.Show()

	def Close(self):
		self.gradeNameSlot.KillFocus()
		self.Hide()
		return True

	def SetGradeNumber(self, gradeNumber):
		self.gradeNumber = gradeNumber

	def GetGradeNumber(self):
		return self.gradeNumber

	def GetGradeName(self):
		return self.gradeNameSlot.GetText()

	def OnPressEscapeKey(self):
		self.Close()
		return True

### MENSAGEM DOS MEMBROS ###### MENSAGEM DOS MEMBROS ###### MENSAGEM DOS MEMBROS ###### MENSAGEM DOS MEMBROS ###
class CommentSlot(ui.Window):
	TEXT_LIMIT = 185

	def __init__(self):
		ui.Window.__init__(self)

		self.slotImage = ui.MakeImageBox(self, "interface/controls/special/guild/dialog_message_slot.tga", 0, 0)
		self.slotImage.AddFlag("not_pick")
		self.noticeMarkImage = ui.MakeImageBox(self, "interface/controls/special/guild/dialog_message_importantmsg.tga", 87, 8)
		self.noticeMarkImage.Hide()
		self.deleteButton = ui.MakeButton(self, 307, 9, "", "interface/controls/special/guild/", "del_msg.tga", "del_msg_hover.tga", "del_msg_hover.tga")
		self.slotSimpleText = ui.MakeTextLine(self)
		self.slotSimpleText.SetPosition(10+96, 0)
		self.slotSimpleText.SetPackedFontColor(0xffa08784)
		self.slotSimpleText.SetWindowHorizontalAlignLeft()
		self.slotSimpleText.SetHorizontalAlignLeft()

		self.tip = ui.ThinBoardNew()
		self.tip.AddFlag("not_pick")
		self.tip.SetParent(self)
		self.tip.Hide()

		self.SetSize(self.slotImage.GetWidth()+10, self.slotImage.GetHeight())
		self.len = 0
		self.LINES = []
		self.Tooltip = 0

	def SplitText(self, text, limit):
		total_tokens = text.split()
		line_tokens = []
		line_len = 0
		lines = []
		for token in total_tokens:
			if "|" in token:
				sep_pos = token.find("|")
				line_tokens.append(token[:sep_pos])

				lines.append(" ".join(line_tokens))
				line_len = len(token) - (sep_pos + 1)
				line_tokens = [token[sep_pos+1:]]
			else:
				line_len += len(token)
				if len(line_tokens) + line_len > limit:
					lines.append(" ".join(line_tokens))
					line_len = len(token)
					line_tokens = [token]
				else:
					line_tokens.append(token)

		if line_tokens:
			lines.append(" ".join(line_tokens))

		return lines

	def SetText(self, text):
		self.len = len(text)
		i = 20

		self.slotSimpleText.SetText(text)
		(ix, iy) = self.slotSimpleText.GetTextSize()
		if ix > self.TEXT_LIMIT:
			self.Tooltip = 1
			ix = 0
			while ix < self.TEXT_LIMIT:
				self.slotSimpleText.SetText(text[:i]+"...")
				(ix, iy) = self.slotSimpleText.GetTextSize()
				i = i + 1

			lines = []
			lines = self.SplitText(text, 50)
			self.LINES = []

			if lines[0] != "":
				for index in range(len(lines)):
					line = ui.TextLine()
					line.SetParent(self.tip)
					line.SetText(lines[index])
					line.SetPackedFontColor(0xffff8784)
					line.SetPosition(0, 15+15*index)
					line.SetHorizontalAlignCenter()
					line.SetWindowHorizontalAlignCenter()
					line.Show()
					self.LINES.append(line)

				(x, y) = self.LINES[0].GetTextSize()
				for linha in self.LINES:
					(x_new, ignore) = linha.GetTextSize()
					bigger = max(x_new, x)
					x = bigger
				self.tip.SetSize(x+40, 30+len(lines)*15)
				self.tip.SetPosition(50, -(len(lines)*15))
				self.tip.SetWindowVerticalAlignTop()
				self.tip.SetWindowHorizontalAlignCenter()
			else:
				line = ui.MakeTextLine(self.tip)
				line.SetText(text)
				line.SetPackedFontColor(0xffff8784)
				line.SetHorizontalAlignCenter()
				line.SetWindowHorizontalAlignCenter()
				(x, y) = line.GetTextSize()
				self.LINES.append(line)
				self.tip.SetSize(x+40, y+30)
				self.tip.SetPosition(50, -12)
				self.tip.SetWindowVerticalAlignTop()
				self.tip.SetWindowHorizontalAlignCenter()
		else:
			self.Tooltip = 0

	def OnMouseOverIn(self):
		self.slotSimpleText.SetPackedFontColor(0xffff8784)
		if self.Tooltip:
			self.tip.Show()

	def OnMouseOverOut(self):
		self.slotSimpleText.SetPackedFontColor(0xffa08784)
		if self.Tooltip:
			self.tip.Hide()

class ListBox(ui.Window):
	IS_IN_COLOR = ui.GenerateColor(50, 34, 31)
	SELECTED_COLOR = ui.GenerateColor(90, 34, 31)
	TEMPORARY_PLACE = 3

	def __init__(self, layer = "UI"):
		ui.Window.__init__(self, layer)
		self.overLine = -1
		self.selectedLine = -1
		self.width = 0
		self.height = 0
		self.stepSize = 25
		self.basePos = 0
		self.showLineCount = 0
		self.itemCenterAlign = False
		self.itemList = []
		self.keyDict = {}
		self.textDict = {}
		self.event = None

	def __del__(self):
		ui.Window.__del__(self)

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetTextCenterAlign(self, flag):
		self.itemCenterAlign = flag

	def SetBasePos(self, pos):
		self.basePos = pos
		self._LocateItem()

	def ClearItem(self):
		self.keyDict = {}
		self.textDict = {}
		self.itemList = []
		self.overLine = -1
		self.selectedLine = -1

	def InsertItem(self, number, text):
		self.keyDict[len(self.itemList)] = number
		self.textDict[len(self.itemList)] = text

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetPackedFontColor(0xffa08784)
		textLine.SetText(text)
		textLine.Show()

		if self.itemCenterAlign:
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		self.itemList.append(textLine)

		self._LocateItem()

	def ChangeItem(self, number, text):
		for key, value in self.keyDict.items():
			if value == number:
				self.textDict[key] = text
				if number < len(self.itemList):
					self.itemList[key].SetText(text)
				return

	def LocateItem(self):
		self._LocateItem()

	def _LocateItem(self):
		skipCount = self.basePos
		yPos = 0
		self.showLineCount = 0

		for textLine in self.itemList:
			textLine.Hide()

			if skipCount > 0:
				skipCount -= 1
				continue

			textLine.SetPosition(5, yPos + 3)

			yPos += self.stepSize

			if yPos <= self.GetHeight():
				self.showLineCount += 1
				textLine.Show()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.itemList) * self.stepSize)
		self._LocateItem()

	def GetViewItemCount(self):
		return int(self.GetHeight() / self.stepSize)

	def GetItemCount(self):
		return len(self.itemList)

	def SetEvent(self, event):
		self.event = ui.__mem_func__(event)

	def SelectItem(self, line):
		if not self.keyDict.__contains__(line):
			return

		if line == self.selectedLine:
			return

		self.selectedLine = line
		self.event(self.keyDict.get(line, 0), self.textDict.get(line, "None"))

	def GetSelectedItem(self):
		return self.keyDict.get(self.selectedLine, 0)

	def OnMouseLeftButtonDown(self):
		if self.overLine < 0:
			return

	def OnMouseLeftButtonUp(self):
		if self.overLine >= 0:
			self.SelectItem(self.overLine+self.basePos)

	def OnUpdate(self):
		self.overLine = -1

		if self.IsIn():
			x, y = self.GetGlobalPosition()
			height = self.GetHeight()
			xMouse, yMouse = wndMgr.GetMousePosition()

			if yMouse - y < height - 1:
				self.overLine = (yMouse - y) / self.stepSize

				if self.overLine < 0:
					self.overLine = -1
				if self.overLine >= len(self.itemList):
					self.overLine = -1

	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE*2

		if -1 != self.overLine:
			grp.SetColor(self.IS_IN_COLOR)
			grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize - 6)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(self.SELECTED_COLOR)
					grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize -6)

class ComboBox(ui.Window):
	BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
	LINE_COLOR = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
	IS_IN_COLOR = grp.GenerateColor(0.1, 0.1, 0.1, 1.0)
	SELECTED_COLOR = ui.GenerateColor(90, 34, 31)

	class ListBoxWithBoard(ListBox):
		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def __del__(self):
			ListBox.__del__(self)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(ComboBox.BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(ComboBox.LINE_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
			grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

			ListBox.OnRender(self)

	def __init__(self):
		ui.Window.__init__(self)
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		self.isSelected = False
		self.isOver = False
		self.isListOpened = False
		self.event = None
		self.args = None
		self.enable = True

		background = ui.ImageBox()
		background.SetParent(self)
		background.AddFlag("not_pick")
		background.SetPosition(73, 4)
		background.LoadImage("interface/controls/common/dropdown/btn_01_normal.tga")
		background.Show()
		self.background = background

		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetVerticalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetText("")
		self.textLine.SetPosition(5, 0)
		self.textLine.Show()
		self.textLine.SetPackedFontColor(0xffff8784)

		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(self.OnSelectItem)
		self.listBox.Hide()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.Hide()
		self.textLine = None
		self.listBox = None

		self.event = None
		self.args = None

		self.background = None

	def SetPosition(self, x, y):
		ui.Window.SetPosition(self, x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		ui.Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = True

	def Disable(self):
		self.enable = False
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event, *args):
		self.event = ui.__mem_func__(event)
		self.args = args

	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):
		self.CloseListBox()
		if self.event:
			self.event(* (index, self.args))

	def CloseListBox(self):
		self.isListOpened = False
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.enable:
			return

		self.isSelected = True

	def OnMouseLeftButtonUp(self):
		if not self.enable:
			return

		self.isSelected = False

		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = True
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):
		if not self.enable:
			return

		if self.IsIn():
			self.isOver = True
		else:
			self.isOver = False

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		grp.SetColor(self.BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		grp.SetColor(self.LINE_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.SetColor(self.LINE_COLOR)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		if self.isOver:
			grp.SetColor(self.IS_IN_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)
			if self.isSelected:
				grp.SetColor(self.SELECTED_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)
				self.background.LoadImage("interface/controls/common/dropdown/btn_03_active.tga")
			else:
				self.background.LoadImage("interface/controls/common/dropdown/btn_02_hover.tga")
		else:
			self.background.LoadImage("interface/controls/common/dropdown/btn_01_normal.tga")

class GuildWindow(ui.ScriptWindow):

	JOB_NAME = {
			0 : localeinfo.JOB_WARRIOR,
			1 : localeinfo.JOB_ASSASSIN,
			2 : localeinfo.JOB_SURA,
			3 : localeinfo.JOB_SHAMAN, }

	FACE_IMAGE_DICT = {
		playersettingmodule.RACE_WARRIOR_M		:"interface/controls/common/faces/small/icon_mwarrior.tga",
		playersettingmodule.RACE_WARRIOR_W		:"interface/controls/common/faces/small/icon_wwarrior.tga",
		playersettingmodule.RACE_ASSASSIN_M		:"interface/controls/common/faces/small/icon_mninja.tga",
		playersettingmodule.RACE_ASSASSIN_W		:"interface/controls/common/faces/small/icon_wninja.tga",
		playersettingmodule.RACE_SURA_M			:"interface/controls/common/faces/small/icon_msura.tga",
		playersettingmodule.RACE_SURA_W			:"interface/controls/common/faces/small/icon_wsura.tga",
		playersettingmodule.RACE_SHAMAN_M		:"interface/controls/common/faces/small/icon_mshaman.tga",
		playersettingmodule.RACE_SHAMAN_W		:"interface/controls/common/faces/small/icon_wshaman.tga",
	}

	GUILD_SKILL_PASSIVE_SLOT = 0
	GUILD_SKILL_ACTIVE_SLOT = 1
	GUILD_SKILL_AFFECT_SLOT = 2

	GRADE_SLOT_NAME = 0
	GRADE_ADD_MEMBER_AUTHORITY = 1
	GRADE_REMOVE_MEMBER_AUTHORITY = 2
	GRADE_NOTICE_AUTHORITY = 3
	GRADE_SKILL_AUTHORITY = 4
	GRADE_WAR = 5
	GRADE_SAFEBOX = 6

	MEMBER_LINE_COUNT = 8

	msgLeader = False

	class PageWindow(ui.ScriptWindow):
		def __init__(self, parent, filename):
			ui.ScriptWindow.__init__(self)
			self.SetParent(parent)
			self.filename = filename

		def GetScriptFileName(self):
			return self.filename

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0

		self.__Initialize()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.board = None
		self.pageName = None
		self.tabButtonDict = None
		self.pickDialog = None
		self.questionDialog = None
		self.offerDialog = None
		self.popupDialog = None
		self.popupBoard = None
		self.moneyDialog = None
		self.changeGradeNameDialog = None
		self.popup = None
		self.popupMessage = None
		self.commentSlot = None
		self.pageWindow = None
		self.tooltipSkill = None

		self.memberLinePos = 0

		self.enemyGuildNameList = []
		self.msgLeader = False

		if app.ENABLE_GUILD_SAFEBOX:
			self.wndSafebox = GuildSafeboxWindow()

	def Open(self):
		self.Show()
		self.SetTop()

		guildID = net.GetGuildID()
		self.largeMarkBox.SetIndex(guildID)
		self.largeMarkBox.SetScale(3)

	def Close(self):
		self.__CloseAllGuildMemberPageGradeComboBox()
		self.offerDialog.Close()
		self.popupDialog.Hide()
		self.changeGradeNameDialog.Hide()
		self.tooltipSkill.Hide()
		self.Hide()

		self.pickDialog = None
		self.questionDialog = None
		self.popup = None

		if app.ENABLE_GUILD_SAFEBOX:
			net.SendChatPacket("/guild_safebox_close")

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

		if app.ENABLE_GUILD_SAFEBOX:
			if self.wndSafebox:
				self.wndSafebox.Destroy()

		if self.offerDialog:
			self.offerDialog.Destroy()

		if self.popupDialog:
			self.popupDialog.ClearDictionary()

		if self.changeGradeNameDialog:
			self.changeGradeNameDialog.ClearDictionary()

		if self.pageWindow:
			for window in self.pageWindow.values():
				window.ClearDictionary()

		self.__Initialize()

	def Show(self):
		if self.isLoaded == 0:
			self.isLoaded = 1
			self.__LoadWindow()

		self.RefreshGuildInfoPage()
		self.RefreshGuildBoardPage()
		self.RefreshGuildMemberPage()
		self.RefreshGuildSkillPage()
		self.RefreshGuildGradePage()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/guildwindow.py")

			self.popupDialog = ui.ScriptWindow()
			pyScrLoader.LoadScriptFile(self.popupDialog, "uiscript/popupdialog.py")

			self.changeGradeNameDialog = ChangeGradeNameDialog()
			pyScrLoader.LoadScriptFile(self.changeGradeNameDialog, "uiscript/changegradenamedialog.py")

			self.pageWindow = {
				"GUILD_INFO"	: self.PageWindow(self, "uiscript/guildwindow_guildinfopage.py"),
				"BOARD"			: self.PageWindow(self, "uiscript/guildwindow_boardpage.py"),
				"MEMBER"		: self.PageWindow(self, "uiscript/guildwindow_memberpage.py"),
				"SKILL"			: self.PageWindow(self, "uiscript/guildwindow_guildskillpage.py"),
				"GRADE"			: self.PageWindow(self, "uiscript/guildwindow_gradepage.py"),
				"RANKING"		: self.PageWindow(self, "uiscript/guildwindow_rankingpage.py"),
				"WAR_LIST"			: self.PageWindow(self, "uiscript/guildwindow_war_list.py"),
				"WAR_INFO"			: self.PageWindow(self, "uiscript/guildwindow_war_info.py"),
				"WAR_LOG"			: self.PageWindow(self, "uiscript/guildwindow_war_log.py"),
			}
			if app.ENABLE_GUILD_SAFEBOX:
				self.pageWindow.update({"SAFEBOX" : self.PageWindow(self, "uiscript/guildwindow_safebox.py")})

			for window in self.pageWindow.values():
				pyScrLoader.LoadScriptFile(window, window.GetScriptFileName())

		except BaseException:
			exception.Abort("GuildWindow.__LoadWindow.LoadScript")

		try:
			getObject = self.GetChild

			self.board = getObject("Board")
			self.pageName = {
				"GUILD_INFO"	: localeinfo.GUILD_TILE_INFO,
				"BOARD"			: localeinfo.GUILD_TILE_BOARD,
				"MEMBER"		: localeinfo.GUILD_TILE_MEMBER,
				"SKILL"			: localeinfo.GUILD_TILE_SKILL,
				"GRADE"			: localeinfo.GUILD_TILE_GRADE,
				"RANKING"		: "Classificaзгo de Guilds",
				"WAR_LIST"			: "Histуrico de Guerras",
			}
			if app.ENABLE_GUILD_SAFEBOX:
				self.pageName.update({ "SAFEBOX" : localeinfo.GUILD_TILE_SAFEBOX})

			self.tabButtonDict = {
				"GUILD_INFO"	: getObject("Tab_Button_01"),
				"BOARD"			: getObject("Tab_Button_02"),
				"MEMBER"		: getObject("Tab_Button_03"),
				"SKILL"			: getObject("Tab_Button_04"),
				"GRADE"			: getObject("Tab_Button_05"),
				"RANKING"		: getObject("Tab_Button_07"),
				"WAR_LIST"			: getObject("Tab_Button_08"),
			}
			if app.ENABLE_GUILD_SAFEBOX:
				self.tabButtonDict.update({"SAFEBOX" : getObject("Tab_Button_06")})
			else:
				getObject("Tab_Button_06").Hide()

			self.popupMessage = self.popupDialog.GetChild("message")
			self.popupBoard = self.popupDialog.GetChild("board")
			self.popupDialog.GetChild("accept").SetEvent(self.popupDialog.Hide)

			self.changeGradeNameDialog.GetChild("AcceptButton").SetEvent(self.OnChangeGradeName)
			self.changeGradeNameDialog.GetChild("CancelButton").SetEvent(self.changeGradeNameDialog.Hide)
			self.changeGradeNameDialog.GetChild("Board").SetCloseEvent(self.changeGradeNameDialog.Hide)
			self.changeGradeNameDialog.gradeNameSlot = self.changeGradeNameDialog.GetChild("GradeNameValue")
			self.changeGradeNameDialog.gradeNameSlot.SetReturnEvent(self.OnChangeGradeName)
			self.changeGradeNameDialog.gradeNameSlot.SetEscapeEvent(self.changeGradeNameDialog.Close)

			self.commentSlot = self.pageWindow["BOARD"].GetChild("CommentValue")
			self.commentSlot.SetIMEUpdateEvent(self.OnPostComment)

			self.pageWindow["BOARD"].GetChild("RefreshButton").SetEvent(self.OnRefreshComments)
			scrollBar = self.pageWindow["MEMBER"].GetChild("ScrollBar")
			scrollBar.SetScrollEvent(self.OnScrollMemberLine)
			self.pageWindow["MEMBER"].scrollBar = scrollBar

		except BaseException:
			exception.Abort("GuildWindow.__LoadWindow.BindObject")

		self.__MakeInfoPage()
		self.__MakeBoardPage()
		self.__MakeMemberPage()
		self.__MakeSkillPage()
		self.__MakeGradePage()
		self.Make_Ranking_Page()
		self.Make_WarLog_Page()

		if app.ENABLE_GUILD_SAFEBOX:
			self.__MakeSafeBox()

		for page in self.pageWindow.values():
			page.UpdateRect()

		for key, btn in self.tabButtonDict.items():
			btn.SetEvent(self.SelectPage, key)

		self.board.SetCloseEvent(self.Close)
		self.GetChild("Button_Return").SetEvent(self.SelectPage, "GUILD_INFO")
		self.SelectPage("GUILD_INFO")

		self.offerDialog = uipickmoney.PickMoneyDialog()
		self.offerDialog.LoadDialog()
		self.offerDialog.SetMax(9)
		self.offerDialog.SetTitleName(localeinfo.GUILD_OFFER_EXP)
		self.offerDialog.SetAcceptEvent(self.OnOffer)

### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ### SAFEBOX ###
	if app.ENABLE_GUILD_SAFEBOX:
		def __MakeSafeBox(self):
			page = self.pageWindow["SAFEBOX"]
			self.wndSafebox.SetParent(page)
			self.wndSafebox.Show()

### INFORMACOES DA GUILD ###### INFORMACOES DA GUILD ###### INFORMACOES DA GUILD ###### INFORMACOES DA GUILD ###### INFORMACOES DA GUILD ###
	def __MakeInfoPage(self):
		page = self.pageWindow["GUILD_INFO"]

		try:
			page.nameSlot = page.GetChild("GuildNameValue")
			page.masterNameSlot = page.GetChild("GuildMasterNameValue")
			page.guildLevelSlot = page.GetChild("GuildLevelValue")
			page.Exp = page.GetChild("Exp_Value")
			page.PercentExp = page.GetChild("PercentExp")
			page.gaugeExp = page.GetChild("ExpImgFull")
			page.memberCountSlot = page.GetChild("GuildMemberCountValue")
			page.levelAverageSlot = page.GetChild("GuildMemberLevelAverageValue")
			page.uploadMarkButton = page.GetChild("UploadGuildMarkButton")
			page.declareWarButton = page.GetChild("DeclareWarButton")
			page.MeetingButton = page.GetChild("MeetingButton")

			page.uploadMarkButton.SetEvent(self.__OnClickSelectGuildMarkButton)
			page.declareWarButton.SetEvent(self.__OnClickDeclareWarButton)
			page.GetChild("OfferButton").SetEvent(self.__OnClickOfferButton)
			page.GetChild("MessageLeaderButton").SetEvent(self.__OnClickMessageLeaderButton)
			page.GetChild("MessageLeaderSlot").SetMouseLeftButtonDownEvent(page.GetChild("smsg1").SetFocus)

			self.largeMarkBox = page.GetChild("LargeGuildMark")
		except BaseException:
			exception.Abort("GuildWindow.__MakeInfoPage")

		self.largeMarkBox.AddFlag("not_pick")

		self.markSelectDialog = uiuploadmark.MarkSelectDialog()
		self.markSelectDialog.SetSelectEvent(self.__OnSelectMark)

### MENSAGEM DOS MEMBROS ###### MENSAGEM DOS MEMBROS ###### MENSAGEM DOS MEMBROS ###### MENSAGEM DOS MEMBROS ###### MENSAGEM DOS MEMBROS ###
	def __MakeBoardPage(self):
		i = 0
		lineStep = 30
		page = self.pageWindow["BOARD"]

		page.boardDict = {}

		for i in range(7):

			yPos = 10 + i * lineStep
			nameSlotImage = ui.MakeImageBox(page, "interface/controls/special/guild/name_msg_slot.tga", 10, yPos-1)
			nameSlot = ui.MakeTextLine(nameSlotImage)
			nameSlot.SetPackedFontColor(0xfff8d090)
			page.Children.append(nameSlotImage)
			page.Children.append(nameSlot)

			commentSlot = CommentSlot()
			commentSlot.SetParent(page)
			commentSlot.SetPosition(14, yPos)
			commentSlot.Show()
			page.Children.append(commentSlot)
			commentSlot.deleteButton.SetEvent(self.OnDeleteComment, i)

			boardSlotList = []
			boardSlotList.append(commentSlot.noticeMarkImage)
			boardSlotList.append(nameSlot)
			boardSlotList.append(commentSlot)
			page.boardDict[i] = boardSlotList

		page.GetChild("CommentValue").SetFocusEvent(self.CommentValueOnFocus)
		page.GetChild("CommentValue").SetKillFocusEvent(self.CommentValueOnKillFocus)
		page.GetChild("CommentValue").SetReturnEvent(self.OnPostComment)

		page.scroll = page.GetChild("CommentScrollBar")
		page.scroll.SetMiddleBarSize(1)
		page.scroll.SetScrollEvent(self.RefreshGuildBoardPage)

	def CommentValueOnFocus(self):
		page = self.pageWindow["BOARD"]
		page.GetChild("Digite").Hide()

	def CommentValueOnKillFocus(self):
		page = self.pageWindow["BOARD"]
		page.GetChild("CommentValue").SetText("")
		page.GetChild("Digite").Show()

	def __MakeMemberPage(self):
		page = self.pageWindow["MEMBER"]

		lineStep = 30
		page.memberDict = {}

		for i in range(self.MEMBER_LINE_COUNT):
			inverseLineIndex = self.MEMBER_LINE_COUNT - i - 1
			yPos = 50 + inverseLineIndex*lineStep
			nameSlotImage = ui.MakeImageBox(page, "interface/controls/special/guild/member/member_slot.tga", 14, yPos)
			nameSlot = ui.TextLine()
			nameSlot.SetParent(nameSlotImage)
			nameSlot.SetPosition(0, 0)
			nameSlot.SetWindowHorizontalAlignCenter()
			nameSlot.SetHorizontalAlignCenter()
			nameSlot.SetWindowVerticalAlignCenter()
			nameSlot.SetVerticalAlignCenter()
			nameSlot.SetPackedFontColor(0xfff8d090)
			nameSlot.Show()
			page.Children.append(nameSlotImage)
			page.Children.append(nameSlot)

			jobSlotImage = ui.MakeImageBox(page, "interface/controls/special/guild/member/slot_small.tga", 14 + 85, yPos)
			jobSlot = ui.MakeImageBox(jobSlotImage, self.FACE_IMAGE_DICT[0], 0 , 0)
			jobSlot.SetWindowVerticalAlignCenter()
			jobSlot.SetWindowHorizontalAlignCenter()
			page.Children.append(jobSlotImage)
			page.Children.append(jobSlot)

			levelSlotImage = ui.MakeImageBox(page, "interface/controls/special/guild/member/slot_small.tga", 14 + 85 + 43, yPos)
			levelSlot = ui.MakeTextLine(levelSlotImage)
			levelSlot.SetPackedFontColor(0xffffffff)
			page.Children.append(levelSlotImage)
			page.Children.append(levelSlot)

			offerSlotImage = ui.MakeImageBox(page, "interface/controls/special/guild/member/slot_small.tga", 14 + 85 + 43*2, yPos)
			offerSlot = ui.MakeTextLine(offerSlotImage)
			offerSlot.SetPackedFontColor(0xffffffff)
			page.Children.append(offerSlotImage)
			page.Children.append(offerSlot)

			gradeSlotImage = ui.MakeImageBox(page, "interface/controls/special/guild/member/positon_slot.tga", 14 + 85 + 43*3, yPos)
			gradeSlot = ComboBox()
			gradeSlot.SetParent(gradeSlotImage)
			gradeSlot.SetPosition(2, 2)
			gradeSlot.SetSize(97, 27)
			gradeSlot.SetEvent(self.OnChangeMemberGrade, inverseLineIndex)
			gradeSlot.Show()
			page.Children.append(gradeSlotImage)
			page.Children.append(gradeSlot)

			memberSlotList = []
			memberSlotList.append(nameSlot)#0
			memberSlotList.append(gradeSlot)#1
			memberSlotList.append(jobSlot)#2
			memberSlotList.append(levelSlot)#3
			memberSlotList.append(offerSlot)#4
			memberSlotList.append(nameSlotImage)#5
			memberSlotList.append(jobSlotImage)#6
			memberSlotList.append(levelSlotImage)#7
			memberSlotList.append(offerSlotImage)#8
			memberSlotList.append(gradeSlotImage)#9
			page.memberDict[inverseLineIndex] = memberSlotList

	def __MakeSkillPage(self):
		page = self.pageWindow["SKILL"]

		page.skillPoint = page.GetChild("Skill_Plus_Value")
		page.activeSlot = page.GetChild("Active_Skill_Slot_Table")
		page.gpGauge = page.GetChild("Dragon_God_Power_Gauge")
		page.gpValue = page.GetChild("Dragon_God_Power_Value")
		page.btnHealGSP = page.GetChild("Heal_GSP_Button")

		place = "interface/controls/common/button_status/"
		page.activeSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		page.activeSlot.SetOverInItemEvent(self.OverInItem)
		page.activeSlot.SetOverOutItemEvent(self.OverOutItem)
		page.activeSlot.SetSelectItemSlotEvent(self.OnPickUpGuildSkill)
		page.activeSlot.SetUnselectItemSlotEvent(self.OnUseGuildSkill)
		page.activeSlot.SetPressedSlotButtonEvent(self.OnUpGuildSkill)
		page.activeSlot.AppendSlotButton(place + "plus_n.tga", place + "plus_h.tga", place + "plus_a.tga")

		page.btnHealGSP.SetEvent(self.__OnOpenHealGSPBoard)

		for i in range(len(playersettingmodule.ACTIVE_GUILD_SKILL_INDEX_LIST)):
			slotIndex = page.activeSlot.GetStartIndex() + i
			skillIndex = playersettingmodule.ACTIVE_GUILD_SKILL_INDEX_LIST[i]

			page.activeSlot.SetSkillSlot(slotIndex, skillIndex, 0)
			page.activeSlot.SetCoverButton(slotIndex)
			page.activeSlot.RefreshSlot()
			guild.SetSkillIndex(slotIndex, len(playersettingmodule.PASSIVE_GUILD_SKILL_INDEX_LIST)+i)

	def __MakeGradePage(self):
		lineStep = 30
		size = 36
		page = self.pageWindow["GRADE"]
		page.gradeDict = {}
		page.GetChild("BoardScrollBar").SetScrollEvent(self.RefreshGuildGradePage)
		for i in range(8):
			yPos = 50 + i * lineStep
			index = i + 1

			gradeNumberSlotImage = ui.MakeImageBox(page, "interface/controls/special/guild/dialog_rank_slot.tga", 1, yPos)
			gradeNumberSlot = ui.TextLine()
			gradeNumberSlot.SetPosition(14, 9)
			gradeNumberSlot.SetHorizontalAlignCenter()
			gradeNumberSlot.SetParent(gradeNumberSlotImage)
			gradeNumberSlot.SetPackedFontColor(0xffffffff)
			gradeNumberSlot.SetText(str(i+1))
			gradeNumberSlot.Show()
			page.Children.append(gradeNumberSlotImage)
			page.Children.append(gradeNumberSlot)

			gradeNameSlot = EditableTextSlot(page, 31, yPos + 2)
			gradeNameSlot.SetEvent(self.OnOpenChangeGradeName, index)
			page.Children.append(gradeNameSlot)

			inviteAuthorityCheckBox = CheckBox(page, 113, yPos, self.OnCheckAuthority, (index, 1<<0))
			page.Children.append(inviteAuthorityCheckBox)

			driveoutAuthorityCheckBox = CheckBox(page, 113 + size*1, yPos, self.OnCheckAuthority, (index, 1<<1))
			page.Children.append(driveoutAuthorityCheckBox)

			noticeAuthorityCheckBox = CheckBox(page, 113 + size*2, yPos, self.OnCheckAuthority, (index, 1<<2))
			page.Children.append(noticeAuthorityCheckBox)

			skillAuthorityCheckBox = CheckBox(page, 113 + size*3, yPos, self.OnCheckAuthority, (index, 1<<3))
			page.Children.append(skillAuthorityCheckBox)

			WarAuthorityCheckBox = CheckBox(page, 113 + size*4, yPos, self.OnCheckAuthority, (index, 1<<4))
			page.Children.append(WarAuthorityCheckBox)

			SafeboxAuthorityCheckBox = CheckBox(page, 113 + size*5, yPos, self.OnCheckAuthority, (index, 1<<5))
			page.Children.append(SafeboxAuthorityCheckBox)

			deleteGradeButton = ui.MakeButton(page, 105, yPos + 9, "", "interface/controls/special/guild/", "del_grade.tga", "del_grade_hover.tga", "del_grade.tga")
			deleteGradeButton.Hide()
			page.Children.append(deleteGradeButton)

			gradeSlotList = []
			gradeSlotList.append(gradeNameSlot)
			gradeSlotList.append(inviteAuthorityCheckBox)
			gradeSlotList.append(driveoutAuthorityCheckBox)
			gradeSlotList.append(noticeAuthorityCheckBox)
			gradeSlotList.append(skillAuthorityCheckBox)
			gradeSlotList.append(WarAuthorityCheckBox)
			gradeSlotList.append(SafeboxAuthorityCheckBox)
			gradeSlotList.append(gradeNumberSlotImage)
			gradeSlotList.append(gradeNumberSlot)
			gradeSlotList.append(deleteGradeButton)
			page.gradeDict[index] = gradeSlotList

		masterSlotList = page.gradeDict[1]
		for x in range(len(masterSlotList)-4):
			masterSlotList[x].Disable()

	def CanOpen(self):
		return guild.IsGuildEnable()

	def Open(self):
		self.Show()
		self.SetTop()

		guildID = net.GetGuildID()
		self.largeMarkBox.SetIndex(guildID)
		self.largeMarkBox.SetScale(3)

		if app.ENABLE_GUILD_SAFEBOX:
			net.SendChatPacket("/guild_safebox_open")

	def Close(self):
		self.__CloseAllGuildMemberPageGradeComboBox()
		self.offerDialog.Close()
		self.popupDialog.Hide()
		self.changeGradeNameDialog.Hide()
		self.Hide()

		if self.tooltipSkill:
			self.tooltipSkill.Hide()

		self.pickDialog = None
		self.questionDialog = None
		self.moneyDialog = None

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.board = None
		self.pageName = None
		self.tabButtonDict = None
		self.pickDialog = None
		self.questionDialog = None
		self.markSelectDialog = None

		if self.offerDialog:
			self.offerDialog.Destroy()
			self.offerDialog = None

		if self.popupDialog:
			self.popupDialog.ClearDictionary()
			self.popupDialog = None

		if self.changeGradeNameDialog:
			self.changeGradeNameDialog.ClearDictionary()
			self.changeGradeNameDialog = None

		self.popupMessage = None
		self.commentSlot = None

		if self.pageWindow:
			for window in self.pageWindow.values():
				window.ClearDictionary()

		self.pageWindow = None
		self.tooltipSkill = None
		self.moneyDialog = None

		self.enemyGuildNameList = []

	def DeleteGuild(self):
		self.RefreshGuildInfoPage()
		self.RefreshGuildBoardPage()
		self.RefreshGuildMemberPage()
		self.RefreshGuildSkillPage()
		self.RefreshGuildGradePage()
		self.Hide()

	def SetSkillToolTip(self, tooltipSkill):
		self.tooltipSkill = proxy(tooltipSkill)

	def HideTabControl(self):
		self.GetChild("TabControl").Hide()
		self.GetChild("Button_Return").Show()

	def ShowTabControl(self):
		self.GetChild("TabControl").Show()
		self.GetChild("Button_Return").Hide()

	def SelectPage(self, arg):
		if "BOARD" == arg:
			self.OnRefreshComments()
			self.RefreshGuildBoardPage()

		if "RANKING" == arg:
			if not len(constinfo.RANKING_LIST):
				net.SendChatPacket("/guild_ranking")
		if "WAR_LIST" == arg:
			self.HideTabControl()
			if not len(constinfo.WAR_LIST):
				net.SendChatPacket("/war_history")
		else:
			self.ShowTabControl()

		for key, page in self.pageWindow.items():
			if arg == key:
				page.Show()
			else:
				page.Hide()

		self.board.SetTitleName(self.pageName[arg])
		self.__CloseAllGuildMemberPageGradeComboBox()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.Enable()
		self.tabButtonDict[arg].Disable()

		self.__RefreshLeaderComment()

	def __CloseAllGuildMemberPageGradeComboBox(self):
		page = self.pageWindow["MEMBER"]
		for key, slotList in page.memberDict.items():
			slotList[1].CloseListBox()

	def RefreshGuildInfoPage(self):
		if self.isLoaded == 0:
			return

		page = self.pageWindow["GUILD_INFO"]
		page.nameSlot.SetText(guild.GetGuildName())
		page.masterNameSlot.SetText(guild.GetGuildMasterName())
		page.guildLevelSlot.SetText("Level " + str(guild.GetGuildLevel()))
## GUILD EXP #### GUILD EXP #### GUILD EXP #### GUILD EXP #### GUILD EXP ##
		curExp, lastExp = guild.GetGuildExperience()
		fpercent = float(curExp)/float(max(1, lastExp))*100
		percent = str(fpercent)
		if len(percent) > 4:
			percent_limited = percent[:4]
		else:
			percent_limited = percent
		page.gaugeExp.SetPercentageNew(min(int(fpercent), 100))
		page.Exp.SetText("Experiкncia: " + str(curExp) + " de " + str(lastExp))
		page.PercentExp.SetText(percent_limited + "%")

		curMemberCount, maxMemberCount = guild.GetGuildMemberCount()
		if maxMemberCount== 0xffff:
			page.memberCountSlot.SetText("%d / %s " % (curMemberCount, localeinfo.GUILD_MEMBER_COUNT_INFINITY))
		else:
			page.memberCountSlot.SetText("%d / %d" % (curMemberCount, maxMemberCount))

		page.levelAverageSlot.SetText(str(guild.GetGuildMemberLevelAverage()))

		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		page.MeetingButton.SetEvent(self.RequestMeeting)

		if mainCharacterName == masterName:
			page.MeetingButton.Show()
			page.uploadMarkButton.Show()
			page.GetChild("MessageLeaderButton").Show()
			page.declareWarButton.Show()
		else:
			page.MeetingButton.Hide()
			page.uploadMarkButton.Hide()
			page.GetChild("MessageLeaderButton").Hide()
			page.declareWarButton.Hide()

		gt = page.GetChild
		for i in range(1, 5):
			gt("msg"+str(i)).SetText("")
		for i in range(0, 4):
			message = self.__GetGuildLeaderCommentData(i)
			if not message or message == "Noname":
				continue
			gt("msg"+str(i+1)).SetText(message)

	def __GetGuildBoardCommentData(self, index):
		commentID, chrName, comment = guild.GetGuildBoardCommentData(index)
		if 0 == commentID:
			if "" == chrName:
				chrName = localeinfo.UI_NONAME
			if "" == comment:
				comment = localeinfo.UI_NOCONTENTS
		return commentID, chrName, comment

#ENABLE_MSG_LEADER
	def __GetGuildLeaderCommentData(self, index):
		commentID, chrName, comment = guild.GetGuildLeaderCommentData(index)
		return comment

	def __RefreshLeaderComment(self):
		net.SendGuildRefreshLeaderPacket(0)

	def RequestMeeting(self):
		question = uicommon.QuestionDialog()
		question.SetText("Deseja solicitar Reuniгo da Guild?")
		question.SetAcceptEvent(self.RequestMeetingYes)
		question.SetCancelEvent(self.RequestMeetingNo)
		question.Open()
		self.RequestMeetingQuestion = question

	def RequestMeetingYes(self):
		net.SendChatPacket("/guild_meeting")
		self.RequestMeetingQuestion.Close()

	def RequestMeetingNo(self):
		self.RequestMeetingQuestion.Close()

	def RefreshGuildBoardPage(self):
		if self.isLoaded == 0:
			return

		page = self.pageWindow["BOARD"]

		lineIndex = 0

		l = guild.GetGuildBoardCommentCount()
		if l > 7:
			page.scroll.SetMiddleBarSize(7.0/float(l))
			page.scroll.Show()
			x = page.scroll.GetPos()
		else:
			page.scroll.SetMiddleBarSize(1.0)
			x = 0
			page.scroll.Hide()

		for i in range(min(int(float(l)*x), l-1), min(7 + int(float(l)*x), l)):
			if lineIndex == 7:
				break

			commentID, chrName, comment = self.__GetGuildBoardCommentData(i)

			if not comment or (chrName == "Noname" and comment == "Noname"):
				continue

			slotList = page.boardDict[lineIndex]
			if "!" == comment[0]:
				slotList[0].Show()
				slotList[1].SetText(chrName)
				slotList[2].SetText(comment[1:])
				slotList[2].Show()
			else:
				slotList[0].Hide()
				slotList[1].SetText(chrName)
				slotList[2].SetText(comment)
				slotList[2].Show()

			lineIndex += 1

		if lineIndex < 7:
			for i in range(7 - lineIndex):
				slotList = page.boardDict[lineIndex+i]
				slotList[0].Hide()
				slotList[1].SetText("")
				slotList[2].SetText("")
				slotList[2].Hide()

	def RefreshGuildMemberPage(self):
		if self.isLoaded == 0:
			return

		page = self.pageWindow["MEMBER"]

		count = guild.GetMemberCount()
		if count > self.MEMBER_LINE_COUNT:
			page.scrollBar.SetMiddleBarSize(float(self.MEMBER_LINE_COUNT) / float(count))
			page.scrollBar.Show()
		else:
			page.scrollBar.Hide()
		self.RefreshGuildMemberPageGradeComboBox()
		self.RefreshGuildMemberPageMemberList()

	def RefreshGuildMemberPageMemberList(self):
		if self.isLoaded == 0:
			return

		page = self.pageWindow["MEMBER"]

		for line, slotList in page.memberDict.items():

			gradeComboBox = slotList[1]
			gradeComboBox.Disable()

			if not guild.IsMember(line):
				slotList[0].SetText("")
				gradeComboBox.Hide()
				slotList[2].Hide()
				slotList[3].SetText("")
				slotList[4].SetText("")
				slotList[5].Hide()
				slotList[6].Hide()
				slotList[7].Hide()
				slotList[8].Hide()
				slotList[9].Hide()
				continue

			pid, name, grade, race, level, offer, general = self.GetMemberData(line)
			if pid < 0:
				continue

			guildExperienceSummary = guild.GetGuildExperienceSummary()

			offerPercentage = 0
			if guildExperienceSummary > 0:
				offerPercentage = int(float(offer) / float(guildExperienceSummary) * 100.0)

			slotList[0].SetText(name)
			slotList[2].LoadImage(self.FACE_IMAGE_DICT[race])
			slotList[2].Show()
			slotList[3].SetText(str(level))
			slotList[4].SetText(str(offerPercentage) + "%")
			slotList[5].Show()
			slotList[6].Show()
			slotList[7].Show()
			slotList[8].Show()
			slotList[9].Show()
			gradeComboBox.SetCurrentItem(guild.GetGradeName(grade))
			gradeComboBox.Show()
			if 1 != grade:
				gradeComboBox.Enable()

	def RefreshGuildMemberPageGradeComboBox(self):
		if self.isLoaded == 0:
			return

		page = self.pageWindow["MEMBER"]

		self.CAN_CHANGE_GRADE_COUNT = 15 - 1
		for key, slotList in page.memberDict.items():
			gradeComboBox = slotList[1]
			gradeComboBox.Disable()

			if not guild.IsMember(key):
				continue

			pid, name, grade, job, level, offer, general = self.GetMemberData(key)
			if pid < 0:
				continue

			gradeComboBox.ClearItem()
			temp = False
			for i in range(self.CAN_CHANGE_GRADE_COUNT):
				if (guild.GetGradeName(i+2) != "Recruta" and guild.GetGradeName(i+2) != "") and temp == False:
					gradeComboBox.InsertItem(i+2, guild.GetGradeName(i+2))
				elif guild.GetGradeName(i+2) in ["Recruta", ""] and temp == False:
					gradeComboBox.InsertItem(i+2, "Recruta")
					temp = True
				else:
					break
			gradeComboBox.SetCurrentItem(guild.GetGradeName(grade))
			if 1 != grade:
				gradeComboBox.Enable()

	def RefreshGuildSkillPage(self):
		if self.isLoaded == 0:
			return

		page = self.pageWindow["SKILL"]

		curPoint, maxPoint = guild.GetDragonPowerPoint()
		maxPoint = max(maxPoint, 1)
		page.gpValue.SetText("Pontos de Enegia:  |cfff8d090" + str(curPoint) + " / " + str(maxPoint))

		percentage = (float(curPoint) / float(maxPoint) * 100)
		page.gpGauge.SetPercentage(int(percentage), 100)

		skillPoint = guild.GetGuildSkillPoint()
		page.skillPoint.SetText("Pontos disponнveis:  |cfff8d090" + str(skillPoint))
		page.activeSlot.HideAllSlotButton()
		try:
			for i in range(len(playersettingmodule.ACTIVE_GUILD_SKILL_INDEX_LIST)):

				slotIndex = page.activeSlot.GetStartIndex()+i
				skillIndex = playersettingmodule.ACTIVE_GUILD_SKILL_INDEX_LIST[i]
				skillLevel = guild.GetSkillLevel(slotIndex)
				skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

				page.activeSlot.SetSlotCount(slotIndex, skillLevel)

				if skillLevel <= 0:
					page.activeSlot.DisableCoverButton(slotIndex)
				else:
					page.activeSlot.EnableCoverButton(slotIndex)

				if skillPoint > 0:
					if skillLevel < skillMaxLevel:
						page.activeSlot.ShowSlotButton(slotIndex)
		except BaseException:
			pass

	def RefreshGuildGradePage(self):
		if self.isLoaded == 0:
			return
		leader = False

		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			leader = True

		exibidos = 0
		page = self.pageWindow["GRADE"]
		scroll = page.GetChild("BoardScrollBar")
		for x in range(16):
			name, authority = guild.GetGradeData(int(x))
			exibidos = x
			if (name == "Recruta") or (name == ""):
				break

		pos = 0
		scroll.Hide()

		if int(exibidos) >= int(8):
			scroll.SetMiddleBarSize(min(8.0/float(15), 1.0))
			pos = int(scroll.GetPos()/2.0 * float(exibidos))
			scroll.Show()

		empty = 0
		buttonMinus = 0
		nameMinus = 0

		for key, slotList in page.gradeDict.items():
			name, authority = guild.GetGradeData(int(key)+pos)
			slotList[7+1].SetText(str(int(key)+pos))
			slotList[0].SetEvent(self.OnOpenChangeGradeName, (int(key)+pos))
			slotList[1].SetEvent(self.OnCheckAuthority, (int(key)+pos), 1<<0)
			slotList[2].SetEvent(self.OnCheckAuthority, (int(key)+pos), 1<<1)
			slotList[3].SetEvent(self.OnCheckAuthority, (int(key)+pos), 1<<2)
			slotList[4].SetEvent(self.OnCheckAuthority, (int(key)+pos), 1<<3)
			slotList[5].SetEvent(self.OnCheckAuthority, (int(key)+pos), 1<<4)
			slotList[6].SetEvent(self.OnCheckAuthority, (int(key)+pos), 1<<5)
			slotList[8+1].SetEvent(self.DelGradeName, (int(key)+pos), authority)
			slotList[8+1].Hide()
			if name == "Lider" or leader == False:
				slotList[0].Disable()
				slotList[1].Disable()
				slotList[2].Disable()
				slotList[3].Disable()
				slotList[4].Disable()
				slotList[5].Disable()
				slotList[6].Disable()
			else:
				slotList[0].EnableW()
				slotList[1].EnableW()
				slotList[2].EnableW()
				slotList[3].EnableW()
				slotList[4].EnableW()
				slotList[5].EnableW()
				slotList[6].EnableW()
			if empty == 1:
				slotList[0].Hide()
				slotList[1].Hide()
				slotList[2].Hide()
				slotList[3].Hide()
				slotList[4].Hide()
				slotList[5].Hide()
				slotList[6].Hide()
				slotList[7].Hide()
			else:
				slotList[0].Show()
				slotList[1].Show()
				slotList[2].Show()
				slotList[3].Show()
				slotList[4].Show()
				slotList[5].Show()
				slotList[6].Show()
				slotList[7].Show()
			if name != "Recruta" and name != "" and empty == 0:
				buttonMinus = slotList[8+1]
				nameMinus = name
			if name in ["", "Recruta",] and empty == 0:
				empty = 1
				slotList[1].Disable()
				slotList[2].Disable()
				slotList[3].Disable()
				slotList[4].Disable()
				slotList[5].Disable()
				slotList[6].Disable()
				slotList[1].SetCheck(0)
				slotList[2].SetCheck(0)
				slotList[3].SetCheck(0)
				slotList[4].SetCheck(0)
				slotList[5].SetCheck(0)
				slotList[6].SetCheck(0)
				slotList[self.GRADE_SLOT_NAME].SetText("Adicionar +")
			else:
				slotList[self.GRADE_SLOT_NAME].SetText(name)
				slotList[self.GRADE_ADD_MEMBER_AUTHORITY].SetCheck(authority & guild.AUTH_ADD_MEMBER)
				slotList[self.GRADE_REMOVE_MEMBER_AUTHORITY].SetCheck(authority & guild.AUTH_REMOVE_MEMBER)
				slotList[self.GRADE_NOTICE_AUTHORITY].SetCheck(authority & guild.AUTH_NOTICE)
				slotList[self.GRADE_SKILL_AUTHORITY].SetCheck(authority & guild.AUTH_SKILL)
				slotList[self.GRADE_WAR].SetCheck(authority & guild.AUTH_WAR)
				slotList[self.GRADE_SAFEBOX].SetCheck(authority & guild.AUTH_GUILD_SAFEBOX)

		if buttonMinus and nameMinus:
			if nameMinus != "Lider" and leader == True:
				buttonMinus.Show()

	def __PopupMessage(self, msg):
		self.popupMessage.SetText(msg)
		(w, h) = self.popupMessage.GetTextSize()
		self.popupBoard.SetSize(w + 50, h)
		self.popupMessage.SetWindowHorizontalAlignCenter()
		self.popupDialog.GetChild("accept").SetWindowHorizontalAlignCenter()
		self.popupDialog.SetTop()
		self.popupDialog.Show()

	def __OnClickSelectGuildMarkButton(self):
		if guild.GetGuildLevel() < int(localeinfo.GUILD_MARK_MIN_LEVEL):
			self.__PopupMessage(localeinfo.GUILD_MARK_NOT_ENOUGH_LEVEL)
		elif not guild.MainPlayerHasAuthority(guild.AUTH_NOTICE):
			self.__PopupMessage(localeinfo.GUILD_NO_NOTICE_PERMISSION)
		else:
			self.markSelectDialog.Open()

	def __OnClickDeclareWarButton(self):
		import uiguildwardeclare
		inputDialog = uiguildwardeclare.DeclareGuildWarDialog()
		inputDialog.Open()
		self.inputDialog = inputDialog

	def __OnSelectMark(self, markFileName):
		ret = net.UploadMark("upload/" + markFileName)

		if net.ERROR_MARK_UPLOAD_NEED_RECONNECT == ret:
			self.__PopupMessage(localeinfo.UPLOAD_MARK_UPLOAD_NEED_RECONNECT)
		return ret

	def __OnSelectSymbol(self, symbolFileName):
		net.UploadSymbol("upload/"+symbolFileName)

	def __OnClickMessageLeaderButton(self):
		page = self.pageWindow["GUILD_INFO"]
		gt = page.GetChild
		button = gt("MessageLeaderButton")
		img = gt("MessageLeaderSlot")
		space = gt("smsg1")
		lines = []
		if self.msgLeader == False:
			self.msgLeader = True
			button.SetUpVisual("interface/icons/special/quest_open.tga")
			button.SetOverVisual("interface/icons/special/quest_open_hover.tga")
			button.SetDownVisual("interface/icons/special/quest_open.tga")
			current = ""
			for i in range(1, 5):
				if gt("msg"+str(i)).GetText() != "":
					if i == 1:
						current += gt("msg"+str(i)).GetText()
					else:
						current += " " + gt("msg"+str(i)).GetText()

			space.SetText(current)
			space.SetFocus()
			space.SetEndPosition()
			img.Show()
		else:
			self.msgLeader = False
			button.SetUpVisual("interface/icons/special/quest_closed.tga")
			button.SetOverVisual("interface/icons/special/quest_closed_hover.tga")
			button.SetDownVisual("interface/icons/special/quest_closed.tga")
			img.Hide()
			current = ""
			for i in range(1, 5):
				if gt("msg"+str(i)).GetText() != "":
					if i == 1:
						current += gt("msg"+str(i)).GetText()
					else:
						current += " " + gt("msg"+str(i)).GetText()
			text = space.GetText()
			if not text or text == current:
				return False
			lines = self.SplitText(text, 37)
			if lines[0] == "":
				space.SetText("")
				return False
			else:
				net.SendGuildDeleteLeaderPacket(1)

			for i in range(5):
				gt("msg"+str(i+1)).SetText("")

			for i in range(len(lines)):
				net.SendGuildPostLeaderPacket(lines[len(lines) - i - 1])

			return True

	def __OnClickOfferButton(self):
		curEXP = player.GetStatus(player.EXP)

		if curEXP <= 100:
			self.__PopupMessage(localeinfo.GUILD_SHORT_EXP)
			return

		self.offerDialog.Open(curEXP, 100)

	def __OnClickDepositButton(self):
		moneyDialog = uipickmoney.PickMoneyDialog()
		moneyDialog.LoadDialog()
		moneyDialog.SetMax(6)
		moneyDialog.SetTitleName(localeinfo.GUILD_DEPOSIT)
		moneyDialog.SetAcceptEvent(self.OnDeposit)
		moneyDialog.Open(player.GetMoney())
		self.moneyDialog = moneyDialog

	def __OnClickWithdrawButton(self):
		moneyDialog = uipickmoney.PickMoneyDialog()
		moneyDialog.LoadDialog()
		moneyDialog.SetMax(6)
		moneyDialog.SetTitleName(localeinfo.GUILD_WITHDRAW)
		moneyDialog.SetAcceptEvent(self.OnWithdraw)
		moneyDialog.Open(guild.GetGuildMoney())
		self.moneyDialog = moneyDialog

	def __OnBlock(self):
		popup = uicommon.PopupDialog()
		popup.SetText(localeinfo.NOT_YET_SUPPORT)
		popup.SetAcceptEvent(self.__OnClosePopupDialog)
		popup.Open()
		self.popup = popup

	def __OnClosePopupDialog(self):
		self.popup = None

	def OnDeposit(self, money):
		net.SendGuildDepositMoneyPacket(money)

	def OnWithdraw(self, money):
		net.SendGuildWithdrawMoneyPacket(money)

	def OnOffer(self, exp):
		net.SendGuildOfferPacket(exp)

	def SplitText(self, text, limit):
		total_tokens = text.split()
		line_tokens = []
		line_len = 0
		lines = []
		for token in total_tokens:
			if "|" in token:
				sep_pos = token.find("|")
				line_tokens.append(token[:sep_pos])

				lines.append(" ".join(line_tokens))
				line_len = len(token) - (sep_pos + 1)
				line_tokens = [token[sep_pos+1:]]
			else:
				line_len += len(token)
				if len(line_tokens) + line_len > limit:
					lines.append(" ".join(line_tokens))
					line_len = len(token)
					line_tokens = [token]
				else:
					line_tokens.append(token)

		if line_tokens:
			lines.append(" ".join(line_tokens))

		return lines

	def OnPostComment(self):
		text = self.commentSlot.GetText()
		if not text:
			return False

		lines = []
		lines = self.SplitText(text, 50)

		if lines[0] == "":
			self.__PopupMessage("Nгo й permitido palavras com mais de 50 letras.")
			return False

		net.SendGuildPostCommentPacket(text[:97])
		self.commentSlot.SetText("")
		return True

	def OnDeleteComment(self, index):
		commentID, chrName, comment = self.__GetGuildBoardCommentData(index)
		net.SendGuildDeleteCommentPacket(commentID)

	def OnRefreshComments(self):
		net.SendGuildRefreshCommentsPacket(0)

	def OnChangeMemberGrade(self, lineIndex, gradeNumber):
		PID = guild.MemberIndexToPID(lineIndex + self.memberLinePos)
		net.SendGuildChangeMemberGradePacket(PID, gradeNumber)

	def OnEnableGeneral(self, lineIndex):
		if not guild.IsMember(lineIndex):
			return

		pid, name, grade, job, level, offer, general = self.GetMemberData(lineIndex)
		if pid < 0:
			return

		net.SendGuildChangeMemberGeneralPacket(pid, 1 - general)

	def DelGradeName(self, index, authority):
		net.SendGuildChangeGradeNamePacket(index, "Recruta")
		if (authority & guild.AUTH_ADD_MEMBER):
			net.SendGuildChangeGradeAuthorityPacket(index, authority ^ 1<<0)
		if (authority & guild.AUTH_REMOVE_MEMBER):
			net.SendGuildChangeGradeAuthorityPacket(index, authority ^ 1<<1)
		if (authority & guild.AUTH_NOTICE):
			net.SendGuildChangeGradeAuthorityPacket(index, authority ^ 1<<2)
		if (authority & guild.AUTH_SKILL):
			net.SendGuildChangeGradeAuthorityPacket(index, authority ^ 1<<3)
		if (authority & guild.AUTH_WAR):
			net.SendGuildChangeGradeAuthorityPacket(index, authority ^ 1<<4)

	def OnOpenChangeGradeName(self, arg):
		self.changeGradeNameDialog.SetGradeNumber(arg)
		self.changeGradeNameDialog.Open()

	def OnChangeGradeName(self):
		self.changeGradeNameDialog.Hide()
		gradeNumber = self.changeGradeNameDialog.GetGradeNumber()
		gradeName = self.changeGradeNameDialog.GetGradeName()

		if gradeName == "Lider" or gradeName == "Lнder":
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Nome invбlido de patente.")
			return True

		if len(gradeName) == 0:
			gradeName = localeinfo.GUILD_DEFAULT_GRADE

		net.SendGuildChangeGradeNamePacket(gradeNumber, gradeName)
		return True

	def OnCheckAuthority(self, argIndex, argAuthority):
		name, authority = guild.GetGradeData(argIndex)
		net.SendGuildChangeGradeAuthorityPacket(argIndex, authority ^ argAuthority)

	def OnScrollMemberLine(self):
		scrollBar = self.pageWindow["MEMBER"].scrollBar
		pos = scrollBar.GetPos()

		count = guild.GetMemberCount()
		newLinePos = int(float(count - self.MEMBER_LINE_COUNT) * pos)

		if newLinePos != self.memberLinePos:
			self.memberLinePos = newLinePos
			self.RefreshGuildMemberPageMemberList()
			self.__CloseAllGuildMemberPageGradeComboBox()

	def GetMemberData(self, localPos):
		return guild.GetMemberData(localPos + self.memberLinePos)

	def __OnOpenHealGSPBoard(self):
		curPoint, maxPoint = guild.GetDragonPowerPoint()

		if maxPoint - curPoint <= 0:
			self.__PopupMessage(localeinfo.GUILD_CANNOT_HEAL_GSP_ANYMORE)
			return

		pickDialog = uipickmoney.PickMoneyDialog()
		pickDialog.LoadDialog()
		pickDialog.SetMax(9)
		pickDialog.SetTitleName(localeinfo.GUILD_HEAL_GSP)
		pickDialog.SetAcceptEvent(self.__OnOpenHealGSPQuestionDialog)
		pickDialog.Open(maxPoint - curPoint, 1)
		self.pickDialog = pickDialog

	def __OnOpenHealGSPQuestionDialog(self, healGSP):
		money = healGSP * constinfo.GUILD_MONEY_PER_GSP

		questionDialog = uicommon.QuestionDialog()
		questionDialog.SetText(localeinfo.GUILD_DO_YOU_HEAL_GSP % (money, healGSP))
		questionDialog.SetAcceptEvent(self.__OnHealGSP)
		questionDialog.SetCancelEvent(self.__OnCloseQuestionDialog)
		questionDialog.SetWidth(400)
		questionDialog.Open()
		questionDialog.healGSP = healGSP
		self.questionDialog = questionDialog

	def __OnHealGSP(self):
		net.SendGuildChargeGSPPacket(self.questionDialog.healGSP)
		self.__OnCloseQuestionDialog()

	def __OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()
		self.questionDialog = None

	def OnPickUpGuildSkill(self, skillSlotIndex):
		mouseController = mousemodule.mouseController

		if False == mouseController.isAttached():
			skillIndex = player.GetSkillIndex(skillSlotIndex)
			skillLevel = guild.GetSkillLevel(skillSlotIndex)

			if skill.CanUseSkill(skillIndex) and skillLevel > 0:
				if app.IsPressed(app.DIK_LCONTROL):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL, skillSlotIndex)
					return

				mouseController.AttachObject(self, player.SLOT_TYPE_SKILL, skillSlotIndex, skillIndex)
		else:
			mouseController.DeattachObject()

	def OnUseGuildSkill(self, slotNumber):
		skillIndex = player.GetSkillIndex(slotNumber)
		skillLevel = guild.GetSkillLevel(slotNumber)

		if skillLevel <= 0:
			return

		player.UseGuildSkill(slotNumber)

	def OnUpGuildSkill(self, slotNumber):
		skillIndex = player.GetSkillIndex(slotNumber)
		net.SendChatPacket("/gskillup " + str(skillIndex))

	def OnUseSkill(self, slotNumber, coolTime):
		if self.isLoaded == 0:
			return

		page = self.pageWindow["SKILL"]

		if page.activeSlot.HasSlot(slotNumber):
			page.activeSlot.SetSlotCoolTime(slotNumber, coolTime)

	def OnStartGuildWar(self, guildSelf, guildOpp):
		if self.isLoaded == 0:
			return

		if guild.GetGuildID() != guildSelf:
			return

		guildName = guild.GetGuildName(guildOpp)
		for guildNameTextLine in self.enemyGuildNameList:
			if localeinfo.GUILD_INFO_ENEMY_GUILD_EMPTY == guildNameTextLine.GetText():
				guildNameTextLine.SetText(guildName)
				return

	def OnEndGuildWar(self, guildSelf, guildOpp):
		if self.isLoaded == 0:
			return

		if guild.GetGuildID() != guildSelf:
			return

		guildName = guild.GetGuildName(guildOpp)
		for guildNameTextLine in self.enemyGuildNameList:
			if guildName == guildNameTextLine.GetText():
				guildNameTextLine.SetText(localeinfo.GUILD_INFO_ENEMY_GUILD_EMPTY)
				return

	def OverInItem(self, slotNumber):
		if mousemodule.mouseController.isAttached():
			return

		if None != self.tooltipSkill:
			skillIndex = player.GetSkillIndex(slotNumber)
			skillLevel = guild.GetSkillLevel(slotNumber)

			self.tooltipSkill.SetSkill(skillIndex, skillLevel)

	def OverOutItem(self):
		if None != self.tooltipSkill:
			self.tooltipSkill.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True

### RANKING ###### RANKING ###### RANKING ###### RANKING ###### RANKING ###### RANKING ###### RANKING ###
	def Make_WarLog_Page(self):
		page = self.pageWindow["WAR_LIST"]
		Get = page.GetChild
		Get("War_ScrollBar").SetScrollEvent(self.OnWarScroll)
		self.SetWarScrollBarSize()
		self.ListTheFuckingWars()

	def Make_Ranking_Page(self):
		page = self.pageWindow["RANKING"]
		Get = page.GetChild
		Get("Ranking_ScrollBar").SetScrollEvent(self.OnRankingScroll)
		self.SetRankingScrollBarSize()
		self.ListTheFuckingRanking()

	def ListTheFuckingWars(self, init = 0):
		page = self.pageWindow["WAR_LIST"]
		Get = page.GetChild

		i = 0
		while i < 15 and init < len(constinfo.WAR_LIST):
			temp = constinfo.WAR_LIST[init]
			Get("slot"+str(i)).SetMouseLeftButtonDownEvent(self.OpenWarDetails, temp[0], temp)
			Get("W_"+str(i)+"_Data").SetText(temp[1])
			if int(temp[4]) > int(temp[7]):
				Get("W_"+str(i)+"_Guild1").SetText(temp[3])
				Get("W_"+str(i)+"_Guild1_Pontos").SetText(temp[4])
				Get("W_"+str(i)+"_Guild1_Online").SetText(temp[5])
				Get("W_"+str(i)+"_Guild2").SetText(temp[6])
				Get("W_"+str(i)+"_Guild2_Pontos").SetText(temp[7])
				Get("W_"+str(i)+"_Guild2_Online").SetText(temp[8])
			else:
				Get("W_"+str(i)+"_Guild1").SetText(temp[6])
				Get("W_"+str(i)+"_Guild1_Pontos").SetText(temp[7])
				Get("W_"+str(i)+"_Guild1_Online").SetText(temp[8])
				Get("W_"+str(i)+"_Guild2").SetText(temp[3])
				Get("W_"+str(i)+"_Guild2_Pontos").SetText(temp[4])
				Get("W_"+str(i)+"_Guild2_Online").SetText(temp[5])
			i += 1
			init += 1

		while i < 15:
			Get("slot"+str(i)).SetMouseLeftButtonDownEvent(self.OpenWarDetails, 0, None)
			Get("W_"+str(i)+"_Data").SetText("")
			Get("W_"+str(i)+"_Guild1").SetText("")
			Get("W_"+str(i)+"_Guild1_Pontos").SetText("")
			Get("W_"+str(i)+"_Guild1_Online").SetText("")
			Get("W_"+str(i)+"_Guild2").SetText("")
			Get("W_"+str(i)+"_Guild2_Pontos").SetText("")
			Get("W_"+str(i)+"_Guild2_Online").SetText("")
			i += 1

	def ListTheFuckingRanking(self, init = 0):
		page = self.pageWindow["RANKING"]
		Get = page.GetChild

		i = 0
		while i < 15 and init < len(constinfo.RANKING_LIST):
			temp = constinfo.RANKING_LIST[init]
			Get("RK_"+str(i)+"_Pos").SetText(str(init + 1))
			Get("RK_"+str(i)+"_Nome").SetText(temp[0])
			Get("RK_"+str(i)+"_Pontos").SetText(temp[1])
			Get("RK_"+str(i)+"_Vitorias").SetText(temp[2])
			Get("RK_"+str(i)+"_Empates").SetText(temp[3])
			Get("RK_"+str(i)+"_Derrotas").SetText(temp[4])

			i += 1
			init += 1

		while i < 15:
			Get("RK_"+str(i)+"_Pos").SetText("")
			Get("RK_"+str(i)+"_Nome").SetText("")
			Get("RK_"+str(i)+"_Pontos").SetText("")
			Get("RK_"+str(i)+"_Vitorias").SetText("")
			Get("RK_"+str(i)+"_Empates").SetText("")
			Get("RK_"+str(i)+"_Derrotas").SetText("")
			i += 1

	def OnRankingScroll(self):
		page = self.pageWindow["RANKING"]
		Get = page.GetChild
		pos = int(Get("Ranking_ScrollBar").GetPos() * max(0, len(constinfo.RANKING_LIST) - 15))
		self.ListTheFuckingRanking(pos)

	def OnWarScroll(self):
		page = self.pageWindow["WAR_LIST"]
		Get = page.GetChild
		pos = int(Get("War_ScrollBar").GetPos() * max(0, len(constinfo.WAR_LIST) - 15))
		self.ListTheFuckingWars(pos)

	def SetRankingScrollBarSize(self):
		page = self.pageWindow["RANKING"]
		Get = page.GetChild
		Get("Ranking_ScrollBar").SetMiddleBarSize(15.0/max(15.0, float(len(constinfo.RANKING_LIST))))

	def SetWarScrollBarSize(self):
		page = self.pageWindow["WAR_LIST"]
		Get = page.GetChild
		Get("War_ScrollBar").SetMiddleBarSize(15.0/max(15.0, float(len(constinfo.WAR_LIST))))

	def RankingAddGuild(self, nome, pontos, vitorias, empates, derrotas):
		constinfo.RANKING_LIST.append([nome, pontos, vitorias, empates, derrotas])
		self.SetRankingScrollBarSize()
		self.ListTheFuckingRanking()

	def RankingClean(self):
		constinfo.RANKING_LIST = []
		self.SetRankingScrollBarSize()
		self.ListTheFuckingRanking()

	def WarHistoryAppend(self, war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount):
		constinfo.WAR_LIST.append([war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount])
		self.SetWarScrollBarSize()
		self.ListTheFuckingWars()

	def WarHistoryInsert(self, war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount):
		constinfo.WAR_LIST.insert(0, [war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount])
		self.SetWarScrollBarSize()
		self.ListTheFuckingWars()

	def WarHistoryClean(self):
		constinfo.WAR_LIST = []
		self.SetWarScrollBarSize()
		self.ListTheFuckingWars()

############################################################################################################
# # # KILLS# # # KILLS# # # KILLS# # # KILLS# # # KILLS# # # KILLS# # # KILLS# # # KILLS# # # KILLS# # # KIL
############################################################################################################
	def SetKillsScrollBarSize(self, war_id):
		if not constinfo.WAR_KILL.__contains__(war_id):
			return
		if not constinfo.WAR_KILL[war_id].__contains__(self.winner):
			return
		if not constinfo.WAR_KILL[war_id].__contains__(self.loser):
			return

		page = self.pageWindow["WAR_INFO"]
		Get = page.GetChild
		table_size = max(len(constinfo.WAR_KILL[war_id][self.winner]), len(constinfo.WAR_KILL[war_id][self.loser]))
		Get("War_ScrollBar").SetMiddleBarSize(15.0/max(15.0, float(table_size)))

	def OnKillsScroll(self, war_id):
		if not constinfo.WAR_KILL.__contains__(war_id):
			return
		if not constinfo.WAR_KILL[war_id].__contains__(self.winner):
			return
		if not constinfo.WAR_KILL[war_id].__contains__(self.loser):
			return

		page = self.pageWindow["WAR_INFO"]
		Get = page.GetChild

		table_size = max(len(constinfo.WAR_KILL[war_id][self.winner]), len(constinfo.WAR_KILL[war_id][self.loser]))
		pos = int(Get("War_ScrollBar").GetPos() * max(0, table_size - 15))
		self.ListTheFuckingKills(war_id, pos)

	def WarKillsAppend(self, war_id, player, killed, died, guild):
		if not constinfo.WAR_KILL.__contains__(war_id):
			constinfo.WAR_KILL.update({war_id : {}})
		if not constinfo.WAR_KILL[war_id].__contains__(guild):
			constinfo.WAR_KILL[war_id].update({guild : []})

		constinfo.WAR_KILL[war_id][guild].append([player, killed, died])
		self.SetKillsScrollBarSize(war_id)
		self.ListTheFuckingKills(war_id)

	def OpenWarDetails(self, war_id, war_data):
		if war_id == 0:
			return
		if not constinfo.WAR_KILL.__contains__(war_id):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Carregando informaзхes da database.")
			constinfo.WAR_KILL.update({war_id : {}})
			net.SendChatPacket("/war_kills " + war_id)
		self.OpenWarDetailsWindow(war_id, war_data)

	winner = ""
	loser = ""

	def OpenWarDetailsWindow(self, war_id, war_data):
		if int(war_data[4]) > int(war_data[7]):
			title = war_data[3] + " " + war_data[4] + " x " + war_data[7] + " " + war_data[6]
			self.winner = war_data[3]
			self.loser = war_data[6]
		else:
			title = war_data[6] + " " + war_data[7] + " x " + war_data[4] + " " + war_data[3]
			self.winner = war_data[6]
			self.loser = war_data[3]

		self.board.SetTitleName(title)
		self.GetChild("Button_Return").SetEvent(self.ReturnToWarList)
		self.pageWindow["WAR_LIST"].Hide()

		page = self.pageWindow["WAR_INFO"]
		Get = page.GetChild
		Get("WINNER").SetText(self.winner)
		Get("LOSER").SetText(self.loser)
		page.Show()

		Get("War_ScrollBar").SetScrollEvent(self.OnKillsScroll, war_id)

		self.SetKillsScrollBarSize(war_id)
		self.ListTheFuckingKills(war_id)

	def ReturnToWarList(self):
		self.SelectPage("WAR_LIST")
		self.GetChild("Button_Return").SetEvent(self.SelectPage, "GUILD_INFO")

	def ListTheFuckingKills(self, war_id, init = 0):
		if not constinfo.WAR_KILL.__contains__(war_id):
			return
		if not constinfo.WAR_KILL[war_id].__contains__(self.winner):
			return
		if not constinfo.WAR_KILL[war_id].__contains__(self.loser):
			return

		winner_table = constinfo.WAR_KILL[war_id][self.winner]
		loser_table = constinfo.WAR_KILL[war_id][self.loser]

		page = self.pageWindow["WAR_INFO"]
		Get = page.GetChild

		i = 0
		while i < 15 and init < len(winner_table) and init < len(loser_table):
			tempw = winner_table[init]
			templ = loser_table[init]
			Get("W_"+str(i)+"_Player1").SetText(tempw[0])
			Get("W_"+str(i)+"_Killed1").SetText(tempw[1])
			Get("W_"+str(i)+"_Died1").SetText(tempw[2])
			Get("W_"+str(i)+"_Player2").SetText(templ[0])
			Get("W_"+str(i)+"_Killed2").SetText(templ[1])
			Get("W_"+str(i)+"_Died2").SetText(templ[2])
			i += 1
			init += 1

		if len(winner_table) > len(loser_table):
			while i < 15 and init < len(winner_table):
				tempw = winner_table[init]
				Get("W_"+str(i)+"_Player1").SetText(tempw[0])
				Get("W_"+str(i)+"_Killed1").SetText(tempw[1])
				Get("W_"+str(i)+"_Died1").SetText(tempw[2])
				Get("W_"+str(i)+"_Player2").SetText("")
				Get("W_"+str(i)+"_Killed2").SetText("")
				Get("W_"+str(i)+"_Died2").SetText("")
				i += 1
				init += 1
		elif len(winner_table) < len(loser_table):
			while i < 15 and init < len(loser_table):
				templ = loser_table[init]
				Get("W_"+str(i)+"_Player1").SetText("")
				Get("W_"+str(i)+"_Killed1").SetText("")
				Get("W_"+str(i)+"_Died1").SetText("")
				Get("W_"+str(i)+"_Player2").SetText(templ[0])
				Get("W_"+str(i)+"_Killed2").SetText(templ[1])
				Get("W_"+str(i)+"_Died2").SetText(templ[2])
				i += 1
				init += 1

		while i < 15:
			Get("W_"+str(i)+"_Player1").SetText("")
			Get("W_"+str(i)+"_Killed1").SetText("")
			Get("W_"+str(i)+"_Died1").SetText("")
			Get("W_"+str(i)+"_Player2").SetText("")
			Get("W_"+str(i)+"_Killed2").SetText("")
			Get("W_"+str(i)+"_Died2").SetText("")
			i += 1

#### WAR SCORE #### WAR SCORE #### WAR SCORE #### WAR SCORE #### WAR SCORE #### WAR SCORE #### WAR SCORE ####
class GuildWarScoreBoard(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self)
		self.Initialize()
		self.AddFlag("not_pick")

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def Initialize(self):
		self.allyGuildID = 0
		self.enemyGuildID = 0
		self.allyDataDict = {}
		self.enemyDataDict = {}

	def Open(self, allyGuildID, enemyGuildID):
		self.allyGuildID = allyGuildID
		self.enemyGuildID = enemyGuildID

		mark = ui.MarkBox()
		mark.SetParent(self)
		mark.SetIndex(allyGuildID)
		mark.SetPosition(15, 15 + 20*0)
		mark.Show()
		scoreText = ui.TextLine()
		scoreText.SetParent(self)
		scoreText.SetPosition(35, 13 + 20*0)
		scoreText.SetHorizontalAlignLeft(),
		scoreText.SetPackedFontColor(0xfff8d090)
		scoreText.Show()
		self.allyDataDict["NAME"] = guild.GetGuildName(allyGuildID)
		self.allyDataDict["SCORE"] = 0
		self.allyDataDict["MEMBER_COUNT"] = -1
		self.allyDataDict["MARK"] = mark
		self.allyDataDict["TEXT"] = scoreText
		self.allyDataDict["TEXT"].SetText(self.allyDataDict["NAME"])

		mark = ui.MarkBox()
		mark.SetParent(self)
		mark.SetIndex(enemyGuildID)
		mark.SetPosition(15, 15 + 20*1)
		mark.Show()
		scoreText = ui.TextLine()
		scoreText.SetParent(self)
		scoreText.SetPosition(35, 13 + 20*1)
		scoreText.SetHorizontalAlignLeft()
		scoreText.SetPackedFontColor(0xfff8d090)
		scoreText.Show()
		self.enemyDataDict["NAME"] = guild.GetGuildName(enemyGuildID)
		self.enemyDataDict["SCORE"] = 0
		self.enemyDataDict["MEMBER_COUNT"] = -1
		self.enemyDataDict["MARK"] = mark
		self.enemyDataDict["TEXT"] = scoreText
		self.enemyDataDict["TEXT"].SetText(self.enemyDataDict["NAME"])

		button = ui.RedButton()
		if str(background.GetCurrentMapName()) in ["metin2_map_t1", "metin2_map_t2", "metin2_map_t3", "metin2_map_t4", "metin2_map_t5",]:
			button.SetText("Sair")
			button.SetEvent(self.WarOut)
		else:
			button.SetEvent(self.WarEnter)
			button.SetText("Entrar")
		button.SetWidth(70)
		button.SetParent(self)
		button.SetPosition(0, 55)
		button.SetWindowHorizontalAlignCenter()
		button.Show()
		self.button = button

		self.RefreshName()
		self.Show()

	def __GetDataDict(self, ID):
		if self.allyGuildID == ID:
			return self.allyDataDict
		if self.enemyGuildID == ID:
			return self.enemyDataDict

		return None

	def SetScore(self, gainGuildID, opponetGuildID, point):
		dataDict = self.__GetDataDict(gainGuildID)
		if not dataDict:
			return
		dataDict["SCORE"] = point
		self.RefreshName()

	def UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2):
		dataDict1 = self.__GetDataDict(guildID1)
		dataDict2 = self.__GetDataDict(guildID2)
		if dataDict1:
			dataDict1["MEMBER_COUNT"] = memberCount1
		if dataDict2:
			dataDict2["MEMBER_COUNT"] = memberCount2
		self.RefreshName()

	def RefreshName(self):
		if -1 == self.allyDataDict["MEMBER_COUNT"] or -1 == self.enemyDataDict["MEMBER_COUNT"]:
			self.allyDataDict["TEXT"].SetText("%s |cffff8784%d" % (self.allyDataDict["NAME"], self.allyDataDict["SCORE"]))
			self.enemyDataDict["TEXT"].SetText("%s |cffff8784%d" % (self.enemyDataDict["NAME"], self.enemyDataDict["SCORE"]))
		else:
			self.allyDataDict["TEXT"].SetText("%s|cfff8d090(%d) |cffff8784%d" % (self.allyDataDict["NAME"], self.allyDataDict["MEMBER_COUNT"], self.allyDataDict["SCORE"]))
			self.enemyDataDict["TEXT"].SetText("%s|cfff8d090(%d) |cffff8784%d" % (self.enemyDataDict["NAME"], self.enemyDataDict["MEMBER_COUNT"], self.enemyDataDict["SCORE"]))

		nameMaxLen = max(self.allyDataDict["TEXT"].GetTextSize()[0], self.enemyDataDict["TEXT"].GetTextSize()[0])
		self.SetSize(60+nameMaxLen, 60 + 40)
		self.SetPosition(wndMgr.GetScreenWidth() - (60 + nameMaxLen), 140)

	def WarEnter(self):
		self.Hide()
		net.SendChatPacket("/war_enter")

	def WarOut(self):
		self.Hide()
		net.SendChatPacket("/war_out")

##### GUILD SAFEBOX ##### GUILD SAFEBOX ##### GUILD SAFEBOX ##### GUILD SAFEBOX ##### GUILD SAFEBOX #####
if app.ENABLE_GUILD_SAFEBOX:
	class GuildSafeboxWindow(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.tooltipItem = None
			self.pageButtonList = []
			self.MoneyOptionsList = []
			self.curPageIndex = 0
			self.isLoaded = 0

			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Show(self):
			self.__LoadWindow()

			ui.ScriptWindow.Show(self)

		def Destroy(self):
			self.ClearDictionary()

			self.tooltipItem = None
			self.wndMoneySlot = None
			self.wndMoney = None
			self.wndItem = None

			self.pageButtonList = []
			self.MoneyOptionsList = []

		def __LoadWindow(self):
			if self.isLoaded == 1:
				return

			self.isLoaded = 1

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/guildsafeboxwindow.py")

			wndItem = self.GetChild("Slots")
			wndItem.SetSelectEmptySlotEvent(self.SelectEmptySlot)
			wndItem.SetSelectItemSlotEvent(self.SelectItemSlot)
			wndItem.SetUnselectItemSlotEvent(self.UseItemSlot)
			wndItem.SetUseSlotEvent(self.UseItemSlot)
			wndItem.SetOverInItemEvent(self.OverInItem)
			wndItem.SetOverOutItemEvent(self.OverOutItem)
			self.wndItem = wndItem

			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			self.wndMoneySlot.SetMouseLeftButtonUpEvent(self.MoneyInputBoardOpen)
			self.wndMoneySlot.SetOverInEvent(self.OnMouseOverInMoneySlot)
			self.wndMoneySlot.SetOverOutEvent(self.OnMouseOverOutMoneySlot)

			self.GetChild("BarInputMoney").SetMouseLeftButtonDownEvent(self.OnSelectBarInputMoney)
			self.GetChild("LineInputMoney").GetNumber = ui.__mem_func__(self.LineInputMoneyGetText)
			self.GetChild("LineInputMoney").SetKillFocusEvent(self.OnKillFocusLineInputMoney)
			self.GetChild("LineInputMoney").SetIMEUpdateEvent(self.OnIMEUpdateMoney)
			self.GetChild("MoneyCancelButton").SetEvent(self.GetChild("MoneyInputBoard").Hide)
			self.GetChild("CopyPasteButton").SetEvent(self.CopyMoneyValue)
			self.GetChild("MoneyInputButton").SetEvent(self.OnMoneyOkButton)

			self.MoneyOptionsList.append(self.GetChild("Deposito"))
			self.MoneyOptionsList.append(self.GetChild("Saque"))
			self.MoneyOptionsList[1].Fill()

			i = 0
			for btn in self.MoneyOptionsList:
				btn.SetEvent(self.OptionListSelect, i)
				i =+ 1

			self.__MakePageButton(2)
			self.RefreshGuildSafeboxMoney()

		def OnMouseOverInMoneySlot(self):
			money = safebox.GetGuildMoney()
			rings = int(money/100000000)
			if rings < 1:
				self.GetChild("tipmoney_text").SetText("(Click Aqui Para Depositar)")
			elif rings == 1:
				self.GetChild("tipmoney_text").SetText("Aprуx. 1 Mбscara da Fortuna")
			else:
				self.GetChild("tipmoney_text").SetText("Aprуx. " + localeinfo.NumberToMoneyString(rings) + " Mбscaras da Fortuna")
			self.GetChild("tipmoney").SetSize(self.GetChild("tipmoney_text").GetTextSize()[0] + 30, 44)
			self.GetChild("tipmoney").SetWindowHorizontalAlignCenter()
			self.GetChild("tipmoney").Show()

		def OnMouseOverOutMoneySlot(self):
			self.GetChild("tipmoney").Hide()

		def OnIMEUpdateMoney(self):
			money = []
			money.append(player.GetElk())
			money.append(safebox.GetGuildMoney())

			index = 0
			for i in range(0, 2):
				if self.MoneyOptionsList[i].GetStatus():
					index = i

			if len(self.GetChild("LineInputMoney").GetText()):
				if self.GetChild("LineInputMoney").GetText()[0] == "0":
					self.GetChild("LineInputMoney").SetText("")

			if money[index] < self.GetChild("LineInputMoney").GetNumber():
				self.GetChild("LineInputMoney").SetText(str(money[index]))

		def CopyMoneyValue(self):
			money = []
			money.append(player.GetElk())
			money.append(safebox.GetGuildMoney())

			i = 0
			for btn in self.MoneyOptionsList:
				if btn.GetStatus():
					self.GetChild("LineInputMoney").SetText(str(money[i]))
				i += 1
			self.OnSelectBarInputMoney()

		def OptionListSelect(self, index):
			self.MoneyOptionsList[1-index].Empty()
			self.OnIMEUpdateMoney()

		def MoneyInputBoardOpen(self):
			self.GetChild("MoneyInputBoard").Show()

		def OnSelectBarInputMoney(self):
			self.GetChild("LineInputMoney").SetFocus()
			self.GetChild("LineInputMoney").SetEndPosition()
			self.GetChild("TextInputMoney").Hide()

		def LineInputMoneyGetText(self):
			res = ui.EditLine.GetText(self.GetChild("LineInputMoney"))
			if res == "":
				return 0
			else:
				return int(res)

		def OnKillFocusLineInputMoney(self):
			value = self.GetChild("LineInputMoney").GetNumber()
			if value == 0: 
				self.GetChild("LineInputMoney").SetText("")
				self.GetChild("TextInputMoney").Show()
			else:
				self.GetChild("TextInputMoney").Hide()

		def OnMoneyOkButton(self):
			money = self.GetChild("LineInputMoney").GetNumber()
			if money < 1:
				return

			if self.MoneyOptionsList[0].GetStatus():
				net.SendGuildSafeboxGiveGoldPacket(money)
			elif self.MoneyOptionsList[1].GetStatus():
				net.SendGuildSafeboxTakeGoldPacket(money)

			self.GetChild("LineInputMoney").SetText("")
			self.GetChild("LineInputMoney").KillFocus()
			self.GetChild("MoneyInputBoard").Hide()

		def __MakePageButton(self, size):
			if size > 2 or size <= 0:
				return

			self.curPageIndex = 0
			self.pageButtonList = []

			for i in range(size):
				button = self.GetChild("Tab_0" + str(i+1))
				button.SetEvent(self.SelectPage, i)
				button.Show()
				self.pageButtonList.append(button)

			self.SelectPage(0)

			if size < 2:
				self.GetChild("Tab_02").Hide()

		def SelectPage(self, index):
			self.curPageIndex = index

			for btn in self.pageButtonList:
				btn.Enable()

			self.pageButtonList[index].Disable()
			self.RefreshGuildSafebox()

		def __LocalPosToGlobalPos(self, local):
			return self.curPageIndex * 88 + local

		def RefreshGuildSafebox(self):
			getItemID = safebox.GetGuildItemID
			getItemCount = safebox.GetGuildItemCount
			setItemID = self.wndItem.SetItemSlot
			for i in range(88):
				slotIndex = self.__LocalPosToGlobalPos(i)
				itemCount = getItemCount(slotIndex)
				if not itemCount:
					itemCount = 0
				if itemCount <= 1:
					itemCount = 0
				setItemID(i, getItemID(slotIndex), itemCount)
			self.wndItem.RefreshSlot()
			self.UpdateRect()

		def RefreshGuildSafeboxMoney(self):
			self.wndMoney.SetText(localeinfo.NumberToMoneyString(safebox.GetGuildMoney()) + " Gold")

		def SetItemToolTip(self, tooltip):
			self.tooltipItem = proxy(tooltip)

		def Close(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()

		def SelectEmptySlot(self, selectedSlotPos):
			selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)
			if mousemodule.mouseController.isAttached():
				attachedSlotType = mousemodule.mouseController.GetAttachedType()
				attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
				if player.SLOT_TYPE_GUILD_SAFEBOX == attachedSlotType:
					net.SendGuildSafeboxItemMovePacket(attachedSlotPos, selectedSlotPos, 0)
				else:
					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
					if player.RESERVED_WINDOW == attachedInvenType:
						return
					if player.ITEM_MONEY == mousemodule.mouseController.GetAttachedItemIndex():
						net.SendGuildSafeboxSaveMoneyPacket(mousemodule.mouseController.GetAttachedItemCount())
						snd.PlaySound("sound/ui/money.wav")
					else:
						net.SendGuildSafeboxCheckinPacket(attachedInvenType, attachedSlotPos, selectedSlotPos)
				mousemodule.mouseController.DeattachObject()

		def SelectItemSlot(self, selectedSlotPos):
			selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)
			if mousemodule.mouseController.isAttached():
				attachedSlotType = mousemodule.mouseController.GetAttachedType()
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
						attachedSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
				mousemodule.mouseController.DeattachObject()
			else:
				curCursorNum = app.GetCursor()
				if app.SELL == curCursorNum:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SAFEBOX_SELL_DISABLE_SAFEITEM)
				elif app.BUY == curCursorNum:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SHOP_BUY_INFO)
				else:
					selectedItemID = safebox.GetGuildItemID(selectedSlotPos)
					mousemodule.mouseController.AttachObject(self, player.SLOT_TYPE_GUILD_SAFEBOX, selectedSlotPos, selectedItemID)
					snd.PlaySound("sound/ui/pick.wav")

		def UseItemSlot(self, slotIndex):
			mousemodule.mouseController.DeattachObject()

		def __ShowToolTip(self, slotIndex):
			if self.tooltipItem:
				self.tooltipItem.SetGuildSafeBoxItem(slotIndex)

		def OverInItem(self, slotIndex):
			slotIndex = self.__LocalPosToGlobalPos(slotIndex)
			self.wndItem.SetUsableItem(False)
			self.__ShowToolTip(slotIndex)

		def OverOutItem(self):
			self.wndItem.SetUsableItem(False)
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()

# guild_teste = GuildWarScoreBoard()
# guild_teste.Open(100, 200)
# guild_teste.Show()

# guild_teste.allyDataDict["NAME"] = "BrunoTeste"
# guild_teste.allyDataDict["SCORE"] = 0
# guild_teste.allyDataDict["MEMBER_COUNT"] = 20
# guild_teste.allyDataDict["TEXT"].SetText(guild_teste.allyDataDict["NAME"])

# guild_teste.RefreshName()
# guild_teste.SetScore(100, 200, 50)
# guild_teste.SetScore(200, 100, 50)
# guild_teste.UpdateMemberCount(100, 20, 200, 30)

# a = GuildWindow()
# a.Open()

# pyScrLoader = ui.PythonScriptLoader()
# a = ChangeGradeNameDialog()
# pyScrLoader.LoadScriptFile(a, "uiscript/changegradenamedialog.py")
# a.gradeNameSlot = a.GetChild("GradeNameValue")
# a.Open()