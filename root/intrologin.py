#favor manter essa linha
import _app as app
import _net as net
import _skill as skill
import playersettingmodule
import emotion
import ui
import _snd as snd
import _wnd_mgr as wndMgr
import musicinfo
import _settings as systemSetting
import localeinfo
import _ime as ime
import os
import time
import binascii
import winreg
import constinfo
import _load_files

import _dbg as dbg
# dbg.TraceError(f'{ime.GetCodePage()}')

REG_PATH = r"SOFTWARE\KEYSTORAGE"

LOGIN_DELAY_SEC = 20.0
LOAD_DATA = 0
ALLOW_LOGIN = 0

def GetServerInfo(name):
	# info = {"IP":"189.127.164.174", "CH1":30011, "AUTH":30001}
	info = {"IP":"192.168.56.101", "CH1":30011, "AUTH":30001}
	return info[name]

def GetLoginDelay():
	global LOGIN_DELAY_SEC
	return LOGIN_DELAY_SEC

def IsLoginDelay():
	global LOGIN_DELAY_SEC
	if LOGIN_DELAY_SEC > 0.0:
		return True
	else:
		return False

class ConnectingDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

		self.eventTimeOver = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "uiscript/connectingdialog.py")

		self.message = self.GetChild("message")
		self.countdownMessage = self.GetChild("countdown_message")

	def Open(self, waitTime):
		curTime = time.time()
		self.endTime = curTime + waitTime
		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.GetChild("message").SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.GetChild("countdown_message").SetText("%d%s" % (waitTime, localeinfo.SECOND))

	def SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.time())
		if 0 == lastTime:
			self.Close()
			if self.eventTimeOver:
				self.eventTimeOver()
		else:
			self.SetCountDownMessage(self.endTime - time.time())

class LoginWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

		self.stream = stream
		self.connectingDialog = None
		self.isNowCountDown = False

		self.onEditFuncDict = []
		self.onDelFuncDict = []
		self.dictAccountButtons = []

	def __del__(self):
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		self.loginFailureMsgDict = {
			"ALREADY"	: localeinfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeinfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeinfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeinfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeinfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeinfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeinfo.LOGIN_FAILURE_BLOCK_ID,
			"BESAMEKEY"	: localeinfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeinfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeinfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeinfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeinfo.LOGIN_FAILURE_WEB_BLOCK,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		self.__LoadScript("uiscript/loginwindow.py")

		if musicinfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("bgm/" + musicinfo.loginMusic)

		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		self.SetChannel("CH1")
		self.idEditLine.SetText("")
		self.idEditLine.SetFocus()

		app.SetWindowTitle(localeinfo.APP_TITLE)
		self.Show()
		app.ShowCursor()

		global LOAD_DATA
		if LOAD_DATA == 0:
			_load_files.Load()
			skill.LoadSkillData()
			playersettingmodule.LoadGameNPC()
			emotion.RegisterEmotionIcons()
			LOAD_DATA = 1

	def __LoadScript(self, fileName):
		ui.PythonScriptLoader().LoadScriptFile(self, fileName)

		self.loginBoard = self.GetChild("LoginBoard")
		self.loginButton = self.GetChild("LoginButton")
		self.loginExitButton = self.GetChild("LoginExitButton")
		self.idEditLine = self.GetChild("ID_EditLine")
		self.pwdEditLine = self.GetChild("Password_EditLine")

		self.loginButton.SetEvent(self.__OnClickLoginButton)
		self.loginExitButton.SetEvent(self.QuitGame)

		self.idEditLine.SetTabEvent(self.pwdEditLine.SetFocus)
		self.idEditLine.SetReturnEvent(self.pwdEditLine.SetFocus)
		self.pwdEditLine.SetReturnEvent(self.__OnClickLoginButton)
		self.pwdEditLine.SetTabEvent(self.idEditLine.SetFocus)

		# self.GetChild("button_website").SetEvent(self.OpenLink, "https://aegon2.com/")

		self.MakeConfigInterface()
		self.MakeAutoLoginInterface()

	def MakeConfigInterface(self):
		get = self.GetChild
		get("btn_config").SetEvent(self.OnClickButtonConfig)

	def OnClickButtonConfig(self):
		get = self.GetChild
		if get("board_config").IsShow():
			get("board_config").Hide()
		else:
			get("board_config").Show()

	def SelectLoginBackground(self, img):
		img_list = [
			{
				'img':'interface/controls/special/loading/1.jpg',
				'w':1665.0,
			},
			{
				'img':'interface/controls/special/loading/2.jpg',
				'w':988.0,
			},
			{
				'img':'interface/controls/special/loading/3.jpg',
				'w':1080.0,
			},
		]

		self.GetChild('bg').LoadImage(img_list[img])
		self.GetChild('bg').SetScale(wndMgr.GetScreenHeight()/img_list[img], wndMgr.GetScreenHeight()/img_list[img])
		self.GetChild('bg').Show()

	def SelectInterface(self, arg):
		constinfo.NEW_INTERFACE = arg

	def SelectTaskbar(self, arg):
		constinfo.NEW_TASKBAR = arg

	def QuitGame(self):
		app.Exit()

	def Close(self):
		if self.stream.popupWindow:
			self.stream.popupWindow.Close()

		self.stream = None

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		if musicinfo.loginMusic != "" and musicinfo.selectMusic != "":
			snd.FadeOutMusic("bgm/"+musicinfo.loginMusic)

		self.idEditLine.SetTabEvent(None)
		self.idEditLine.SetReturnEvent(None)
		self.pwdEditLine.SetReturnEvent(None)
		self.pwdEditLine.SetTabEvent(None)

		self.idEditLine = None
		self.pwdEditLine = None

		self.loginFailureMsgDict = {}

		self.onEditFuncDict = []
		self.onDelFuncDict = []
		self.dictAccountButtons = []

		self.Hide()
		app.HideCursor()
		ime.ClearExceptKey()

	def OnEndCountDown(self):
		self.isNowCountDown = False
		self.OnConnectFailure()

	def OnConnectFailure(self):
		if self.isNowCountDown:
			return

		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		snd.PlaySound("sound/ui/loginfail.wav")
		self.PopupNotifyMessage(localeinfo.LOGIN_CONNECT_FAILURE, 0)

	def OnHandShake(self):
		if not IsLoginDelay():
			snd.PlaySound("sound/ui/loginok.wav")
			self.PopupNotifyMessage(localeinfo.LOGIN_CONNECT_SUCCESS, 0)

	def OnLoginStart(self):
		if not IsLoginDelay():
			self.PopupDisplayMessage(localeinfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		if self.connectingDialog:
			self.connectingDialog.Close()
		self.connectingDialog = None

		if self.loginFailureMsgDict.__contains__(error):
			loginFailureMsg = self.loginFailureMsgDict[error]
		else:
			loginFailureMsg = localeinfo.LOGIN_FAILURE_UNKNOWN + error

		self.PopupNotifyMessage(loginFailureMsg, 0)
		snd.PlaySound("sound/ui/loginfail.wav")

	def OpenLink(self, link):
		os.system("start " + link)

	def SetChannel(self, ch):
		self.stream.SetConnectInfo(GetServerInfo("IP"), GetServerInfo(ch), GetServerInfo("IP"), GetServerInfo("AUTH"))
		net.SetMarkServer(GetServerInfo("IP"), GetServerInfo("CH1"))
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")

	def AllowLogin(self):
		global ALLOW_LOGIN
		ALLOW_LOGIN = 1

	def Connect(self, id, pwd):
		global ALLOW_LOGIN
		if ALLOW_LOGIN == 0:
			return

		if IsLoginDelay():
			loginDelay = GetLoginDelay()
			self.connectingDialog = ConnectingDialog()
			self.connectingDialog.Open(loginDelay)
			self.connectingDialog.SetTimeOverEvent(self.OnEndCountDown)
			# self.connectingDialog.SetExitEvent(self.OnPressExitKey)
			self.isNowCountDown = True
		else:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeinfo.LOGIN_CONNETING, 0, localeinfo.UI_CANCEL)

		self.stream.SetLoginInfo(id, pwd)
		self.stream.Connect()

	def PopupDisplayMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0)

	def PopupNotifyMessage(self, msg, func = 0):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeinfo.UI_OK)

	def OnPressExitKey(self):
		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
		return True

	def EmptyFunc(self):
		pass

	def __OnClickLoginButton(self):
		id = self.idEditLine.GetText()
		pwd = self.pwdEditLine.GetText()
		if len(id) < 2:
			self.PopupNotifyMessage("Contas devem possuir pelo menos 2 (dois) caracteres.")
			self.idEditLine.SetText("")
			self.idEditLine.SetFocus()
			return
		if len(pwd) < 6:
			self.PopupNotifyMessage("Senhas devem ter pelo menos 6 (seis) caracteres.")
			self.pwdEditLine.SetText("")
			self.pwdEditLine.SetFocus()
			return

		self.Connect(id, pwd)

