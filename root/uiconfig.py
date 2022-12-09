#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import LURMxMaKZJqliYt2QSHG as chat
import enszxc3467hc3kokdueq as app
import ga3vqy6jtxqi9yf344j7 as player
import ui
import snd
import systemSetting
import localeinfo
import constinfo
import musicinfo
import uiselectmusic
import uiprivateshopbuilder
import uiofflineshopbuilder
import sys

import _subprocess

class GameOptions(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.board = None
		self.state = "AUDIO"

		self.tabButtonDict = {}
		self.pageDict = {}

		self.musicListDlg = 0
		self.ctrlMusicVolume = None
		self.ctrlSoundVolume = None
		self.selectMusicFile = None

		self.NivelSombra = 0
		self.SombraModeButtonList = []

		self.WindowModeButtonList = []
		self.RESOLUTION_LIST = []
		self.RESOLUTION_CONT = 0
		self.nameColorModeButtonList = []
		self.viewTargetButtonList = []
		self.viewChatButtonList = []
		self.showsalesTextButtonList = []
		self.showDamageButtonList = []
		self.alwaysShowNameButtonList = []
		self.pvpModeButtonDict = {}
		self.pvpDescriptionDict = {}
		self.blockButtonList = []
		self.ActiveModeGraphicButtonList = []

	def __BindObject(self):
		self.board = self.GetChild("board")
		self.board.SetCloseEvent(self.Close)

		self.tabButtonDict = {
			"AUDIO"				: self.GetChild("Tab_Button_01"),
			"CAMERA"			: self.GetChild("Tab_Button_02"),
			"DISPLAY"			: self.GetChild("Tab_Button_03"),
			"PLAYER"			: self.GetChild("Tab_Button_04"),
			"PVP"				: self.GetChild("Tab_Button_05"),
			"BLOCK"				: self.GetChild("Tab_Button_06"),
		}
		self.pageDict = {
			"AUDIO"				: self.GetChild("Audio_Page"),
			"CAMERA"			: self.GetChild("Camera_Page"),
			"DISPLAY"			: self.GetChild("Display_Page"),
			"PLAYER"			: self.GetChild("Player_Page"),
			"PVP"				: self.GetChild("PvP_Page"),
			"BLOCK"				: self.GetChild("Block_Page"),
		}

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(self.__OnClickTabButton, tabKey)

		self.ctrlMusicVolume = self.GetChild("music_slider")
		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(self.OnChangeMusicVolume)

		self.ctrlSoundVolume = self.GetChild("audio_slider")
		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
		self.ctrlSoundVolume.SetEvent(self.OnChangeSoundVolume)
		self.OnChangeMusicVolume()
		self.OnChangeSoundVolume()

		self.GetChild("change_music_button").SetEvent(self.__OnClickChangeMusicButton)
		self.selectMusicFile = self.GetChild("nome_musica")
		self.selectMusicFile.SetText("|cfff8d090"+musicinfo.fieldMusic)
	## FIM AUDIO ##

	## CAMERA ##
		self.GetChild("camera_max_slider").SetEvent(self.__CameraMax)
		self.GetChild("camera_max_slider").SetSliderPos(float((constinfo.GET_CAMERA_MAX_DISTANCE()-2500.0)/4000.0))
		self.GetChild("camera_max_slider_percent").SetText("|cfff8d090"+str(self.GetChild("camera_max_slider").GetPercent())+"%")

		self.GetChild("neblina_slider").SetEvent(self.__Neblina)
		self.GetChild("neblina_slider").SetSliderPos(((30000.0 - float(constinfo.GET_FOG()))/25000.0))
		self.GetChild("neblina_slider_percent").SetText("|cfff8d090"+str(self.GetChild("neblina_slider").GetPercent())+"%")

		self.SombraModeButtonList.append(self.GetChild("sombras_none"))
		self.SombraModeButtonList.append(self.GetChild("sombras_word"))
		self.SombraModeButtonList.append(self.GetChild("sombras_player"))
		self.SombraModeButtonList.append(self.GetChild("sombras_all"))
		self.SombraModeButtonList.append(self.GetChild("sombras_all_all"))
		self.SombraModeButtonList[0].SetEvent(self.__Sombra, 0)
		self.SombraModeButtonList[1].SetEvent(self.__Sombra, 1)
		self.SombraModeButtonList[2].SetEvent(self.__Sombra, 2)
		self.SombraModeButtonList[3].SetEvent(self.__Sombra, 3)
		self.SombraModeButtonList[4].SetEvent(self.__Sombra, 4)
		i = int(systemSetting.GetShadowLevel()) -1
		self.SombraModeButtonList[i].Fill()

	## FIM CAMERA ##
	## DISPLAY ##
		self.WindowModeButtonList.append(self.GetChild("modo_janela"))
		self.WindowModeButtonList.append(self.GetChild("modo_fullscreen"))
		self.WindowModeButtonList[0].SetEvent(self.__Change_Window_Mode, 0)
		self.WindowModeButtonList[1].SetEvent(self.__Change_Window_Mode, 1)
		i = (systemSetting.IsWindowed() - 1)**2
		self.WindowModeButtonList[i].Fill()
# MONTA A LISTA DE RESOLUCOES DISPONIVEIS
		self.RESOLUTION_CONT = systemSetting.GetResolutionCount()
		for i in xrange(self.RESOLUTION_CONT):
			width, height, bpp = systemSetting.GetResolution(i)
			if bpp == 32:
				self.RESOLUTION_LIST.append(systemSetting.GetResolution(i))
# SETA O NOME DA RESOLUCAO CORRENTE #
		self.cur_width, self.cur_height, self.cur_bpp = systemSetting.GetCurrentResolution()
		self.GetChild("resolucao_slider_title").SetText("|cfff8d090"+str(self.cur_width)+":"+str(self.cur_height))
# BUSCA NA LISTA DE RESOLUCOES A RESOLUCAO CORRENTE
		resolution_index = -1
		len_res = len(self.RESOLUTION_LIST)
		for i in xrange(len_res):
			w, h, b = self.RESOLUTION_LIST[i]
			if w == self.cur_width and h == self.cur_height:
				resolution_index = i
				break
		if resolution_index == -1:
			self.GetChild("resolucao_slider_title").SetText("|cfff8d090Resolução Fora do Padão! "+str(self.cur_width)+":"+str(self.cur_height))
		else:
			self.GetChild("resolucao_slider").SetSliderPos((1.0/float(len_res))*float(resolution_index))

### REGULA A EXIBICAO DA IMAGEM
		pos = self.GetChild("resolucao_slider").GetSliderPos()
		i = 1.0/float(len(self.RESOLUTION_LIST))
		res_index = int(pos/i)
		scale = 0.5 + 0.3*i*float(res_index)
		self.GetChild("resolucao_imagem").SetScale(scale, scale)
		self.GetChild("resolucao_imagem").SetWindowHorizontalAlignCenter()
# SETA A FUNCAO DE TROCAR RESOLUCAO PARA O SLIDER
		self.GetChild("resolucao_slider").SetEvent(self.__Change_Window_Size)

	## FIM DISPLAY ##
	## PLAYER ##
		self.nameColorModeButtonList.append(self.GetChild("name_color_normal"))
		self.nameColorModeButtonList.append(self.GetChild("name_color_empire"))
		self.nameColorModeButtonList[0].SetEvent(self.__SetNameColorMode, 0)
		self.nameColorModeButtonList[1].SetEvent(self.__SetNameColorMode, 1)
		self.__ClickRadioButton(self.nameColorModeButtonList, constinfo.GET_CHRNAME_COLOR_INDEX())

		self.viewTargetButtonList.append(self.GetChild("target_board_view"))
		self.viewTargetButtonList.append(self.GetChild("target_board_no_view"))
		self.viewTargetButtonList[0].SetEvent(self.__SetTargetBoardViewMode, 0)
		self.viewTargetButtonList[1].SetEvent(self.__SetTargetBoardViewMode, 1)
		self.__ClickRadioButton(self.viewTargetButtonList, constinfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD())

		self.viewChatButtonList.append(self.GetChild("view_chat_on_button"))
		self.viewChatButtonList.append(self.GetChild("view_chat_off_button"))
		self.viewChatButtonList[0].SetEvent(self.__OnClickViewChat, 1)
		self.viewChatButtonList[1].SetEvent(self.__OnClickViewChat, 0)
		self.RefreshViewChat()

		self.showsalesTextButtonList.append(self.GetChild("salestext_on_button"))
		self.showsalesTextButtonList.append(self.GetChild("salestext_off_button"))
		self.showsalesTextButtonList[0].SetEvent(self.__OnClickSalesTextOnButton)
		self.showsalesTextButtonList[1].SetEvent(self.__OnClickSalesTextOffButton)
		self.RefreshShowSalesText()

		self.showDamageButtonList.append(self.GetChild("show_damage_on_button"))
		self.showDamageButtonList.append(self.GetChild("show_damage_off_button"))
		self.showDamageButtonList[0].SetEvent(self.__OnClickShowDamageOnButton)
		self.showDamageButtonList[1].SetEvent(self.__OnClickShowDamageOffButton)
		self.RefreshShowDamage()

		self.alwaysShowNameButtonList.append(self.GetChild("always_show_name_on_button"))
		self.alwaysShowNameButtonList.append(self.GetChild("always_show_name_off_button"))
		self.alwaysShowNameButtonList[0].SetEvent(self.__OnClickAlwaysShowNameOnButton)
		self.alwaysShowNameButtonList[1].SetEvent(self.__OnClickAlwaysShowNameOffButton)
		self.RefreshAlwaysShowName()

	## FIM PLAYER ##
	## PVP MODE ##
		self.pvpModeButtonDict[player.PK_MODE_PEACE] = self.GetChild("pvp_peace")
		self.pvpModeButtonDict[player.PK_MODE_REVENGE] = self.GetChild("pvp_revenge")
		self.pvpModeButtonDict[player.PK_MODE_GUILD] = self.GetChild("pvp_guild")
		self.pvpModeButtonDict[player.PK_MODE_FREE] = self.GetChild("pvp_free")
		self.pvpModeButtonDict[player.PK_MODE_PEACE].SetEvent(self.__OnClickPvPModePeaceButton)
		self.pvpModeButtonDict[player.PK_MODE_REVENGE].SetEvent(self.__OnClickPvPModeRevengeButton)
		self.pvpModeButtonDict[player.PK_MODE_GUILD].SetEvent(self.__OnClickPvPModeGuildButton)
		self.pvpModeButtonDict[player.PK_MODE_FREE].SetEvent(self.__OnClickPvPModeFreeButton)
		self.__SetPeacePKMode()

		##Mostrar descricoes:
		self.pvpDescriptionDict[player.PK_MODE_PEACE] = self.GetChild("pvp_peace_descript")
		self.pvpDescriptionDict[player.PK_MODE_REVENGE] = self.GetChild("pvp_revenge_descript")
		self.pvpDescriptionDict[player.PK_MODE_GUILD] = self.GetChild("pvp_guild_descript")
		self.pvpDescriptionDict[player.PK_MODE_FREE] = self.GetChild("pvp_free_descript")
		self.pvpDescriptionDict[player.PK_MODE_PEACE].Hide()
		self.pvpDescriptionDict[player.PK_MODE_REVENGE].Hide()
		self.pvpDescriptionDict[player.PK_MODE_GUILD].Hide()
		self.pvpDescriptionDict[player.PK_MODE_FREE].Hide()

		self.pvpModeButtonDict[player.PK_MODE_PEACE].SetToolTipWindow(self.pvpDescriptionDict[player.PK_MODE_PEACE])
		self.pvpModeButtonDict[player.PK_MODE_REVENGE].SetToolTipWindow(self.pvpDescriptionDict[player.PK_MODE_REVENGE])
		self.pvpModeButtonDict[player.PK_MODE_GUILD].SetToolTipWindow(self.pvpDescriptionDict[player.PK_MODE_GUILD])
		self.pvpModeButtonDict[player.PK_MODE_FREE].SetToolTipWindow(self.pvpDescriptionDict[player.PK_MODE_FREE])

		self.GetChild("aplicar_resolucao").SetEvent(self.__Aplicar)

		self.BlockExchangeButtonList = []
		self.BlockPartyButtonList = []
		self.BlockGuildButtonList = []
		self.BlockWhisperButtonList = []
		self.BlockFriendButtonList = []
		self.BlockPartyRequestButtonList = []
		self.BlockVerSetButtonList = []

		self.BlockExchangeButtonList.append(self.GetChild("BlockExchange_off_button"))
		self.BlockExchangeButtonList.append(self.GetChild("BlockExchange_on_button"))
		for i in xrange(len(self.BlockExchangeButtonList)):
			self.BlockExchangeButtonList[i].SetEvent(self.__OnClickBlock, player.BLOCK_EXCHANGE)

		self.BlockPartyButtonList.append(self.GetChild("BlockParty_off_button"))
		self.BlockPartyButtonList.append(self.GetChild("BlockParty_on_button"))
		for i in xrange(len(self.BlockPartyButtonList)):
			self.BlockPartyButtonList[i].SetEvent(self.__OnClickBlock, player.BLOCK_PARTY)

		self.BlockGuildButtonList.append(self.GetChild("BlockGuild_off_button"))
		self.BlockGuildButtonList.append(self.GetChild("BlockGuild_on_button"))
		for i in xrange(len(self.BlockGuildButtonList)):
			self.BlockGuildButtonList[i].SetEvent(self.__OnClickBlock, player.BLOCK_GUILD)

		self.BlockWhisperButtonList.append(self.GetChild("BlockWhisper_off_button"))
		self.BlockWhisperButtonList.append(self.GetChild("BlockWhisper_on_button"))
		for i in xrange(len(self.BlockWhisperButtonList)): 
			self.BlockWhisperButtonList[i].SetEvent(self.__OnClickBlock, player.BLOCK_WHISPER)

		self.BlockFriendButtonList.append(self.GetChild("BlockFriend_off_button"))
		self.BlockFriendButtonList.append(self.GetChild("BlockFriend_on_button"))
		for i in xrange(len(self.BlockFriendButtonList)):
			self.BlockFriendButtonList[i].SetEvent(self.__OnClickBlock, player.BLOCK_FRIEND)

		self.BlockPartyRequestButtonList.append(self.GetChild("BlockPartyRequest_off_button"))
		self.BlockPartyRequestButtonList.append(self.GetChild("BlockPartyRequest_on_button"))
		for i in xrange(len(self.BlockPartyRequestButtonList)):
			self.BlockPartyRequestButtonList[i].SetEvent(self.__OnClickBlock, player.BLOCK_PARTY_REQUEST)

		self.BlockVerSetButtonList.append(self.GetChild("VerSet_off_button"))
		self.BlockVerSetButtonList.append(self.GetChild("VerSet_on_button"))
		for i in xrange(len(self.BlockVerSetButtonList)):
			self.BlockVerSetButtonList[i].SetEvent(self.__OnClickBlock, player.BLOCK_VIEW_EQUIPMENT)

		self.blockButtonList.append(self.BlockExchangeButtonList)
		self.blockButtonList.append(self.BlockPartyButtonList)
		self.blockButtonList.append(self.BlockGuildButtonList)
		self.blockButtonList.append(self.BlockWhisperButtonList)
		self.blockButtonList.append(self.BlockFriendButtonList)
		self.blockButtonList.append(self.BlockPartyRequestButtonList)
		self.blockButtonList.append(self.BlockVerSetButtonList)
		self.RefreshBlock()

	## FIM BLOQUEIOS ##
	# INICILIZAR NA ABA AUDIO
		self.SetState("AUDIO")
	# INICILIZAR NA ABA AUDIO
### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS ### BLOQUEIOS 
	def RefreshBlock(self):
		for i in xrange(len(self.blockButtonList)):
			if 0 != (constinfo.blockMode & (1 << i)):
				self.blockButtonList[i][1].Empty()
				self.blockButtonList[i][0].Fill()
			else:
				self.blockButtonList[i][0].Empty()
				self.blockButtonList[i][1].Fill()

	def __OnClickBlock(self, block):
		net.SendChatPacket("/setblockmode " + str(constinfo.blockMode ^ block))
		self.RefreshBlock()

	def OnBlockMode(self, mode):
		constinfo.blockMode = mode
		self.RefreshBlock()

### EFEITOS DIRECTX ### EFEITOS DIRECTX ### EFEITOS DIRECTX ### EFEITOS DIRECTX ### EFEITOS DIRECTX ### EFEITOS DIRECTX ### EFEITOS DIRECTX ### 
	def __Aplicar(self):
		pos = self.GetChild("resolucao_slider").GetSliderPos()
		i = 1.0/float(len(self.RESOLUTION_LIST))
		res_index = int(pos/i)
		scale = 0.5 + 0.3*i*float(res_index)
		if not res_index == len(self.RESOLUTION_LIST):
			(width, height, bpp) = self.RESOLUTION_LIST[res_index]
			systemSetting.SetResolution(width, height)
			systemSetting.SaveConfig()

		if app.ADJUST_WINDOWS_SIZE_WITHOUT_CLOSING:
			app.AdjustWindowSize()
		else:
			app.Exit()
			startupinfo = STARTUPINFO()
			startupinfo.dwFlags |= _subprocess.STARTF_USESTDHANDLES
			if app.START_WITH_ARGUMENT:
				_subprocess.CreateProcess(sys.executable, "Adoaksdaj5siodq94jow123e", None, None, 1, 0, None, None, startupinfo)
			else:
				_subprocess.CreateProcess(sys.executable, "", None, None, 1, 0, None, None, startupinfo)

### PLAYER FUNCOES ### PLAYER FUNCOES ### PLAYER FUNCOES ### PLAYER FUNCOES ### PLAYER FUNCOES ### PLAYER FUNCOES ###
	def __CheckPvPProtectedLevelPlayer(self):
		if player.GetStatus(player.LEVEL)<constinfo.PVPMODE_PROTECTED_LEVEL:
			self.__SetPeacePKMode()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OPTION_PVPMODE_PROTECT % (constinfo.PVPMODE_PROTECTED_LEVEL))
			return 1
		return 0

	def __SetPKMode(self, mode):
		for btn in self.pvpModeButtonDict.values():
			btn.Empty()
		if self.pvpModeButtonDict.has_key(mode):
			self.pvpModeButtonDict[mode].Fill()

	def __SetPeacePKMode(self):
		self.__SetPKMode(player.PK_MODE_PEACE)

	def __RefreshPVPButtonList(self):
		self.__SetPKMode(player.GetPKMode())

	def __OnClickPvPModePeaceButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constinfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 0", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeRevengeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constinfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 1", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeFreeButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if constinfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 2", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OPTION_PVPMODE_NOT_SUPPORT)

	def __OnClickPvPModeGuildButton(self):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		self.__RefreshPVPButtonList()

		if 0 == player.GetGuildID():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
			return

		if constinfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode 4", chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.OPTION_PVPMODE_NOT_SUPPORT)

	def OnChangePKMode(self):
		self.__RefreshPVPButtonList()

	def __OnClickAlwaysShowNameOnButton(self):
		systemSetting.SetAlwaysShowNameFlag(True)
		self.RefreshAlwaysShowName()

	def __OnClickAlwaysShowNameOffButton(self):
		systemSetting.SetAlwaysShowNameFlag(False)
		self.RefreshAlwaysShowName()

	def RefreshAlwaysShowName(self):
		if systemSetting.IsAlwaysShowName():
			self.alwaysShowNameButtonList[0].Fill()
			self.alwaysShowNameButtonList[1].Empty()
		else:
			self.alwaysShowNameButtonList[0].Empty()
			self.alwaysShowNameButtonList[1].Fill()

	def __OnClickSalesTextOnButton(self):
		systemSetting.SetShowSalesTextFlag(1)
		systemSetting.SetHideShops(0)
		self.RefreshShowSalesText()
		uiprivateshopbuilder.UpdateADBoard()
		uiofflineshopbuilder.UpdateADBoard()

	def __OnClickSalesTextOffButton(self):
		systemSetting.SetShowSalesTextFlag(0)
		systemSetting.SetHideShops(1)
		self.RefreshShowSalesText()

	def RefreshShowSalesText(self):
		if systemSetting.IsShowSalesText():
			self.showsalesTextButtonList[0].Fill()
			self.showsalesTextButtonList[1].Empty()
		else:
			self.showsalesTextButtonList[0].Empty()
			self.showsalesTextButtonList[1].Fill()

	def __OnClickShowDamageOnButton(self):
		systemSetting.SetShowDamageFlag(True)
		self.RefreshShowDamage()

	def __OnClickShowDamageOffButton(self):
		systemSetting.SetShowDamageFlag(False)
		self.RefreshShowDamage()

	def RefreshShowDamage(self):
		if systemSetting.IsShowDamage():
			self.showDamageButtonList[0].Fill()
			self.showDamageButtonList[1].Empty()
		else:
			self.showDamageButtonList[0].Empty()
			self.showDamageButtonList[1].Fill()

	def __OnClickViewChat(self, flag):
		global viewChatMode
		viewChatMode = flag
		systemSetting.SetViewChatFlag(viewChatMode)
		self.RefreshViewChat()

	def RefreshViewChat(self):
		if systemSetting.IsViewChat():
			self.viewChatButtonList[0].Fill()
			self.viewChatButtonList[1].Empty()
		else:
			self.viewChatButtonList[0].Empty()
			self.viewChatButtonList[1].Fill()

	def __SetNameColorMode(self, index):
		constinfo.SET_CHRNAME_COLOR_INDEX(index)
		self.__ClickRadioButton(self.nameColorModeButtonList, index)

	def __SetTargetBoardViewMode(self, flag):
		constinfo.SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(flag)
		self.__ClickRadioButton(self.viewTargetButtonList, flag)

