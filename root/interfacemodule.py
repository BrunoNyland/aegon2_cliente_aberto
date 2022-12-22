#favor manter essa linha
import XXjvumrgrYBZompk3PS8 as item
import LURMxMaKZJqliYt2QSHG as chat
import enszxc3467hc3kokdueq as app
import ga3vqy6jtxqi9yf344j7 as player
import constinfo
import systemSetting
import wndMgr
import uichat
import uimessenger
import ui
import uiwhisper
import uishop
import uiexchange
import uisystem
import uisystem_center
import uirestart
import uitooltip
import uiminimap
import uiparty
import uisafebox
import uiguild
import uiquest
import uiprivateshopbuilder
import uicommon
import uirefine
import uiequipmentdialog
import uigamebutton
import uitip
import uiofflineshop
import uiofflineshopbuilder
import event
import localeinfo
import uiantimacro
import boot
import uisiegewar

if app.ENABLE_DROP_COFRE:
	import uichestdrop

if app.ALUGAR_ITENS:
	import uirentinputdialog

if app.ENABLE_INVENTORY_VIEWER:
	import uiinventoryviewer

if constinfo.NEW_TASKBAR:
	import ztaskbar as uitaskbar
else:
	import uitaskbar

if constinfo.NEW_CHARACTER:
	import zcharacter as uicharacter
else:
	import uicharacter

import zinventory as uiinventory


IsQBHide = 0
IsWisperHide = 0