############################################################################################################
### AUTO LOGIN ###### AUTO LOGIN ###### AUTO LOGIN ###### AUTO LOGIN ###### AUTO LOGIN ###### AUTO LOGIN ###
############################################################################################################
	dictControsl = [app.DIK_F1, app.DIK_F2, app.DIK_F3, app.DIK_F4, app.DIK_F5, app.DIK_F6, app.DIK_F7, app.DIK_F8, app.DIK_F9, app.DIK_F10, app.DIK_F11, app.DIK_F12]
	dictControslDesc = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]

	def AddLogin(self):
		if len(self.dictAccountButtons) > 12:
			return

		Get = self.GetChild
		get_reg = self.Get_WinReg
		set_reg = self.Set_WinReg

		acc = str(Get("SaveAccountID_EditLine").GetText())
		pwd = str(Get("SaveAccountPassword_EditLine").GetText())

		if len(acc) < 2:
			self.PopupNotifyMessage("Contas devem possuir pelo menos 2 caracteres.")
			Get("SaveAccountID_EditLine").SetText("")
			Get("SaveAccountID_EditLine").SetFocus()
			return

		if len(pwd) < 6:
			self.PopupNotifyMessage("Senhas devem ter pelo menos 6 caracteres.")
			Get("SaveAccountPassword_EditLine").SetText("")
			Get("SaveAccountPassword_EditLine").SetFocus()
			return

		for index in range(0, 12):
			if get_reg("%d_id" % index) == "" or get_reg("%d_id" % index) == None:
				set_reg("%d_id" % index, binascii.b2a_base64(bytes(acc, 'utf-8')).decode('utf-8'))
				set_reg("%d_pwd" % index, binascii.b2a_base64(bytes(pwd, 'utf-8')).decode('utf-8'))
				self.PopupNotifyMessage("Conta salva com sucesso")
				break

		self.HideSaveAccountBoard()
		self.SortLogin()

	def RemoveLogin(self, index):
		get_reg = self.Get_WinReg
		set_reg = self.Set_WinReg

		Get = self.GetChild
		Get("DeleteAccountBoard").Hide()

		if get_reg("%d_id" % index):
			set_reg("%d_id" % index, "")
			set_reg("%d_pwd" % index, "")
			self.SortLogin()

	def EditLogin(self, index):
		get_reg = self.Get_WinReg
		set_reg = self.Set_WinReg
		Get = self.GetChild

		acc = Get("EditAccountBoardID_EditLine").GetText()
		pwd = Get("EditAccountBoard_EditLine").GetText()

		if len(acc) < 2:
			self.PopupNotifyMessage("Contas devem possuir pelo menos 2 caracteres.")
			Get("EditAccountBoardID_EditLine").SetText("")
			Get("EditAccountBoardID_EditLine").SetFocus()
			return

		if len(pwd) < 6:
			self.PopupNotifyMessage("Senhas devem ter pelo menos 6 caracteres.")
			Get("EditAccountBoard_EditLine").SetText("")
			Get("EditAccountBoard_EditLine").SetFocus()
			return

		Get("EditAccountBoard").Hide()

		if get_reg("%d_id" % index):
			set_reg("%d_id" % index, str(binascii.b2a_base64(acc)))
			set_reg("%d_pwd" % index, str(binascii.b2a_base64(pwd)))
			self.PopupNotifyMessage("Conta alterada com sucesso")
			self.SortLogin()

	def SortLogin(self):
		Get = self.GetChild
		get_reg = self.Get_WinReg

		self.dictAccountButtons = []
		self.onEditFuncDict = []
		self.onDelFuncDict = []

		for index in range(0, 12):
			Get("account" + str(index)).Hide()

		i = 0
		for index in range(0, 12):
			if get_reg("%d_id" % index):
				acc = binascii.a2b_base64(get_reg("%d_id" % index)).decode('utf-8')

				Get("account" + str(i) + "_line1").SetText("Conta: " + acc)
				Get("account" + str(i) + "_line2").SetText("Tecla de Atalho: [" + self.dictControslDesc[index] + "]")

				button = Get("account" + str(i))
				button.SetMouseLeftButtonDownEvent(self.LoginBySavedAccount, index)
				button.SetMouseRightButtonDownEvent(self.ShowEditAccountsMenuBar, i)
				button.Show()

				self.dictAccountButtons.append(button)
				self.onEditFuncDict.append([self.ShowEditLoginBoard, index, acc])
				self.onDelFuncDict.append([self.ShowRemoveLoginBoard, index, acc])

				i += 1

	def ShowEditLoginBoard(self, index, account):
		Get = self.GetChild
		Get("EditAccountsMenuBar").Hide()

		Get("EditAccountBoardID_EditLine").SetText("")
		Get("EditAccountBoardID_EditLine").EditLine.KillFocus()
		Get("EditAccountBoard_EditLine").SetText("")
		Get("EditAccountBoard_EditLine").EditLine.KillFocus()

		Get("EditAccountBoard").Show()
		Get("EditAccountBoard_EditLine").SetReturnEvent(self.EditLogin, index)
		Get("EditAccountBoardSave").SetEvent(self.EditLogin, index)

	def ShowRemoveLoginBoard(self, index, account):
		Get = self.GetChild
		Get("EditAccountsMenuBar").Hide()
		Get("DeleteAccountBoard").Show()
		Get("DeleteAccountBoardAccount").SetText(account)
		Get("DeleteAccountBoardYes").SetEvent(self.RemoveLogin, index)

	def OnUpdate(self):
		Get = self.GetChild

		if ALLOW_LOGIN == 1:
			xMouse, yMouse = wndMgr.GetMousePosition()
			if xMouse < 60 and Get("SavedAccountsWindow").GetLeft() <= -2:
				Get("SavedAccountsWindow").SetLeft(Get("SavedAccountsWindow").GetLeft() + 20)
			elif xMouse > 160 and Get("SavedAccountsWindow").GetLeft() >= -160:
				Get("SavedAccountsWindow").SetLeft(Get("SavedAccountsWindow").GetLeft() - 20)
				Get("text1").SetTextLimitedNew("Adicionar Conta", Get("SavedAccountsWindow").GetWidth() - 40)

			if Get('loadind_files').GetTop() > -50:
				Get('loadind_files').SetPosition(Get('loadind_files').GetLeft(), Get('loadind_files').GetTop() - 5)
		else:
			if Get('loadind_files').GetTop() < 10:
				Get('loadind_files').SetPosition(Get('loadind_files').GetLeft(), Get('loadind_files').GetTop() + 5)

	def OnUpdataEditAccountsMenuBar(self):
		Get = self.GetChild

		if Get("EditAccountsMenuBar").IsInPosition():
			Get("EditAccountsMenuBar").Time = 0
		else:
			if Get("EditAccountsMenuBar").Time < 40:
				Get("EditAccountsMenuBar").Time += 1
			else:
				Get("EditAccountsMenuBar").Hide()

	def MakeAutoLoginInterface(self):
		Get = self.GetChild
		Get("AddAccountButton").OnUpdate = ui.__mem_func__(self.AddAccountButtonOverIn)
		Get("AddAccountButton").SetMouseLeftButtonDownEvent(self.ShowSaveAccountBoard)
		Get("plus_image").AddFlag("not_pick")

		Get("SaveAccountCancelButton").SetEvent(self.HideSaveAccountBoard)
		Get("SaveAccountBoard").SetCloseEvent(self.HideSaveAccountBoard)
		Get("SaveAccountButton").SetEvent(self.AddLogin)

		Get("SaveAccountID_EditLine").SetTabEvent(Get("SaveAccountPassword_EditLine").SetFocus)
		Get("SaveAccountID_EditLine").SetReturnEvent(Get("SaveAccountPassword_EditLine").SetFocus)
		Get("SaveAccountPassword_EditLine").SetReturnEvent(self.AddLogin)
		Get("SaveAccountPassword_EditLine").SetTabEvent(Get("SaveAccountID_EditLine").SetFocus)

		Get("EditAccountsMenuBar").OnUpdate = ui.__mem_func__(self.OnUpdataEditAccountsMenuBar)

		Get("EditAccountBoardCancel").SetEvent(Get("EditAccountBoard").Hide)
		Get("DeleteAccountBoardNo").SetEvent(Get("DeleteAccountBoard").Hide)

		Get("EditAccountBoardID_EditLine").SetTabEvent(Get("EditAccountBoard_EditLine").SetFocus)
		Get("EditAccountBoardID_EditLine").SetReturnEvent(Get("EditAccountBoard_EditLine").SetFocus)
		Get("EditAccountBoard_EditLine").SetTabEvent(Get("EditAccountBoardID_EditLine").SetFocus)

		self.SortLogin()

	def ShowEditAccountsMenuBar(self, index):
		Get = self.GetChild
		xMouse, yMouse = wndMgr.GetMousePosition()
		Get("EditAccountsMenuBar").SetPosition(xMouse, yMouse)
		Get("EditAccountsMenuBar").Time = 0
		Get("EditAccountsMenuBar").Show()

		func = self.onEditFuncDict[index]
		Get("EditAccountButton").SetMouseLeftButtonDownEvent(func[0], func[1], func[2])

		func = self.onDelFuncDict[index]
		Get("DeleteAccountButton").SetMouseLeftButtonDownEvent(func[0], func[1], func[2])

	def ShowSaveAccountBoard(self):
		self.GetChild("SaveAccountID_EditLine").EditLine.KillFocus()
		self.GetChild("SaveAccountPassword_EditLine").EditLine.KillFocus()
		self.GetChild("SaveAccountBoard").Show()

	def HideSaveAccountBoard(self):
		self.GetChild("SaveAccountBoard").Hide()
		self.GetChild("SaveAccountID_EditLine").SetText("")
		self.GetChild("SaveAccountID_EditLine").EditLine.KillFocus()
		self.GetChild("SaveAccountID_EditLine").KillFocus()
		self.GetChild("SaveAccountPassword_EditLine").SetText("")
		self.GetChild("SaveAccountPassword_EditLine").EditLine.KillFocus()
		self.GetChild("SaveAccountPassword_EditLine").KillFocus()

	def AddAccountButtonOverIn(self):
		Get = self.GetChild
		if Get("AddAccountButton").IsIn() and Get("AddAccountButton").GetWidth() < 155:
			Get("AddAccountButton").SetLeft(Get("AddAccountButton").GetLeft() - 23)
			Get("AddAccountButton").SetSize(Get("AddAccountButton").GetWidth() + 23, Get("AddAccountButton").GetHeight())
			Get("text1").SetTextLimitedNew("Adicionar Conta", Get("AddAccountButton").GetWidth() - 45)
			Get("text1").Show()
		elif Get("AddAccountButton").GetWidth() > 49 and not Get("AddAccountButton").IsIn():
			Get("AddAccountButton").SetLeft(Get("AddAccountButton").GetLeft() + 23)
			Get("AddAccountButton").SetSize(Get("AddAccountButton").GetWidth() - 23, Get("AddAccountButton").GetHeight())
			Get("text1").SetTextLimitedNew("Adicionar Conta", Get("AddAccountButton").GetWidth() - 45)

	def Set_WinReg(self, name, value):
		try:
			winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
			registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
			winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
			winreg.CloseKey(registry_key)
			return True
		except WindowsError:
			return False

	def Get_WinReg(self, name):
		try:
			registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
			value, regtype = winreg.QueryValueEx(registry_key, name)
			winreg.CloseKey(registry_key)
			return value
		except WindowsError:
			return None

	def LoginBySavedAccount(self, index):
		get_reg = self.Get_WinReg
		if not get_reg("%d_id" % index):
			return

		if get_reg("%d_id" % index) == "":
			return

		account = binascii.a2b_base64("%s" % get_reg("%d_id" % index)).decode('utf-8')
		password = binascii.a2b_base64("%s" % get_reg("%d_pwd" % index)).decode('utf-8')

		if len(account) < 2:
			self.PopupNotifyMessage("Contas devem possuir pelo menos 2 caracteres.")
			return

		if len(password) < 6:
			self.PopupNotifyMessage("Senhas devem ter pelo menos 6 caracteres.")
			return

		self.Connect(account, password)

	def OnKeyDown(self, key):
		if key in self.dictControsl:
			self.LoginBySavedAccount(self.dictControsl.index(key))
		return True