### DISPLAY FUNCOES ### DISPLAY FUNCOES ### DISPLAY FUNCOES ### DISPLAY FUNCOES ### DISPLAY FUNCOES ### DISPLAY FUNCOES 
	def __Change_Window_Size(self):
		pos = self.GetChild("resolucao_slider").GetSliderPos()
		i = 1.0/float(len(self.RESOLUTION_LIST))
		res_index = int(pos/i)
		scale = 0.5 + 0.3*i*float(res_index)
		if not res_index == len(self.RESOLUTION_LIST):
			(width, height, bpp) = self.RESOLUTION_LIST[res_index]
			self.GetChild("resolucao_slider_title").SetText(str(width)+":"+str(height))
			self.GetChild("resolucao_imagem").SetScale(scale, scale)
			self.GetChild("resolucao_imagem").SetWindowHorizontalAlignCenter()
			# systemSetting.SetResolution(width, height)
			# systemSetting.SaveConfig()

	def ReLoad_3D_Settings(self):
		self.RESOLUTION_LIST = []
		self.RESOLUTION_CONT = systemSetting.GetResolutionCount()
		for i in xrange(self.RESOLUTION_CONT):
			width, height, bpp = systemSetting.GetResolution(i)
			if bpp == 32 and width > 800:
				self.RESOLUTION_LIST.append(systemSetting.GetResolution(i))
			elif bpp == 32 and width == 800 and height == 600 and systemSetting.IsWindowed():
				self.RESOLUTION_LIST.append([1032, 600, 32])
