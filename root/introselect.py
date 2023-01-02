#favor manter essa linha
import enszxc3467hc3kokdueq as app
import zn94xlgo573hf8xmddzq as net
import Js4k2l7BrdasmVRt8Wem as chr
import LURMxMaKZJqliYt2QSHG as chat
import ga3vqy6jtxqi9yf344j7 as player
import grp
import wndMgr
import snd
import systemSetting
import localeinfo
import ui
import musicinfo
import uicommon
import constinfo
import os
import wait

class CharacterRenderer(ui.Window):
	zoom = 10.0
	height = 95.0

	def OnRender(self):
		grp.ClearDepthBuffer()
		grp.SetGameRenderState()
		grp.PushState()
		grp.SetOmniLight()
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()
		newScreenWidth = float(screenWidth - 270)
		newScreenHeight = float(screenHeight)
		grp.SetViewport(270.0/screenWidth, 0.0, newScreenWidth/screenWidth, newScreenHeight/screenHeight)
		app.SetCenterPosition(-5.0, 0.0, 0.0)
		app.SetCamera(1550.0, 15.0, 180.0, self.height)
		grp.SetPerspective(self.zoom, newScreenWidth/newScreenHeight, 1000.0, 3000.0)
		(x, y) = app.GetCursorPosition()
		grp.SetCursorPosition(x, y)
		chr.Deform()
		chr.Render()
		grp.RestoreViewport()
		grp.PopState()
		grp.SetInterfaceRenderState()

