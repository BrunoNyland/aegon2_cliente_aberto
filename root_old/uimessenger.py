#favor manter essa linha
import enszxc3467hc3kokdueq as app
import zn94xlgo573hf8xmddzq as net
import ui
import grp
import guild
import messenger
import localeinfo
import uitooltip
import exception
import uipopup
import uicommon

FRIEND = 0
GUILD = 1
TEAM = 2

class MessengerItem(ui.Bar):
	def __init__(self, getParentEvent):
		ui.Bar.__init__(self)
		self.SetParent(getParentEvent())
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))

		self.separator = ui.HorizontalSeparator()
		self.separator.SetParent(self)
		self.separator.SetPosition(-1, -3)
		self.separator.SetWidth(160)
		self.separator.Hide()

		self.AddFlag("float")

		self.name = ""
		self.image = ui.ImageBox()
		self.image.AddFlag("not_pick")
		self.image.SetParent(self)
		self.image.Show()

		self.text = ui.TextLine()
		self.text.SetPackedFontColor(0xffa08784)
		self.text.SetParent(self)
		self.text.SetPosition(10, 1)
		self.text.Show()

		self.lovePoint = -1
		self.lovePointToolTip = None

		self.isSelected = False
		self.wasShowed = False

		self.getParentEvent = getParentEvent

	#Amigo System
	def SetShowed(self):
		self.wasShowed = True

	def SetUnShowed(self):
		self.wasShowed = False

	def WasShowed(self):
		return self.wasShowed
	#Amigo System Final

	def SetName(self, name):
		self.name = name
		if name:
			self.text.SetTextLimited(name, 130)

	def SetLovePoint(self, lovePoint):
		self.lovePoint = lovePoint

	def Select(self):
		self.isSelected = True

	def UnSelect(self):
		self.isSelected = False

	def GetName(self):
		return self.name

	def GetStepWidth(self):
		return 8

	def GetStepHeight(self):
		return 0

	def CanWhisper(self):
		return False

	def IsOnline(self):
		return False

	def OnWhisper(self):
		pass

	def CanRemove(self):
		return False

	def OnRemove(self):
		return False

	def CanWarp(self):
		return False

	def OnWarp(self):
		pass

	def OnMouseOverIn(self):
		if -1 != self.lovePoint:
			if not self.lovePointToolTip:
				self.lovePointToolTip = uitooltip.ToolTip(160)
				self.lovePointToolTip.SetTitle(self.name)
				self.lovePointToolTip.AppendTextLine(localeinfo.AFF_LOVE_POINT % (self.lovePoint))
				self.lovePointToolTip.ResizeToolTip()
			self.lovePointToolTip.ShowToolTip()

	def OnMouseOverOut(self):
		if self.lovePointToolTip:
			self.lovePointToolTip.HideToolTip()

	def OnMouseLeftButtonDown(self):
		self.getParentEvent().OnSelectItem(self)

	def OnMouseLeftButtonDoubleClick(self):
		self.getParentEvent().OnDoubleClickItem(self)

class MessengerMemberItem(MessengerItem):
	STATE_OFFLINE = 0
	STATE_ONLINE = 1

	IMAGE_FILE_NAME = {
		"ONLINE" : "interface/controls/special/friendlist/online.tga",
		"OFFLINE" : "interface/controls/special/friendlist/offline.tga"
	}

	def __init__(self, getParentEvent):
		MessengerItem.__init__(self, getParentEvent)
		self.key = None
		self.state = self.STATE_OFFLINE
		self.SetSize(144, 17)
		self.image.SetPosition(-10, 0)
		self.Offline()

	def GetStepWidth(self):
		return 22

	def GetStepHeight(self):
		return 21

	def SetKey(self, key):
		self.key = key

	def IsSameKey(self, key):
		return self.key == key

	def IsOnline(self):
		if self.STATE_ONLINE == self.state:
			return True
		return False

	def Online(self):
		self.text.SetPackedFontColor(0xfff8d090)
		self.image.LoadImage(self.IMAGE_FILE_NAME["ONLINE"])
		self.state = self.STATE_ONLINE

	def Offline(self):
		self.text.SetPackedFontColor(0xffff8784)
		self.image.LoadImage(self.IMAGE_FILE_NAME["OFFLINE"])
		self.state = self.STATE_OFFLINE

	def CanWhisper(self):
		if self.IsOnline():
			return True
		return False

	def OnWhisper(self):
		if self.IsOnline():
			if self.getParentEvent().whisperButtonEvent:
				self.getParentEvent().whisperButtonEvent(self.GetName())

	def Select(self):
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.4))
		MessengerItem.Select(self)

	def UnSelect(self):
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))
		MessengerItem.UnSelect(self)

