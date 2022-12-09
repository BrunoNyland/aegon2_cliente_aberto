#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import ui
import background

class SiegeWarScore(ui.ScriptWindow):

	maps = ["None", "Castelo Shinso", "Castelo Chunjo", "Castelo Jinno"]

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/siege_war_score.py")

	def Open(self, empire, tower, shinso, chunjo, jinno, time):
		if int(empire) == 0:
			return

		get = self.GetChild
		get("MapName").SetText(self.maps[int(empire)])
		get("Towers").SetText("Tochas rest.:" + str(tower))
		if int(time) > 0:
			get("Time").SetText("Tempo: " + str(time) + "min")
		else:
			get("Time").SetText("Tempo: Esgotado")
		if int(empire) == 1:
			get("Empire1").SetText("Chunjo: " + str(chunjo))
			get("Empire2").SetText("Jinno: " + str(jinno))
		elif int(empire) == 2:
			get("Empire1").SetText("Shinso: " + str(shinso))
			get("Empire2").SetText("Jinno: " + str(jinno))
		elif int(empire) == 3:
			get("Empire1").SetText("Shinso: " + str(shinso))
			get("Empire2").SetText("Chunjo: " + str(chunjo))

		self.Show()

class SiegeWarEnter(ui.ScriptWindow):

	names = ["None", "Shinso", "Chunjo", "Jinno"]

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/siege_war_enter.py")
		get = self.GetChild
		get("EnterButton").SetEvent(self.EnterInTheFuckingWar)

	def EnterInTheFuckingWar(self):
		net.SendChatPacket("/siege_enter")

	def Open(self, empire):
		if "metin2_map_empirewar" in background.GetCurrentMapName():
			return

		get = self.GetChild

		get("Empire").SetText("Defensor: " + self.names[int(empire)])
		self.Show()

# x = SiegeWarScoreBoard()
# x = SiegeWarEnter()
# x.Show()