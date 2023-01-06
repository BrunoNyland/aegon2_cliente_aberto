#favor manter essa linha
import _net as net
import _app as app
import ui
import constinfo

class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)

		self.stream = stream
		self.progress = 0

	def __del__(self):
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOAD, self)
		ui.Window.__del__(self)

	def Open(self):
		chrSlot = self.stream.GetCharacterSlot()
		net.SendSelectCharacterPacket(chrSlot)

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/loadingwindow.py")

		self.GetChild("FullGage").SetPercentage(0, 100)
		self.GetChild("LoadingPercent_Text").SetText("0%")

		self.Show()
		app.SetFrameSkip(0)

	def Close(self):
		self.stream = None
		app.SetFrameSkip(1)
		self.Hide()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		app.SetFrameSkip(1)
		self.stream.SetLoginPhase()
		return True

	def __SetProgress(self, p):
		self.progress = p
		self.GetChild("LoadingPercent_Text").SetText(str(p)+"%")
		self.GetChild("FullGage").SetPercentage(p, 100)

	def UpdadeCoins(coins):
		constinfo.coins = coins

	def OnUpdate(self):
		if self.progress < 100:
			self.__SetProgress(min(self.progress + 3, 100))