class SelectCharacterWindow(ui.ScriptWindow):

	SLOT_COUNT = 4
	onPressKeyDict = {}

	def __init__(self, stream):
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)
		self.stream = stream
		self.slot = self.stream.GetCharacterSlot()
		self.startIndex = -1
		self.flagDict = {}
		self.dlgBoard = 0
		self.isLoad = 0

		self.privateInputBoard = None

		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			self.HAIR_STYLE = 0
			self.SHAPE_STYLE = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)

	def Open(self):
		self.onPressKeyDict[app.DIK_1]				= lambda : self.SelectSlot(0)
		self.onPressKeyDict[app.DIK_2]				= lambda : self.SelectSlot(1)
		self.onPressKeyDict[app.DIK_3]				= lambda : self.SelectSlot(2)
		self.onPressKeyDict[app.DIK_4]				= lambda : self.SelectSlot(3)
		self.onPressKeyDict[app.DIK_NUMPAD1]		= lambda : self.SelectSlot(0)
		self.onPressKeyDict[app.DIK_NUMPAD2]		= lambda : self.SelectSlot(1)
		self.onPressKeyDict[app.DIK_NUMPAD3]		= lambda : self.SelectSlot(2)
		self.onPressKeyDict[app.DIK_NUMPAD4]		= lambda : self.SelectSlot(3)
		self.onPressKeyDict[app.DIK_SPACE]			= lambda : self.NewStartGame()
		self.onPressKeyDict[app.DIK_NUMPADCOMMA]	= lambda : self.NewStartGame()
		self.onPressKeyDict[app.DIK_COMMA]			= lambda : self.NewStartGame()
		self.onPressKeyDict[app.DIK_DELETE]			= lambda : self.InputPrivateCode()
		self.onPressKeyDict[app.DIK_A]				= lambda : self.DecreaseSlotIndex()
		self.onPressKeyDict[app.DIK_D]				= lambda : self.IncreaseSlotIndex()
		self.onPressKeyDict[app.DIK_S]				= lambda : self.DecreaseSlotIndex()
		self.onPressKeyDict[app.DIK_W]				= lambda : self.IncreaseSlotIndex()
		self.onPressKeyDict[app.DIK_LEFT]			= lambda : self.DecreaseSlotIndex()
		self.onPressKeyDict[app.DIK_RIGHT]			= lambda : self.IncreaseSlotIndex()
		self.onPressKeyDict[app.DIK_DOWN]			= lambda : self.DecreaseSlotIndex()
		self.onPressKeyDict[app.DIK_UP]				= lambda : self.IncreaseSlotIndex()
		self.onPressKeyDict[app.VK_LEFT]			= lambda : self.DecreaseSlotIndex()
		self.onPressKeyDict[app.VK_RIGHT]			= lambda : self.IncreaseSlotIndex()
		self.onPressKeyDict[app.VK_DOWN]			= lambda : self.DecreaseSlotIndex()
		self.onPressKeyDict[app.VK_UP]				= lambda : self.IncreaseSlotIndex()
		self.onPressKeyDict[app.DIK_SYSRQ]			= lambda : self.SaveScreen()

		self.__LoadBoardDialog("uiscript/selectcharacterwindow.py")

		self.InitCharacterBoard()

		self.btnStart.Enable()
		self.btnCreate.Enable()
		self.btnDelete.Enable()
		self.btnExit.Enable()
		self.dlgBoard.Show()

		self.SetWindowName("SelectCharacterWindow")
		self.Show()

		if musicinfo.selectMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("bgm/" + musicinfo.selectMusic)

		self.isLoad = 1
		self.Refresh()

		self.HideAllFlag()
		self.SetEmpire(net.GetEmpireID())
		app.ShowCursor()
		self.SetFocus()

	def Close(self):
		self.stream.popupWindow.Close()
		self.stream = None

		self.onPressKeyDict = {}

		if musicinfo.selectMusic != "":
			snd.FadeOutMusic("bgm/" + musicinfo.selectMusic)

		if self.dlgBoard:
			self.dlgBoard.ClearDictionary()

		self.empireName = None
		self.flagDict = {}
		self.dlgBoard = None
		self.btnStart = None
		self.btnExit = None
		self.btnCreate = None
		self.btnDelete = None
		self.backGround = None
		self.chrRenderer = None

		if self.privateInputBoard:
			self.privateInputBoard.Hide()
			self.privateInputBoard = None

		chr.DeleteInstance(0)
		chr.DeleteInstance(1)
		chr.DeleteInstance(2)
		chr.DeleteInstance(3)

		self.Hide()
		self.KillFocus()

		app.HideCursor()

	def NewStartGame(self):
		id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if 0 == id:
			self.CreateCharacter()
		else:
			self.StartGame()

	def SetEmpire(self, id):
		self.empireName.SetText("Reino: %s" % {1:"Shinsoo", 2:"Chunjo", 3:"Jinno"}.get(net.GetEmpireID(), "Nenhum"))
		if self.flagDict.__contains__(id):
			self.flagDict[id].Show()

	def HideAllFlag(self):
		for flag in self.flagDict.values():
			flag.Hide()

	def Refresh(self):
		if not self.isLoad:
			return

		priority = []
		for index in [3, 2, 1, 0]:
			last_playtime = 0
			if app.ENABLE_LAST_PLAY_SELECT:
				last_playtime = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_LAST_PLAYTIME)

			priority.append([last_playtime, index])

		priority.sort(reverse = True)
		self.SelectSlot(priority[0][1])

	def GetCharacterSlotID(self, slotIndex):
		return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)

	def __LoadBoardDialog(self, fileName):
		self.dlgBoard = ui.ScriptWindow()

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self.dlgBoard, fileName)

		Get = self.dlgBoard.GetChild
		self.btnStart = Get("select_button")
		self.btnCreate = Get("create_button")
		self.btnDelete = Get("delete_button")
		self.btnExit = Get("exit_button")

		self.backGround = Get("BackGround")

		self.charName = Get("name")
		self.empireName = Get("empire")

		self.flagDict[net.EMPIRE_A] = Get("EmpireFlag_A")
		self.flagDict[net.EMPIRE_B] = Get("EmpireFlag_B")
		self.flagDict[net.EMPIRE_C] = Get("EmpireFlag_C")

		self.guildName = Get("guild")
		self.level = Get("level")
		self.playTime = Get("playtime")

		self.btnLeft = Get("left_button")
		self.btnRight = Get("right_button")

		self.btnStart.SetEvent(self.StartGame)
		self.btnCreate.SetEvent(self.CreateCharacter)
		self.btnDelete.SetEvent(self.InputPrivateCode)
		self.btnExit.SetEvent(self.ExitSelect)

		self.btnLeft.SetEvent(self.DecreaseSlotIndex)
		self.btnRight.SetEvent(self.IncreaseSlotIndex)

		self.chrRenderer = CharacterRenderer()
		self.chrRenderer.SetParent(self.backGround)
		self.chrRenderer.Show()

		self.SetOnRunMouseWheelEvent(self.OnRunMouseWheel)
		self.chrRenderer.SetOnRunMouseWheelEvent(self.OnRunMouseWheel)
		self.backGround.SetOnRunMouseWheelEvent(self.OnRunMouseWheel)

		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			Get("show_hide_hair").SetEvent(self.ShowAndHideHair)
			Get("show_hide_shape").SetEvent(self.ShowAndHideShape)
			Get("select_hair_btn").SetEvent(self.OpenSelectHairPage)
			Get("hair_cancel_btn").SetEvent(self.CloseSelectHairPage)
			Get("hair_save_btn").SetEvent(self.SaveNewStyleQuestion)

			Get("select_shape_btn").SetEvent(self.OpenSelectShapePage)
			Get("shape_cancel_btn").SetEvent(self.CloseSelectShapePage)
			Get("shape_save_btn").SetEvent(self.SaveNewStyleQuestion)

	def SameLoginDisconnect(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeinfo.LOGIN_FAILURE_SAMELOGIN, self.ExitSelect, localeinfo.UI_OK)

	def MakeCharacter(self, index, id, name, race, form, hair):
		if 0 == id:
			return

		chr.CreateInstance(index)
		chr.SelectInstance(index)
		chr.SetVirtualID(index)
		chr.SetNameString(name)

		chr.SetRace(race)
		chr.SetArmor(form)
		chr.SetHair(hair)
		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		chr.SetRotation(0.0)
		chr.Show()

	def StartGame(self):
		if -1 != self.startIndex:
			return

		self.startIndex = self.slot

		if musicinfo.selectMusic != "":
			snd.FadeLimitOutMusic("bgm/" + musicinfo.selectMusic, systemSetting.GetMusicVolume() * 0.05)

		self.DisableWindow()

		self.stream.SetCharacterSlot(self.slot)

		chr.SelectInstance(self.slot)
		chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED, 0.1)

		chrSlot = self.stream.GetCharacterSlot()
		net.DirectEnter(chrSlot)
		playTime = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
		player.SetPlayTime(playTime)
		chat.Clear()

	def OnCreateFailure(self, type):
		if 0 == type:
			self.PopupMessage(localeinfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
		elif 1 == type:
			self.PopupMessage(localeinfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
		elif 100 == type:
			self.PopupMessage(localeinfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)
		elif 101 == type:
			self.PopupMessage("Você precisa escolher novos visuais.")
		elif 102 == type:
			self.PopupMessage("Não foi possível alterar o visual.")

	def CreateCharacter(self):
		if 0 == self.GetCharacterSlotID(self.slot):
			self.stream.SetCharacterSlot(self.slot)

			if self.__AreAllSlotEmpty():
				self.stream.SetReselectEmpirePhase()
			else:
				self.stream.SetCreateCharacterPhase()

	def __AreAllSlotEmpty(self):
		for iSlot in range(self.SLOT_COUNT):
			if 0 != net.GetAccountCharacterSlotDataInteger(iSlot, net.ACCOUNT_CHARACTER_SLOT_ID):
				return 0
		return 1

	def ExitSelect(self):
		self.Hide()
		self.stream.SetLoginPhase()

	def SelectSlot(self, index):
		if index < 0:
			return

		if index >= self.SLOT_COUNT:
			return

		self.slot = index

		for i in range(self.SLOT_COUNT):
			chr.DeleteInstance(i)

		chr.SelectInstance(self.slot)

		id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if 0 != id:
			self.btnStart.Show()
			self.btnDelete.Show()
			self.btnCreate.Hide()

			name = net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_NAME)
			level = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			playTime = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			hth = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HTH)
			int = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_INT)
			str = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_STR)
			dex = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_DEX)
			race = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
			form = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_FORM)
			hair = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_HAIR)

			if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
				main_hair = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_BASE_PART_HAIR)
				main_style = net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_BASE_PART)
				Get = self.dlgBoard.GetChild

				if main_hair == hair:
					Get("show_hide_hair").Empty()
					Get("show_hide_hair").Disable()
				else:
					Get("show_hide_hair").Fill()
					Get("show_hide_hair").Enable()

				if main_style == form:
					Get("show_hide_shape").Empty()
					Get("show_hide_shape").Disable()
				else:
					Get("show_hide_shape").Fill()
					Get("show_hide_shape").Enable()

				self.HAIR_STYLE = main_hair
				self.SHAPE_STYLE = main_style

			self.MakeCharacter(index, id, name, race, form, hair)

			app.SetWindowTitle("%s - Level: %d -  %s" % (name, level, localeinfo.APP_TITLE))
			constinfo.APP_TITLE_NEW = "%s - Level: %d -  %s" % (name, level, localeinfo.APP_TITLE)

			self.charName.SetText("%s" % name)
			self.empireName.SetText("Reino: %s" % {1:"Shinsoo", 2:"Chunjo", 3:"Jinno"}.get(net.GetEmpireID(), "Nenhum"))

			if net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME):
				self.guildName.SetText("Guild: " + net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME))
			else:
				self.guildName.SetText("Guild: " + localeinfo.SELECT_NOT_JOIN_GUILD)

			self.level.SetText("%d" % level)
			self.playTime.SetText(localeinfo.SecondToDHM(playTime * 60))
		else:
			app.SetWindowTitle(localeinfo.APP_TITLE)
			self.InitCharacterBoard()

	def InitCharacterBoard(self):
		self.btnStart.Hide()
		self.btnDelete.Hide()
		self.btnCreate.Show()
		self.charName.SetText("")
		self.empireName.SetText("")
		self.guildName.SetText("")
		self.level.SetText("")
		self.playTime.SetText("")

		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			Get = self.dlgBoard.GetChild

			Get("show_hide_hair").Empty()
			Get("show_hide_hair").Disable()
			Get("show_hide_shape").Empty()
			Get("show_hide_shape").Disable()

	def OnRunMouseWheel(self, nLen):
		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			Get = self.dlgBoard.GetChild
			if Get("board_hair").IsShow():
				return
			if Get("board_shape").IsShow():
				if nLen > 0:
					chr.ChangeShape(0)
					self.SetMotionGeneral()
				else:
					chr.ChangeShape(1)
					self.SetMotionGeneral()
				return

		if self.privateInputBoard:
			if self.privateInputBoard.IsShow():
				return

		if nLen > 0:
			self.IncreaseSlotIndex()
		else:
			self.DecreaseSlotIndex()

	def DecreaseSlotIndex(self):
		if self.startIndex == -1:
			slotIndex = (self.slot - 1 + self.SLOT_COUNT) % self.SLOT_COUNT
			self.SelectSlot(slotIndex)

	def IncreaseSlotIndex(self):
		if self.startIndex == -1:
			slotIndex = (self.slot + 1) % self.SLOT_COUNT
			self.SelectSlot(slotIndex)

	def OnUpdate(self):
		chr.Update()

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func = 0):
		if not func:
			func = self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeinfo.UI_OK)

	def OnPressExitKey(self):
		self.ExitSelect()
		return True

	def OnKeyDown(self, key):
		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			Get = self.dlgBoard.GetChild
			if not Get("board").IsShow() and key != app.DIK_SYSRQ:
				return

		if self.privateInputBoard:
			if self.privateInputBoard.IsShow():
				return

		try:
			self.onPressKeyDict[key]()
		except BaseException:
			pass

		return True

	def OnPressEscapeKey(self):
		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			Get = self.dlgBoard.GetChild
			if Get("board_shape").IsShow():
				self.CloseSelectShapePage()
				return
			if Get("board_hair").IsShow():
				self.CloseSelectHairPage()
				return

		self.ExitSelect()
		return True

	def OnIMEReturn(self):
		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			Get = self.dlgBoard.GetChild
			if Get("board_shape").IsShow():
				return
			if Get("board_hair").IsShow():
				return

		self.NewStartGame()
		return True

	def SaveScreen(self):
		if not os.path.exists(os.getcwd() + os.sep + "screenshot"):
			os.mkdir(os.getcwd() + os.sep + "screenshot")

		(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd() + os.sep + "screenshot" + os.sep)

	def DisableWindow(self):
		self.btnStart.Disable()
		self.btnCreate.Disable()
		self.btnExit.Disable()
		self.btnDelete.Disable()
		self.btnLeft.Disable()
		self.btnRight.Disable()

		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			Get = self.dlgBoard.GetChild

			Get("select_hair_btn").Disable()
			Get("select_shape_btn").Disable()
			Get("show_hide_hair").Disable()
			Get("show_hide_shape").Disable()

	def EnableWindow(self):
		self.btnStart.Enable()
		self.btnCreate.Enable()
		self.btnExit.Enable()
		self.btnDelete.Enable()
		self.btnLeft.Enable()
		self.btnRight.Enable()

		if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
			form = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_FORM)
			main_style = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART)

			hair = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			main_hair = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART_HAIR)

			Get = self.dlgBoard.GetChild

			Get("select_hair_btn").Enable()
			Get("select_shape_btn").Enable()

			if main_hair == hair:
				Get("show_hide_hair").Fill()
				Get("show_hide_hair").Disable()
			else:
				Get("show_hide_hair").Empty()
				Get("show_hide_hair").Enable()

			if main_style == form:
				Get("show_hide_shape").Fill()
				Get("show_hide_shape").Disable()
			else:
				Get("show_hide_shape").Empty()
				Get("show_hide_shape").Enable()

	#########################################################################################
	## DELETAR PERSONAGEM ## DELETAR PERSONAGEM ## DELETAR PERSONAGEM ## DELETAR PERSONAGEM #
	#########################################################################################
	def InputPrivateCode(self):
		if not self.GetCharacterSlotID(self.slot):
			return

		privateInputBoard = uicommon.InputDialogWithDescription()
		privateInputBoard.SetTitle(localeinfo.INPUT_PRIVATE_CODE_DIALOG_TITLE)
		privateInputBoard.SetAcceptEvent(self.AcceptInputPrivateCode)
		privateInputBoard.SetCancelEvent(self.CancelInputPrivateCode)

		privateInputBoard.SetNumberMode()
		privateInputBoard.SetSecretMode()
		privateInputBoard.SetMaxLength(7)

		# privateInputBoard.SetBoardWidth(250)
		privateInputBoard.SetDescription(localeinfo.INPUT_PRIVATE_CODE_DIALOG_DESCRIPTION)
		privateInputBoard.Open()
		self.privateInputBoard = privateInputBoard

		self.DisableWindow()

		chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED, 0.1)

	def AcceptInputPrivateCode(self):
		privateCode = self.privateInputBoard.GetText()
		if not privateCode:
			return

		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			self.PopupMessage(localeinfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(self.slot, privateCode)
		self.PopupMessage(localeinfo.SELECT_DELEING)

		self.CancelInputPrivateCode()
		return True

	def CancelInputPrivateCode(self):
		self.privateInputBoard.Hide()
		self.privateInputBoard = None
		self.EnableWindow()
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
		return True

	def OnDeleteSuccess(self, slot):
		self.PopupMessage(localeinfo.SELECT_DELETED)
		self.DeleteCharacter(slot)

	def OnDeleteFailure(self, num):
		self.PopupMessage(localeinfo.SELECT_CAN_NOT_DELETE)

	def DeleteCharacter(self, index):
		chr.DeleteInstance(index)
		self.SelectSlot(self.slot)

	#########################################################################################
	## SELECIONAR CABELO E CORPO ## SELECIONAR CABELO E CORPO ## SELECIONAR CABELO E CORPO ##
	#########################################################################################
	if app.ENABLE_ON_CREATE_SELECT_HAIR_SHAPE:
		hair_index_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47]

		hair_color_list = {
			1 : [0, 12, 24, 36],
			2 : [1, 13, 25, 37],
			3 : [2, 14, 26, 38],
			4 : [3, 15, 27, 39],
			5 : [4, 16, 28, 40],
			6 : [5, 17, 29, 41],
			7 : [6, 18, 30, 42],
			8 : [7, 19, 31, 43],
			9 : [8, 20, 32, 44],
			10 : [9, 21, 33, 45],
			11 : [10, 22, 34, 46],
			12 : [11, 23, 35, 47],
		}

		hair_icon_folder = {
			0 : "interface/controls/special/select/hair/warrior_m/",
			1 : "interface/controls/special/select/hair/ninja_w/",
			2 : "interface/controls/special/select/hair/shura_m/",
			3 : "interface/controls/special/select/hair/shaman_w/",
			4 : "interface/controls/special/select/hair/warrior_w/",
			5 : "interface/controls/special/select/hair/ninja_m/",
			6 : "interface/controls/special/select/hair/shura_w/",
			7 : "interface/controls/special/select/hair/shaman_m/",
		}

		shape_icon_folder = {
			0 : "interface/controls/special/select/shape/warrior_m/",
			1 : "interface/controls/special/select/shape/ninja_w/",
			2 : "interface/controls/special/select/shape/shura_m/",
			3 : "interface/controls/special/select/shape/shaman_w/",
			4 : "interface/controls/special/select/shape/warrior_w/",
			5 : "interface/controls/special/select/shape/ninja_m/",
			6 : "interface/controls/special/select/shape/shura_w/",
			7 : "interface/controls/special/select/shape/shaman_m/",
		}

		shape_pos_x = {
			0 : 3,
			1 : -4,
			2 : 9,
			3 : 1,
			4 : -1,
			5 : 0,
			6 : 6,
			7 : 4,
		}

		zoom_list = {
			0 : [3.3, 140.0,],
			1 : [3.1, 140.0,],
			2 : [3.3, 160.0,],
			3 : [3.1, 145.0,],
			4 : [3.1, 145.0,],
			5 : [3.1, 155.0,],
			6 : [3.1, 145.0,],
			7 : [3.2, 155.0,],
		}

		def OpenSelectShapePage(self):
			Get = self.dlgBoard.GetChild
			Get("board").Hide()
			Get("board_shape").Show()

			race = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
			hair = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			main_style = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART)
			style = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_FORM)

			self.chrRenderer.zoom = 8.0
			self.chrRenderer.height = 90.0

			chr.ChangeShape(main_style)
			self.SetMotionGeneral()

			for x in [0, 1]:
				Get("shape_image_" + str(x)).LoadImage(self.shape_icon_folder[race] + "0" + str(x) + ".png")
				Get("shape_image_" + str(x)).SetPosition(self.shape_pos_x[race], -10)
				Get("shape_btn_" + str(x)).SetEvent(self.SelectShape, x)


		def CloseSelectShapePage(self, delay = 0.0):
			Get = self.dlgBoard.GetChild

			if not Get("board_shape").IsShow():
				return

			Get("board_shape").Hide()
			Get("board").Show()

			self.chrRenderer.zoom = 10.0
			self.chrRenderer.height = 95.0

			self.time = wait.WaitingDialog()
			self.time.Open(delay)
			self.time.SetTimeOverEvent(self.SetMotionGeneral)

			main_style = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART)
			style = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_FORM)

			if delay == 0.0:
				chr.ChangeShape(style)
				self.SHAPE_STYLE = main_style
				if not main_style == style:
					Get("show_hide_shape").Fill()
			else:
				Get("show_hide_shape").Empty()


		def OpenSelectHairPage(self):
			Get = self.dlgBoard.GetChild
			Get("board").Hide()
			Get("board_hair").Show()

			race = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
			hair = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HAIR)

			self.chrRenderer.zoom = self.zoom_list[race][0]
			self.chrRenderer.height = self.zoom_list[race][1]

			if hair in self.hair_index_list:
				hair_color = hair % 12
			else:
				hair_color = 0

			for x in [0, 1, 2, 3]:
				Get("hair_image_" + str(x)).LoadImage(self.hair_icon_folder[race] + str(self.hair_color_list[1][x] + 1) + ".png")
				Get("hair_btn_" + str(x)).SetEvent(self.SelectHair, self.hair_color_list[1][x])

			for color in range(1, 13):
				Get("hair_color_btn_" + str(color)).SetEvent(self.SelectHairColor, color)

			chr.SetLoopMotion(chr.MOTION_MODE_GENERAL)

		def SelectHairColor(self, color_number):
			if not self.hair_color_list.__contains__(color_number):
				return

			Get = self.dlgBoard.GetChild
			race = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)

			for x in [0, 1, 2, 3]:
				Get("hair_image_" + str(x)).LoadImage(self.hair_icon_folder[race] + str(self.hair_color_list[color_number][x] + 1) + ".png")
				Get("hair_btn_" + str(x)).SetEvent(self.SelectHair, self.hair_color_list[color_number][x])

			self.SelectHair((self.HAIR_STYLE / 12) * 12 + color_number -1)

		def CloseSelectHairPage(self, delay = 0.0):
			Get = self.dlgBoard.GetChild

			if not Get("board_hair").IsShow():
				return

			Get("board_hair").Hide()
			Get("board").Show()

			self.chrRenderer.zoom = 10.0
			self.chrRenderer.height = 95.0

			self.time = wait.WaitingDialog()
			self.time.Open(delay)
			self.time.SetTimeOverEvent(self.SetMotionGeneral)

			if delay == 0.0:
				if Get("show_hide_hair").GetStatus():
					chr.ChangeHair(net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HAIR))
					self.HAIR_STYLE = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART_HAIR)
				else:
					chr.ChangeHair(net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART_HAIR))
					self.HAIR_STYLE = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART_HAIR)
			else:
				chr.ChangeHair(net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART_HAIR))
				Get("show_hide_hair").Empty()

		def SetMotionGeneral(self):
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
			self.time = None

		def SelectHair(self, num):
			chr.ChangeHair(int(num))
			self.HAIR_STYLE = num

		def ShowAndHideHair(self):
			Get = self.dlgBoard.GetChild

			if Get("show_hide_hair").GetStatus():
				chr.ChangeHair(net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART_HAIR))
				Get("show_hide_hair").Empty()
			else:
				chr.ChangeHair(net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HAIR))
				Get("show_hide_hair").Fill()

		def SelectShape(self, num):
			self.SHAPE_STYLE = num
			chr.ChangeShape(self.SHAPE_STYLE)
			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
			chr.SetRotation(0.0)

		def ShowAndHideShape(self):
			Get = self.dlgBoard.GetChild

			if Get("show_hide_shape").GetStatus():
				chr.ChangeShape(net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_BASE_PART))
				Get("show_hide_shape").Empty()
			else:
				chr.ChangeShape(net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_FORM))
				Get("show_hide_shape").Fill()

			chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
			chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
			chr.SetRotation(0.0)

		def SaveNewStyleQuestion(self):
			SaveBoard = uicommon.QuestionDialog()
			SaveBoard.SetText("Deseja realmente alterar o visual?")
			SaveBoard.SetAcceptEvent(self.AcceptStyleChange)
			SaveBoard.SetCancelEvent(self.CancelStyleChange)
			SaveBoard.Open()
			self.SaveBoard = SaveBoard

		def AcceptStyleChange(self):
			pid = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
			if not pid:
				self.PopupMessage(localeinfo.SELECT_EMPTY_SLOT)
				return

			chr.PushOnceMotion(chr.MOTION_SELFIE, 0.1)

			self.PopupMessage("Alterando o visual...")
			net.SendChangeHairShapePacket(self.slot, int(self.HAIR_STYLE), int(self.SHAPE_STYLE))

			self.SaveBoard.Hide()
			self.SaveBoard = None
			self.CloseSelectHairPage(2.0)
			self.CloseSelectShapePage(2.0)
			return True

		def CancelStyleChange(self):
			self.SaveBoard.Hide()
			self.SaveBoard = None
			self.CloseSelectHairPage()
			self.CloseSelectShapePage()
			return True

		def OnChangeHairShape(self, slot, hair, shape):
			self.PopupMessage("O visual foi alterado.")