# SETA O NOME DA RESOLUCAO CORRENTE #
		self.cur_width, self.cur_height, self.cur_bpp = systemSetting.GetCurrentResolution()
		self.GetChild("resolucao_slider_title").SetText("|cfff8d090"+str(self.cur_width)+":"+str(self.cur_height))
# BUSCA NA LISTA DE RESOLUCOES A RESOLUCAO CORRENTE
		resolution_index = -1
		len_res = len(self.RESOLUTION_LIST)
		for i in xrange(len_res):
			w, h, b = self.RESOLUTION_LIST[i]
			if w == self.cur_width and h == self.cur_height:
				resolution_index = i
				break
		if resolution_index == -1:
			self.GetChild("resolucao_slider_title").SetText("|cfff8d090Resolução Fora do Padão! "+str(self.cur_width)+":"+str(self.cur_height))
		else:
			self.GetChild("resolucao_slider").SetSliderPos((1.0/float(len_res))*float(resolution_index))
### REGULA A EXIBICAO DA IMAGEM
		pos = self.GetChild("resolucao_slider").GetSliderPos()
		i = 1.0/float(len(self.RESOLUTION_LIST))
		res_index = int(pos/i)
		scale = 0.5 + 0.3*i*float(res_index)
		self.GetChild("resolucao_imagem").SetScale(scale, scale)
		self.GetChild("resolucao_imagem").SetWindowHorizontalAlignCenter()

	def __Change_Window_Mode(self, index):
		self.__ClickRadioButton(self.WindowModeButtonList, index)
		if index == 0:
			systemSetting.SetWindowed()
		else:
			systemSetting.NoWindowed()
		self.ReLoad_3D_Settings()
		self.__Change_Window_Size()
		systemSetting.SaveConfig()