class Interface(object):
	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		self.onTopWindow = player.ON_TOP_WND_NONE
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndBot = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndSiegeWarEnter = None
		self.wndSiegeWarScore = None
		self.WndAntRobo = None
		self.WndAntRoboTimer = None

		if app.ENABLE_DROP_COFRE:
			self.dlgChestDrop = None

		if app.ALUGAR_ITENS:
			self.RentTimeDialog = None

		if app.ENABLE_INVENTORY_VIEWER:
			self.wndInventoryViewer = None

		self.listGMName = {}
		self.wndQuestWindow = []
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		self.offlineShopAdvertisementBoardDict = {}
		event.SetInterfaceWindow(self)

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uimessenger.MessengerWindow()
		self.wndMessenger.SetWhisperButtonEvent(self.OpenWhisperDialog)
		self.wndMessenger.SetGuildButtonEvent(self.ToggleGuildWindow)

	def __MakeGuildWindow(self):
		self.wndGuild = uiguild.GuildWindow()

	def __MakeChatWindow(self):
		wndChat = uichat.ChatWindow()
		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)

		self.wndChat.btnSendWhisper.SetEvent(self.OpenWhisperDialogWithoutTarget)
		self.wndChat.btnChatLog.SetEvent(self.ToggleChatLogWindow)

	def __MakeTaskBar(self):
		wndTaskBar = uitaskbar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar

		self.wndTaskBar.SetToggleButtonEvent(uitaskbar.TaskBar.BUTTON_CHARACTER, self.ToggleCharacterWindowStatusPage)
		self.wndTaskBar.SetToggleButtonEvent(uitaskbar.TaskBar.BUTTON_INVENTORY, self.ToggleInventoryWindow)
		self.wndTaskBar.SetToggleButtonEvent(uitaskbar.TaskBar.BUTTON_MESSENGER, self.ToggleMessenger)
		self.wndTaskBar.SetToggleButtonEvent(uitaskbar.TaskBar.BUTTON_SYSTEM, self.ToggleSystemDialog)
		self.wndTaskBar.SetToggleButtonEvent(uitaskbar.TaskBar.BUTTON_CHAT, self.ToggleChat)

	def __MakeParty(self):
		wndParty = uiparty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty
		self.wndParty.WhisperEvent = ui.__mem_func__(self.OpenWhisperDialog)

	def __MakeGameButtonWindow(self):
		wndGameButton = uigamebutton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", self.__OnClickStatusPlusButton)
		wndGameButton.SetButtonEvent("SKILL", self.__OnClickSkillPlusButton)
		wndGameButton.SetButtonEvent("QUEST", self.__OnClickQuestButton)

		self.wndGameButton = wndGameButton

	def __MakeMiniMap(self):
		wndMiniMap = uiminimap.MiniMap()
		self.wndMiniMap = wndMiniMap

	def __MakeWindows(self):
		wndCharacter = uicharacter.CharacterWindow()
		self.wndCharacter = wndCharacter

		wndInventory = uiinventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)
		self.wndInventory = wndInventory

		self.wndBot = boot.Bot()
		self.wndBot.EnableInventoryTweak(self.wndInventory)
		self.wndInventory.SetEventClickBot(self.OpenWndBot)

		wndSafebox = uisafebox.SafeboxWindow()
		wndSafebox.BindInterface(self)
		self.wndSafebox = wndSafebox

		wndChatLog = uichat.ChatLogWindow()
		wndChatLog.BindInterface(self)
		self.wndChatLog = wndChatLog

		self.WndAntRobo = uiantimacro.Anti_Robotics_Window()
		self.WndAntRoboTimer = uiantimacro.TimeManager()
		self.WndAntRobo.SetTimeManager(self.WndAntRoboTimer)
		self.WndAntRoboTimer.SetWindow(self.WndAntRobo)
		self.WndAntRobo.Show()

		self.wndSiegeWarEnter = uisiegewar.SiegeWarEnter()
		self.wndSiegeWarScore = uisiegewar.SiegeWarScore()

		if app.ALUGAR_ITENS:
			self.RentTimeDialog = uirentinputdialog.RentTimeDialog()

		if app.ENABLE_INVENTORY_VIEWER:
			self.wndInventoryViewer = uiinventoryviewer.InventoryWindow()
			self.wndInventoryViewer.BindInterfaceClass(self)

	def __MakeDialogs(self):
		self.dlgExchange = uiexchange.ExchangeDialog()
		self.dlgExchange.BindInterface(self)
		self.dlgExchange.SetInven(self.wndInventory)
		self.dlgExchange.OpenWhisperDialog = ui.__mem_func__(self.OpenWhisperDialog)
		self.dlgExchange.ToggleInventoryWindow = ui.__mem_func__(self.ToggleInventoryWindow)
		self.wndInventory.BindWindow(self.dlgExchange)

		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()

		self.dlgShop = uishop.ShopDialog()
		self.dlgShop.BindInterface(self)
		self.dlgShop.LoadDialog()
		self.dlgShop.Hide()

		self.dlgOfflineShop = uiofflineshop.OfflineShopDialog()
		self.dlgOfflineShop.LoadDialog()
		self.dlgOfflineShop.Hide()

		self.dlgRestart = uirestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uisystem.SystemDialog()
		self.dlgSystem.SetInterface(self)
		self.dlgSystem.LoadDialog()

		self.dlgSystem.Hide()

		self.dlgSystemC = uisystem_center.SystemDialogCenter()
		self.dlgSystemC.SetInterface(self)
		self.dlgSystemC.LoadDialog()

		self.dlgSystemC.Hide()

		self.dlgPassword = uisafebox.PasswordDialog()
		self.dlgPassword.Hide()

		if app.ENABLE_FLAGS_CHAT:
			self.hyperlinkTooltip = uitooltip.HyperlinkToolTip()
			self.hyperlinkTooltip.Hide()

		self.hyperlinkItemTooltip = uitooltip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uitooltip.ItemToolTip()
		self.tooltipItem.Hide()

		self.tooltipSkill = uitooltip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.privateShopBuilder = uiprivateshopbuilder.PrivateShopBuilder()
		self.privateShopBuilder.BindInterface(self)
		self.privateShopBuilder.SetInven(self.wndInventory)
		self.wndInventory.BindWindow(self.privateShopBuilder)
		self.privateShopBuilder.Hide()

		self.offlineShopBuilder = uiofflineshopbuilder.OfflineShopBuilder()
		self.offlineShopBuilder.Hide()

		self.dlgRefineNew = uirefine.RefineDialogNew()
		self.dlgRefineNew.SetInven(self.wndInventory)
		self.wndInventory.BindWindow(self.dlgRefineNew)
		self.dlgRefineNew.Hide()

		if app.ENABLE_DROP_COFRE:
			self.dlgChestDrop = uichestdrop.ChestDropWindow()
			self.dlgChestDrop.SetItemToolTip(self.tooltipItem)

	def __MakeTipBoard(self):
		self.tipBoard = uitip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uitip.BigBoard()
		self.bigBoard.Hide()

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeMiniMap()
		self.__MakeGameButtonWindow()

		self.__MakeTipBoard()

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		self.wndBot.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		if constinfo.NEW_CHARACTER:
			self.wndCharacter.SetGuildNameSlotEvent(self.ToggleGuildWindow)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)
		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		self.dlgOfflineShop.SetItemToolTip(self.tooltipItem)
		self.offlineShopBuilder.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_GUILD_SAFEBOX:
			self.wndGuild.wndSafebox.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_INVENTORY_VIEWER:
			self.wndInventoryViewer.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()

	if app.ENABLE_FLAGS_CHAT:
		def HyperlinkTooltip(self, hyperlink):
			if hyperlink:
				if hyperlink.find("#") >= 0:
					check = hyperlink.split("#")
					if check and len(check):
						tok = check[1]
						token = tok.split(":")
						if token and len(token):
							type = token[0]
							if "lang" == type or "reino" == type or "race" == type or "msg" == type:
								self.hyperlinkTooltip.SetHyperlink(check[1])
			else:
				self.hyperlinkTooltip.HideHyperlink()

	def MakeHyperlinkTooltip(self, hyperlink):
		if hyperlink:
			if app.ENABLE_FLAGS_CHAT:
				if hyperlink.find("#") >= 0:
					check = hyperlink.split("#")
					if check and len(check):
						tok = check[1]
						token = tok.split(":")
						if token and len(token):
							typ = token[0]
							if "msg" == typ:
								self.OpenWhisperDialog(str(token[1]))
						return

			tokens = hyperlink.split(":")
			if tokens and len(tokens):
				type = tokens[0]
				if "item" == type:
					self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
				elif "web" == type:
					app.ExecuteShell(tokens[1].replace("w<?", "://"))

	def Close(self):
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if uiquest.QuestDialog.__dict__.__contains__("QuestCurtain"):
			uiquest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for eachQuestWindow in self.wndQuestWindow:
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None

		if self.wndChat:
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndBot:
			self.wndBot.Destroy()

		if self.wndInventory:
			self.wndInventory.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgSystemC:
			self.dlgSystemC.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if self.WndAntRobo:
			self.WndAntRobo.Destroy()

		if self.wndSiegeWarEnter:
			self.wndSiegeWarEnter.Destroy()

		if self.wndSiegeWarScore:
			self.wndSiegeWarScore.Destroy()

		if self.WndAntRoboTimer:
			self.WndAntRoboTimer.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()

		if self.dlgOfflineShop:
			self.dlgOfflineShop.Destroy()

		if self.offlineShopBuilder:
			self.offlineShopBuilder.Destroy()

		if app.ENABLE_DROP_COFRE:
			if self.dlgChestDrop:
				self.dlgChestDrop.Destroy()

		if app.ALUGAR_ITENS:
			if self.RentTimeDialog:
				self.RentTimeDialog.Destroy()

		if app.ENABLE_INVENTORY_VIEWER:
			if self.wndInventoryViewer:
				self.wndInventoryViewer.Destroy()

		self.wndChatLog.Destroy()

		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.values():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.values():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.values():
			dlg.Destroy()

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.wndTaskBar
		del self.wndCharacter
		del self.wndInventory
		del self.wndBot
		del self.dlgExchange
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgSystemC
		del self.dlgPassword
		if app.ENABLE_FLAGS_CHAT:
			del self.hyperlinkTooltip
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndParty
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.dlgOfflineShop
		del self.WndAntRobo
		del self.WndAntRoboTimer
		del self.wndSiegeWarEnter
		del self.wndSiegeWarScore

		if app.ENABLE_DROP_COFRE:
			if self.dlgChestDrop:
				del self.dlgChestDrop

		if app.ALUGAR_ITENS:
			del self.RentTimeDialog

		if app.ENABLE_INVENTORY_VIEWER:
			if self.wndInventoryViewer:
				del self.wndInventoryViewer

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		self.offlineShopAdvertisementBoardDict = {}

		uichat.DestroyChatInputSetWindow()

	def OpenWndBot(self):
		self.wndBot.Show()

	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	if app.SKILL_COOLTIME_UPDATE:
		def SkillClearCoolTime(self, slotIndex):
			self.wndCharacter.SkillClearCoolTime(slotIndex)
			self.wndTaskBar.SkillClearCoolTime(slotIndex)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()

	def RefreshInventory(self):
		self.wndInventory.RefreshGold()
		self.wndInventory.RefreshItemSlot()

	def UpdateAveragePrice(self, price, mode):
		if (int(mode) == int(1)) and self.privateShopBuilder:
			self.privateShopBuilder.UpdateAveragePrice(price)
		elif (int(mode) == int(2)) and self.offlineShopBuilder:
			self.offlineShopBuilder.UpdateAveragePrice(price)
		elif (int(mode) == int(3)):
			self.wndInventory.uiofflineshopWnd.wndOfflineShopAddItem.UpdateAveragePrice(price)
		elif (int(mode) == int(4)):
			self.wndInventory.uiofflineshopWnd.wndOfflineShopChangePrice.UpdateAveragePrice(price)

	def UpdateEXPMode(self, mode):
		if self.wndTaskBar:
			self.wndTaskBar.UpdateEXPMode(mode)

	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def SetBlockExpMode(self, mode):
		self.wndTaskBar.SetBlockExperience(mode)

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	if app.ENABLE_GUILD_SAFEBOX:
		def RefreshGuildSafebox(self):
			self.wndGuild.wndSafebox.RefreshGuildSafebox()

		def RefreshGuildSafeboxMoney(self):
			self.wndGuild.wndSafebox.RefreshGuildSafeboxMoney()

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)
		self.dlgSystemC.OnBlockMode(mode)

	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	if app.ENABLE_DROP_COFRE:
		def RefreshChestDropInfo(self, chestVnum):
			self.dlgChestDrop.RefreshItems(chestVnum)

	def OpenOfflineShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgOfflineShop.Open(vid)
		self.dlgOfflineShop.SetTop()

	def CloseOfflineShopDialog(self):
		self.dlgOfflineShop.Close()

	def RefreshOfflineShopDialog(self):
		self.dlgOfflineShop.Refresh()

	def RefreshOfflineShopMoney(self, value):
		if self.wndInventory.uiofflineshopWnd.wndOfflineShopMyBank:
			self.wndInventory.uiofflineshopWnd.wndOfflineShopMyBank.UpdateMoneyString(value)

	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):
		wnds = ()
		q = uiquest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda s = self, qw = q: s.__dict__.__getitem__("wndQuestWindow").remove(qw))
		self.wndQuestWindow.append(q)

	def StartExchange(self, level, race, guild):
		self.dlgExchange.OpenDialog(level, race, guild)
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	def CantTradableItemExchange(self, dstSlotIndex, srcSlotIndex):
		self.dlgExchange.CantTradableItem(dstSlotIndex, srcSlotIndex)

	def CanTradableItemExchange(self, srcSlotIndex):
		self.dlgExchange.CanTradableItem(srcSlotIndex)

	def AddPartyMember(self, pid, name, race, online):
		self.wndParty.AddPartyMember(pid, name, race, online)

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)
		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	#Salvar Senha Ao abrir
	def InitSafeboxPassword(self):
		self.dlgPassword.InitSafeboxPassword()
	# def AskSafeboxPassword(self):
		# if self.wndSafebox.IsShow():
			# return

		# self.dlgPassword.SetTitle(localeinfo.PASSWORD_TITLE)
		# self.dlgPassword.SetSendMessage("/safebox_password ")
		# self.dlgPassword.ShowDialog()

	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		if self.dlgPassword.IsShow():
			self.dlgPassword.CloseDialog()
			return

		self.dlgPassword.SetSendMessage("/safebox_password ")
		if self.dlgPassword.GetSafeboxPwd() != "":
			self.dlgPassword.OnAccept()
			return

		self.dlgPassword.SetTitle(localeinfo.PASSWORD_TITLE)
		self.dlgPassword.ShowDialog()
	#Final Salvar Senha Ao abrir

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	def OnStartGuildWar(self, guildSelf, guildOpp):
		key = uiguild.GetGVGKey(guildSelf, guildOpp)
		if self.guildScoreBoardDict.__contains__(key):
			self.guildScoreBoardDict[key].Hide()

		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)
		guildWarScoreBoard = uiguild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[key] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiguild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.__contains__(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiguild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.__contains__(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiguild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.__contains__(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndChat.Show()
		self.wndMiniMap.Show()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndCharacter:
			self.wndCharacter.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if app.ALUGAR_ITENS:
			if self.RentTimeDialog:
				self.RentTimeDialog.Hide()

		if app.ENABLE_INVENTORY_VIEWER:
			if self.wndInventoryViewer:
				self.wndInventoryViewer.Hide()

	def ToggleChat(self):
		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	def OpenRestartDialog(self, d_time):
		self.dlgRestart.OpenDialog(d_time)
		self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def ToggleSystemCDialog(self):
		if False == self.dlgSystemC.IsShow():
			self.dlgSystemC.OpenDialog()
			self.dlgSystemC.SetTop()
		else:
			self.dlgSystemC.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def OpenSystemCDialog(self):
		self.dlgSystemC.OpenDialog()
		self.dlgSystemC.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()
		else:
			self.ToggleMiniMap()

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state = "STATUS"):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if player.IsObserverMode():
			return

		if self.wndInventory.IsShow():
			self.wndInventory.OverOutItem()
			self.wndInventory.Hide()
		else:
			self.wndInventory.Show()
			self.wndInventory.SetTop()

	def ToggleOfflineShopAdminPanelWindow(self):
		if self.wndOfflineShopAdminPanel.IsShow():
			self.wndOfflineShopAdminPanel.Close()
		else:
			self.wndOfflineShopAdminPanel.Show()

	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	def OpenPrivateShopInputNameDialog(self):
		inputDialog = uicommon.InputDialog()
		inputDialog.SetTitle(localeinfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(self.OpenPrivateShopBuilder)
		inputDialog.SetCancelEvent(self.ClosePrivateShopInputNameDialog)
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):
		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):
		board = uiprivateshopbuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)
		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):
		if not self.privateShopAdvertisementBoardDict.__contains__(vid):
			return
		del self.privateShopAdvertisementBoardDict[vid]
		uiprivateshopbuilder.DeleteADBoard(vid)

	def OpenOfflineShopInputNameDialog(self):
		inputDialog = uiofflineshop.OfflineShopInputDialog()
		inputDialog.SetAcceptEvent(self.OpenOfflineShopBuilder)
		inputDialog.SetCancelEvent(self.CloseOfflineShopInputNameDialog)
		inputDialog.Open()
		self.inputDialog = inputDialog

	def CloseOfflineShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenOfflineShopBuilder(self):
		if (not self.inputDialog):
			return True

		if (not len(self.inputDialog.GetTitle())):
			return True

		self.offlineShopBuilder.Open(self.inputDialog.GetTitle())
		self.CloseOfflineShopInputNameDialog()
		return True

	def AppearOfflineShop(self, vid, text):
		board = uiofflineshopbuilder.OfflineShopAdvertisementBoard()
		board.Open(vid, text)
		self.offlineShopAdvertisementBoardDict[vid] = board

	def DisappearOfflineShop(self, vid):
		if (not self.offlineShopAdvertisementBoardDict.__contains__(vid)):
			return
		del self.offlineShopAdvertisementBoardDict[vid]
		uiofflineshopbuilder.DeleteADBoard(vid)

	def OpenEquipmentDialog(self, vid):
		dlg = uiequipmentdialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(self.CloseEquipmentDialog)
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		self.BINARY_RecvQuest(index, name, "file", localeinfo.GetLetterImageName())

	def BINARY_RecvQuest(self, index, name, iconType, iconName):
		# chat.AppendChat(chat.CHAT_TYPE_INFO, "Quest Recebida: " + str(name))

		btn = self.__FindQuestButton(index)

		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiwhisper.WhisperButton()

		if "item" == iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName = item.GetIconImageFileName()
		else:
			buttonImageFileName = iconName

		if "highlight" == iconType:
			btn.SetUpVisual("locale/ymir_ui/highlighted_quest.tga")
			btn.SetOverVisual("locale/ymir_ui/highlighted_quest_r.tga")
			btn.SetDownVisual("locale/ymir_ui/highlighted_quest_r.tga")
		else:
			btn.SetUpVisual(localeinfo.GetLetterCloseImageName())
			btn.SetOverVisual(localeinfo.GetLetterOpenImageName())
			btn.SetDownVisual(localeinfo.GetLetterOpenImageName())

		btn.SetToolTipText(name, -20, 35)
		btn.ToolTipText.SetHorizontalAlignLeft()
		btn.SetEvent(self.__StartQuest, btn)
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				btn.Show()

	def __StartQuest(self, btn):
		event.QuestButtonClick(btn.index)
		self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn
		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()

	def HideAllQuestWindow(self):
		for obj in self.wndQuestWindow:
			obj.OnClose()

	def __InitWhisper(self):
		chat.InitWhisper(self)

	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiwhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper
			self.windowOpenPosition = (self.windowOpenPosition+1) % 5
		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.__contains__(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	def OpenWhisperDialog(self, name):
		if not self.whisperDialogDict.__contains__(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name, True)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, mode, name, line, loadMsg):
		if loadMsg:
			for text in constinfo.WHISPER_MESSAGES[name]:
				chat.AppendWhisper(text[0], name, text[1])

		if not self.whisperDialogDict.__contains__(name):
			btn = self.FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()
				app.FlashApplication()
				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeinfo.RECEIVE_MESSAGE % (name))
			else:
				btn.Flash()
				app.FlashApplication()

		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except BaseException:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")
		self.__DestroyWhisperButton(btn)


	def MinimizeWhisperDialog(self, name):
		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):
		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except BaseException:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):
		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	def FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiwhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper
		self.windowOpenPosition = (self.windowOpenPosition+1) % 5
		return dlgWhisper

	def __MakeWhisperButton(self, name):
		whisperButton = uiwhisper.WhisperButton()
		whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(self.ShowWhisperDialog, whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.__contains__(name):
			return
		if self.whisperDialogDict.__contains__(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.__contains__(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.__contains__(name):
			return True
		else:
			return False

	if app.ENABLE_DEFENSE_WAVE:
		def BINARY_Update_Mast_HP(self, hp):
			self.wndMiniMap.SetMastHP(hp)

		def BINARY_Update_Mast_Window(self, i):
			self.wndMiniMap.SetMastWindow(i)

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1
		return 0

	def GetInventoryPageIndex(self):
		if self.wndInventory:
			return self.wndInventory.GetInventoryPageIndex()
		else:
			return -1

	def SetOnTopWindow(self, onTopWnd):
		self.onTopWindow = onTopWnd

	def GetOnTopWindow(self):
		return self.onTopWindow

	def RefreshMarkInventoryBag(self):
		self.wndInventory.RefreshMarkSlots()