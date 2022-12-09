#favor manter essa linha
import Js4k2l7BrdasmVRt8Wem as chr
import enszxc3467hc3kokdueq as app
import zn94xlgo573hf8xmddzq as net
import playersettingmodule
import systemSetting
import localeinfo
import musicinfo
import uitooltip
import wndMgr
import grp
import snd
import ui

MAN			= 0
WOMAN		= 1
PAGE_COUNT	= 2
SLOT_COUNT	= 5
BASE_CHR_ID	= 3

class CreateCharacterWindow(ui.Window):

	CREATE_STAT_POINT = 0

	STAT_CON = 0
	STAT_INT = 1
	STAT_STR = 2
	STAT_DEX = 3

	START_STAT = (
		[4, 3, 6, 3,],
		[3, 3, 4, 6,],
		[3, 5, 5, 3,],
		[4, 6, 3, 3,],
	)

	STAT_DESCRIPTION = {
			STAT_CON : localeinfo.STAT_TOOLTIP_CON,
			STAT_INT : localeinfo.STAT_TOOLTIP_INT,
			STAT_STR : localeinfo.STAT_TOOLTIP_STR,
			STAT_DEX : localeinfo.STAT_TOOLTIP_DEX,
	}

	class CharacterRenderer(ui.Window):
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
			app.SetCenterPosition(-35.0, 0.0, 0.0)
			app.SetCamera(1550.0, 15.0, 180.0, 95.0)
			grp.SetPerspective(10.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)
			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)
			chr.Deform()
			chr.Render()
			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()

	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, self)

		self.stream = stream

	def __del__(self):
		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, 0)
		ui.Window.__del__(self)

	def Open(self):
		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1
		self.reservingStartTime = 0

		self.gender = 0
		self.stat = [0, 0, 0, 0]
		self.slot = -1
		self.shape = 0
		self.Setar = 0
		self.Rotation = 0
		self.HAIR = 0
		self.HAIR_STYLE = 0

		dlgBoard = ui.ScriptWindow()
		pythonScriptLoader = ui.PythonScriptLoader()
		pythonScriptLoader.LoadScriptFile(dlgBoard, "uiscript/createcharacterwindow.py")

		getChild = dlgBoard.GetChild

		self.btnCreate = getChild("create_button")
		self.btnCancel = getChild("cancel_button")

		self.editCharacterName = getChild("name")

		self.genderButton = []
		self.genderButton.append(getChild("gender_man"))
		self.genderButton.append(getChild("gender_woman"))

		#CabeloCriarChar
		self.btnPrevHair = getChild("prev_button_hair")
		self.btnNextHair = getChild("next_button_hair")
		#FinalCabeloCriarChar

		#GIRAR
		self.GirarEsquerda = getChild("esquerda_char")
		self.GirarDireita = getChild("direita_char")
		#FINAL GIRAR

		## Setas
		self.imgChar = getChild("ImgChar")
		self.btnSetaEsquerda = getChild("seta_esquerda")
		self.btnSetaDireita = getChild("seta_direita")
		self.backGround = getChild("BackGround")

		#CabeloCriarChar
		self.btnPrevHair.SetEvent(self.__PrevHair)
		self.btnNextHair.SetEvent(self.__NextHair)
		#FinalCabeloCriarChar

		#GIRAR
		self.GirarEsquerda.SetEvent(self.Girar_Esquerda)
		self.GirarDireita.SetEvent(self.Girar_Direita)
		#FINAL GIRAR

		self.btnCreate.SetEvent(self.CreateCharacter)
		self.btnCancel.SetEvent(self.CancelCreate)

		self.genderButton[0].SetEvent(self.__SelectGender, MAN)
		self.genderButton[1].SetEvent(self.__SelectGender, WOMAN)

		self.editCharacterName.SetText("")
		self.editCharacterName.SetReturnEvent(self.CreateCharacter)
		self.editCharacterName.SetEscapeEvent(self.CancelCreate)

		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.backGround)
		self.chrRenderer.Show()

		self.dlgBoard = dlgBoard

		self.characters = {
			0 : [playersettingmodule.RACE_WARRIOR_M, playersettingmodule.RACE_ASSASSIN_M, playersettingmodule.RACE_SURA_M, playersettingmodule.RACE_SHAMAN_M],
			1 : [playersettingmodule.RACE_WARRIOR_W, playersettingmodule.RACE_ASSASSIN_W, playersettingmodule.RACE_SURA_W, playersettingmodule.RACE_SHAMAN_W]}


		self.btnSetaEsquerda.SetEvent(self.__SelectSetaEsquerda)
		self.btnSetaDireita.SetEvent(self.__SelectSetaDireita)

		self.EnableWindow()
		self.__SelectSlot(0)

		self.toolTip = uitooltip.ToolTip()
		self.toolTip.ClearToolTip()

		self.curGauge = [0.0, 0.0, 0.0, 0.0]
		self.destGauge = [0.0, 0.0, 0.0, 0.0]

		app.SetCamera(500.0, 10.0, 180.0, 95.0)

		self.__SelectGender(0)
		self.__SelectShape(1)

		self.Show()
		self.dlgBoard.Show()

		if musicinfo.createMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("bgm/"+musicinfo.createMusic)

		app.ShowCursor()

	def __SelectSetaEsquerda(self):
		if self.Setar == 1:
			self.Setar = self.Setar - 1
			self.__SelectSlot(0)
		elif self.Setar == 2:
			self.Setar = self.Setar - 1
			self.__SelectSlot(1)
		elif self.Setar == 3:
			self.Setar = self.Setar - 1
			self.__SelectSlot(2)
		else:
			self.Setar = self.Setar + 3
			self.__SelectSlot(3)

	def __SelectSetaDireita(self):
		if self.Setar == 0:
			self.Setar = self.Setar + 1
			self.__SelectSlot(1)
		elif self.Setar == 1:
			self.Setar = self.Setar + 1
			self.__SelectSlot(2)
		elif self.Setar == 2:
			self.Setar = self.Setar + 1
			self.__SelectSlot(3)
		else:
			self.Setar = self.Setar - 3
			self.__SelectSlot(0)

	def Close(self):
		self.stream = None

		if musicinfo.createMusic != "":
			snd.FadeOutMusic("bgm/"+musicinfo.createMusic)

		for id in xrange(BASE_CHR_ID + SLOT_COUNT * PAGE_COUNT):
			chr.DeleteInstance(id)

		self.btnCancel = 0
		self.dlgBoard.Hide()
		self.Hide()

		app.HideCursor()

	def __PrevHair(self):
		if self.HAIR == 0 and self.HAIR_STYLE == 0:
			self.HAIR = self.HAIR + 17
			self.HAIR_STYLE = self.HAIR_STYLE + 44

		elif self.HAIR == 14 and self.HAIR_STYLE == 41:
			self.HAIR = self.HAIR - 1
			self.HAIR_STYLE = self.HAIR_STYLE - 7

		elif self.HAIR == 10 and self.HAIR_STYLE == 31:
			self.HAIR = self.HAIR - 1
			self.HAIR_STYLE = self.HAIR_STYLE - 7

		elif self.HAIR == 6 and self.HAIR_STYLE == 21:
			self.HAIR = self.HAIR - 1
			self.HAIR_STYLE = self.HAIR_STYLE - 16

		else:
			self.HAIR = self.HAIR - 1
			self.HAIR_STYLE = self.HAIR_STYLE - 1

		chr.ChangeHair(self.HAIR_STYLE)

	def __NextHair(self):
		if self.HAIR == 17 and self.HAIR_STYLE == 44:
			self.HAIR = self.HAIR - 17
			self.HAIR_STYLE = self.HAIR_STYLE - 44

		elif self.HAIR == 5 and self.HAIR_STYLE == 5:
			self.HAIR = self.HAIR + 1
			self.HAIR_STYLE = self.HAIR_STYLE + 16

		elif self.HAIR == 9 and self.HAIR_STYLE == 24:
			self.HAIR = self.HAIR + 1
			self.HAIR_STYLE = self.HAIR_STYLE + 7

		elif self.HAIR == 13 and self.HAIR_STYLE == 34:
			self.HAIR = self.HAIR + 1
			self.HAIR_STYLE = self.HAIR_STYLE + 7

		else:
			self.HAIR = self.HAIR + 1
			self.HAIR_STYLE = self.HAIR_STYLE + 1

		chr.ChangeHair(self.HAIR_STYLE)
	#Final CabeloCriarChar

	#GIRAR CHAR
	def Girar_Esquerda(self):
		self.Rotation = self.Rotation - 15
		chr.SetRotation(self.Rotation)

	def Girar_Direita(self):
		self.Rotation = self.Rotation + 15
		chr.SetRotation(self.Rotation)
	#FINAL GIRAR CHAR

	def EnableWindow(self):
		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1
		self.reservingHairstyleIndex = -1

		self.btnCreate.Enable()
		self.btnCancel.Enable()

		self.editCharacterName.SetFocus()
		self.editCharacterName.Enable()

		self.genderButton[0].Enable()
		self.genderButton[1].Enable()

		for page in xrange(PAGE_COUNT):
			for slot in xrange(SLOT_COUNT):
				chr_id = self.__GetSlotChrID(page, slot)
				chr.SelectInstance(chr_id)
				chr.BlendLoopMotion(chr.MOTION_INTRO_WAIT, 0.1)

	def DisableWindow(self):
		self.btnCreate.Disable()
		self.btnCancel.Disable()
		self.genderButton[0].Disable()
		self.genderButton[1].Disable()
		self.editCharacterName.Disable()

	def __GetSlotChrID(self, page, slot):
		return BASE_CHR_ID + page * SLOT_COUNT + slot

	def __MakeCharacter(self,chr_id,race):

		chr.CreateInstance(chr_id)
		chr.SelectInstance(chr_id)
		chr.SetVirtualID(chr_id)
		chr.SetRace(race)
		chr.SetArmor(0)
		chr.SetHair(0)
		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		chr.SetRotation(0.0)
		chr.Hide()

	def __SelectGender(self, gender):
		for button in self.genderButton:
			button.SetUp()

		self.genderButton[gender].Down()

		self.gender = gender

		if gender == MAN:
			for i in xrange(SLOT_COUNT):
				chr.SelectInstance(self.__GetSlotChrID(0, i))
				chr.Show()
			for i in xrange(SLOT_COUNT):
				chr.SelectInstance(self.__GetSlotChrID(1, i))
				chr.Hide()
		else:
			for i in xrange(SLOT_COUNT):
				chr.SelectInstance(self.__GetSlotChrID(0, i))
				chr.Hide()
			for i in xrange(SLOT_COUNT):
				chr.SelectInstance(self.__GetSlotChrID(1, i))
				chr.Show()

		for id in xrange(BASE_CHR_ID + SLOT_COUNT * PAGE_COUNT):
			chr.DeleteInstance(id)

		self.__SelectSlot(self.slot)
		chr_id = self.__GetSlotChrID(self.gender, self.slot)
		chr.SetHair(self.HAIR_STYLE)
		self.__MakeCharacter(chr_id, self.characters[self.gender][self.slot])
		self.__SelectShape(self.shape)
		chr.SetRotation(0.0)

	def __SelectShape(self, shape):
		self.shape = shape
		chr_id = self.__GetSlotChrID(self.gender, self.slot)
		chr.SelectInstance(chr_id)
		chr.ChangeShape(shape)
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
		chr.SetRotation(0.0)

	def __SelectSlot(self, slot):
		if self.gender == 0:#MAN
			if slot == 0:
				self.imgChar.LoadImage("interface/icons/faces/warrior_m.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/guerreiro.tga")
				self.imgChar.Show()
			elif slot == 1:
				self.imgChar.LoadImage("interface/icons/faces/assassin_m.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/ninja.tga")
				self.imgChar.Show()
			elif slot == 2:
				self.imgChar.LoadImage("interface/icons/faces/sura_m.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/shura.tga")
				self.imgChar.Show()
			elif slot == 3:
				self.imgChar.LoadImage("interface/icons/faces/shaman_m.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/shama.tga")
				self.imgChar.Show()
		elif self.gender == 1:#WOMAN
			if slot == 0:
				self.imgChar.LoadImage("interface/icons/faces/warrior_w.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/guerreiro.tga")
				self.imgChar.Show()
			elif slot == 1:
				self.imgChar.LoadImage("interface/icons/faces/assassin_w.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/ninja.tga")
				self.imgChar.Show()
			elif slot == 2:
				self.imgChar.LoadImage("interface/icons/faces/sura_w.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/shura.tga")
				self.imgChar.Show()
			elif slot == 3:
				self.imgChar.LoadImage("interface/icons/faces/shaman_w.tga")
				self.dlgBoard.GetChild("classe_name").LoadImage("interface/controls/special/create/shama.tga")
				self.imgChar.Show()

		if slot < 0:
			return

		if slot >= SLOT_COUNT:
			return

		if self.slot == slot:
			return

		self.slot = slot
		#STATUS DO CHAR
		self.ResetStat()
		#FINAL STATUS DO CHAR

		if self.IsShow():
			snd.PlaySound("sound/ui/click.wav")

		chr_id = self.__GetSlotChrID(self.gender, slot)

		for id in xrange(BASE_CHR_ID + SLOT_COUNT * PAGE_COUNT):
			chr.DeleteInstance(id)

		chr.SelectInstance(chr_id)

		chr.SetHair(0)
		self.HAIR = 0
		self.HAIR_STYLE = 0
		self.__MakeCharacter(chr_id, self.characters[self.gender][slot])
		self.__SelectShape(self.shape)
		self.__SelectGender(self.gender)

	def CreateCharacter(self):
		if -1 != self.reservingRaceIndex:
			return

		textName = self.editCharacterName.GetText()
		if False == self.__CheckCreateCharacter(textName):
			return

		if musicinfo.selectMusic != "":
			snd.FadeLimitOutMusic("bgm/"+musicinfo.selectMusic, systemSetting.GetMusicVolume()*0.05)

		self.DisableWindow()

		chr.SelectInstance(self.__GetSlotChrID(self.gender, self.slot))
		chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)

		self.reservingRaceIndex = chr.GetRace()
		self.reservingShapeIndex = self.shape
		self.reservingStartTime = app.GetTime()
		self.toolTip.Hide()

	def CancelCreate(self):
		self.stream.SetSelectCharacterPhase()

	def __CheckCreateCharacter(self, name):
		if len(name) == 0:
			self.PopupMessage(localeinfo.CREATE_INPUT_NAME, self.EnableWindow)
			return False

		if name.find(localeinfo.CREATE_GM_NAME)!=-1:
			self.PopupMessage(localeinfo.CREATE_ERROR_GM_NAME, self.EnableWindow)
			return False

		if net.IsInsultIn(name):
			self.PopupMessage(localeinfo.CREATE_ERROR_INSULT_NAME, self.EnableWindow)
			return False

		return True

	def ResetStat(self):
		for i in xrange(4):
			self.stat[i] = self.START_STAT[self.slot][i]
		self.lastStatPoint = self.CREATE_STAT_POINT

	def OverInStatButton(self, stat):
		if not self.STAT_DESCRIPTION.has_key(stat):
			return

		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(self.STAT_DESCRIPTION[stat])
		self.toolTip.Show()

	def OverOutStatButton(self):
		self.toolTip.Hide()

	def OnCreateSuccess(self):
		self.stream.SetSelectCharacterPhase()

	def OnCreateFailure(self, type):
		if 1 == type:
			self.PopupMessage(localeinfo.CREATE_EXIST_SAME_NAME, self.EnableWindow)
		else:
			self.PopupMessage(localeinfo.CREATE_FAILURE, self.EnableWindow)

	def OnUpdate(self):
		chr.Update()

		for page in xrange(PAGE_COUNT):
			for i in xrange(SLOT_COUNT):
				chr.SelectInstance(self.__GetSlotChrID(page, i))
				chr.Show()

		if -1 != self.reservingRaceIndex:
			if app.GetTime() - self.reservingStartTime >= 1.5:

				chrSlot=self.stream.GetCharacterSlot()
				textName = self.editCharacterName.GetText()
				raceIndex = self.reservingRaceIndex
				shapeIndex = self.reservingShapeIndex

				#STATUS DO CHAR
				startStat = self.START_STAT[self.slot]
				statCon = self.stat[0] - startStat[0]
				statInt = self.stat[1] - startStat[1]
				statStr = self.stat[2] - startStat[2]
				statDex = self.stat[3] - startStat[3]
				net.SendCreateCharacterPacket(chrSlot, textName, raceIndex, shapeIndex, statCon, statInt, statStr, statDex, self.HAIR_STYLE)
				#FINAL STATUS DO CHAR
				self.reservingRaceIndex = -1

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func = 0):
		if not func:
			func = self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeinfo.UI_OK)

	def OnPressExitKey(self):
		self.CancelCreate()
		return True
