#favor manter essa linha
import ui
import uiscriptlocale
import _wnd_mgr as wndMgr
import _player as player
import _mini_map as miniMap
import localeinfo
import _net as net
import _app as app
import constinfo
import _background as background
import exception

class MapTextToolTip(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self, "TOP_MOST")
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetHorizontalAlignCenter()
		textLine.SetOutline()
		textLine.SetHorizontalAlignRight()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetTooltipPosition(self, PosX, PosY):
		self.textLine.SetPosition(PosX - 5, PosY)

	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)

	def GetTextSize(self):
		return self.textLine.GetTextSize()

class AtlasWindow(ui.ScriptWindow):
	class AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def OnUpdate(self):
			miniMap.UpdateAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			fx = float(x)
			fy = float(y)
			miniMap.RenderAtlas(fx, fy)

		def HideAtlas(self):
			miniMap.HideAtlas()

		def ShowAtlas(self):
			miniMap.ShowAtlas()

	def __init__(self):
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Hide()
		self.infoGuildMark = ui.MarkBox()
		self.infoGuildMark.Hide()
		self.AtlasMainWindow = None
		self.mapName = ""
		self.board = 0

		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/atlaswindow.py")

		self.board = self.GetChild("board")

		self.AtlasMainWindow = self.AtlasRenderer()
		self.board.SetCloseEvent(self.Hide)
		self.AtlasMainWindow.SetParent(self.board)
		self.AtlasMainWindow.SetPosition(9, 40)
		self.tooltipInfo.SetParent(self.board)
		self.infoGuildMark.SetParent(self.board)
		self.SetPosition(wndMgr.GetScreenWidth() - 136 - 256 - 10, 0)
		self.Hide()

		miniMap.RegisterAtlasWindow(self)

	def Destroy(self):
		miniMap.UnregisterAtlasWindow()
		self.ClearDictionary()
		self.AtlasMainWindow = None
		self.tooltipInfo = None
		self.infoGuildMark = None
		self.board = None

	def OnUpdate(self):
		if not self.tooltipInfo:
			return

		if not self.infoGuildMark:
			return

		self.infoGuildMark.Hide()
		self.tooltipInfo.Hide()

		if False == self.board.IsIn():
			return

		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

		if False == bFind:
			return

		if "empty_guild_area" == sName:
			sName = localeinfo.GUILD_EMPTY_AREA

		self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
		(x, y) = self.GetGlobalPosition()
		self.tooltipInfo.SetTooltipPosition(mouseX - x, mouseY - y)
		self.tooltipInfo.SetTextColor(dwTextColor)
		self.tooltipInfo.Show()
		self.tooltipInfo.SetTop()

		if 0 != dwGuildID:
			textWidth, textHeight = self.tooltipInfo.GetTextSize()
			self.infoGuildMark.SetIndex(dwGuildID)
			self.infoGuildMark.SetPosition(mouseX - x - textWidth - 18 - 5, mouseY - y)
			self.infoGuildMark.Show()

	def Hide(self):
		if self.AtlasMainWindow:
			self.AtlasMainWindow.HideAtlas()
			self.AtlasMainWindow.Hide()
		ui.ScriptWindow.Hide(self)

	def Show(self):
		if self.AtlasMainWindow:
			(bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
			if bGet:
				self.SetSize(iSizeX + 35, iSizeY + 58)
				self.board.SetSize(iSizeX + 31 - 13, iSizeY + 56 - 8)
				self.AtlasMainWindow.ShowAtlas()
				self.AtlasMainWindow.Show()
		ui.ScriptWindow.Show(self)

	def SetCenterPositionAdjust(self, x, y):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def OnPressEscapeKey(self):
		self.Hide()
		return True

class MiniMap(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI_BOTTOM")

		self.__Initialize()

		miniMap.Create()
		miniMap.SetScale(2.0)

		self.AtlasWindow = AtlasWindow()
		self.AtlasWindow.LoadWindow()
		self.AtlasWindow.Hide()

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()

		self.mapName = ""

		self.isLoaded = 0
		self.canSeeInfo = True
		self.toggleButtonDict = {}
		self.__LoadWindow()

	def __del__(self):
		miniMap.Destroy()
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.positionInfo = 0
		self.observerCount = 0
		self.OpenWindow = 0
		self.ScaleUpButton = 0
		self.ScaleDownButton = 0
		self.AtlasShowButton = 0

		self.tooltipMiniMapOpen = 0
		self.tooltipMiniMapClose = 0
		self.tooltipScaleUp = 0
		self.tooltipScaleDown = 0
		self.tooltipAtlasOpen = 0
		self.tooltipInfo = None
		self.serverInfo = None

		if app.ENABLE_DEFENSE_WAVE:
			self.MastHp = 0

	def Show(self):
		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/minimap.py")

		self.OpenWindow = self.GetChild("OpenWindow")
		self.MiniMapWindow = self.GetChild("MiniMapWindow")
		self.ScaleUpButton = self.GetChild("ScaleUpButton")
		self.ScaleDownButton = self.GetChild("ScaleDownButton")
		self.AtlasShowButton = self.GetChild("AtlasShowButton")
		self.positionInfo = self.GetChild("PositionInfo")
		self.observerCount = self.GetChild("ObserverCount")
		self.serverInfo = self.GetChild("ServerInfo")

		if constinfo.MINIMAP_POSITIONINFO_ENABLE == 0:
			self.positionInfo.Hide()

		if app.ENABLE_DEFENSE_WAVE:
			self.MastHp = self.GetChild("MastHp")
			self.MastWindow = self.GetChild("MastWindow")
			self.MastHp.SetOverInEvent(self.MastHp.ShowToolTip)
			self.MastHp.SetOverOutEvent(self.MastHp.HideToolTip)
			self.MastHp.SetShowToolTipEvent(self.MastHp.ShowToolTip)
			self.MastHp.SetHideToolTipEvent(self.MastHp.HideToolTip)
			self.MastHp.SetPercentage(5000000, 5000000)
			self.MastWindow.Hide()

		self.serverInfo.SetText(net.GetServerInfo())
		self.ScaleUpButton.SetEvent(self.ScaleUp)
		self.ScaleDownButton.SetEvent(self.ScaleDown)

		if miniMap.IsAtlas():
			self.AtlasShowButton.SetEvent(self.ShowAtlas)

		self.GetChild("MiniMapHideButton").SetEvent(self.HideMiniMap)
		self.GetChild("MiniMapShowButton").SetEvent(self.ShowMiniMap)

		self.ShowMiniMap()

	def Destroy(self):
		self.HideMiniMap()

		self.AtlasWindow.Destroy()
		self.AtlasWindow = None
		self.ClearDictionary()

		self.__Initialize()

	def UpdateObserverCount(self, observerCount):
		if observerCount > 0:
			self.observerCount.Show()
		elif observerCount <= 0:
			self.observerCount.Hide()

		self.observerCount.SetText(localeinfo.MINIMAP_OBSERVER_COUNT % observerCount)

	def OnUpdate(self):
		self.SetTop()
		(x, y, z) = player.GetMainCharacterPosition()
		miniMap.Update(x, y)

		self.positionInfo.SetText("(%.0f, %.0f)" % (x/100, y/100))

		if self.tooltipInfo:
			if self.MiniMapWindow.IsIn():
				(mouseX, mouseY) = wndMgr.GetMousePosition()
				(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
				if bFind == 0:
					self.tooltipInfo.Hide()
				elif not self.canSeeInfo:
					self.tooltipInfo.SetText("%s(%s)" % (sName, localeinfo.UI_POS_UNKNOWN))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
				else:
					self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
					self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
					self.tooltipInfo.SetTextColor(dwTextColor)
					self.tooltipInfo.Show()
			else:
				self.tooltipInfo.Hide()

	def OnRender(self):
		(x, y) = self.GetGlobalPosition()
		fx = float(x + 8)
		fy = float(y)
		miniMap.Render(fx, fy)

	def Close(self):
		self.HideMiniMap()

	def HideMiniMap(self):
		self.SetSize(32, 32)
		self.SetPosition(wndMgr.GetScreenWidth() - 32, 0)
		self.GetChild("OpenWindow").Hide()
		miniMap.Hide()
		self.GetChild("MiniMapShowButton").Show()

	def ShowMiniMap(self):
		if not self.canSeeInfo:
			return

		self.SetSize(136, 137)
		self.SetPosition(wndMgr.GetScreenWidth() - 136, 0)
		self.GetChild("MiniMapShowButton").Hide()
		self.GetChild("OpenWindow").Show()
		miniMap.Show()

	def isShowMiniMap(self):
		return miniMap.isShow()

	def ScaleUp(self):
		miniMap.ScaleUp()

	def ScaleDown(self):
		miniMap.ScaleDown()

	def ShowAtlas(self):
		if not miniMap.IsAtlas():
			return
		if not self.AtlasWindow.IsShow():
			self.AtlasWindow.Show()
		else:
			self.AtlasWindow.Hide()

	def SetToggleButtonEvent(self, button, kEventFunc):
		button.SetEvent(kEventFunc)

	def ToggleAtlasWindow(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()

	if app.ENABLE_DEFENSE_WAVE:
		def SetMastHP(self, hp):
			self.MastHp.SetPercentage(hp, 5000000)
			self.MastHp.SetToolTipText("HP:  %d /5000000" % hp)

		def SetMastWindow(self, i):
			if i:
				self.MastWindow.Show()
			else:
				self.MastWindow.Hide()