class MessengerGroupItem(MessengerItem):

	IMAGE_FILE_NAME = {
		"OPEN" : "interface/controls/special/friendlist/opened.png",
		"CLOSE" : "interface/controls/special/friendlist/closed.png",
	}

	def __init__(self, getParentEvent):
		self.isOpen = False
		self.memberList = []
		MessengerItem.__init__(self, getParentEvent)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.8))
		self.SetSize(158, 24)
		self.text.SetPosition(25, 2)
		self.text.SetFontName('Verdana:14b')
		self.image.SetPosition(5, 0)
		self.image.SetWindowVerticalAlignCenter()
		self.separator.Show()

	def AppendMember(self, member, key, name):
		# for i in xrange(len(self.memberList)):
			# self.memberList[i].SetNormal()
		member.SetKey(key)
		member.SetName(name)
		# member.SetLast()
		self.memberList.append(member)
		return member

	def RemoveMember(self, item):
		for i in xrange(len(self.memberList)):
			if item == self.memberList[i]:
				del self.memberList[i]
				break

	def ClearMember(self):
		self.memberList = []

	def FindMember(self, key):
		list = filter(lambda argMember, argKey=key: argMember.IsSameKey(argKey), self.memberList)
		if list:
			return list[0]

		return None

	def GetLoginMemberList(self):
		return filter(MessengerMemberItem.IsOnline, self.memberList)

	def GetLogoutMemberList(self):
		return filter(lambda arg: not arg.IsOnline(), self.memberList)

	def IsOpen(self):
		return self.isOpen

	def Open(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["OPEN"])
		self.isOpen = True

	def Close(self):
		self.image.LoadImage(self.IMAGE_FILE_NAME["CLOSE"])
		self.isOpen = False

		map(ui.Bar.Hide, self.memberList)

	def GetStepHeight(self):
		return 26

	def Select(self):
		if self.IsOpen():
			self.Close()
		else:
			self.Open()

		self.getParentEvent().OnRefreshList()

	def OnMouseOverIn(self):
		self.SetColor(grp.GenerateColor(0.05, 0.05, 0.05, 1.0))

	def OnMouseOverOut(self):
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.8))

class MessengerFriendItem(MessengerMemberItem):
	def __init__(self, getParentEvent):
		MessengerMemberItem.__init__(self, getParentEvent)

	def CanRemove(self):
		return True

	def OnRemove(self):
		messenger.RemoveFriend(self.key)
		net.SendMessengerRemovePacket(self.key, self.name)
		return True

class MessengerTeamItem(MessengerMemberItem):
	def __init__(self, getParentEvent):
		MessengerMemberItem.__init__(self, getParentEvent)

	def CanRemove(self):
		return False

	def OnRemove(self):
		messenger.RemoveFriend(self.key)
		net.SendMessengerRemovePacket(self.key, self.name)
		return False

class MessengerGuildItem(MessengerMemberItem):
	def __init__(self, getParentEvent):
		MessengerMemberItem.__init__(self, getParentEvent)

	def CanWarp(self):
		if not self.IsOnline():
			return False
		return True

	def OnWarp(self):
		net.SendGuildUseSkillPacket(155, self.key)

	def CanRemove(self):
		for i in xrange(guild.ENEMY_GUILD_SLOT_MAX_COUNT):
			if guild.GetEnemyGuildName(i) != "":
				return False

		if guild.MainPlayerHasAuthority(guild.AUTH_REMOVE_MEMBER):
			if guild.IsMemberByName(self.name):
				return True

		return False

	def OnRemove(self):
		net.SendGuildRemoveMemberPacket(self.key)
		return True

class MessengerFriendGroup(MessengerGroupItem):
	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeinfo.MESSENGER_FRIEND)

	def AppendMember(self, key, name):
		item = MessengerFriendItem(self.getParentEvent)
		return MessengerGroupItem.AppendMember(self, item, key, name)

class MessengerTeamGroup(MessengerGroupItem):
	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName("Suporte Aegon2")

	def AppendMember(self, key, name):
		item = MessengerTeamItem(self.getParentEvent)
		return MessengerGroupItem.AppendMember(self, item, key, name)

class MessengerGuildGroup(MessengerGroupItem):
	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeinfo.MESSENGER_GUILD)
		self.AddFlag("float")

	def AppendMember(self, key, name):
		item = MessengerGuildItem(self.getParentEvent)
		return MessengerGroupItem.AppendMember(self, item, key, name)

