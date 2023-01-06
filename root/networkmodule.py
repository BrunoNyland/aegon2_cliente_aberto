#favor manter essa linha
import _app as app
import _net as net
import ui
import _dbg as dbg
import uiphasecurtain
import localeinfo
import game
import intrologin
import constinfo

if constinfo.DETECT_LEAKING_WINDOWS:
	import gc, os

class PopupDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.CloseEvent = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "uiscript/popupdialog.py")

	def Open(self, Message, event = 0, ButtonName = localeinfo.UI_CANCEL):
		if self.IsShow():
			self.Close()

		self.Lock()
		self.SetTop()

		if event:
			self.CloseEvent = ui.__mem_func__(event)
		else:
			self.CloseEvent = ui.__mem_func__(self.EmptyFunc)

		AcceptButton = self.GetChild("accept")
		AcceptButton.SetText(ButtonName)
		AcceptButton.SetEvent(self.Close)

		self.GetChild("message").SetText(Message)
		self.Show()

	def EmptyFunc(self):
		pass

	def Close(self):
		if False == self.IsShow():
			self.CloseEvent = 0
			return

		self.Unlock()
		self.Hide()

		if self.CloseEvent:
			self.CloseEvent()
			self.CloseEvent = 0

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class MainStream(object):
	isChrData = 0

	def __init__(self):
		net.SetHandler(self)
		net.SetTCPRecvBufferSize(1048576)
		net.SetTCPSendBufferSize(4096)

		self.id = ""
		self.pwd = ""
		self.addr = ""
		self.port = 0
		self.account_addr = 0
		self.account_port = 0
		self.slot = 0

		self.curtain = 0
		self.curPhaseWindow = 0
		self.newPhaseWindow = 0

	def Destroy(self):
		if self.curPhaseWindow:
			self.curPhaseWindow.Close()
			self.curPhaseWindow = 0

		if self.newPhaseWindow:
			self.newPhaseWindow.Close()
			self.newPhaseWindow = 0

		self.popupWindow.Destroy()
		self.popupWindow = 0

		self.curtain = 0

	def Create(self):
		self.CreatePopupDialog()

		self.curtain = uiphasecurtain.PhaseCurtain()

	def SetPhaseWindow(self, newPhaseWindow):
		if self.newPhaseWindow:
			self.__ChangePhaseWindow()

		self.newPhaseWindow = newPhaseWindow
		if self.curPhaseWindow:
			self.curtain.FadeOut(self.__ChangePhaseWindow)
		else:
			self.__ChangePhaseWindow()

	def __ChangePhaseWindow(self):
		oldPhaseWindow = self.curPhaseWindow
		newPhaseWindow = self.newPhaseWindow
		self.curPhaseWindow = 0
		self.newPhaseWindow = 0

		if constinfo.DETECT_LEAKING_WINDOWS:
			if oldPhaseWindow:
				oldPhaseWindow.Close()
			del oldPhaseWindow

			gc.collect()

			if constinfo.WINDOW_OBJ_COUNT > 0:
				dbg.LogBox("!ATTENTION! WINDOW_MEMORY_LEAK DETECTED\n LEAKING WINDOW COUNT: " + str(constinfo.WINDOW_OBJ_COUNT))

				if not os.path.isdir("memory_leak"):
					os.mkdir("memory_leak")

				leakReport = 0
				while os.path.isfile("memory_leak/window_memory_leak%i.txt" % leakReport):
					leakReport += 1

				opFile = open("memory_leak/window_memory_leak%i.txt" % leakReport, "w+")
				opRootFile = open("memory_leak/window_memory_leak_root%i.txt" % leakReport, "w+")

				for i, v in constinfo.WINDOW_OBJ_LIST.items():
					opFile.write(v.typeStr + " parent type: " + v.strParent + "\n")
					for j in v.traceBack:
						opFile.write("\t" + j + "\n")
					if v.strParent == "":
						opRootFile.write(v.typeStr + "\n")

				opRootFile.flush()
				opRootFile.close()
				opFile.flush()
				opFile.close()
		else:
			if oldPhaseWindow:
				oldPhaseWindow.Close()

		if newPhaseWindow:
			newPhaseWindow.Open()

		self.curPhaseWindow = newPhaseWindow

		if self.curPhaseWindow:
			self.curtain.FadeIn()
		else:
			app.Exit()

	def CreatePopupDialog(self):
		self.popupWindow = PopupDialog()
		self.popupWindow.LoadDialog()
		self.popupWindow.SetCenterPosition()
		self.popupWindow.Hide()

	def SetLoginPhase(self):
		net.Disconnect()
		self.SetPhaseWindow(intrologin.LoginWindow(self))

	def SetSelectEmpirePhase(self):
		import introempire
		self.SetPhaseWindow(introempire.SelectEmpireWindow(self))

	def SetReselectEmpirePhase(self):
		import introempire
		self.SetPhaseWindow(introempire.ReselectEmpireWindow(self))

	def SetSelectCharacterPhase(self):
		localeinfo.LoadLocaleData()
		import introselect
		self.popupWindow.Close()
		self.SetPhaseWindow(introselect.SelectCharacterWindow(self))

	def SetCreateCharacterPhase(self):
		import introcreate
		self.SetPhaseWindow(introcreate.CreateCharacterWindow(self))

	def SetLoadingPhase(self):
		if constinfo.DETECT_LEAKING_WINDOWS:
			constinfo.WINDOW_COUNT_OBJ = True
			# constinfo.WINDOW_OBJ_COUNT = 0
			# constinfo.WINDOW_OBJ_LIST = {}

		import introloading
		self.SetPhaseWindow(introloading.LoadingWindow(self))

	def SetGamePhase(self):
		self.popupWindow.Close()
		self.SetPhaseWindow(game.GameWindow(self))

	def Connect(self):
		net.ConnectToAccountServer(self.addr, self.port, self.account_addr, self.account_port)

	def SetConnectInfo(self, addr, port, account_addr=0, account_port=0):
		self.addr = addr
		self.port = port
		self.account_addr = account_addr
		self.account_port = account_port

	def GetConnectAddr(self):
		return self.addr

	def SetLoginInfo(self, id, pwd):
		self.id = id
		self.pwd = pwd
		net.SetLoginInfo(id, pwd)

	def SetCharacterSlot(self, slot):
		self.slot = slot

	def GetCharacterSlot(self):
		return self.slot