#favor manter essa linha
import enszxc3467hc3kokdueq as app
import zn94xlgo573hf8xmddzq as net
import ui
import snd
import event
import wndMgr
import _weakref
import localeinfo
import uiscriptlocale
import musicinfo
import systemSetting
import uitooltip

class SelectEmpireWindow(ui.ScriptWindow):

	EMPIRE_NAME = { 
		net.EMPIRE_A : localeinfo.EMPIRE_A,
		net.EMPIRE_B : localeinfo.EMPIRE_B,
		net.EMPIRE_C : localeinfo.EMPIRE_C
	}

	EMPIRE_NAME_COLOR = { 
		net.EMPIRE_A : (0.7450, 0, 0),
		net.EMPIRE_B : (0.8666, 0.6156, 0.1843),
		net.EMPIRE_C : (0.2235, 0.2549, 0.7490)
	}

	EMPIRE_DESCRIPTION_TEXT_FILE_NAME = {
		net.EMPIRE_A : uiscriptlocale.EMPIREDESC_A,
		net.EMPIRE_B : uiscriptlocale.EMPIREDESC_B,
		net.EMPIRE_C : uiscriptlocale.EMPIREDESC_C,
	}

	class EmpireButton(ui.Window):

		def __init__(self, owner, arg):
			ui.Window.__init__(self)
			self.owner = owner
			self.arg = arg

		def OnMouseOverIn(self):
			self.owner.OnOverInEmpire(self.arg)

			text = None
			if net.EMPIRE_A == self.arg :
				text = localeinfo.EMPIRE_A
			elif net.EMPIRE_B == self.arg :
				text = localeinfo.EMPIRE_B
			elif net.EMPIRE_C == self.arg :
				text = localeinfo.EMPIRE_C

		def OnMouseOverOut(self):
			self.owner.OnOverOutEmpire(self.arg)
			self.owner.OverOutToolTip()

		def OnMouseLeftButtonDown(self):
			if self.owner.empireID != self.arg:
				self.owner.OnSelectEmpire(self.arg)

	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet(self.descIndex)

	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, self)

		self.stream=stream
		self.empireID = net.GetEmpireID()

		self.descIndex=0
		self.empireArea = {}
		self.empireAreaFlag = {}
		self.empireFlag = {}
		self.empireAreaButton = {}
		self.empireAreaCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaFlagCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaFlagDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireFlagCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }
		self.empireFlagDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0, net.EMPIRE_C:0.0 }

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, 0)

	def Close(self):
		self.ClearDictionary()
		self.leftButton = None
		self.rightButton = None
		self.selectButton = None
		self.exitButton = None
		self.textBoard = None
		self.descriptionBox = None
		self.empireArea = None
		self.empireAreaButton = None

		if musicinfo.selectMusic != "":
			snd.FadeOutMusic("bgm/"+musicinfo.selectMusic)

		self.empireName = None
		self.EMPIRE_NAME = None
		self.EMPIRE_NAME_COLOR = None
		self.toolTip = None
		self.ShowToolTip = None
		self.btnPrev = None
		self.btnNext = None

		self.KillFocus()
		self.Hide()

		app.HideCursor()
		event.Destroy()

	def Open(self):
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("SelectEmpireWindow")
		self.Show()

		self.__LoadScript("uiscript/selectempirewindow.py")

		self.OnSelectEmpire(self.empireID)
		self.__CreateButtons()
		self.__CreateDescriptionBox()
		app.ShowCursor()

		if musicinfo.selectMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("bgm/"+musicinfo.selectMusic)	

			self.toolTip = uitooltip.ToolTip()
			self.toolTip.ClearToolTip()

			self.ShowToolTip = False

	def __CreateButtons(self):
		for key, img in self.empireArea.items():

			img.SetAlpha(0.0)

			(x, y) = img.GetGlobalPosition()
			btn = self.EmpireButton(_weakref.proxy(self), key)
			btn.SetParent(self)
			btn.SetPosition(x, y)
			btn.SetSize(img.GetWidth(), img.GetHeight())
			btn.Show()
			self.empireAreaButton[key] = btn

	def __CreateDescriptionBox(self):
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.Show()

	def OnOverInEmpire(self, arg):
		self.empireAreaDestAlpha[arg] = 1.0

	def OnOverOutEmpire(self, arg):
		if arg != self.empireID:
			self.empireAreaDestAlpha[arg] = 0.0

	def OnSelectEmpire(self, arg):
		for key in self.empireArea.keys():
			self.empireAreaDestAlpha[key] = 0.0
			self.empireAreaFlagDestAlpha[key] = 0.0
			self.empireFlagDestAlpha[key] = 0.0
		self.empireAreaDestAlpha[arg] = 1.0
		self.empireAreaFlagDestAlpha[arg] = 1.0
		self.empireFlagDestAlpha[arg] = 1.0
		self.empireID = arg

		self.empireName.SetText(self.EMPIRE_NAME.get(self.empireID, ""))
		rgb = self.EMPIRE_NAME_COLOR[self.empireID]
		self.empireName.SetFontColor(rgb[0], rgb[1], rgb[2])
		snd.PlaySound("sound/ui/click.wav")

		event.ClearEventSet(self.descIndex)
		if self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME.has_key(arg):
			self.descIndex = event.RegisterEventSet(self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME[arg])

			event.SetFontColor(self.descIndex, 0.7843, 0.7843, 0.7843)
			event.SetRestrictedCount(self.descIndex, 35)

		if event.BOX_VISIBLE_LINE_COUNT >= event.GetTotalLineCount(self.descIndex) :
			self.btnPrev.Hide()
			self.btnNext.Hide()
		else :
			self.btnPrev.Show()
			self.btnNext.Show()

	def PrevDescriptionPage(self):
		if event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def NextDescriptionPage(self):
		if event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + event.BOX_VISIBLE_LINE_COUNT)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

		GetObject = self.GetChild
		self.leftButton = GetObject("left_button")
		self.rightButton = GetObject("right_button")
		self.selectButton = GetObject("select_button")
		self.exitButton = GetObject("exit_button")
		self.textBoard = GetObject("text_board")
		self.empireArea[net.EMPIRE_A] = GetObject("EmpireArea_A")
		self.empireArea[net.EMPIRE_B] = GetObject("EmpireArea_B")
		self.empireArea[net.EMPIRE_C] = GetObject("EmpireArea_C")
		self.empireAreaFlag[net.EMPIRE_A] = GetObject("EmpireAreaFlag_A")
		self.empireAreaFlag[net.EMPIRE_B] = GetObject("EmpireAreaFlag_B")
		self.empireAreaFlag[net.EMPIRE_C] = GetObject("EmpireAreaFlag_C")
		self.empireFlag[net.EMPIRE_A] = GetObject("EmpireFlag_A")
		self.empireFlag[net.EMPIRE_B] = GetObject("EmpireFlag_B")
		self.empireFlag[net.EMPIRE_C] = GetObject("EmpireFlag_C")
		GetObject("prev_text_button").SetEvent(self.PrevDescriptionPage)
		GetObject("next_text_button").SetEvent(self.NextDescriptionPage)

		self.empireName = GetObject("EmpireName")
		self.btnPrev = GetObject("prev_text_button")
		self.btnNext = GetObject("next_text_button")

		GetObject("left_button").ShowToolTip = lambda arg = uiscriptlocale.EMPIRE_PREV : self.OverInToolTip(arg)
		GetObject("left_button").HideToolTip = ui.__mem_func__(self.OverOutToolTip)
		GetObject("right_button").ShowToolTip = lambda arg = uiscriptlocale.EMPIRE_NEXT : self.OverInToolTip(arg)
		GetObject("right_button").HideToolTip = ui.__mem_func__(self.OverOutToolTip)

		GetObject("prev_text_button").ShowToolTip = lambda arg = uiscriptlocale.EMPIRE_PREV : self.OverInToolTip(arg)
		GetObject("prev_text_button").HideToolTip = ui.__mem_func__(self.OverOutToolTip)
		GetObject("next_text_button").ShowToolTip = lambda arg = uiscriptlocale.EMPIRE_NEXT : self.OverInToolTip(arg)
		GetObject("next_text_button").HideToolTip = ui.__mem_func__(self.OverOutToolTip)

		GetObject("select_button").ShowToolTip = lambda arg = uiscriptlocale.EMPIRE_SELECT : self.OverInToolTip(arg)
		GetObject("select_button").HideToolTip = ui.__mem_func__(self.OverOutToolTip)
		GetObject("exit_button").ShowToolTip = lambda arg = uiscriptlocale.EMPIRE_EXIT : self.OverInToolTip(arg)
		GetObject("exit_button").HideToolTip = ui.__mem_func__(self.OverOutToolTip)

		self.selectButton.SetEvent(self.ClickSelectButton)
		self.exitButton.SetEvent(self.ClickExitButton)
		self.leftButton.SetEvent(self.ClickRightButton)
		self.rightButton.SetEvent(self.ClickLeftButton)

		for flag in self.empireAreaFlag.values():
			flag.SetAlpha(0.0)
		for flag in self.empireFlag.values():
			flag.SetAlpha(0.0)

		return 1

	def ClickLeftButton(self):
		self.empireID -= 1
		if self.empireID < 1:
			self.empireID = 3

		self.OnSelectEmpire(self.empireID)

	def ClickRightButton(self):
		self.empireID += 1
		if self.empireID > 3:
			self.empireID = 1

		self.OnSelectEmpire(self.empireID)

	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetSelectCharacterPhase()
		self.Hide()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()
		self.Hide()

	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7))
		self.descriptionBox.SetIndex(self.descIndex)

		self.__UpdateAlpha(self.empireArea, self.empireAreaCurAlpha, self.empireAreaDestAlpha)
		self.__UpdateAlpha(self.empireAreaFlag, self.empireAreaFlagCurAlpha, self.empireAreaFlagDestAlpha)
		self.__UpdateAlpha(self.empireFlag, self.empireFlagCurAlpha, self.empireFlagDestAlpha)

		self.ToolTipProgress()

	def __UpdateAlpha(self, dict, curAlphaDict, destAlphaDict):
		for key, img in dict.items():

			curAlpha = curAlphaDict[key]
			destAlpha = destAlphaDict[key]

			if abs(destAlpha - curAlpha) / 10 > 0.0001:
				curAlpha += (destAlpha - curAlpha) / 7
			else:
				curAlpha = destAlpha

			curAlphaDict[key] = curAlpha
			img.SetAlpha(curAlpha)

	def OnPressEscapeKey(self):
		self.ClickExitButton()
		return True

	def OverInToolTip(self, arg):
		arglen = len(str(arg))
		pos_x, pos_y = wndMgr.GetMousePosition()

		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(11 * arglen)
		self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.toolTip.AppendTextLine(str(arg), 0xffffff00)
		self.toolTip.Show()
		self.ShowToolTip = True

	def OverOutToolTip(self):
		self.toolTip.Hide()
		self.ShowToolTip = False

	def ToolTipProgress(self):
		if self.ShowToolTip:
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)

	def OnPressExitKey(self):
		self.stream.SetLoginPhase()
		self.Hide()
		return True

class ReselectEmpireWindow(SelectEmpireWindow):
	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetCreateCharacterPhase()
		self.Hide()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()
		self.Hide()