class MessengerFamilyGroup(MessengerGroupItem):
	def __init__(self, getParentEvent):
		MessengerGroupItem.__init__(self, getParentEvent)
		self.SetName(localeinfo.MESSENGER_FAMILY)
		self.AddFlag("float")

		self.lover = None

	def AppendMember(self, key, name):
		item = MessengerGuildItem(self.getParentEvent)
		self.lover = item
		return MessengerGroupItem.AppendMember(self, item, key, name)

	def GetLover(self):
		return self.lover

class MessengerWindow(ui.ScriptWindow):

	START_POSITION = 39

	class ResizeButton(ui.DragButton):
		def OnMouseOverIn(self):
			app.SetCursor(app.VSIZE)

		def OnMouseOverOut(self):
			app.SetCursor(app.NORMAL)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		messenger.SetMessengerHandler(self)

		self.board = None
		self.groupList = []
		self.showingItemList = []
		self.selectedItem = None
		self.familyGroup = None

		self.TimeToShowInfoAboutLogin = app.GetTime()+ 15
		self.wasLogged = []

		self.whisperButtonEvent = None
		self.guildButtonEvent = None

		self.showingPageSize = 0
		self.startLine = 0
		self.isLoaded = 0

		self.__AddGroup()
		messenger.RefreshGuildMember()

	def Show(self):
		if self.isLoaded == 0:
			self.isLoaded = 1

			self.__LoadWindow()
			self.OnRefreshList()
			self.OnResizeDialog()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/messengerwindow.py")

		try:
			self.board = self.GetChild("board")
			self.scrollBar = self.GetChild("ScrollBar")
			self.whisperButton = self.GetChild("WhisperButton")
			self.removeButton = self.GetChild("RemoveButton")
			self.addFriendButton = self.GetChild("AddFriendButton")
			self.guildButton = self.GetChild("GuildButton")
			self.buttonsSeparator = self.GetChild("ButtonsSeparator")
			self.scrollBarSeparator = self.GetChild("ScrollBarSeparator")
		except:
			exception.Abort("MessengerWindow.__LoadWindow.__Bind")

		self.board.SetCloseEvent(self.Close)
		self.scrollBar.SetScrollEvent(self.OnScroll)
		self.whisperButton.SetEvent(self.OnPressWhisperButton)
		self.removeButton.SetEvent(self.OnPressRemoveButton)
		self.addFriendButton.SetEvent(self.OnPressAddFriendButton)
		self.guildButton.SetEvent(self.OnPressGuildButton)

		width = self.GetWidth()
		height = self.GetHeight()
		self.addFriendButton.SetPosition(-60, 50)
		self.whisperButton.SetPosition(-20, 50)
		self.removeButton.SetPosition(20, 50)
		self.guildButton.SetPosition(60, 50)

		self.buttonsSeparator.Show()
		self.scrollBarSeparator.Show()

		self.whisperButton.Disable()
		self.removeButton.Disable()

		resizeButton = self.ResizeButton()
		resizeButton.AddFlag("restrict_x")
		resizeButton.SetParent(self)
		resizeButton.SetSize(self.GetWidth(), 10)
		resizeButton.SetWindowVerticalAlignBottom()
		resizeButton.SetPosition(0, 0)
		resizeButton.Show()
		self.resizeButton = resizeButton
		self.resizeButton.SetMoveEvent(self.OnResizeDialog)
		self.resizeButton.SetPosition(0, 300)

		for list in self.groupList:
			list.SetTop()

		self.SetOnRunMouseWheelEvent(self.OnRunMouseWheel)

	def __del__(self):
		messenger.SetMessengerHandler(None)
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.Hide()
		self.board = None
		self.scrollBar = None
		self.resizeButton = None
		self.friendNameBoard = None
		self.questionDialog = None
		self.popupDialog = None
		self.inputDialog = None
		self.familyGroup = None
		self.whisperButton = None
		self.removeButton = None

	def OnRunMouseWheel(self, nLen):
		if nLen > 0:
			self.scrollBar.OnUp()
		else:
			self.scrollBar.OnDown()

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def Close(self):
		self.questionDialog = None
		self.Hide()

	def SetSize(self, width, height):
		ui.ScriptWindow.SetSize(self, width, height)
		if self.board:
			self.board.SetSize(width, height)

	def OnResizeDialog(self):
		x, y = self.resizeButton.GetLocalPosition()
		if y < 250:
			self.resizeButton.SetPosition(x, 250)
			return
		self.SetSize(self.GetWidth(), y + self.resizeButton.GetHeight())

		self.showingPageSize = y - (self.START_POSITION + 26)
		self.scrollBar.SetScrollBarSize(self.showingPageSize-35)
		self.scrollBarSeparator.SetHeight(self.showingPageSize-22)
		self.buttonsSeparator.SetPosition(7, self.showingPageSize+15)
		self.__LocateMember()

		self.resizeButton.TurnOffCallBack()
		self.UpdateRect()
		self.resizeButton.TurnOnCallBack()

	def __LocateMember(self):
		if self.isLoaded == 0:
			return

		if (self.showingPageSize-35)/24 >= len(self.showingItemList):
			self.scrollBar.SetMiddleBarSize(1.0)
			self.startLine = 0
		else:
			if self.showingItemList:
				self.scrollBar.SetMiddleBarSize(min(1.0, float(((self.showingPageSize-35)/24)) / float(len(self.showingItemList)+5)))

		yPos = self.START_POSITION
		heightLimit = self.GetHeight() - (self.START_POSITION + 13 + 35)

		map(ui.Bar.Hide, self.showingItemList)

		for item in self.showingItemList[self.startLine:]:
			item.SetPosition(item.GetStepWidth(), yPos)
			item.SetTop()
			item.Show()

			yPos += item.GetStepHeight()
			if yPos > heightLimit:
				break

	def __AddGroup(self):
		member = MessengerFriendGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()
		self.groupList.append(member)

		member = MessengerGuildGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()
		self.groupList.append(member)

		member = MessengerTeamGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()
		self.TeamGroup = member
		self.groupList.append(member)

	def __AddFamilyGroup(self):
		member = MessengerFamilyGroup(ui.__mem_func__(self.GetSelf))
		member.Open()
		member.Show()

		self.familyGroup = member

	def ClearGuildMember(self):
		self.groupList[GUILD].ClearMember()

	def SetWhisperButtonEvent(self, event):
		self.whisperButtonEvent = ui.__mem_func__(event)

	def SetGuildButtonEvent(self, event):
		self.guildButtonEvent = ui.__mem_func__(event)

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnPressGuildButton(self):
		self.guildButtonEvent()

	def OnPressAddFriendButton(self):
		friendNameBoard = uicommon.InputDialog()
		friendNameBoard.SetTitle(localeinfo.MESSENGER_ADD_FRIEND)
		friendNameBoard.SetAcceptEvent(self.OnAddFriend)
		friendNameBoard.SetCancelEvent(self.OnCancelAddFriend)
		friendNameBoard.Open()
		self.friendNameBoard = friendNameBoard

	def OnAddFriend(self):
		text = self.friendNameBoard.GetText()
		if text:
			net.SendMessengerAddByNamePacket(text)
		self.friendNameBoard.Close()
		self.friendNameBoard = None
		return True

	def OnCancelAddFriend(self):
		self.friendNameBoard.Close()
		self.friendNameBoard = None
		return True

	def OnPressWhisperButton(self):
		if self.selectedItem:
			self.selectedItem.OnWhisper()

	def OnPressRemoveButton(self):
		if self.selectedItem:
			if self.selectedItem.CanRemove():
				self.questionDialog = uicommon.QuestionDialog()
				self.questionDialog.SetText(localeinfo.MESSENGER_DO_YOU_DELETE)
				self.questionDialog.SetAcceptEvent(self.OnRemove)
				self.questionDialog.SetCancelEvent(self.OnCloseQuestionDialog)
				self.questionDialog.Open()

	def OnRemove(self):
		if self.selectedItem:
			if self.selectedItem.CanRemove():
				map(lambda arg, argDeletingItem=self.selectedItem: arg.RemoveMember(argDeletingItem), self.groupList)
				self.selectedItem.OnRemove()
				self.selectedItem.UnSelect()
				self.selectedItem = None
				self.OnRefreshList()

		self.OnCloseQuestionDialog()

	def OnScroll(self):
		scrollLineCount = len(self.showingItemList) - (self.showingPageSize/35)
		startLine = int(scrollLineCount * self.scrollBar.GetPos())

		if startLine != self.startLine:
			self.startLine = startLine
			self.__LocateMember()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnSelectItem(self, item):

		if self.selectedItem:
			if item != self.selectedItem:
				self.selectedItem.UnSelect()

		self.selectedItem = item

		if self.selectedItem:
			self.selectedItem.Select()

			if self.selectedItem.CanWhisper():
				self.whisperButton.Enable()
			else:
				self.whisperButton.Disable()

			if self.selectedItem.CanRemove():
				self.removeButton.Enable()
			else:
				self.removeButton.Disable()

	def OnDoubleClickItem(self, item):
		if not self.selectedItem:
			return

		if self.selectedItem.IsOnline():
			self.OnPressWhisperButton()

	def GetSelf(self):
		return self

	def OnRefreshList(self):
		self.showingItemList = []

		if self.familyGroup:
			self.showingItemList.append(self.familyGroup)
			if self.familyGroup.GetLover():
				self.showingItemList.append(self.familyGroup.GetLover())

		for group in self.groupList:
			self.showingItemList.append(group)

			if group.IsOpen():
				loginMemberList = group.GetLoginMemberList()
				logoutMemberList = group.GetLogoutMemberList()

				if loginMemberList or logoutMemberList:
					for member in loginMemberList:
						self.showingItemList.append(member)
					for member in logoutMemberList:
						self.showingItemList.append(member)

		self.__LocateMember()

	def RefreshMessenger(self):
		self.OnRefreshList()

	def __AddList(self, groupIndex, key, name):
		group = self.groupList[groupIndex]
		member = group.FindMember(key)
		if not member:
			member = group.AppendMember(key, name)
			self.OnSelectItem(None)
		return member

	def OnRemoveList(self, groupIndex, key):
		group = self.groupList[groupIndex]
		group.RemoveMember(group.FindMember(key))
		self.OnRefreshList()

	def OnRemoveAllList(self, groupIndex):
		group = self.groupList[groupIndex]
		group.ClearMember()
		self.OnRefreshList()

	def IsStaff(self, name):
		for item in ["[GM]", "[ADM]", "[DEV]", "[AUX]"]:
			if item in name:
				return True
		return False

	def OnLogin(self, groupIndex, key, name = None):
		if not name:
			name = key

		if self.IsStaff(name):
			groupIndex = TEAM

		group = self.groupList[groupIndex]
		member = self.__AddList(groupIndex, key, name)
		member.SetName(name)
		member.Online()
		self.OnRefreshList()

		#Amigo System
		if app.GetTime() > self.TimeToShowInfoAboutLogin:
			if member.WasShowed() == False:
				self.pop = uipopup .PopupMsg()
				self.pop.SetType(1)
				self.pop.SetMsg("Seu amigo %s entrou no jogo!"% name)
				self.pop.Show()
				member.SetShowed()
		#Amigo System Final

	def OnLogout(self, groupIndex, key, name = None):
		if not name:
			name = key

		if self.IsStaff(name):
			groupIndex = TEAM

		group = self.groupList[groupIndex]
		member = self.__AddList(groupIndex, key, name)

		member.SetName(name)
		member.Offline()
		self.OnRefreshList()

		#Amigo System
		if app.GetTime() > self.TimeToShowInfoAboutLogin:
			if member.WasShowed() == True:
				self.pop = uipopup .PopupMsg()
				self.pop.SetType(1)
				self.pop.SetMsg("Seu amigo %s saiu do jogo!"% name)
				self.pop.Show()
				member.SetUnShowed()
		#Amigo System Final

	def OnAddLover(self, name, lovePoint):
		if not self.familyGroup:
			self.__AddFamilyGroup()

		member = self.familyGroup.AppendMember(0, name)

		member.SetName(name)
		member.SetLovePoint(lovePoint)
		member.Offline()
		self.OnRefreshList()

	def OnUpdateLovePoint(self, lovePoint):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.SetLovePoint(lovePoint)

	def OnLoginLover(self):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.Online()

	def OnLogoutLover(self):
		if not self.familyGroup:
			return

		lover = self.familyGroup.GetLover()
		if not lover:
			return

		lover.Offline()

	def ClearLoverInfo(self):
		if not self.familyGroup:
			return

		self.familyGroup.ClearMember()
		self.familyGroup = None
		self.OnRefreshList()

# x = MessengerWindow()
# x.Show()

# try:
	# x.OnLogin(1, 0, "Bruno")
	# x.OnLogin(1, 1, "João")
	# x.OnLogin(0, 0, "Junior")
	# x.OnLogin(0, 1, "Alan")
	# x.OnLogin(0, 2, "Marcos")
	# x.OnLogin(0, 3, "Vamos testar")
	# x.OnLogin(0, 4, "PlayerNoobdokacete")
	# x.OnLogin(2, 0, "[Dev]Crazy")
	# x.OnLogin(2, 1, "[Dev]Minions")
# except:
	# pass