### CAMERA FUNCOES ### CAMERA FUNCOES ### CAMERA FUNCOES ### CAMERA FUNCOES ### CAMERA FUNCOES ### CAMERA FUNCOES ###
	def __Sombra(self, index):
		self.__ClickRadioButton(self.SombraModeButtonList, index)
		index = index + 1
		systemSetting.SetShadowLevel(index)
		systemSetting.SaveConfig()

	def __CameraMax(self):
		pos = self.GetChild("camera_max_slider").GetSliderPos()
		per = self.GetChild("camera_max_slider").GetPercent()
		self.GetChild("camera_max_slider_percent").SetText("|cfff8d090"+str(per)+"%")
		index = 2500.0 + (4000.0 * float(pos))
		app.SetCameraMaxDistance(index)
		constinfo.SetCameraSetting(0, index)

	def __Neblina(self):
		pos = self.GetChild("neblina_slider").GetSliderPos()
		per = self.GetChild("neblina_slider").GetPercent()
		self.GetChild("neblina_slider_percent").SetText("|cfff8d090"+str(per)+"%")
		neblina = (30000 - (25000 * pos))
		app.SetMinFog(neblina)
		constinfo.SetCameraSetting(1, neblina)

### AUDIO FUNCOES ### AUDIO FUNCOES ### AUDIO FUNCOES ### AUDIO FUNCOES ### AUDIO FUNCOES ### AUDIO FUNCOES ### 
	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:
			self.musicListDlg = uiselectmusic.FileListDialog()
			self.musicListDlg.SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText("|cfff8d090"+fileName)
		if musicinfo.fieldMusic != "":
			snd.FadeOutMusic("bgm/"+ musicinfo.fieldMusic)

		if fileName == uiselectmusic.DEFAULT_THEMA:
			musicinfo.fieldMusic = musicinfo.METIN2THEMA
		else:
			musicinfo.fieldMusic = fileName

		musicinfo.SaveLastPlayFieldMusic()

		if musicinfo.fieldMusic != "":
			snd.FadeInMusic("bgm/" + musicinfo.fieldMusic)

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		per = self.ctrlMusicVolume.GetPercent()
		snd.SetMusicVolume(pos * 1.0)
		systemSetting.SetMusicVolume(pos)
		self.GetChild("music_slider_percent").SetText("|cfff8d090"+str(per)+"%")
		if per == 0:
			self.GetChild("music_1").Hide()
			self.GetChild("music_2").Hide()
			self.GetChild("music_3").Hide()
			self.GetChild("music_x").Show()
		elif per <= 30:
			self.GetChild("music_1").Show()
			self.GetChild("music_2").Hide()
			self.GetChild("music_3").Hide()
			self.GetChild("music_x").Hide()
		elif per <= 60:
			self.GetChild("music_1").Show()
			self.GetChild("music_2").Show()
			self.GetChild("music_3").Hide()
			self.GetChild("music_x").Hide()
		else:
			self.GetChild("music_1").Show()
			self.GetChild("music_2").Show()
			self.GetChild("music_3").Show()
			self.GetChild("music_x").Hide()

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		per = self.ctrlSoundVolume.GetPercent()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)
		self.GetChild("audio_slider_percent").SetText("|cfff8d090"+str(per)+"%")
		if per == 0:
			self.GetChild("audio_1").Hide()
			self.GetChild("audio_2").Hide()
			self.GetChild("audio_3").Hide()
			self.GetChild("audio_x").Show()
		elif per <= 30:
			self.GetChild("audio_1").Show()
			self.GetChild("audio_2").Hide()
			self.GetChild("audio_3").Hide()
			self.GetChild("audio_x").Hide()
		elif per <= 60:
			self.GetChild("audio_1").Show()
			self.GetChild("audio_2").Show()
			self.GetChild("audio_3").Hide()
			self.GetChild("audio_x").Hide()
		else:
			self.GetChild("audio_1").Show()
			self.GetChild("audio_2").Show()
			self.GetChild("audio_3").Show()
			self.GetChild("audio_x").Hide()

### MAIN FUNCOES ### MAIN FUNCOES ### MAIN FUNCOES ### MAIN FUNCOES ### MAIN FUNCOES ### MAIN FUNCOES ### MAIN FUNCOES ### 
	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __LoadWindow(self):
		self.__LoadScript("uiscript/configdialog.py")
		self.__BindObject()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()
		self.__Initialize()

	def Close(self):
		constinfo.SaveCameraSettings()
		systemSetting.SaveConfig()
		self.Hide()

	def Show(self):
		ui.ScriptWindow.Show(self)
		self.board.Show()

	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton = buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.Empty()

		selButton.Fill()

	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	def SetState(self, stateKey):
		self.state = stateKey

		for pageValue in self.pageDict.itervalues():
			pageValue.Hide()
		self.pageDict[stateKey].Show()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.Enable()
		self.tabButtonDict[stateKey].Disable()

	def GetState(self):
		return self.state

	def OnPressEscapeKey(self):
		self.Close()
		return True

class STARTUPINFO:
	dwFlags = 0
	hStdInput = None
	hStdOutput = None
	hStdError = None
	wShowWindow = 0

# a = GameOptions()
# a.Show()