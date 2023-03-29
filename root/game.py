#favor manter essa linha
import _app as app
import _item as item
import _player as player
import _chat as chat
import _net as net
import _chr as chr
import _chr_mgr as chrmgr
import os
import _dbg as dbg
import _grp as grp
import _background as background
import _text_tail as textTail
import _snd as snd
import _wnd_mgr as wndMgr
import _settings as systemSetting
import _quest as quest
import _guild as guild
import _skill as skill
import _messenger as messenger
import localeinfo
import constinfo
import _trade as exchange
import _ime as ime
import ui
import uicommon
import uiphasecurtain
import uimapnameshower
import uiaffectshower
import uiplayergauge
import uitarget
import uiprivateshopbuilder
import uiofflineshop
import uiofflineshopbuilder
import mousemodule
import interfacemodule
import musicinfo
import debuginfo
import stringcommander
import _event as event
import exception
import uipopup
import uiscriptlocale
import uicommon

from uikillmessage import KillPopup

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		self.itemShopWnd = None
		self.stream=stream
		self.interface = interfacemodule.Interface()
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()
		self.curtain = uiphasecurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uitarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(self.interface.OpenWhisperDialog)
		self.targetBoard.Hide()

		self.mapNameShower = uimapnameshower.MapNameShower()
		self.affectShower = uiaffectshower.AffectShower()

		self.playerGauge = uiplayergauge.PlayerGauge(self)
		self.playerGauge.Hide()

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constinfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constinfo.SET_DEFAULT_CHRNAME_COLOR()
		# constinfo.SET_DEFAULT_FOG_LEVEL()
		constinfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constinfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()
		constinfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		event.SetLeftTimeString(localeinfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constinfo.PVPMODE_ENABLE)

		self.__BuildKeyDict()
		self.__BuildDebugInfo()
		uiprivateshopbuilder.Clear()
		uiofflineshopbuilder.Clear()
		exchange.InitTrading()

		if debuginfo.IsDebugMode():
			self.ToggleDebugInfo()

		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("bgm/" + netFieldMusicFileName)
		elif musicinfo.fieldMusic != "":
			snd.FadeInMusic("bgm/" + musicinfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()
		try:
			self.StartGame()
		except BaseException:
			exception.Abort("GameWindow.Open")

	def Close(self):
		self.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicinfo.fieldMusic != "":
			snd.FadeOutMusic("bgm/"+ musicinfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		mousemodule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None
		self.itemDropQuestionDialog = None
		self.confirmDialog = None
		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None
		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None

		if self.itemShopWnd:
			self.itemShopWnd.Destroy()
			self.itemShopWnd = None

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		app.HideCursor()

	def __BuildKeyDict(self):
		onPressKeyDict = {}
		onPressKeyDict[app.DIK_1]			= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]			= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]			= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]			= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]			= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]			= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]			= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]			= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]			= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]			= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]			= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]			= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]			= lambda : self.__PressQuickSlot(7)

		onPressKeyDict[app.DIK_F5]			= lambda : self.interface.OpenWndBot()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_H]			= self.__PressHKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey
		onPressKeyDict[app.DIK_P]			= self.__PressPKey
		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)

		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_K]			= lambda : self.__PressKKey()
		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()
		onPressKeyDict[app.DIK_X]			= lambda : player.KeyAutoAttack()

		self.onPressKeyDict					= onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()
		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		self.onClickKeyDict = onClickKeyDict
		interfacemodule.IsQBHide = 0
		self.interface.HideAllQuestButton()

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num -1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constinfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()

	def __PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			else:
				if not uiprivateshopbuilder.IsBuildingPrivateShop() or not uiofflineshopbuilder.IsBuildingOfflineShop():
					for i in range(player.INVENTORY_PAGE_SIZE):
						if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							net.SendItemUsePacket(i)
							break

	def __PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def __PressKKey(self):
		self.interface.ToggleGuildWindow()

	def __PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/ride")

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/ride")
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def __ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0 == interfacemodule.IsQBHide:
				interfacemodule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfacemodule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __PressPKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0 == interfacemodule.IsWisperHide:
				chat.AppendChat(chat.CHAT_TYPE_NOTICE, "PM's ocultados com sucesso!")
				interfacemodule.IsWisperHide = 1
				self.interface.HideAllWhisperButton()
			else:
				interfacemodule.IsWisperHide = 0
				chat.AppendChat(chat.CHAT_TYPE_NOTICE, "PM's desocultados com sucesso!")
				self.interface.ShowAllWhisperButton()

	def __SetQuickSlotMode(self):
		self.pressNumber = ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber = ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		if localSlotIndex == 7 and app.IsPressed(app.DIK_LALT):
			questionDialog = uicommon.QuestionDialog()
			questionDialog.SetText("VocÃª quer fechar o jogo?")
			questionDialog.SetAcceptEvent(self.Yes)
			questionDialog.SetCancelEvent(self.No)
			questionDialog.Open()
			self.questionDialog = questionDialog

		player.RequestUseLocalQuickSlot(localSlotIndex)

	def Yes(self):
		app.Exit()

	def No(self):
		self.questionDialog.Close()

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeinfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeinfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeinfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeinfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeinfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeinfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeinfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeinfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):
		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constinfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeinfo.OPTION_PVPMODE_PROTECT % (constinfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constinfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print("PKMode %d" % nextPKMode)

	def OnChangePKMode(self):
		try:
			self.__NotifyError(localeinfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print("UNKNOWN PVPMode[%d]" % (player.GetPKMode()))

	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		self.interface.OpenQuestWindow(skin, idx)

	def HideAllQuestWindow(self):
		self.interface.HideAllQuestWindow()

	def UpdateCoins(self, coins):
		constinfo.coins = coins
		# self.interface.UpdateCoins(coins)

	def UpdateAveragePrice(self, price, mode):
		self.interface.UpdateAveragePrice(price, mode)

	def UpdateEXPMode(self, mode):
		self.interface.UpdateEXPMode(mode)

	def AskGuildName(self):
		guildNameBoard = uicommon.InputDialog()
		guildNameBoard.SetTitle(localeinfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(self.ConfirmGuildName)
		guildNameBoard.SetCancelEvent(self.CancelGuildName)
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeinfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeinfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	def OnGameOver(self, d_time):
		self.CloseTargetBoard()
		self.OpenRestartDialog(d_time)

	def OpenRestartDialog(self, d_time):
		self.interface.OpenRestartDialog(d_time)

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)
		if app.IsPressed(app.DIK_LCONTROL):
			if not player.IsSameEmpire(vid):
				return
			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return
			self.interface.OpenWhisperDialog(name)

	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	def SetHPTargetBoard(self, vid, hpPercentage):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.ResetTargetBoard()
			self.targetBoard.SetEnemyVID(vid)

		self.targetBoard.SetHP(hpPercentage)
		self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	#VER SET
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)
	#FINAL VER SET

	def ShowMapName(self, mapName, x, y):
		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	def OnRecvWhisper(self, mode, name, line):
		if mode == chat.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)

		if not self.interface.FindWhisperButton(name) and constinfo.WHISPER_MESSAGES.__contains__(name) and not self.interface.whisperDialogDict.__contains__(name):
			self.interface.RecvWhisper(mode, name, line, True)
		else:
			self.interface.RecvWhisper(mode, name, line, False)

		if not constinfo.WHISPER_MESSAGES.__contains__(name):
			constinfo.WHISPER_MESSAGES.update({name : [(mode, line)]})
		else:
			constinfo.WHISPER_MESSAGES[name].append((mode, line))

		chat.AppendWhisper(mode, name, line)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(mode, name, line, False)

	def OnRecvWhisperError(self, mode, name, line):
		if localeinfo.WHISPER_ERROR.__contains__(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeinfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(mode, name, line, False)

	def OnPickMoney(self, money):
		pass
		# chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.GAME_PICK_MONEY % (money))
		# self.interface.OnPickMoneyNew(money)

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeinfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeinfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeinfo.SAFEBOX_ERROR)
		#Salvar Senha Ao abrir
		self.interface.InitSafeboxPassword()
		#Final Salvar Senha Ao abrir

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeinfo.FISHING_SUCCESS(isFish, fishName), 2000)

	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.FISHING_WRONG_PLACE)

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeinfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.GAME_CANNOT_PICK_ITEM)

	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.GAME_CANNOT_MINING)

	def OnCannotUseSkill(self, vid, type):
		textTail.RegisterInfoTail(vid, localeinfo.USE_SKILL_ERROR_TAIL_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeinfo.SHOT_ERROR_TAIL_DICT.get(type, localeinfo.SHOT_ERROR_UNKNOWN % (type)))

	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def StartOfflineShop(self, vid):
		self.interface.OpenOfflineShopDialog(vid)

	def EndOfflineShop(self):
		self.interface.CloseOfflineShopDialog()

	def RefreshOfflineShop(self):
		self.interface.RefreshOfflineShopDialog()

	def RefreshOfflineShopMoney(self, value):
		self.interface.RefreshOfflineShopMoney(value)

	def StartExchange(self, level, race, guild, name):
		self.interface.StartExchange(level, race, guild)

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uicommon.QuestionDialogWithTimeLimit()
		partyInviteQuestionDialog.SetText1(leaderName + localeinfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetTimeOverMsg(localeinfo.PARTY_ANSWER_TIMEOVER)
		partyInviteQuestionDialog.SetTimeOverEvent(self.AnswerPartyInvite, False)
		partyInviteQuestionDialog.SetAcceptEvent(self.AnswerPartyInvite, True)
		partyInviteQuestionDialog.SetCancelEvent(self.AnswerPartyInvite, False)
		partyInviteQuestionDialog.Open(20)
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):
		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name, race, online):
		self.interface.AddPartyMember(pid, name, race, online)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uicommon.QuestionDialogWithTimeLimit()
		messengerAddFriendQuestion.SetText1(localeinfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND % (name))
		messengerAddFriendQuestion.SetTimeOverMsg(localeinfo.MESSENGER_ADD_FRIEND_ANSWER_TIMEOVER)
		messengerAddFriendQuestion.SetTimeOverEvent(self.OnDenyAddFriend)
		messengerAddFriendQuestion.SetAcceptEvent(self.OnAcceptAddFriend)
		messengerAddFriendQuestion.SetCancelEvent(self.OnDenyAddFriend)
		messengerAddFriendQuestion.Open(10)
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	if app.ENABLE_GUILD_SAFEBOX:
		def RefreshGuildSafebox(self):
			self.interface.RefreshGuildSafebox()

		def RefreshGuildSafeboxMoney(self):
			self.interface.RefreshGuildSafeboxMoney()

	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uicommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeinfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(self.AnswerGuildInvite, True)
		guildInviteQuestionDialog.SetCancelEvent(self.AnswerGuildInvite, False)
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):
		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None

	def DeleteGuild(self):
		self.interface.DeleteGuild()

	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	def CheckFocus(self):
		if False == self.IsFocus():
			if self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
			os.mkdir(os.getcwd()+os.sep+"screenshot")
		(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)

		if succeeded:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Tela Capturada com sucesso.")
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.SCREENSHOT_SAVE_FAILURE)

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		player.SetQuickPage(self.interface.wndTaskBar.quickSlotPageIndex+1)

	def __IsShowName(self):
		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True
		return False

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.interface.wndTaskBar.quickSlotPageIndex)

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
		player.SetAttackKeyState(False)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)

	def PickUpItem(self):
		player.PickCloseItem()

	def OnKeyDown(self, key):
		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except BaseException:
			raise

		return True

	def OnKeyUp(self, key):
		try:
			self.onClickKeyDict[key]()
		except KeyError:
			pass
		except BaseException:
			raise

		return True

	def OnMouseLeftButtonDown(self):
		if mousemodule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);
		return True

	def OnMouseLeftButtonUp(self):
		if mousemodule.mouseController.isAttached():
			attachedType = mousemodule.mouseController.GetAttachedType()
			attachedItemIndex = mousemodule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mousemodule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mousemodule.mouseController.GetAttachedItemCount()

			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)
			elif player.SLOT_TYPE_INVENTORY == attachedType:
				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)
			mousemodule.mouseController.DeattachObject()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType:
			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos):
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeinfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeinfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID):
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						if app.ALUGAR_ITENS and (app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT)):
							self.interface.RentTimeDialog.Open(attachedInvenType, attachedItemSlotPos, 0)
						else:
							net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		if uiprivateshopbuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if (uiofflineshopbuilder.IsBuildingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if (uiofflineshop.IsEditingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if attachedMoney >= 1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeinfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeinfo.UI_OK)
			return

		itemDropQuestionDialog = uicommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeinfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(self.RequestDropItem, True)
		itemDropQuestionDialog.SetCancelEvent(self.RequestDropItem, False)
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if uiprivateshopbuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if (uiofflineshopbuilder.IsBuildingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if (uiofflineshop.IsEditingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeinfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeinfo.UI_OK)

		else:
			if player.SLOT_TYPE_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(attachedItemSlotPos)
				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()
				questionText = localeinfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)
				itemDropQuestionDialog = uicommon.ItemQuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(self.RequestDropItem, True)
				itemDropQuestionDialog.SetCancelEvent(self.RequestDropItem, False)
				itemDropQuestionDialog.SetEscapeEvent(self.RequestDropItem, False)
				itemDropQuestionDialog.window_type = "inv"
				itemDropQuestionDialog.count = attachedItemCount
				itemDropQuestionDialog.Open(dropItemIndex, attachedItemSlotPos)
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog
				constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(1)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return
		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if player.SLOT_TYPE_INVENTORY == dropType:
				if dropNumber == player.ITEM_MONEY:
					net.SendGoldDropPacket(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				else:
					self.__SendDropItemPacket(dropNumber, dropCount)

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constinfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		if uiprivateshopbuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		if (uiofflineshopbuilder.IsBuildingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if (uiofflineshop.IsEditingOfflineShop()):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.DROP_ITEM_FAILURE_OFFLINE_SHOP)
			return

		if background.GetCurrentMapName() == "maps/113_ox":
			chat.AppendChat(chat.CHAT_TYPE_INFO, "NÃ£o permitido neste mapa")
			return

		net.SendItemDropPacket(itemInvenType, itemVNum, itemCount)

	if app.ENABLE_FLAGS_CHAT:
		def OnMouseOver(self):
			hyperlink = ui.GetHyperlink()
			self.interface.HyperlinkTooltip(hyperlink)

	def OnMouseRightButtonDown(self):
		self.CheckFocus()

		if mousemodule.mouseController.isAttached():
			mousemodule.mouseController.DeattachObject()
		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)
		return True

	def OnMouseRightButtonUp(self):
		if mousemodule.mouseController.isAttached():
			return True
		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		app.UpdateGame()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

	def UpdateDebugInfo(self):
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()

		if iPatch == 0:
			iPatch = 1

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f" % (x, y, z))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()
		(x, y) = app.GetCursorPosition()
		textTail.UpdateAllTextTail()

		if wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)

		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif mousemodule.mouseController.isAttached():
			mousemodule.mouseController.DeattachObject()
		else:
			self.interface.OpenSystemCDialog()
		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemCDialog()
		return True

	def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
		if inven_type == player.INVENTORY:
			self.interface.CantTradableItemExchange(display_pos, inven_pos)

	def BINARY_DelItemToExchange(self, display_pos):
		self.interface.CanTradableItemExchange(display_pos)

	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)

	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uicommon.QuestionDialogWithTimeLimit()
		confirmDialog.SetText1(msg)
		confirmDialog.Open(timeout)
		confirmDialog.SetAcceptEvent(net.SendQuestConfirmPacket, True, pid)
		confirmDialog.SetCancelEvent(net.SendQuestConfirmPacket, False, pid)
		self.confirmDialog = confirmDialog

	def Players_online(self, all, r1, r2, r3):
		if not self.interface:
			return
		if not self.interface.wndGameButton.online:
			return
		if not systemSetting.IsWindowed():
			self.interface.wndGameButton.Players_online(all, r1, r2, r3)
		else:
			app.SetWindowTitle(constinfo.APP_TITLE_NEW + "    Online: "+str(all)+"    Chunjo:"+str(r1)+"    Shinso:"+str(r2)+"    Jinno:"+str(r3))
			for item in self.interface.wndGameButton.online:
				item.Hide()

	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeinfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)	

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):
		guildName = guild.GetGuildName(guildID)

		if "Noname" == guildName:
			return

		import uiguildwardeclare
		questionDialog = uiguildwardeclare.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):
		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):
		guildName = self.guildWarQuestionDialog.GetGuildName()
		net.SendChatPacket("/warno " + guildName)
		self.__GuildWar_CloseAskDialog()
		return 1

	def __ServerCommand_Build(self):
		serverCommandList = {
			"guild_meeting"			: self.guild_meeting_request,
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"OpenOfflineShop"		: self.__OfflineShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,
			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,

			#Amigo System
			"spop"					: self.__ShowPopup,
			#Amigo System Final

			"distance_exchange"		: self.Open_Remote_Exchange_Question,

			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,

			"sit_down"				: self.__BINARY_SIT_DOWN,
			"break_sit"				: self.__BINARY_BREAK_SIT,
			"block_exp"				: self.SetBlockExpMode,

			"MyShopPriceList"		: self.__PrivateShop_PriceList,

			"ViewEquipRequest"						: self.__ViewEquipRequest,
			"ViewEquipRequestDenied"				: self.__ViewEquipRequestDenied,

			"ranking_clean"							: self.RankingClean,
			"ranking_position"						: self.RankingPosition,
			"ranking_add"							: self.RankingAddPlayer,

			"ranking_guild_clean"					: self.RankingGuildClean,
			"ranking_guild_add"						: self.RankingAddGuild,

			"wh_clear"								: self.WarHistoryClean,
			"wh_append"								: self.WarHistoryAppend,
			"wh_insert"								: self.WarHistoryInsert,
			"wh_append_kills"						: self.WarKillsAppend,

			"whl_append_msgs"						: self.WarLogAppend,

			"siege_war_running"						: self.SiegeWarStart,
			"siege_event"							: self.SiegeUpdate,
			"siege_war_end"							: self.SiegeWarEnd,

			"kill_msg"								: self.KillPopupAppend,
		}

		if app.ENABLE_DEFENSE_WAVE:
			serverCommandList["BINARY_Update_Mast_HP"] = self.BINARY_Update_Mast_HP
			serverCommandList["BINARY_Update_Mast_Window"] = self.BINARY_Update_Mast_Window

		self.serverCommander = stringcommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(serverCommandItem[0], serverCommandItem[1])

	def BINARY_ServerCommand_Run(self, line):
		try:
			return self.serverCommander.Run(line)
		except RuntimeError as msg:
			dbg.TraceError(msg)
			return 0

	KillPopupList = []
	def KillPopupAppend(self, killer_name, killer_empire, killer_race, victim_name, victim_empire, victim_race):
		KillPopup(killer_name, killer_empire, killer_race, victim_name, victim_empire, victim_race, self.KillPopupList)

	def SiegeWarStart(self, empire):
		if self.interface:
			if self.interface.wndSiegeWarEnter:
				self.interface.wndSiegeWarEnter.Open(empire)

	def SiegeUpdate(self, empire, tower, shinso, chunjo, jinno, time):
		if self.interface:
			if self.interface.wndSiegeWarScore:
				self.interface.wndSiegeWarScore.Open(empire, tower, shinso, chunjo, jinno, time)

	def SiegeWarEnd(self):
		if self.interface:
			if self.interface.wndSiegeWarEnter:
				self.interface.wndSiegeWarEnter.Hide()

	def RankingPosition(self, pos):
		if not constinfo.NEW_CHARACTER:
			return

		if self.interface:
			if self.interface.wndCharacter:
				self.interface.wndCharacter.RankingPosition(pos)

	def RankingAddPlayer(self, name, points):
		if not constinfo.NEW_CHARACTER:
			return

		if self.interface:
			if self.interface.wndCharacter:
				self.interface.wndCharacter.RankingAddPlayer(name, points)

	def RankingClean(self):
		if not constinfo.NEW_CHARACTER:
			return

		if self.interface:
			if self.interface.wndCharacter:
				self.interface.wndCharacter.RankingClean()

	def RankingAddGuild(self, nome, pontos, vitorias, empates, derrotas):
		if self.interface:
			if self.interface.wndGuild:
				self.interface.wndGuild.RankingAddGuild(nome, pontos, vitorias, empates, derrotas)

	def RankingGuildClean(self):
		if self.interface:
			if self.interface.wndGuild:
				self.interface.wndGuild.RankingClean()

	def WarHistoryAppend(self, war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount):
		if self.interface:
			if self.interface.wndGuild:
				self.interface.wndGuild.WarHistoryAppend(war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount)

	def WarHistoryInsert(self, war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount):
		if self.interface:
			if self.interface.wndGuild:
				self.interface.wndGuild.WarHistoryAppend(war_id, data_end, time_end, guild1_name, guild1_score, guild1_pcount, guild2_name, guild2_score, guild2_pcount)

	def WarHistoryClean(self):
		if self.interface:
			if self.interface.wndGuild:
				self.interface.wndGuild.WarHistoryClean()

	def WarKillsAppend(self, war_id, player, killed, died, guild):
		if self.interface:
			if self.interface.wndGuild:
				self.interface.wndGuild.WarKillsAppend(war_id, player, killed, died, guild)

	def WarLogAppend(self, war_id, data, time, msg):
		pass
		# if self.interface:
			# if self.interface.wndGuild:
				# self.interface.wndGuild.WarLogAppend(war_id, data, time, msg)

	def SetBlockExpMode(self, mode):
		self.interface.SetBlockExpMode(int(mode))

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	def __BINARY_SIT_DOWN(self):
		net.SendCharacterPositionPacket(4)

	def __BINARY_BREAK_SIT(self):
		net.SendCharacterPositionPacket(0)

	def guild_meeting_request(self):
		dialog = uicommon.QuestionDialog()
		dialog.SetText(uiscriptlocale.GUILD_MEETING_REQUEST)
		dialog.SetAcceptEvent(self.guild_meeting_yes)
		dialog.SetCancelEvent(self.guild_meeting_no)
		dialog.Open()
		self.guild_meeting_request_dialog = dialog
		return

	def guild_meeting_yes(self):
		net.SendChatPacket("/guild_meeting_yes")
		self.guild_meeting_request_dialog.Close()

	def guild_meeting_no(self):
		self.guild_meeting_request_dialog.Close()

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "Item refinado com sucesso!")

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		chat.AppendChat(chat.CHAT_TYPE_INFO, "NÃ£o foi dessa vez tente novamente!")

	def Open_Remote_Exchange_Question(self, name, level): 
		remote_exchange_question = uicommon.QuestionDialog()
		remote_exchange_question.SetText("|cffFDD017|H|h" + str(name)+ "|cff00ccff" + "(Lv."+str(level)+")"+ "|h|r" + " Quer negociar com vocÃª.")
		remote_exchange_question.SetAcceptEvent(self.Accept_Remote_Exchange, name)
		remote_exchange_question.SetCancelEvent(self.Deny_Remote_Exchange, name)
		remote_exchange_question.Open()
		self.remote_exchange_question = remote_exchange_question

	def Accept_Remote_Exchange(self, name):
		net.SendExchangeStartPacket(name)
		net.SendChatPacket("/exchange_remote_accept " + str(name))
		self.remote_exchange_question.Close()

	def Deny_Remote_Exchange(self, name):
		net.SendChatPacket("/exchange_remote_deny " + str(name))
		self.remote_exchange_question.Close()

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiprivateshopbuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = [
			"metin2_map_n_flame_01",
			"metin2_map_n_desert_01",
			"metin2_map_spiderdungeon",
			"metin2_map_deviltower1",
		]

		if background.GetCurrentMapName() in mapDict:
			return False
		return True

	def __XMasSnow_Enable(self, mode):
		self.__XMasSong_Enable(mode)

		if "1" == mode:
			if not self.__IsXMasMap():
				return
			background.EnableSnow(1)
		else:
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1" == mode:
			if not self.__IsXMasMap():
				return
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1" == mode:
			XMAS_BGM = "xmas.mp3"
			if app.IsExistFile("bgm/" + XMAS_BGM) == 1:
				if musicinfo.fieldMusic != "":
					snd.FadeOutMusic("bgm/" + musicinfo.fieldMusic)
				musicinfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("bgm/" + musicinfo.fieldMusic)
		else:
			if musicinfo.fieldMusic != "":
				snd.FadeOutMusic("bgm/" + musicinfo.fieldMusic)
			musicinfo.fieldMusic = musicinfo.METIN2THEMA
			snd.FadeInMusic("bgm/" + musicinfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __PrivateShop_Open(self):
		self.interface.OpenPrivateShopInputNameDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	def __OfflineShop_Open(self):
		self.interface.OpenOfflineShopInputNameDialog()

	def BINARY_OfflineShop_Appear(self, vid, text):
		if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
			self.interface.AppearOfflineShop(vid, text)

	def BINARY_OfflineShop_Disappear(self, vid):
		if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
			self.interface.DisappearOfflineShop(vid)

	def __PRESERVE_DayMode_Update(self, mode):
		if "light" == mode:
			background.SetEnvironmentData(0)
		elif "dark" == mode:
			if not self.__IsXMasMap():
				return
			background.RegisterEnvironmentData(1, constinfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light" == mode:
			self.curtain.FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark" == mode:
			if not self.__IsXMasMap():
				return
			self.curtain.FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constinfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	def __XMasBoom_Update(self):
		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return
		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]
		if app.GetTime() - self.startTimeXMasBoom > boomTime:
			self.indexXMasBoom += 1
			for i in range(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)
		snd.PlaySound3D(randX + x, randY - y, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uicommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeinfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeinfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeinfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(self.__AnswerPartyRequest, True)
		partyRequestQuestionDialog.SetCancelEvent(self.__AnswerPartyRequest, False)
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeinfo.PARTY_REQUEST_DENIED)

	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	if app.ENABLE_DEFENSE_WAVE:
		def BINARY_Update_Mast_HP(self, hp):
			self.interface.BINARY_Update_Mast_HP(int(hp))

		def BINARY_Update_Mast_Window(self, i):
			self.interface.BINARY_Update_Mast_Window(int(i))

	if app.ENABLE_SEND_TARGET_INFO:
		def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount):
			if not raceNum in constinfo.MONSTER_INFO_DATA:
				constinfo.MONSTER_INFO_DATA.update({raceNum : {}})
				constinfo.MONSTER_INFO_DATA[raceNum].update({"items" : []})
			curList = constinfo.MONSTER_INFO_DATA[raceNum]["items"]

			isUpgradeable = False
			isMetin = False
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				isUpgradeable = True
			elif item.GetItemType() == item.ITEM_TYPE_METIN:
				isMetin = True

			for curItem in curList:
				if isUpgradeable:
					if curItem.__contains__("vnum_list") and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				elif isMetin:
					if curItem.__contains__("vnum_list"):
						baseVnum = curItem["vnum_list"][0]
					if curItem.__contains__("vnum_list") and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				else:
					if curItem.__contains__("vnum") and curItem["vnum"] == itemVnum and curItem["count"] == itemCount:
						return

			if isUpgradeable or isMetin:
				curList.append({"vnum_list":[itemVnum], "count":itemCount})
			else:
				curList.append({"vnum":itemVnum, "count":itemCount})

		def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
			self.targetBoard.RefreshMonsterInfoBoard()

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicinfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("bgm/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicinfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("bgm/" + musicinfo.fieldMusic)

	def __ViewEquipRequest(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uicommon.QuestionDialog()
		partyRequestQuestionDialog.SetText("Permite ao jogador " + chr.GetNameByVID(vid) + " ver seus equipes?")
		partyRequestQuestionDialog.SetAcceptText(localeinfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeinfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(self.__AnswerViewEquipRequest, True)
		partyRequestQuestionDialog.SetCancelEvent(self.__AnswerViewEquipRequest, False)
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerViewEquipRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/view_equip_accept " + str(vid))
		else:
			net.SendChatPacket("/view_equip_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __ViewEquipRequestDenied(self, vid):
		vid = int(vid)
		self.PopupMessage("Pedido negado pelo usuário " + chr.GetNameByVID(vid) + ".")

	#Amigos System
	def __ShowPopup(self, arg):
		self.pop = uipopup.PopupMsg()
		data = arg.split("|")
		self.pop.SetType(int(data[0]))
		self.pop.SetMsg(data[1])
		self.pop.Show()
	#Amigos System Final

	if app.ENABLE_DROP_COFRE:
		def BINARY_AddChestDropInfo(self, chestVnum, pageIndex, slotIndex, itemVnum, itemCount):
			if not constinfo.CHEST_DROP_INFO_DATA.__contains__(chestVnum):
				constinfo.CHEST_DROP_INFO_DATA[chestVnum] = {}

			if not constinfo.CHEST_DROP_INFO_DATA[chestVnum].__contains__(pageIndex):
				constinfo.CHEST_DROP_INFO_DATA[chestVnum][pageIndex] = {}

			curList = constinfo.CHEST_DROP_INFO_DATA[chestVnum]

			if curList.__contains__(pageIndex):
				if curList[pageIndex].__contains__(slotIndex):
					if curList[pageIndex][slotIndex][0] == itemVnum and curList[pageIndex][slotIndex][1] == itemCount:
						return

			curList[pageIndex][slotIndex] = [itemVnum, itemCount]

		def BINARY_RefreshChestDropInfo(self, chestVnum):
			if self.interface:
				self.interface.RefreshChestDropInfo(chestVnum)

	if app.ENABLE_INVENTORY_VIEWER:
		def BINARY_InventoryViewerAddItem(self, pageIndex, slotIndex, itemVnum, itemCount):
			if self.interface:
				if self.interface.wndInventoryViewer:
					self.interface.wndInventoryViewer.AddItemInInventory(pageIndex, slotIndex, itemVnum, itemCount)

		def BINARY_InventoryViewerAddSocket(self, pageIndex, slotIndex, socketIndex, socketValue):
			if self.interface:
				if self.interface.wndInventoryViewer:
					self.interface.wndInventoryViewer.InventoryItemAddSocket(pageIndex, slotIndex, socketIndex, socketValue)

		def BINARY_InventoryViewerAddAttr(self, pageIndex, slotIndex, attrIndex, attrType, attrValue):
			if self.interface:
				if self.interface.wndInventoryViewer:
					self.interface.wndInventoryViewer.InventoryItemAddAttr(pageIndex, slotIndex, attrIndex, attrType, attrValue)

		def BINARY_OpenInventoryViewer(self, chrVid):
			if self.interface:
				if self.interface.wndInventoryViewer:
					self.interface.wndInventoryViewer.Open(chrVid)

		if app.ALUGAR_ITENS:
			def BINARY_InventoryViewerAddRent(self, pageIndex, slotIndex, renttime):
				if self.interface:
					if self.interface.wndInventoryViewer:
						self.interface.wndInventoryViewer.InventoryItemAddRent(pageIndex, slotIndex, renttime)

		if app.ENABLE_SOULBIND_SYSTEM:
			def BINARY_InventoryViewerAddBind(self, pageIndex, slotIndex, bind):
				if self.interface:
					if self.interface.wndInventoryViewer:
						self.interface.wndInventoryViewer.InventoryItemAddBind(pageIndex, slotIndex, bind)

	if app.ENABLE_SWITCH_IMPROVEMENT:
		def BINARY_SetItemUpdated(self, slotIndex):
			constinfo.SetItemUpdated(slotIndex)

	if app.SKILL_COOLTIME_UPDATE:
		def	SkillClearCoolTime(self, slotIndex):
			self.interface.SkillClearCoolTime(slotIndex)
