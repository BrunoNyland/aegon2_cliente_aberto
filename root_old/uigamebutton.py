#favor manter essa linha
import ui
import ga3vqy6jtxqi9yf344j7 as player
import zn94xlgo573hf8xmddzq as net
import localeinfo

class GameButtonWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow("uiscript/gamewindow.py")

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self, filename):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, filename)

		self.gameButtonDict = {
			"STATUS" : self.GetChild("StatusPlusButton"),
			"SKILL" : self.GetChild("SkillPlusButton"),
			"QUEST" : self.GetChild("QuestButton"),
			"EXIT_OBSERVER" : self.GetChild("ExitObserver"),
		}

		self.gameButtonDict["EXIT_OBSERVER"].SetEvent(self.__OnClickExitObserver)

		self.__HideAllGameButton()
		self.SetObserverMode(player.IsObserverMode())

		self.online = []
		for i in xrange(0, 4):
			self.online.append(ui.MakeTextRight(self, 8, 200 + 15 * i))

		return True

	def Destroy(self):
		self.Hide()
		for key in self.gameButtonDict:
			self.gameButtonDict[key].eventFunc = None
		self.gameButtonDict = {}

	def SetButtonEvent(self, name, event):
		self.gameButtonDict[name].SetEvent(event)

	def Players_online(self, all, r1, r2, r3):
		self.online[0].SetText(localeinfo.ALL_PLAYERS_ONLINE + str(all))
		self.online[1].SetText(localeinfo.YELLOWS_ONLINE + str(r1))
		self.online[2].SetText(localeinfo.REDS_ONLINE + str(r2))
		self.online[3].SetText(localeinfo.BLUES_ONLINE + str(r3))

	def CheckGameButton(self):
		if not self.IsShow():
			return

		statusPlusButton=self.gameButtonDict["STATUS"]
		skillPlusButton=self.gameButtonDict["SKILL"]

		if player.GetStatus(player.STAT) > 0:
			statusPlusButton.Show()
		else:
			statusPlusButton.Hide()

		if self.__IsSkillStat():
			skillPlusButton.Show()
		else:
			skillPlusButton.Hide()

	def __IsSkillStat(self):
		if player.GetStatus(player.SKILL_ACTIVE) > 0:
			return True

		return False

	def __OnClickExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __HideAllGameButton(self):
		for btn in self.gameButtonDict.values():
			btn.Hide()

	def SetObserverMode(self, isEnable):
		if isEnable:
			self.gameButtonDict["EXIT_OBSERVER"].Show()
		else:
			self.gameButtonDict["EXIT_OBSERVER"].Hide()

