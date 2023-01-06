#favor manter essa linha
import _app as app
import _chr_mgr as chrmgr
import _grp as grp
import _snd as snd
import _background as background
import ui
import wait

COLOR_NAGATIVE = grp.GenerateColor(1.0, 0.0, 0.0, 0.2)
COLOR_POSITIVE = grp.GenerateColor(0.0, 1.0, 0.0, 0.2)

class Anti_Robotics_Window(ui.ScriptWindow):

	AntMacroMapList = [
		# "maps/271_mapa_pvm",
	]

	def __init__(self):
		ui.ScriptWindow.__init__(self, "TOP_MOST")
		self.__LoadScript()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadScript(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/capcha.py")

		get = self.GetChild
		self.SetMouseLeftButtonDownEvent(get("input").SetFocus)
		self.SetMouseRightButtonDownEvent(get("input").SetFocus)
		get("edit_box").SetMouseLeftButtonDownEvent(get("input").SetFocus)
		get("edit_box").SetMouseRightButtonDownEvent(get("input").SetFocus)
		get("number_box").SetMouseLeftButtonDownEvent(get("input").SetFocus)
		get("number_box").SetMouseRightButtonDownEvent(get("input").SetFocus)
		get("input").SetIMEUpdateEvent(self.OnTypeEvent)
		get("input").SetFocus()

	def OnTypeEvent(self):
		get = self.GetChild
		value = get("numbers").GetText()
		input = get("input").GetText()
		if value == input:
			chrmgr.SetBlockPlayer(0)
			self.Hide()
			snd.PlaySound("sound/ui/potion.wav")
			if self.TimeManager:
				self.TimeManager.Active()
			return

		if len(input) == 4:
			get("input").SetText("")

		i = 0
		for number in input:
			if number == value[i]:
				i += 1

		if i == len(input):
			get("input").SetPackedFontColor(COLOR_POSITIVE)
		else:
			get("input").SetPackedFontColor(COLOR_NAGATIVE)

	def Show(self):
		get = self.GetChild
		if str(background.GetCurrentMapName()) in self.AntMacroMapList:
			value = app.GetRandom(1000, 9999)
			get("numbers").SetText(str(value))
			get("input").SetText("")
			ui.ScriptWindow.Show(self)
			snd.PlaySound("sound/ui/loginfail.wav")
			chrmgr.SetBlockPlayer(1)
		else:
			chrmgr.SetBlockPlayer(0)

	def SetTimeManager(self, wnd):
		from weakref import proxy
		self.TimeManager = proxy(wnd)

	def Destroy(self):
		self.TimeManager = None
		self.Hide()

class TimeManager(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Inicializar()
		self.LoadMainForm()

	def Inicializar(self):
		self.Delay = wait.WaitingDialog()
		self.Window = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadMainForm(self):
		self.Board = ui.New_BoardWithTitleBar()
		self.Board.SetSize(200, 110)
		self.Board.SetPosition(100, 200)
		self.Board.AddFlag("movable")
		self.Board.AddFlag("float")
		self.Board.SetTitleName("AntiBot")
		self.Board.SetCloseEvent(self.__Close)
		self.Board.Hide()

	def Active(self):
		self.Delay.Open(3600.0)
		self.Delay.SetTimeOverEvent(self.ShowWindow)

	def ShowWindow(self):
		if self.Window:
			self.Window.Show()

	def SetWindow(self, wnd):
		from weakref import proxy
		self.Window = proxy(wnd)

	def __Close(self):
		self.Board.Hide()

	def Destroy(self):
		self.Window = None
		self.Hide()

# a = Anti_Robotics_Window()
# a.Show()