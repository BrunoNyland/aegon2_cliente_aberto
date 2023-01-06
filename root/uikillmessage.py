#favor manter essa linha
import ui
import _wnd_mgr as wndMgr
import playersettingmodule

# temp = []
# def Debug(msg):
	# line = ui.MakeTextLine(None)
	# line.SetText(msg)
	# line.SetPosition(0, -260 + len(temp)*10)
	# temp.append(line)

class KillPopup(ui.ScriptWindow):

	faces = "interface/controls/common/faces/"
	RACE_ICONS = {
		playersettingmodule.RACE_WARRIOR_M		: faces + "warrior_m.tga",
		playersettingmodule.RACE_WARRIOR_W		: faces + "warrior_w.tga",
		playersettingmodule.RACE_ASSASSIN_M		: faces + "assassin_m.tga",
		playersettingmodule.RACE_ASSASSIN_W		: faces + "assassin_w.tga",
		playersettingmodule.RACE_SURA_M			: faces + "sura_m.tga",
		playersettingmodule.RACE_SURA_W			: faces + "sura_w.tga",
		playersettingmodule.RACE_SHAMAN_M		: faces + "shaman_m.tga",
		playersettingmodule.RACE_SHAMAN_W		: faces + "shaman_w.tga",
	}

	EMPIRE_ICONS = {
		1 : "d:/ymir work/ui/empire_flag/1.png",
		2 : "d:/ymir work/ui/empire_flag/2.png",
		3 : "d:/ymir work/ui/empire_flag/3.png",
	}

	def __init__(self, killer_name, killer_empire, killer_race, victim_name, victim_empire, victim_race, list):
		ui.ScriptWindow.__init__(self, "TOP_MOST")
		self.time = 0
		self.list = list
		self.list.insert(0, self)
		self.LoadDialog()
		self.Open(killer_name, killer_empire, killer_race, victim_name, victim_empire, victim_race)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/kill_message.py")
		get = self.GetChild

	def Open(self, killer_name, killer_empire, killer_race, victim_name, victim_empire, victim_race):
		get = self.GetChild

		get("message").SetText(killer_name + " matou " + victim_name)
		(width, height) = get("message").GetTextSize()
		get("board").SetSize(width + 90, 30)

		get("victim_race").LoadImage(self.RACE_ICONS[int(victim_race)])
		get("victim_race").SetScale(0.6, 0.6)
		get("victim_empire").LoadImage(self.EMPIRE_ICONS[int(victim_empire)])
		get("victim_empire").SetScale(0.7, 0.7)

		get("killer_race").LoadImage(self.RACE_ICONS[int(killer_race)])
		get("killer_race").SetScale(0.6, 0.6)
		get("killer_empire").LoadImage(self.EMPIRE_ICONS[int(killer_empire)])
		get("killer_empire").SetScale(0.7, 0.7)

		self.Show()

	def OnUpdate(self):
		self.SetPosition(20, wndMgr.GetScreenHeight() - 100 - (50 * self.list.index(self)))
		if self.time > 260:
			self.list.remove(self)
			self.Hide()

		self.time += 1