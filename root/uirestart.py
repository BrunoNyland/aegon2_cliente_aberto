#favor manter essa linha
import _dbg as dbg
import _app as app
import _net as net
import _player as player
import _chat as chat
import ui
import _grp as grp

class RestartDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.AutoRestartTownTime = 0
		self.RestartHereTime = 0
		self.RestartTownTime = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/restartdialog.py")
		self.restartHereButton = self.GetChild("restart_here_button")
		self.restartTownButton = self.GetChild("restart_town_button")
		self.restartHereButton.SetEvent(self.RestartHere)
		self.restartTownButton.SetEvent(self.RestartTown)

	def Destroy(self):
		self.Hide()

		self.restartHereButton = 0
		self.restartTownButton = 0
		self.AutoRestartTownTime = 0
		self.RestartHereTime = 0
		self.RestartTownTime = 0
		self.ClearDictionary()

	def OpenDialog(self, times):
		chat.AppendChat(2, str(times))
		self.RestartHereTime = app.GetGlobalTimeStamp() + times[player.REVIVE_TYPE_HERE]
		self.RestartTownTime = app.GetGlobalTimeStamp() + times[player.REVIVE_TYPE_TOWN]
		self.AutoRestartTownTime = app.GetGlobalTimeStamp() + times[player.REVIVE_TYPE_AUTO_TOWN]
		self.Show()

	def OnUpdate(self):
		self.UpdateButtonRestartHere(int(self.RestartHereTime))
		self.UpdateButtonRestartTown(int(self.RestartTownTime))
		self.UpdateAutoRestartTownDesc(int(self.AutoRestartTownTime))

	def Close(self):
		self.Hide()
		return True

	def RestartHere(self):
		net.SendChatPacket("/restart_here")

	def RestartTown(self):
		net.SendChatPacket("/restart_town")

	def UpdateButtonRestartHere(self, time):
		left = time - app.GetGlobalTimeStamp()

		if left < 0:
			return

		if left < 1:
			self.restartHereButton.SetText("Reviver Agora")
			self.restartHereButton.Enable()
		else:
			self.restartHereButton.SetText("Liberado em %s segundos" % self.SecondsFormat(left))
			self.restartHereButton.Disable()

	def UpdateButtonRestartTown(self, time):
		left = time - app.GetGlobalTimeStamp()

		if left < 0:
			return

		if left < 1:
			self.restartTownButton.SetText("Retornar ao Início")
			self.restartTownButton.Enable()
		else:
			self.restartTownButton.SetText("Liberado em %s segundos" % self.SecondsFormat(left))
			self.restartTownButton.Disable()

	def UpdateAutoRestartTownDesc(self, time):
		left = time - app.GetGlobalTimeStamp()
		if left < 0:
			left = 0
		color = grp.GenerateColor(1.0 - (float(left)/1000.0)*4, 0.0 + (float(left)/1000.0)*4, 0.0, 1.0)
		self.GetChild("restart_town_desc2").SetText("%s" % self.MinuteFormat(left))
		self.GetChild("restart_town_desc2").SetPackedFontColor(color)

	def MinuteFormat(self, time):
		d, s = divmod(time, 60)
		ss, d = divmod(d, 60)
		return "%02d:%02d" % (d, s)

	def SecondsFormat(self, time):
		d, s2 = divmod(time, 60)
		ss2, d = divmod(d, 60)
		return "%d" % (s2)

	def OnPressExitKey(self):
		return True

	def OnPressEscapeKey(self):
		return True

# x=RestartDialog()
# x.LoadDialog()
# x.OpenDialog()