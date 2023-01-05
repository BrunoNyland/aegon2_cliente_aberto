#favor manter essa linha
import enszxc3467hc3kokdueq as app
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import ime
import grp
import snd
import wndMgr
import skill
import localeinfo
import guild
import constinfo
import colorinfo
import dbg

import exception
import os

from weakref import proxy, WeakMethod

BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
DARK_COLOR = grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
BRIGHT_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)
SELECT_COLOR = grp.GenerateColor(0.0, 0.0, 0.5, 0.3)
WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

OLD_STUFF = False

createToolTipWindowDict = {}
def RegisterToolTipWindow(type, createToolTipWindow):
	createToolTipWindowDict[type] = createToolTipWindow

if OLD_STUFF:
	def RegisterCandidateWindowClass(codePage, candidateWindowClass):
		EditLine.candidateWindowClassDict[codePage] = candidateWindowClass

app.SetDefaultFontName(localeinfo.UI_DEF_FONT)

############################################################################################################################################
### WINDOW & SCRIPWINDOW ###### WINDOW & SCRIPWINDOW ###### WINDOW & SCRIPWINDOW ###### WINDOW & SCRIPWINDOW ###### WINDOW & SCRIPWINDOW ###
############################################################################################################################################
if constinfo.DETECT_LEAKING_WINDOWS:
	import weakref
	import sys
	def trace_calls_and_returns(frame, event, arg): #as the name (somewhat) implies build trace of calls and remove trace on returns
		co = frame.f_code
		func_name = co.co_name
		line_no = frame.f_lineno
		filename = co.co_filename
		if event == 'call' or event == 'c_call':
			constinfo.WINDOW_OBJ_TRACE.append('Call to %s on line %s of %s' % (func_name, line_no, filename))
			return trace_calls_and_returns
		elif (event == 'return' or event == 'c_return') and len(constinfo.WINDOW_OBJ_TRACE):
			constinfo.WINDOW_OBJ_TRACE.pop()
		return

	sys.settrace(trace_calls_and_returns)

	class ExtendedRef(weakref.ref): # extended weakref object to store the backtrace, type of actual object and the parent name, if any
		def __init__(self, ob, callback = None):
			super(ExtendedRef, self).__init__(ob, callback)
			self.typeStr = str(ob)
			self.strParent = ""
			self.traceBack = constinfo.WINDOW_OBJ_TRACE[:] # just deepcopy the current trace

class __mem_func__:
	class __noarg_call__:
		def __init__(self, cls, obj, func):
			self.cls = cls
			self.obj = proxy(obj)
			self.func = proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj)

	class __arg_call__:
		def __init__(self, cls, obj, func):
			self.cls = cls
			self.obj = proxy(obj)
			self.func = proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj, *arg)

	def __init__(self, mfunc):
		if mfunc.__code__.co_argcount > 1:
			self.call = __mem_func__.__arg_call__(mfunc.__class__, mfunc.__self__, mfunc.__func__)
		else:
			self.call = __mem_func__.__noarg_call__(mfunc.__class__, mfunc.__self__, mfunc.__func__)

	def __call__(self, *arg):
		return self.call(*arg)

class Window(object):

	onHideEvent = None
	onHideArgs = None

	onShowEvent = None
	onShowArgs = None

	def __init__(self, layer:str="UI") -> None:
		if constinfo.DETECT_LEAKING_WINDOWS:
			constinfo.WINDOW_TOTAL_OBJ_COUNT += 1
			if constinfo.WINDOW_COUNT_OBJ:
				constinfo.WINDOW_OBJ_COUNT += 1
				constinfo.WINDOW_OBJ_LIST[id(self)] = ExtendedRef(self) # save trace and other data

		self.hWnd = None
		self.parentWindow = None
		self.RegisterWindow(layer)
		self.Hide()

		self.InitializeEvents()

		self.baseX = 0
		self.baseY = 0

		self.SetWindowName("NONAME_Window")

	def __del__(self) -> None:
		if constinfo.DETECT_LEAKING_WINDOWS:
			constinfo.WINDOW_TOTAL_OBJ_COUNT -= 1
			if constinfo.WINDOW_COUNT_OBJ and id(self) in constinfo.WINDOW_OBJ_LIST:
				constinfo.WINDOW_OBJ_COUNT -= 1
				constinfo.WINDOW_OBJ_LIST.pop(id(self))

		wndMgr.Destroy(self.hWnd)

	def RegisterWindow(self, layer:str) -> None:
		self.hWnd = wndMgr.Register(self, layer)

	def Destroy(self) -> None:
		self.InitializeEvents()
		self.Hide()

	def InitializeEvents(self) -> None:
		#Args Provided by C++
		self.onRunMouseWheelEvent = None
		self.moveWindowEvent = None

		#Args Provided by Python
		self.onHideEvent = None
		self.onHideArgs = None

		self.onShowEvent = None
		self.onShowArgs = None

		self.mouseLeftButtonDownEvent = None
		self.mouseLeftButtonDownArgs = None

		self.mouseLeftButtonUpEvent = None
		self.mouseLeftButtonUpArgs = None

		self.mouseLeftButtonDoubleClickEvent = None
		self.mouseLeftButtonDoubleClickArgs = None

		self.mouseRightButtonDownEvent = None
		self.mouseRightButtonDownArgs = None

		self.renderEvent = None
		self.renderArgs = None

		self.overInEvent = None
		self.overInArgs = None

		self.overOutEvent = None
		self.overOutArgs = None

	def GetWindowHandle(self):
		return self.hWnd

	def AddFlag(self, style:str) -> None:
		wndMgr.AddFlag(self.hWnd, style)

	def IsRTL(self):
		return wndMgr.IsRTL(self.hWnd)

	def SetWindowName(self, name:str) -> None:
		wndMgr.SetName(self.hWnd, name)

	def GetWindowName(self) -> str:
		return wndMgr.GetName(self.hWnd)

	def SetParent(self, parent) -> None:
		if parent:
			if constinfo.DETECT_LEAKING_WINDOWS: # find our window in the saved obj list and save its parent address
				if constinfo.WINDOW_COUNT_OBJ and id(self) in constinfo.WINDOW_OBJ_LIST:
					constinfo.WINDOW_OBJ_LIST[id(self)].strParent = str(parent)
			wndMgr.SetParent(self.hWnd, parent.hWnd)
		else:
			wndMgr.SetParent(self.hWnd, 0)

	def SetAttachParent(self, parent) -> None:
		wndMgr.SetAttachParent(self.hWnd, parent.hWnd)

	def SetParentProxy(self, parent) -> None:
		self.parentWindow = proxy(parent)
		wndMgr.SetParent(self.hWnd, parent.hWnd)

	def GetParentProxy(self):
		return self.parentWindow

	def SetPickAlways(self) -> None:
		wndMgr.SetPickAlways(self.hWnd)

	def SetWindowHorizontalAlignLeft(self) -> None:
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_LEFT)

	def SetWindowHorizontalAlignCenter(self) -> None:
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_CENTER)

	def SetWindowHorizontalAlignRight(self) -> None:
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_RIGHT)

	def SetWindowVerticalAlignTop(self) -> None:
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_TOP)

	def SetWindowVerticalAlignCenter(self) -> None:
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_CENTER)

	def SetWindowVerticalAlignBottom(self) -> None:
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_BOTTOM)

	def SetTop(self) -> None:
		wndMgr.SetTop(self.hWnd)

	def Show(self) -> None:
		if self.onShowEvent:
			self.onShowEvent(*self.onShowArgs)
		wndMgr.Show(self.hWnd)

	def Hide(self) -> None:
		if self.onHideEvent:
			self.onHideEvent(*self.onHideArgs)
		wndMgr.Hide(self.hWnd)

	def Lock(self) -> None:
		wndMgr.Lock(self.hWnd)

	def Unlock(self) -> None:
		wndMgr.Unlock(self.hWnd)

	def IsShow(self):
		return wndMgr.IsShow(self.hWnd)

	def UpdateRect(self) -> None:
		wndMgr.UpdateRect(self.hWnd)

	def SetSize(self, width, height) -> None:
		wndMgr.SetWindowSize(self.hWnd, int(width), int(height))

	def GetWidth(self) -> int:
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self) -> int:
		return wndMgr.GetWindowHeight(self.hWnd)

	def GetLocalPosition(self) -> int:
		return wndMgr.GetWindowLocalPosition(self.hWnd)

	def GetGlobalPosition(self) -> int:
		return wndMgr.GetWindowGlobalPosition(self.hWnd)

	def GetMouseLocalPosition(self) -> int:
		return wndMgr.GetMouseLocalPosition(self.hWnd)

	def GetRect(self) -> int:
		return wndMgr.GetWindowRect(self.hWnd)

	def GetLeft(self) -> int:
		x, y = self.GetLocalPosition()
		return x

	def GetGlobalLeft(self) -> int:
		x, y = self.GetGlobalPosition()
		return x

	def GetTop(self) -> int:
		x, y = self.GetLocalPosition()
		return y

	def GetGlobalTop(self) -> int:
		x, y = self.GetGlobalPosition()
		return y

	def GetRight(self) -> int:
		return self.GetLeft() + self.GetWidth()

	def GetBottom(self) -> int:
		return self.GetTop() + self.GetHeight()

	def SetLeft(self, x) -> None:
		wndMgr.SetWindowPosition(self.hWnd, int(x), self.GetTop())

	def SavePosition(self) -> None:
		self.baseX = self.GetLeft()
		self.baseY = self.GetTop()

	def UpdatePositionByScale(self, scale) -> None:
		self.SetPosition(int(self.baseX * scale), int(self.baseY * scale))

	def IsInPosition(self) -> bool:
		xMouse, yMouse = wndMgr.GetMousePosition()
		x, y = self.GetGlobalPosition()
		return xMouse >= x and xMouse < x + self.GetWidth() and yMouse >= y and yMouse < y + self.GetHeight()

	def SetMouseLeftButtonDownEvent(self, event, *args) -> None:
		self.mouseLeftButtonDownEvent = __mem_func__(event)
		self.mouseLeftButtonDownArgs = args

	def OnMouseLeftButtonDown(self) -> None:
		if self.mouseLeftButtonDownEvent:
			self.mouseLeftButtonDownEvent(*self.mouseLeftButtonDownArgs)

	def SetMouseLeftButtonDoubleClickEvent(self, event, *args) -> None:
		self.mouseLeftButtonDoubleClickEvent = __mem_func__(event)
		self.mouseLeftButtonDoubleClickArgs = args

	def OnMouseLeftButtonDoubleClick(self) -> None:
		if self.mouseLeftButtonDoubleClickEvent:
			self.mouseLeftButtonDoubleClickEvent(*self.mouseLeftButtonDoubleClickArgs)

	def SetMouseRightButtonDownEvent(self, event, *args) -> None:
		self.mouseRightButtonDownEvent = __mem_func__(event)
		self.mouseRightButtonDownArgs = args

	def OnMouseRightButtonDown(self) -> None:
		if self.mouseRightButtonDownEvent:
			self.mouseRightButtonDownEvent(*self.mouseRightButtonDownArgs)

	def SetMouseLeftButtonUpEvent(self, event, *args) -> None:
		self.mouseLeftButtonUpEvent = __mem_func__(event)
		self.mouseLeftButtonUpArgs = args

	def OnMouseLeftButtonUp(self) -> None:
		if self.mouseLeftButtonUpEvent:
			self.mouseLeftButtonUpEvent(*self.mouseLeftButtonUpArgs)

	def SetOnRunMouseWheelEvent(self, event) -> None:
		self.onRunMouseWheelEvent = __mem_func__(event)

	def OnRunMouseWheel(self, nLen) -> bool:
		if self.onRunMouseWheelEvent:
			self.onRunMouseWheelEvent(*(bool(nLen < 0), ))
			return True
		return False

	def SetShowEvent(self, event, *args) -> None:
		self.onShowEvent = __mem_func__(event)
		self.onShowArgs = args

	def SetHideEvent(self, event, *args) -> None:
		self.onHideEvent = __mem_func__(event)
		self.onHideArgs = args

	def SetMoveWindowEvent(self, event) -> None:
		self.moveWindowEvent = __mem_func__(event)

	def OnMoveWindow(self, x, y) -> None:
		if self.moveWindowEvent:
			self.moveWindowEvent(x, y)

	def SetOverInEvent(self, func, *args) -> None:
		self.overInEvent = __mem_func__(func)
		self.overInArgs = args

	def SetOverOutEvent(self, func, *args) -> None:
		self.overOutEvent = __mem_func__(func)
		self.overOutArgs = args

	def OnMouseOverIn(self) -> None:
		if self.overInEvent:
			self.overInEvent(*self.overInArgs)

	def OnMouseOverOut(self) -> None:
		if self.overOutEvent:
			self.overOutEvent(*self.overOutArgs)

	def SetRenderEvent(self, event, *args) -> None:
		self.renderEvent = __mem_func__(event)
		self.renderArgs = args

	def OnRender(self) -> None:
		if self.renderEvent:
			self.renderEvent(*self.renderArgs)

	def SetVisible(self, is_show) -> None:
		if is_show:
			self.Show()
		else:
			self.Hide()

	def SetPosition(self, x, y) -> None:
		wndMgr.SetWindowPosition(self.hWnd, int(x), int(y))

	def SetCenterPosition(self, x:int = 0, y:int = 0) -> None:
		self.SetPosition(int((wndMgr.GetScreenWidth() - self.GetWidth()) / 2) + x, int((wndMgr.GetScreenHeight() - self.GetHeight()) / 2) + y)

	def IsFocus(self):
		return wndMgr.IsFocus(self.hWnd)

	def SetFocus(self):
		wndMgr.SetFocus(self.hWnd)

	def KillFocus(self):
		wndMgr.KillFocus(self.hWnd)

	def GetChildCount(self):
		return wndMgr.GetChildCount(self.hWnd)

	def IsIn(self):
		return wndMgr.IsIn(self.hWnd)

class ScriptWindow(Window):
	def __init__(self, layer:str="UI") -> None:
		Window.__init__(self, layer)
		self.Children = []
		self.ElementDictionary = {}

	def __del__(self) -> None:
		Window.__del__(self)

	def ClearDictionary(self) -> None:
		self.Children = []
		self.ElementDictionary = {}

	def InsertChild(self, name:str, child:Window) -> None:
		self.ElementDictionary[name] = child

	def IsChild(self, name:str) -> bool:
		return self.ElementDictionary.__contains__(name)

	def GetChild(self, name:str):
		return self.ElementDictionary[name]

	def GetChild2(self, name:str):
		return self.ElementDictionary.get(name, None)

############################################################################################################################################
### WINDOW & SCRIPWINDOW END ###### WINDOW & SCRIPWINDOW END ###### WINDOW & SCRIPWINDOW ###### WINDOW & SCRIPWINDOW ###### WINDOW END #####
############################################################################################################################################

############################################################################################################################################
### RENDER TARGET ### RENDER TARGET ### RENDER TARGET ### RENDER TARGET ### RENDER TARGET ### RENDER TARGET ### RENDER TARGET ### RENDER ###
############################################################################################################################################
if app.RENDER_TARGET:
	class RenderTarget(Window):
		def __init__(self, layer:str="UI") -> None:
			Window.__init__(self, layer)

			self.number = -1

		def __del__(self) -> None:
			Window.__del__(self)

		def RegisterWindow(self, layer:str) -> None:
			self.hWnd = wndMgr.RegisterRenderTarget(self, layer)

		def SetRenderTarget(self, number:int) -> None:
			self.number = number
			wndMgr.SetRenderTarget(self.hWnd, self.number)

############################################################################################################################################
### IMAGE CLASSES ### IMAGE CLASSES ### IMAGE CLASSES ### IMAGE CLASSES ### IMAGE CLASSES ### IMAGE CLASSES ### IMAGE CLASSES ### IMAGE CLAS
############################################################################################################################################
class MarkBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterMarkBox(self, layer)

	def Load(self):
		wndMgr.MarkBox_Load(self.hWnd)

	def SetScale(self, scale):
		wndMgr.MarkBox_SetScale(self.hWnd, scale)

	def SetIndex(self, guildID):
		MarkID = guild.GuildIDToMarkID(guildID)
		wndMgr.MarkBox_SetImageFilename(self.hWnd, guild.GetMarkImageFilenameByMarkID(MarkID))
		wndMgr.MarkBox_SetIndex(self.hWnd, guild.GetMarkIndexByMarkID(MarkID))

	def SetAlpha(self, alpha):
		wndMgr.MarkBox_SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, float(alpha))

class ImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name = imageName
		wndMgr.LoadImage(self.hWnd, imageName)

	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, float(alpha))

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

class ExpandedImageBox(ImageBox):
	def __init__(self, layer = "UI"):
		ImageBox.__init__(self, layer)

	def __del__(self):
		ImageBox.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterExpandedImageBox(self, layer)

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)

	def SetOrigin(self, x, y):
		wndMgr.SetOrigin(self.hWnd, x, y)

	def SetRotation(self, rotation):
		wndMgr.SetRotation(self.hWnd, rotation)

	def SetRenderingMode(self, mode):
		wndMgr.SetRenderingMode(self.hWnd, mode)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetPercentage(self, curValue, maxValue):
		if curValue < maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def SetPercentageNew(self, percent):
		tmp = float(percent)/100.0
		self.SetRenderingRect(0.0, 0.0, tmp - 1.0, 0.0)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	def SetSizeFixed(self, width, height):
		self.SetScale(float(width)/float(wndMgr.GetWidth(self.hWnd)), float(height)/float(wndMgr.GetHeight(self.hWnd)))
		ImageBox.SetSize(self, width, height)
		

class AniImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterAniImageBox(self, layer)

	def SetDelay(self, delay):
		wndMgr.SetDelay(self.hWnd, delay)

	def AppendImage(self, filename):
		wndMgr.AppendImage(self.hWnd, filename)

	def SetPercentage(self, curValue, maxValue):
		if curValue > maxValue:
			wndMgr.SetRenderingRect(self.hWnd, 0.0, 0.0, 0.0, 0.0)
		else:
			wndMgr.SetRenderingRect(self.hWnd, 0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)

	def SetPercentageNew(self, percent):
		wndMgr.SetRenderingRect(self.hWnd, 0.0, 0.0, -1.0 + float(min(percent, 100)) / float(100.00), 0.0)

	def OnEndFrame(self):
		pass

############################################################################################################################################
### IMAGE CLASSES END ### IMAGE CLASSES END ### IMAGE CLASSES END ### IMAGE CLASSES END ### IMAGE CLASSES END ### IMAGE CLASSES END ########
############################################################################################################################################

############################################################################################################################################
### TEXT CLASSES ### TEXT CLASSES ### TEXT CLASSES ### TEXT CLASSES ### TEXT CLASSES ### TEXT CLASSES ### TEXT CLASSES ### TEXT CLASSES ####
############################################################################################################################################
class TextLine(Window):
	def __init__(self, font = None):
		Window.__init__(self)
		self.max = 0
		if font:
			self.SetFontName(font)
			self.SetPackedFontColor(colorinfo.COR_TEXTO_PADRAO)
		else:
			self.SetFontName('Verdana:12b')
			self.SetPackedFontColor(colorinfo.COR_TEXTO_PADRAO)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	def SetMax(self, max):
		wndMgr.SetMax(self.hWnd, max)

	def SetLimitWidth(self, width):
		wndMgr.SetLimitWidth(self.hWnd, width)

	def SetMultiLine(self):
		wndMgr.SetMultiLine(self.hWnd, True)

	def SetHorizontalAlignArabic(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_ARABIC)

	def SetHorizontalAlignLeft(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_LEFT)

	def SetHorizontalAlignRight(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_RIGHT)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_CENTER)

	def SetVerticalAlignTop(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_TOP)

	def SetVerticalAlignBottom(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_BOTTOM)

	def SetVerticalAlignCenter(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_CENTER)

	def SetSecret(self, Value = True):
		wndMgr.SetSecret(self.hWnd, Value)

	def SetOutline(self, Value = True):
		wndMgr.SetOutline(self.hWnd, Value)

	def SetFeather(self, value = True):
		wndMgr.SetFeather(self.hWnd, value)

	def SetFontName(self, fontName):
		wndMgr.SetFontName(self.hWnd, fontName)

	def SetDefaultFontName(self):
		wndMgr.SetFontName(self.hWnd, localeinfo.UI_DEF_FONT)

	def SetFontColor(self, red, green, blue):
		wndMgr.SetFontColor(self.hWnd, red, green, blue)

	def SetPackedFontColor(self, color):
		wndMgr.SetFontColor(self.hWnd, color)

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

	def GetText(self):
		return wndMgr.GetText(self.hWnd)

	def GetTextSize(self):
		return wndMgr.GetTextSize(self.hWnd)

	def SetTextLimited(self, text, limit):
		self.SetText(text)
		(ix, iy) = self.GetTextSize()
		i = 0
		if ix > limit:
			ix = 0
			while ix < limit:
				self.SetText(text[:i]+"...")
				(ix, iy) = self.GetTextSize()
				i = i + 1

	def SetTextLimitedNew(self, text, limit):
		if limit < 0:
			self.Hide()
			return

		self.SetText(text)
		(ix, iy) = self.GetTextSize()
		i = 0
		if ix > limit:
			ix = 0
			while ix < limit:
				self.SetText(text[:i])
				(ix, iy) = self.GetTextSize()
				i = i + 1

class EditLine(TextLine):
	if OLD_STUFF:
		candidateWindowClassDict = {}

	def __init__(self):
		TextLine.__init__(self)

		self.eventReturn = None
		self.eventReturnArgs = None

		self.eventEscape = None
		self.eventEscapeArgs = None

		self.eventTab = None
		self.eventTabArgs = None

		self.eventIMEUpdate = None
		self.eventIMEUpdateArgs = None

		self.eventFocus = None
		self.eventKillFocus = None
		self.numberMode = False
		self.moneyMode = False
		self.useIME = True
		self.bCodePage = False
		self.CanClick = None

		if OLD_STUFF:
			self.candidateWindowClass = None
			self.candidateWindow = None
			self.SetCodePage(app.GetDefaultCodePage())
			self.readingWnd = ReadingWnd()
			self.readingWnd.Hide()

	def __del__(self):
		TextLine.__del__(self)

	if OLD_STUFF:
		def SetCodePage(self, codePage):
			candidateWindowClass=EditLine.candidateWindowClassDict.get(codePage, EmptyCandidateWindow)
			self.__SetCandidateClass(candidateWindowClass)

		def __SetCandidateClass(self, candidateWindowClass):
			if self.candidateWindowClass==candidateWindowClass:
				return

			self.candidateWindowClass = candidateWindowClass
			self.candidateWindow = self.candidateWindowClass()
			self.candidateWindow.Load()
			self.candidateWindow.Hide()

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	def SetReturnEvent(self, event, *args):
		self.eventReturn = __mem_func__(event)
		self.eventReturnArgs = args

	def SetEscapeEvent(self, event, *args):
		self.eventEscape = __mem_func__(event)
		self.eventEscapeArgs = args

	def SetTabEvent(self, event, *args):
		self.eventTab = __mem_func__(event)
		self.eventTabArgs = args

	def SetMax(self, max):
		self.max = max
		wndMgr.SetMax(self.hWnd, self.max)
		ime.SetMax(self.max)
		self.SetUserMax(self.max)

	def SetUserMax(self, max):
		self.userMax = max
		ime.SetUserMax(self.userMax)

	def SetNumberMode(self):
		self.numberMode = True

	def SetMoneyMode(self):
		self.numberMode = False
		self.moneyMode = True

	def SetIMEFlag(self, flag):
		self.useIME = flag

	if app.ENABLE_EMOJI_SYSTEM:
		def SetTextEmoji(self, text):
			wndMgr.SetText(self.hWnd, text)

	def GetText(self):
		if self.moneyMode:
			return wndMgr.GetText(self.hWnd).replace(".", "")
		return wndMgr.GetText(self.hWnd)

	def SetText(self, text):
		if self.moneyMode:
			text = self.FormatToMoneyString(text)

		wndMgr.SetText(self.hWnd, text)

		if self.IsFocus():
			ime.SetText(text)

		if self.moneyMode:
			ime.SetCursorPosition(-1)

	def Enable(self):
		wndMgr.ShowCursor(self.hWnd)

	def Disable(self):
		wndMgr.HideCursor(self.hWnd)

	def SetEndPosition(self):
		ime.MoveEnd()

	def CanEdit(self, flag):
		self.CanClick = flag

	def SetFocusEvent(self, event):
		self.eventFocus = event

	def SetKillFocusEvent(self, event):
		self.eventKillFocus = event

	def OnSetFocus(self):
		Text = self.GetText()
		ime.SetText(Text)
		ime.SetMax(self.max)
		ime.SetUserMax(self.userMax)
		ime.SetCursorPosition(-1)

		if self.numberMode:
			ime.SetNumberMode()
		else:
			ime.SetStringMode()

		ime.EnableCaptureInput()

		if self.useIME:
			ime.EnableIME()
		else:
			ime.DisableIME()

		if self.eventFocus:
			self.eventFocus()

		wndMgr.ShowCursor(self.hWnd, True)

	def OnKillFocus(self):
		if self.eventKillFocus:
			self.eventKillFocus()

		self.SetText(ime.GetText(self.bCodePage))

		if OLD_STUFF:
			self.OnIMECloseCandidateList()
			self.OnIMECloseReadingWnd()

		ime.DisableIME()
		ime.DisableCaptureInput()
		wndMgr.HideCursor(self.hWnd)

	if OLD_STUFF:
		def OnIMEChangeCodePage(self):
			self.SetCodePage(ime.GetCodePage())

		def OnIMEOpenCandidateList(self):
			self.candidateWindow.Show()
			self.candidateWindow.Clear()
			self.candidateWindow.Refresh()

			gx, gy = self.GetGlobalPosition()
			self.candidateWindow.SetCandidatePosition(gx, gy, len(self.GetText()))
			return True

		def OnIMECloseCandidateList(self):
			self.candidateWindow.Hide()
			return True

		def OnIMEOpenReadingWnd(self):
			gx, gy = self.GetGlobalPosition()
			textlen = len(self.GetText())-2
			reading = ime.GetReading()
			readinglen = len(reading)
			self.readingWnd.SetReadingPosition( gx + textlen*6-24-readinglen*6, gy )
			self.readingWnd.SetText(reading)
			if ime.GetReadingError() == 0:
				self.readingWnd.SetTextColor(0xffffffff)
			else:
				self.readingWnd.SetTextColor(0xffff0000)
			self.readingWnd.SetSize(readinglen * 6 + 4, 19)
			self.readingWnd.Show()
			return True

		def OnIMECloseReadingWnd(self):
			self.readingWnd.Hide()
			return True

	def SetIMEUpdateEvent(self, event, *args):
		self.eventIMEUpdate = __mem_func__(event)
		self.eventIMEUpdateArgs = args

	def OnIMEUpdate(self):
		self.SetText(ime.GetText(self.bCodePage))
		if self.eventIMEUpdate:
			self.eventIMEUpdate(*self.eventIMEUpdateArgs)
			return True
		return False

	def FormatToMoneyString(self, text:str) -> str:
		if text in ["k", "K"]:
			return "1.000"
		elif text in ["m", "M"]:
			return "1.000.000"
		elif text in ["b", "B"]:
			return "1.000.000.000"
		elif text == "0":
			return ""

		text = text.replace(".", "")
		text = text.replace("k", "000")
		text = text.replace("m", "000000")
		text = text.replace("b", "000000000")
		text = text.replace("K", "000")
		text = text.replace("M", "000000")
		text = text.replace("B", "000000000")

		for item in text:
			if item not in "0123456789":
				text = text.replace(item, "")

		if len(text) and text:
			text = str(int(text))
		else:
			return ""

		return localeinfo.NumberToMoneyString(int(text))

	def OnIMETab(self) -> bool:
		if self.eventTab:
			self.eventTab(*self.eventTabArgs)
			return True
		return False

	def OnIMEReturn(self) -> True:
		if self.eventReturn:
			self.eventReturn(*self.eventReturnArgs)
		return True

	def OnPressEscapeKey(self) -> True:
		if self.eventEscape:
			self.eventEscape(*self.eventEscapeArgs)
		return True

	def OnKeyDown(self, key) -> bool:
		if app.DIK_F1 == key:
			return False
		if app.DIK_F2 == key:
			return False
		if app.DIK_F3 == key:
			return False
		if app.DIK_F4 == key:
			return False
		if app.DIK_LALT == key:
			return False
		if app.DIK_SYSRQ == key:
			return False
		if app.DIK_LCONTROL == key:
			return False
		if app.DIK_V == key:
			if app.IsPressed(app.DIK_LCONTROL):
				ime.PasteTextFromClipBoard()
		return True

	def OnKeyUp(self, key):
		if app.DIK_F1 == key:
			return False
		if app.DIK_F2 == key:
			return False
		if app.DIK_F3 == key:
			return False
		if app.DIK_F4 == key:
			return False
		if app.DIK_LALT == key:
			return False
		if app.DIK_SYSRQ == key:
			return False
		if app.DIK_LCONTROL == key:
			return False
		return True

	def OnIMEKeyDown(self, key):
		if app.VK_LEFT == key:
			ime.MoveLeft()
			return True
		if app.VK_RIGHT == key:
			ime.MoveRight()
			return True
		if app.VK_HOME == key:
			ime.MoveHome()
			return True
		if app.VK_END == key:
			ime.MoveEnd()
			return True
		if app.VK_DELETE == key:
			ime.Delete()
			TextLine.SetText(self, ime.GetText(self.bCodePage))
			return True
		return True

	def OnMouseLeftButtonDown(self):
		if False == self.IsIn():
			return False

		if False == self.CanClick:
			return

		self.SetFocus()
		PixelPosition = wndMgr.GetCursorPosition(self.hWnd)
		ime.SetCursorPosition(PixelPosition)

class ListBoxEx(Window):
	class Item(Window):
		def __init__(self):
			Window.__init__(self)

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent = proxy(parent)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			if self.parent.GetSelectedItem() == self:
				self.OnSelectedRender()

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.7, 0.7, 0.7, 0.5))
			grp.RenderBar(x, y + 1, self.GetWidth(), self.GetHeight() + 1)

	def __init__(self):
		Window.__init__(self)

		self.viewItemCount = 10
		self.basePos = 0
		self.itemHeight = 16
		self.itemStep = 20
		self.selItem = 0
		self.itemList = []
		self.onSelectItemEvent = None
		self.itemWidth = 100

		self.scrollBar = None
		self.__UpdateSize()

	def __del__(self):
		Window.__del__(self)

	def __UpdateSize(self):
		height = self.itemStep * self.__GetViewItemCount()
		self.SetSize(self.itemWidth, height)

	def IsEmpty(self):
		if len(self.itemList) == 0:
			return 1
		return 0

	def SetItemStep(self, itemStep):
		self.itemStep = itemStep
		self.__UpdateSize()

	def SetItemSize(self, itemWidth, itemHeight):
		self.itemWidth = itemWidth
		self.itemHeight = itemHeight
		self.__UpdateSize()

	def SetViewItemCount(self, viewItemCount):
		self.viewItemCount = viewItemCount

	def SetSelectEvent(self, event):
		self.onSelectItemEvent = __mem_func__(event)

	def SetBasePos(self, basePos):
		for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()

		self.basePos = basePos

		pos = basePos
		for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			(x, y) = self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x, y)
			newItem.Show()
			pos += 1

	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)

	def GetSelectedItem(self):
		return self.selItem

	def SelectIndex(self, index):
		if index >= len(self.itemList) or index < 0:
			self.selItem = None
			return

		try:
			self.selItem = self.itemList[index]
		except BaseException:
			pass

	def SelectItem(self, selItem):
		self.selItem = selItem
		if self.onSelectItemEvent:
			self.onSelectItemEvent(selItem)

	def RemoveAllItems(self):
		self.selItem = None
		self.itemList = []

		if self.scrollBar:
			self.scrollBar.SetPos(0)

	def RemoveItem(self, delItem):
		if delItem == self.selItem:
			self.selItem = None

		self.itemList.remove(delItem)

	def AppendItem(self, newItem):
		newItem.SetParent(self)
		newItem.SetSize(self.itemWidth, self.itemHeight)

		pos = len(self.itemList)
		if self.__IsInViewRange(pos):
			(x, y) = self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x, y)
			newItem.Show()
		else:
			newItem.Hide()

		self.itemList.append(newItem)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(self.__OnScroll)
		self.scrollBar = scrollBar

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos() * self.__GetScrollLen()))

	def __GetScrollLen(self):
		scrollLen = self.__GetItemCount() - self.__GetViewItemCount()
		if scrollLen < 0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def __GetItemCount(self):
		return len(self.itemList)

	def GetItemViewCoord(self, pos, itemWidth):
		return (0, (pos-self.basePos) * self.itemStep)

	def __IsInViewRange(self, pos):
		if pos < self.basePos:
			return 0
		if pos >= self.basePos + self.viewItemCount:
			return 0
		return 1

if app.ENABLE_SEND_TARGET_INFO:
	class ListBoxExNew(Window):
		class Item(Window):
			def __init__(self):
				Window.__init__(self)

				self.realWidth = 0
				self.realHeight = 0

				self.removeTop = 0
				self.removeBottom = 0

				self.SetWindowName("NONAME_ListBoxExNew_Item")

			def __del__(self):
				Window.__del__(self)

			def SetParent(self, parent):
				Window.SetParent(self, parent)
				self.parent = proxy(parent)

			def SetSize(self, width, height):
				self.realWidth = width
				self.realHeight = height
				Window.SetSize(self, width, height)

			def SetRemoveTop(self, height):
				self.removeTop = height
				self.RefreshHeight()

			def SetRemoveBottom(self, height):
				self.removeBottom = height
				self.RefreshHeight()

			def SetCurrentHeight(self, height):
				Window.SetSize(self, self.GetWidth(), height)

			def GetCurrentHeight(self):
				return Window.GetHeight(self)

			def ResetCurrentHeight(self):
				self.removeTop = 0
				self.removeBottom = 0
				self.RefreshHeight()

			def RefreshHeight(self):
				self.SetCurrentHeight(self.GetHeight() - self.removeTop - self.removeBottom)

			def GetHeight(self):
				return self.realHeight

		def __init__(self, stepSize, viewSteps):
			Window.__init__(self)

			self.viewItemCount = 10
			self.basePos = 0
			self.baseIndex = 0
			self.maxSteps = 0
			self.viewSteps = viewSteps
			self.stepSize = stepSize
			self.itemList = []

			self.scrollBar = None

			self.SetWindowName("NONAME_ListBoxEx")

		def __del__(self):
			Window.__del__(self)

		def IsEmpty(self):
			if len(self.itemList) == 0:
				return 1
			return 0

		def __CheckBasePos(self, pos):
			self.viewItemCount = 0

			start_pos = pos

			height = 0
			while height < self.GetHeight():
				if pos >= len(self.itemList):
					return start_pos == 0
				height += self.itemList[pos].GetHeight()
				pos += 1
				self.viewItemCount += 1
			return height == self.GetHeight()

		def SetBasePos(self, basePos, forceRefresh = True):
			if forceRefresh == False and self.basePos == basePos:
				return

			for oldItem in self.itemList[self.baseIndex:self.baseIndex+self.viewItemCount]:
				oldItem.ResetCurrentHeight()
				oldItem.Hide()

			self.basePos=basePos

			baseIndex = 0
			while basePos > 0:
				basePos -= self.itemList[baseIndex].GetHeight() / self.stepSize
				if basePos < 0:
					self.itemList[baseIndex].SetRemoveTop(self.stepSize * abs(basePos))
					break
				baseIndex += 1
			self.baseIndex = baseIndex

			stepCount = 0
			self.viewItemCount = 0
			while baseIndex < len(self.itemList):
				stepCount += self.itemList[baseIndex].GetCurrentHeight() / self.stepSize
				self.viewItemCount += 1
				if stepCount > self.viewSteps:
					self.itemList[baseIndex].SetRemoveBottom(self.stepSize * (stepCount - self.viewSteps))
					break
				elif stepCount == self.viewSteps:
					break
				baseIndex += 1

			y = 0
			for newItem in self.itemList[self.baseIndex: self.baseIndex + self.viewItemCount]:
				newItem.SetPosition(0, y)
				newItem.Show()
				y += newItem.GetCurrentHeight()

		def GetItemIndex(self, argItem):
			return self.itemList.index(argItem)

		def GetSelectedItem(self):
			return self.selItem

		def GetSelectedItemIndex(self):
			return self.selItemIdx

		def RemoveAllItems(self):
			self.itemList=[]
			self.maxSteps=0

			if self.scrollBar:
				self.scrollBar.SetPos(0)

		def RemoveItem(self, delItem):
			self.maxSteps -= delItem.GetHeight() / self.stepSize
			self.itemList.remove(delItem)

		def AppendItem(self, newItem):
			if newItem.GetHeight() % self.stepSize != 0:
				import dbg
				dbg.TraceError("Invalid AppendItem height %d stepSize %d" % (newItem.GetHeight(), self.stepSize))
				return

			self.maxSteps += newItem.GetHeight() / self.stepSize
			newItem.SetParent(self)
			self.itemList.append(newItem)

		def SetScrollBar(self, scrollBar):
			scrollBar.SetScrollEvent(self.__OnScroll)
			self.scrollBar = scrollBar

		def __OnScroll(self):
			self.SetBasePos(int(self.scrollBar.GetPos() * self.__GetScrollLen()), False)

		def __GetScrollLen(self):
			scrollLen = self.maxSteps-self.viewSteps
			if scrollLen < 0:
				return 0

			return scrollLen

		def __GetViewItemCount(self):
			return self.viewItemCount

		def __GetItemCount(self):
			return len(self.itemList)

		def GetViewItemCount(self):
			return self.viewItemCount

		def GetItemCount(self):
			return len(self.itemList)

#############################################################################################################################################################
### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ### NATIVE UI ###
#############################################################################################################################################################
class Button(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventFunc = None
		self.eventArgs = None

		self.ButtonText = None
		self.ToolTipText = None

	def __del__(self):
		self.eventFunc = None
		self.eventArgs = None
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterButton(self, layer)

	def SetUpVisual(self, filename):
		wndMgr.SetUpVisual(self.hWnd, filename)

	def SetOverVisual(self, filename):
		wndMgr.SetOverVisual(self.hWnd, filename)

	def SetDownVisual(self, filename):
		wndMgr.SetDownVisual(self.hWnd, filename)

	def SetDisableVisual(self, filename):
		wndMgr.SetDisableVisual(self.hWnd, filename)

	def GetUpVisualFileName(self):
		return wndMgr.GetUpVisualFileName(self.hWnd)

	def GetOverVisualFileName(self):
		return wndMgr.GetOverVisualFileName(self.hWnd)

	def GetDownVisualFileName(self):
		return wndMgr.GetDownVisualFileName(self.hWnd)

	def Flash(self):
		wndMgr.Flash(self.hWnd)

	def Enable(self):
		wndMgr.Enable(self.hWnd)

	def Disable(self):
		wndMgr.Disable(self.hWnd)

	def Down(self):
		wndMgr.Down(self.hWnd)

	def SetUp(self):
		wndMgr.SetUp(self.hWnd)

	def SetTextColor(self, color):
		if not self.ButtonText:
			return
		self.ButtonText.SetPackedFontColor(color)

	def SetText(self, text, height = 4):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	def GetText(self):
		if not self.ButtonText:
			return ""
		return self.ButtonText.GetText()

	def SetTextAlignLeft(self, text, height = 4):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(27, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)
		self.ButtonText.SetPosition(27, self.GetHeight()/2)
		self.ButtonText.SetVerticalAlignCenter()
		self.ButtonText.SetHorizontalAlignLeft()

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:
			toolTip = createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText = toolTip
		self.ToolTipText.SetText(text)

	def SetToolTipWindow(self, toolTip):
		self.ToolTipText = toolTip
		self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x = 0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def SetEvent(self, func, *args):
		if func:
			self.eventFunc = __mem_func__(func)
			self.eventArgs = args
		else:
			self.eventFunc = None
			self.eventArgs = None

	def CallEvent(self):
		snd.PlaySound("sound/ui/click.wav")

		if self.eventFunc:
			self.eventFunc(*self.eventArgs)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def IsDown(self):
		return wndMgr.IsDown(self.hWnd)

	if app.ENABLE_EMOJI_SYSTEM:
		def SetButtonScale(self, xScale, yScale):
			wndMgr.SetButtonScale(self.hWnd, xScale, yScale)

	if app.ENABLE_SKILL_COLOR_SYSTEM:
		def SetTextAlignLeft(self, text, x = 27, height = 4):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(x, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignLeft()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)
			self.ButtonText.SetPosition(x, self.GetHeight()/2)
			self.ButtonText.SetVerticalAlignCenter()
			self.ButtonText.SetHorizontalAlignLeft()

		def SetListText(self, text, x = 8):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(x, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignLeft()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)

class RadioButton(Button):
	def __init__(self):
		Button.__init__(self)

	def __del__(self):
		Button.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterRadioButton(self, layer)

class ToggleButton(Button):
	def __init__(self):
		Button.__init__(self)

		self.eventUp = None
		self.eventUpArgs = None

		self.eventDown = None
		self.eventDownArgs = None

	def __del__(self):
		self.eventUp = None
		self.eventUpArgs = None

		self.eventDown = None
		self.eventDownArgs = None

		Button.__del__(self)

	def SetToggleUpEvent(self, event, *args):
		if event:
			self.eventUp = __mem_func__(event)
			self.eventUpArgs = args
		else:
			self.eventUp = None
			self.eventUpArgs = None

	def SetToggleDownEvent(self, event, *args):
		if event:
			self.eventDown = __mem_func__(event)
			self.eventDownArgs = args
		else:
			self.eventDown = None
			self.eventDownArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterToggleButton(self, layer)

	def OnToggleUp(self):
		if self.eventUp:
			self.eventUp(*self.eventUpArgs)

	def OnToggleDown(self):
		if self.eventDown:
			self.eventDown(*self.eventDownArgs)

class DragButton(Button):
	def __init__(self):
		Button.__init__(self)
		self.AddFlag("movable")

		self.callbackEnable = True
		self.eventMove = None

	def __del__(self):
		self.eventMove = None
		Button.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterDragButton(self, layer)

	def SetMoveEvent(self, event):
		self.eventMove = __mem_func__(event)

	def SetRestrictMovementArea(self, x, y, width, height):
		wndMgr.SetRestrictMovementArea(self.hWnd, x, y, width, height)

	def TurnOnCallBack(self):
		self.callbackEnable = True

	def TurnOffCallBack(self):
		self.callbackEnable = False

	def OnMove(self):
		if self.callbackEnable:
			if self.eventMove:
				self.eventMove()

class NumberLine(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterNumberLine(self, layer)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetNumberHorizontalAlignCenter(self.hWnd)

	def SetHorizontalAlignRight(self):
		wndMgr.SetNumberHorizontalAlignRight(self.hWnd)

	def SetPath(self, path):
		wndMgr.SetPath(self.hWnd, path)

	def SetNumber(self, number):
		wndMgr.SetNumber(self.hWnd, number)

class Box(Window):
	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBox(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Bar(Window):
	color = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar(self, layer)

	def SetColor(self, color):
		self.color = color
		wndMgr.SetColor(self.hWnd, color)

	def GetColor(self):
		return self.color

class Line(Window):
	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterLine(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class SlotBar(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

class Bar3D(Window):
	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

	def SetColor(self, left, right, center):
		wndMgr.SetColor(self.hWnd, left, right, center)

class SlotWindow(Window):
	def __init__(self):
		Window.__init__(self)

		self.StartIndex = 0

		self.eventSelectEmptySlot = None
		self.eventSelectEmptyArgs = None

		self.eventSelectItemSlot = None
		self.eventSelectItemArgs = None

		self.eventUnselectEmptySlot = None
		self.eventUnselectEmptyArgs = None

		self.eventUnselectItemSlot = None
		self.eventUnselectItemArgs = None

		self.eventUseSlot = None
		self.eventUseArgs = None

		self.eventOverInItem = None
		self.eventOverInArgs = None

		self.eventOverOutItem = None
		self.eventOverOutArgs = None

		self.eventPressedSlotButton = None
		self.eventPressedSlotArgs = None

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterSlotWindow(self, layer)

	def SetSlotStyle(self, style):
		wndMgr.SetSlotStyle(self.hWnd, style)

	def HasSlot(self, slotIndex):
		return wndMgr.HasSlot(self.hWnd, slotIndex)

	def SetSlotBaseImage(self, imageFileName, r, g, b, a):
		wndMgr.SetSlotBaseImage(self.hWnd, imageFileName, r, g, b, a)

	def SetCoverButton(self, slotIndex,\
						upName="d:/ymir work/ui/public/slot_cover_button_01.sub",\
						overName="d:/ymir work/ui/public/slot_cover_button_02.sub",\
						downName="d:/ymir work/ui/public/slot_cover_button_03.sub",\
						disableName="d:/ymir work/ui/public/slot_cover_button_04.sub",\
						LeftButtonEnable = False,\
						RightButtonEnable = True):
		wndMgr.SetCoverButton(self.hWnd, slotIndex, upName, overName, downName, disableName, LeftButtonEnable, RightButtonEnable)

	def EnableCoverButton(self, slotIndex):
		wndMgr.EnableCoverButton(self.hWnd, slotIndex)

	def DisableCoverButton(self, slotIndex):
		wndMgr.DisableCoverButton(self.hWnd, slotIndex)

	def SetAlwaysRenderCoverButton(self, slotIndex, bAlwaysRender = True):
		wndMgr.SetAlwaysRenderCoverButton(self.hWnd, slotIndex, bAlwaysRender)

	def AppendSlotButton(self, upName, overName, downName):
		wndMgr.AppendSlotButton(self.hWnd, upName, overName, downName)

	def ShowSlotButton(self, slotNumber):
		wndMgr.ShowSlotButton(self.hWnd, slotNumber)

	def HideAllSlotButton(self):
		wndMgr.HideAllSlotButton(self.hWnd)

	def AppendRequirementSignImage(self, filename):
		wndMgr.AppendRequirementSignImage(self.hWnd, filename)

	def ShowRequirementSign(self, slotNumber):
		wndMgr.ShowRequirementSign(self.hWnd, slotNumber)

	def HideRequirementSign(self, slotNumber):
		wndMgr.HideRequirementSign(self.hWnd, slotNumber)

	def ActivateSlot(self, slotNumber):
		wndMgr.ActivateSlot(self.hWnd, slotNumber)

	def DeactivateSlot(self, slotNumber):
		wndMgr.DeactivateSlot(self.hWnd, slotNumber)

	def SetUsableSlot(self, index):
		wndMgr.SetUsableSlot(self.hWnd, index)

	def SetUnusableWorldSlot(self, index):
		wndMgr.SetUnusableWorldSlot(self.hWnd, index)

	def SetUnusableSlot(self, index):
		wndMgr.SetUnusableSlot(self.hWnd, index)

	def SetUsableWorldSlot(self, index):
		wndMgr.SetUsableWorldSlot(self.hWnd, index)

	def ShowSlotBaseImage(self, slotNumber):
		wndMgr.ShowSlotBaseImage(self.hWnd, slotNumber)

	def HideSlotBaseImage(self, slotNumber):
		wndMgr.HideSlotBaseImage(self.hWnd, slotNumber)

	def SetButtonEvent(self, button, state, event, *args):
		if "LEFT" == button:
			if "EMPTY" == state:
				self.eventSelectEmptySlot = __mem_func__(event)
				self.eventSelectEmptyArgs = args
			elif "EXIST" == state:
				self.eventSelectItemSlot = __mem_func__(event)
				self.eventSelectItemArgs = args
			elif "ALWAYS" == state:
				self.eventSelectEmptySlot = __mem_func__(event)
				self.eventSelectEmptyArgs = args
				self.eventSelectItemSlot = __mem_func__(event)
				self.eventSelectItemArgs = args
		elif "RIGHT" == button:
			if "EMPTY" == state:
				self.eventUnselectEmptySlot = __mem_func__(event)
				self.eventUnselectEmptyArgs = args
			elif "EXIST" == state:
				self.eventUnselectItemSlot = __mem_func__(event)
				self.eventUnselectItemArgs = args
			elif "ALWAYS" == state:
				self.eventUnselectEmptySlot = __mem_func__(event)
				self.eventUnselectEmptyArgs = args
				self.eventUnselectItemSlot = __mem_func__(event)
				self.eventUnselectItemArgs = args

	def SetSelectEmptySlotEvent(self, event, *args):
		self.eventSelectEmptySlot = __mem_func__(event)
		self.eventSelectEmptyArgs = args

	def SetSelectItemSlotEvent(self, event, *args):
		self.eventSelectItemSlot = __mem_func__(event)
		self.eventSelectItemArgs = args

	def SetUnselectEmptySlotEvent(self, event, *args):
		self.eventUnselectEmptySlot = __mem_func__(event)
		self.eventUnselectEmptyArgs = args

	def SetUnselectItemSlotEvent(self, event, *args):
		self.eventUnselectItemSlot = __mem_func__(event)
		self.eventUnselectItemArgs = args

	def SetUseSlotEvent(self, event, *args):
		self.eventUseSlot = __mem_func__(event)
		self.eventUseArgs = args

	def SetOverInItemEvent(self, event, *args):
		self.eventOverInItem = __mem_func__(event)
		self.eventOverInArgs = args

	def SetOverOutItemEvent(self, event, *args):
		self.eventOverOutItem = __mem_func__(event)
		self.eventOverOutArgs = args

	def SetPressedSlotButtonEvent(self, event, *args):
		self.eventPressedSlotButton = __mem_func__(event)
		self.eventPressedSlotArgs = args

	def GetSlotCount(self):
		return wndMgr.GetSlotCount(self.hWnd)

	def SetUseMode(self, flag):
		wndMgr.SetUseMode(self.hWnd, flag)

	def SetUsableItem(self, flag):
		wndMgr.SetUsableItem(self.hWnd, flag)

	def SetUsableItem2(self, flag): 
		wndMgr.SetUsableItem(self.hWnd, flag)

	def SetCanMouseEventSlot(self, slotIndex):
		wndMgr.SetCanMouseEventSlot(self.hWnd, slotIndex)

	def SetCantMouseEventSlot(self, slotIndex):
		wndMgr.SetCantMouseEventSlot(self.hWnd, slotIndex)

	def SetUsableSlotOnTopWnd(self, slotIndex):
		wndMgr.SetUsableSlotOnTopWnd(self.hWnd, slotIndex)

	def SetUnusableSlotOnTopWnd(self, slotIndex):
		wndMgr.SetUnusableSlotOnTopWnd(self.hWnd, slotIndex)

	def SetSlotCoolTime(self, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.SetSlotCoolTime(self.hWnd, slotIndex, coolTime, elapsedTime)

	def DisableSlot(self, slotIndex):
		wndMgr.DisableSlot(self.hWnd, slotIndex)

	def EnableSlot(self, slotIndex):
		wndMgr.EnableSlot(self.hWnd, slotIndex)

	def LockSlot(self, slotIndex):
		wndMgr.LockSlot(self.hWnd, slotIndex)

	def UnlockSlot(self, slotIndex):
		wndMgr.UnlockSlot(self.hWnd, slotIndex)

	def RefreshSlot(self):
		wndMgr.RefreshSlot(self.hWnd)

	def ClearSlot(self, slotNumber):
		wndMgr.ClearSlot(self.hWnd, slotNumber)

	def ClearAllSlot(self):
		wndMgr.ClearAllSlot(self.hWnd)

	def AppendSlot(self, index, x, y, width, height):
		wndMgr.AppendSlot(self.hWnd, index, x, y, width, height)

	def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

	def SetSlotCount(self, slotNumber, count):
		wndMgr.SetSlotCount(self.hWnd, slotNumber, count)

	def SetSlotCountNew(self, slotNumber, grade, count):
		wndMgr.SetSlotCountNew(self.hWnd, slotNumber, grade, count)

	def SetItemSlot(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)
		itemName = item.GetItemName().strip()
		itemNameP = item.GetItemName().rfind('+')
		if itemNameP > 0 and len(itemName) > itemNameP + 1:
			level=itemName[itemNameP + 1:]
			if level.isdigit():
				wndMgr.SetSlotLevelImage(self.hWnd, renderingSlotNumber, ("icon/level/%d.tga"%int(level)))

	def SetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel):
		skillIcon = skill.GetIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, skillLevel)

	def SetSkillSlotNew(self, renderingSlotNumber, skillIndex, skillGrade, skillLevel):
		skillIcon = skill.GetIconImageNew(skillIndex, skillGrade)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)

	def SetEmotionSlot(self, renderingSlotNumber, emotionIndex):
		icon = player.GetEmotionIconImage(emotionIndex)

		if 0 == icon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, emotionIndex, 1, 1, icon)

	def OnSelectEmptySlot(self, slotNumber):
		if self.eventSelectEmptySlot:
			if self.eventSelectEmptyArgs:
				self.eventSelectEmptySlot(*self.eventSelectEmptyArgs)
			else:
				self.eventSelectEmptySlot(slotNumber)

	def OnSelectItemSlot(self, slotNumber):
		if self.eventSelectItemSlot:
			if self.eventSelectItemArgs:
				self.eventSelectItemSlot(*self.eventSelectItemArgs)
			else:
				self.eventSelectItemSlot(slotNumber)

	def OnUnselectEmptySlot(self, slotNumber):
		if self.eventUnselectEmptySlot:
			if self.eventUnselectEmptyArgs:
				self.eventUnselectEmptySlot(*self.eventUnselectEmptyArgs)
			else:
				self.eventUnselectEmptySlot(slotNumber)

	def OnUnselectItemSlot(self, slotNumber):
		if self.eventUnselectItemSlot:
			if self.eventUnselectItemArgs:
				self.eventUnselectItemSlot(*self.eventUnselectItemArgs)
			else:
				self.eventUnselectItemSlot(slotNumber)

	def OnUseSlot(self, slotNumber):
		if self.eventUseSlot:
			if self.eventUseArgs:
				self.eventUseSlot(*self.eventUseArgs)
			else:
				self.eventUseSlot(slotNumber)

	def OnOverInItem(self, slotNumber):
		if self.eventOverInItem:
			if self.eventOverInArgs:
				self.eventOverInItem(*self.eventOverInArgs)
			else:
				self.eventOverInItem(slotNumber)

	def OnOverOutItem(self):
		if self.eventOverOutItem:
			if self.eventOverOutArgs:
				self.eventOverOutItem(*self.eventOverOutArgs)
			else:
				self.eventOverOutItem()

	def OnPressedSlotButton(self, slotNumber):
		if self.eventPressedSlotButton:
			if self.eventPressedSlotArgs:
				self.eventPressedSlotButton(*self.eventPressedSlotArgs)
			else:
				self.eventPressedSlotButton(slotNumber)

	def GetStartIndex(self):
		return 0

class GridSlotWindow(SlotWindow):
	def __init__(self):
		SlotWindow.__init__(self)

		self.startIndex = 0

	def __del__(self):
		SlotWindow.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterGridSlotWindow(self, layer)

	def ArrangeSlot(self, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank):
		self.startIndex = StartIndex

		wndMgr.ArrangeSlot(self.hWnd, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank)
		self.startIndex = StartIndex

	def GetStartIndex(self):
		return self.startIndex

class Gauge(Window):
	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 12
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.width = 0

		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None
		self.ToolTipText = None

	def __del__(self):
		Window.__del__(self)
		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None
		self.ToolTipText = None

	def MakeGauge(self, width, color):
		self.width = max(48, width)

		imgSlotLeft = ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage("d:/ymir work/ui/pattern/gauge_slot_left.tga")
		imgSlotLeft.Show()

		imgSlotRight = ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage("d:/ymir work/ui/pattern/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage("d:/ymir work/ui/pattern/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge

		self.SetSize(width, self.SLOT_HEIGHT)

	def SetPercentage(self, curValue, maxValue):
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)

	def SetShowToolTipEvent(self, func, *args):
		self.showtooltipevent = __mem_func__(func)
		self.showtooltiparg = args

	def SetHideToolTipEvent(self, func, *args):
		self.hidetooltipevent = __mem_func__(func)
		self.hidetooltiparg = args

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def SetToolTipText(self, text, x=0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:
			toolTip = createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText = toolTip

		self.ToolTipText.SetText(text)

#################################################################################################################################
### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ###
#################################################################################################################################
class ScrollBar(Window):
	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 5
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Top.tga")
			top.SetPosition(0, 0)
			top.AddFlag("not_pick")
			top.Show()
			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Middle.tga")
			middle.SetPosition(0, 4)
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.bottom = bottom
			self.middle = middle

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)
			self.bottom.SetPosition(0, height-4)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.lockFlag = False
		self.scrollStep = 0.20
		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = Bar3D()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(self.OnMove)
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(self.OnUp)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_up_button_03.sub")
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(self.OnDown)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_down_button_03.sub")
		downButton.Show()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()

	def Destroy(self):
		self.Hide()
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.eventScroll = None

	def SetScrollEvent(self, event):
		self.eventScroll = __mem_func__(event)

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 0)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
		self.barSlot.SetSize(self.GetWidth() - 2, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):
		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		if self.eventScroll:
			self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

class ThinScrollBar(ScrollBar):
	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(self.OnMove)
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_02.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_03.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_03.sub")
		upButton.SetEvent(self.OnUp)
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_03.sub")
		downButton.SetEvent(self.OnDown)
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class SmallThinScrollBar(ScrollBar):

	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(self.OnMove)
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_03.sub")
		upButton.SetEvent(self.OnUp)
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_03.sub")
		downButton.SetEvent(self.OnDown)
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class TitleBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 23

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)

	def MakeTitleBar(self, width):
		width = max(64, width)

		imgLeft = ImageBox()
		imgCenter = ExpandedImageBox()
		imgRight = ImageBox()
		imgLeft.AddFlag("not_pick")
		imgCenter.AddFlag("not_pick")
		imgRight.AddFlag("not_pick")
		imgLeft.SetParent(self)
		imgCenter.SetParent(self)
		imgRight.SetParent(self)

		imgLeft.LoadImage("d:/ymir work/ui/pattern/titlebar_left.tga")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/titlebar_center.tga")
		imgRight.LoadImage("d:/ymir work/ui/pattern/titlebar_right.tga")

		imgLeft.Show()
		imgCenter.Show()
		imgRight.Show()

		btnClose = Button()
		btnClose.SetParent(self)
		btnClose.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		btnClose.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		btnClose.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		btnClose.SetToolTipText(localeinfo.UI_CLOSE, 0, -23)
		btnClose.Show()

		self.__txtTitle = None

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.btnClose = btnClose

		self.SetWidth(width)

	def SetTitle(self, title):
		if not self.__txtTitle:
			self.__txtTitle = TextLine()
			self.__txtTitle.SetParent(self)
			self.__txtTitle.SetPackedFontColor(grp.GenerateColor(1.0, 1.0, 1.0, 1.0))
			self.__txtTitle.SetHorizontalAlignCenter()
			self.__txtTitle.SetVerticalAlignBottom()
			self.__txtTitle.Show()

		self.__txtTitle.SetText(title)
		self.UpdateTitlePosition()

	def UpdateTitlePosition(self):
		if not self.__txtTitle:
			return

		self.__txtTitle.SetPosition(self.GetWidth() / 2, 17)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)

		self.btnClose.SetPosition(width - self.btnClose.GetWidth() - 3, 3)

		self.SetSize(width, self.BLOCK_HEIGHT)

		self.UpdateTitlePosition()

	def SetCloseEvent(self, event, args = None):
		self.btnClose.SetEvent(event, args)

class HorizontalBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 17

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)

	def Create(self, width):

		width = max(96, width)

		imgLeft = ImageBox()
		imgLeft.SetParent(self)
		imgLeft.AddFlag("not_pick")
		imgLeft.LoadImage("d:/ymir work/ui/pattern/horizontalbar_left.tga")
		imgLeft.Show()

		imgCenter = ExpandedImageBox()
		imgCenter.SetParent(self)
		imgCenter.AddFlag("not_pick")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/horizontalbar_center.tga")
		imgCenter.Show()

		imgRight = ImageBox()
		imgRight.SetParent(self)
		imgRight.AddFlag("not_pick")
		imgRight.LoadImage("d:/ymir work/ui/pattern/horizontalbar_right.tga")
		imgRight.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.SetWidth(width)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
		self.SetSize(width, self.BLOCK_HEIGHT)

class Board(Window):

	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self):
		Window.__init__(self)

		self.MakeBoard("d:/ymir work/ui/pattern/Board_Corner_", "d:/ymir work/ui/pattern/Board_Line_")
		self.MakeBase()

	def MakeBoard(self, cornerPath, linePath):

		CornerFileNames = [ cornerPath+dir+".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]
		LineFileNames = [ linePath+dir+".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/Board_Base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class BoardWithTitleBar(Board):
	def __init__(self):
		Board.__init__(self)

		titleBar = TitleBar()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0)
		titleBar.SetPosition(8, 7)
		titleBar.Show()

		self.titleBar = titleBar

		self.SetTitle = __mem_func__(self.titleBar.SetTitle)
		self.SetTitleName = __mem_func__(self.titleBar.SetTitle)
		self.SetCloseEvent(self.Hide)

	def __del__(self):
		Board.__del__(self)
		self.titleBar = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		Board.SetSize(self, width, height)

	def SetCloseEvent(self, event, args = None):
		self.titleBar.SetCloseEvent(event, args)

class ThinBoard(Window):

	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class SliderBar(Window):
	def __init__(self):
		Window.__init__(self)

		self.curPos = 1.0
		self.pageSize = 1.0
		self.eventChange = None

		self.__CreateBackGroundImage()
		self.__CreateCursor()

	def __del__(self):
		Window.__del__(self)

	def __CreateBackGroundImage(self):
		img = ImageBox()
		img.SetParent(self)
		img.LoadImage("d:/ymir work/ui/game/windows/sliderbar.sub")
		img.Show()
		self.backGroundImage = img
		self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())

	def __CreateCursor(self):
		cursor = DragButton()
		cursor.AddFlag("movable")
		cursor.AddFlag("restrict_y")
		cursor.SetParent(self)
		cursor.SetMoveEvent(self.__OnMove)
		cursor.SetUpVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetOverVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.SetDownVisual("d:/ymir work/ui/game/windows/sliderbar_cursor.sub")
		cursor.Show()
		self.cursor = cursor
		self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)
		self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

	def __OnMove(self):
		(xLocal, yLocal) = self.cursor.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)

		if self.eventChange:
			self.eventChange()

	def SetSliderPos(self, pos):
		self.curPos = pos
		self.cursor.SetPosition(int(self.pageSize * pos), 0)

	def GetSliderPos(self):
		return self.curPos

	def SetEvent(self, event):
		self.eventChange = __mem_func__(event)

	def Enable(self):
		self.cursor.Show()

	def Disable(self):
		self.cursor.Hide()

class ListBox(Window):
	TEMPORARY_PLACE = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.overLine = -1
		self.selectedLine = -1
		self.width = 0
		self.height = 0
		self.stepSize = 17
		self.basePos = 0
		self.showLineCount = 0
		self.itemCenterAlign = True
		self.itemList = []
		self.keyDict = {}
		self.textDict = {}
		self.event = None

	def __del__(self):
		Window.__del__(self)

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetTextCenterAlign(self, flag):
		self.itemCenterAlign = flag

	def SetBasePos(self, pos):
		self.basePos = pos
		self._LocateItem()

	def ClearItem(self):
		self.keyDict = {}
		self.textDict = {}
		self.itemList = []
		self.overLine = -1
		self.selectedLine = -1

	def InsertItem(self, number, text):
		self.keyDict[len(self.itemList)] = number
		self.textDict[len(self.itemList)] = text

		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetText(text)
		textLine.Show()

		if self.itemCenterAlign:
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		self.itemList.append(textLine)

		self._LocateItem()

	def ChangeItem(self, number, text):
		for key, value in self.keyDict.items():
			if value == number:
				self.textDict[key] = text

				if number < len(self.itemList):
					self.itemList[key].SetText(text)
				return

	def LocateItem(self):
		self._LocateItem()

	def _LocateItem(self):
		skipCount = self.basePos
		yPos = 0
		self.showLineCount = 0

		for textLine in self.itemList:
			textLine.Hide()

			if skipCount > 0:
				skipCount -= 1
				continue

			textLine.SetPosition(0, yPos + 3)

			yPos += self.stepSize

			if yPos <= self.GetHeight():
				self.showLineCount += 1
				textLine.Show()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.itemList) * self.stepSize)
		self._LocateItem()

	def GetViewItemCount(self):
		return int(self.GetHeight() / self.stepSize)

	def GetItemCount(self):
		return len(self.itemList)

	def SetEvent(self, event):
		self.event = __mem_func__(event)

	def SelectItem(self, line):
		if not self.keyDict.__contains__(line):
			return

		if line == self.selectedLine:
			return

		self.selectedLine = line

		if self.event:
			self.event(self.keyDict.get(line, 0), self.textDict.get(line, "None"))

	def GetSelectedItem(self):
		return self.keyDict.get(self.selectedLine, 0)

	def OnMouseLeftButtonDown(self):
		if self.overLine < 0:
			return

	def OnMouseLeftButtonUp(self):
		if self.overLine >= 0:
			self.SelectItem(self.overLine+self.basePos)

	def OnUpdate(self):
		self.overLine = -1

		if self.IsIn():
			x, y = self.GetGlobalPosition()
			height = self.GetHeight()
			xMouse, yMouse = wndMgr.GetMousePosition()

			if yMouse - y < height - 1:
				self.overLine = (yMouse - y) / self.stepSize

				if self.overLine < 0:
					self.overLine = -1
				if self.overLine >= len(self.itemList):
					self.overLine = -1

	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE*2
		
		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize)				

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize)

class ListBox2(ListBox):
	def __init__(self, *args, **kwargs):
		ListBox.__init__(self, *args, **kwargs)
		self.rowCount = 10
		self.barWidth = 0
		self.colCount = 0

	def SetRowCount(self, rowCount):
		self.rowCount = rowCount

	def SetSize(self, width, height):
		ListBox.SetSize(self, width, height)
		self._RefreshForm()

	def ClearItem(self):
		ListBox.ClearItem(self)
		self._RefreshForm()

	def InsertItem(self, *args, **kwargs):
		ListBox.InsertItem(self, *args, **kwargs)
		self._RefreshForm()

	def OnUpdate(self):
		mpos = wndMgr.GetMousePosition()
		self.overLine = self._CalcPointIndex(mpos)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		pos = (x + 2, y)

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			self._RenderBar(pos, self.overLine)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					self._RenderBar(pos, self.selectedLine-self.basePos)

	def _CalcPointIndex(self, mpos):
		if self.IsIn():
			px, py = mpos
			gx, gy = self.GetGlobalPosition()
			lx, ly = px - gx, py - gy

			col = lx / self.barWidth
			row = ly / self.stepSize
			idx = col * self.rowCount + row
			if col >= 0 and col < self.colCount:
				if row >= 0 and row < self.rowCount:
					if idx >= 0 and idx < len(self.itemList):
						return idx
		return -1

	def _CalcRenderPos(self, pos, idx):
		x, y = pos
		row = idx % self.rowCount
		col = idx / self.rowCount
		return (x + col * self.barWidth, y + row * self.stepSize)

	def _RenderBar(self, basePos, idx):
		x, y = self._CalcRenderPos(basePos, idx)
		grp.RenderBar(x, y, self.barWidth - 3, self.stepSize)

	def _LocateItem(self):
		pos = (0, self.TEMPORARY_PLACE)

		self.showLineCount = 0
		for textLine in self.itemList:
			x, y = self._CalcRenderPos(pos, self.showLineCount)
			textLine.SetPosition(x, y)
			textLine.Show()

			self.showLineCount += 1

	def _RefreshForm(self):
		if len(self.itemList) % self.rowCount:
			self.colCount = len(self.itemList) / self.rowCount + 1
		else:
			self.colCount = len(self.itemList) / self.rowCount

		if self.colCount:
			self.barWidth = self.width / self.colCount
		else:
			self.barWidth = self.width

#################################################################################################################################
### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT ####
#################################################################################################################################
'''
class CandidateListBox(ListBoxEx):

	HORIZONTAL_MODE = 0
	VERTICAL_MODE = 1

	class Item(ListBoxEx.Item):
		def __init__(self, text):
			ListBoxEx.Item.__init__(self)

			self.textBox=TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.Show()

		def __del__(self):
			ListBoxEx.Item.__del__(self)

	def __init__(self, mode = HORIZONTAL_MODE):
		ListBoxEx.__init__(self)
		self.itemWidth=32
		self.itemHeight=32
		self.mode = mode

	def __del__(self):
		ListBoxEx.__del__(self)

	def SetMode(self, mode):
		self.mode = mode

	def AppendItem(self, newItem):
		ListBoxEx.AppendItem(self, newItem)

	def GetItemViewCoord(self, pos):
		if self.mode == self.HORIZONTAL_MODE:
			return ((pos-self.basePos)*self.itemStep, 0)
		elif self.mode == self.VERTICAL_MODE:
			return (0, (pos-self.basePos)*self.itemStep)

class RadioButtonGroup:
	def __init__(self):
		self.buttonGroup = []
		self.selectedBtnIdx = -1

	def __del__(self):
		for button, ue, de in self.buttonGroup:
			button.__del__()

	def Show(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Show()

	def Hide(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Hide()

	def SetText(self, idx, text):
		if idx >= len(self.buttonGroup):
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[idx]
		button.SetText(text)

	def OnClick(self, btnIdx):
		if btnIdx == self.selectedBtnIdx:
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[self.selectedBtnIdx]
		if unselectEvent:
			unselectEvent()
		button.SetUp()

		self.selectedBtnIdx = btnIdx
		(button, selectEvent, unselectEvent) = self.buttonGroup[btnIdx]
		if selectEvent:
			selectEvent()

		button.Down()

	def AddButton(self, button, selectEvent, unselectEvent):
		i = len(self.buttonGroup)
		button.SetEvent(self.OnClick, i)
		self.buttonGroup.append([button, selectEvent, unselectEvent])
		button.SetUp()

	def Create(rawButtonGroup):
		radioGroup = RadioButtonGroup()
		for (button, selectEvent, unselectEvent) in rawButtonGroup:
			radioGroup.AddButton(button, selectEvent, unselectEvent)

		radioGroup.OnClick(0)

		return radioGroup

	Create = staticmethod(Create)

class ComboBox(Window):
	class ListBoxWithBoard(ListBox):
		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			grp.SetColor(BRIGHT_COLOR)
			grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
			grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

			ListBox.OnRender(self)

	def __init__(self):
		Window.__init__(self)
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		self.isSelected = False
		self.isOver = False
		self.isListOpened = False
		self.event = None
		self.enable = True

		self.textLine = MakeTextLine(self)
		self.textLine.SetText(localeinfo.UI_ITEM)

		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(self.OnSelectItem)
		self.listBox.Hide()

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.Hide()
		self.textLine = None
		self.listBox = None

	def SetPosition(self, x, y):
		Window.SetPosition(self, x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = True

	def Disable(self):
		self.enable = False
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event):
		self.event = __mem_func__(event)

	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):
		self.CloseListBox()
		if self.event:
			self.event(index)

	def CloseListBox(self):
		self.isListOpened = False
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.enable:
			return

		self.isSelected = True

	def OnMouseLeftButtonUp(self):
		if not self.enable:
			return

		self.isSelected = False

		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = True
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):
		if not self.enable:
			return

		if self.IsIn():
			self.isOver = True
		else:
			self.isOver = False

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		grp.SetColor(BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		grp.SetColor(DARK_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.SetColor(BRIGHT_COLOR)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		if self.isOver:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

			if self.isSelected:
				grp.SetColor(WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

class TextLink(Window):
	NORMAL_COLOR =  0xffa08784
	OVER_COLOR = 0xffe6d0a2
	DOWN_COLOR = 0xffefe4cd

	def __init__(self):
		Window.__init__(self)

		self.eventFunc = None
		self.eventArgs = None

		self.text = TextLine()
		self.text.SetParent(self)
		self.text.SetPackedFontColor(self.NORMAL_COLOR)
		self.text.Show()
 
		self.underline = Line()
		self.underline.SetParent(self)
		self.underline.SetColor(self.NORMAL_COLOR)
		self.underline.Hide()

	def __del__(self):
		Window.__del__(self)

	def SetText(self, text):
		self.text.SetText(text)
		self.SetSize(self.text.GetTextSize()[0], self.text.GetTextSize()[1])
		self.underline.SetPosition(-50, self.text.GetTextSize()[1])
		self.underline.SetWindowHorizontalAlignCenter()
		self.underline.SetSize(self.text.GetTextSize()[0], 0)

	def OnMouseOverIn(self):
		self.text.SetPackedFontColor(self.OVER_COLOR)
		self.underline.Show()

	def OnMouseOverOut(self):
		self.text.SetPackedFontColor(self.NORMAL_COLOR)
		self.underline.Hide()

	def OnMouseLeftButtonDown(self):
		self.text.SetPackedFontColor(self.DOWN_COLOR)
		self.underline.SetColor(self.DOWN_COLOR)
		self.underline.Show()

	def OnMouseLeftButtonUp(self):
		if self.eventFunc:
			self.eventFunc(*self.eventArgs)
		self.OnMouseOverOut()

	def SetEvent(self, event, *args):
		self.eventFunc = __mem_func__(event)
		self.eventArgs = args

class CoolButton(Window):
	BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
	DARK_COLOR = grp.GenerateColor(0.4, 0.4, 0.4, 1.0)
	WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.3)
	HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventFunc = None
		self.eventArgs = None

		self.ButtonText = None
		self.ToolTipText = None

		self.EdgeColor = None
		self.isOver = False
		self.isSelected = False

		self.width = 0
		self.height = 0

	def __del__(self):
		Window.__del__(self)

		self.eventFunc = None
		self.eventArgs = None

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetEvent(self, func, *args):
		self.eventFunc = __mem_func__(func)
		self.eventArgs = args

	def SetTextColor(self, color):
		if not self.ButtonText:
			return
		self.ButtonText.SetPackedFontColor(color)

	def SetEdgeColor(self, color):
		self.EdgeColor = color

	def SetText(self, text):
		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.SetOutline()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	def SetToolTipText(self, text, x=0, y = -19):
		if not self.ToolTipText:
			toolTip=createToolTipWindowDict["TEXT"]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def SetTextPosition(self, width):
		self.ButtonText.SetPosition(width, self.GetHeight()/2)
		self.ButtonText.SetHorizontalAlignLeft()

	def Enable(self):
		wndMgr.Enable(self.hWnd)

	def Disable(self):
		wndMgr.Disable(self.hWnd)

	def OnMouseLeftButtonDown(self):
		self.isSelected = True

	def OnMouseLeftButtonUp(self):
		self.isSelected = False
		if self.eventFunc:
			self.eventFunc(*self.eventArgs)

	def OnUpdate(self):
		if self.IsIn():
			self.isOver = True
			self.ShowToolTip()
		else:
			self.isOver = False
			self.HideToolTip()

	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()

		widthRender = self.width
		heightRender = self.height
		grp.SetColor(self.BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		if self.EdgeColor:
			grp.SetColor(self.EdgeColor)
		else:
			grp.SetColor(self.DARK_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		if self.isOver:
			grp.SetColor(self.HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + 2, self.width - 3, heightRender - 3)

			if self.isSelected:
				grp.SetColor(self.WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 2, self.width - 3, heightRender - 3)
'''

#################################################################################################################################
### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ###
#################################################################################################################################
class _ButtonState(object):
	NORMAL = 0
	HOVER = 1
	ACTIVE = 2
	DISABLED = 3

class _BaseButton(Window):
	class WidthType(object):
		STRETCH = 0
		REPEAT = 1

	BASE_PATH = "interface/controls/common/button/"

	IMAGES = None

	OPACITY = {
		_ButtonState.NORMAL : 1.0,
		_ButtonState.HOVER : 1.0,
		_ButtonState.ACTIVE : 1.0,
		_ButtonState.DISABLED : 1.0
	}

	WIDTH = None
	HEIGHT = None

	WIDTH_TYPE = None

	TEXT_COLOR = None

	TEXT_Y = -2
	TEXT_X = 6
	TEXT_ALIGN = "CENTER"

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__state = _ButtonState.NORMAL

		self.eventFunc = None
		self.eventArgs = None

		self.ButtonText = None
		self.ToolTipText = None
		self.__CreateUI()

		self.SetWidth(0)
		self.SetState(_ButtonState.NORMAL)

	def __del__(self):
		self.eventFunc = None
		self.eventArgs = None
		Window.__del__(self)

	def __CreateUI(self):
		self.__dictImages = {
			'LEFT' : {
				_ButtonState.NORMAL : ImageBox(),
				_ButtonState.HOVER : ImageBox(),
				_ButtonState.ACTIVE : ImageBox(),
				_ButtonState.DISABLED : ImageBox()
			},
			'CENTER' : {
				_ButtonState.NORMAL : ExpandedImageBox(),
				_ButtonState.HOVER : ExpandedImageBox(),
				_ButtonState.ACTIVE : ExpandedImageBox(),
				_ButtonState.DISABLED : ExpandedImageBox()
			},
			'RIGHT' : {
				_ButtonState.NORMAL : ImageBox(),
				_ButtonState.HOVER : ImageBox(),
				_ButtonState.ACTIVE : ImageBox(),
				_ButtonState.DISABLED : ImageBox()
			}
		}

		self.__txtText = None

		for position, imageDictByState in self.__dictImages.items():
			for state, image in imageDictByState.items():
				image.SetParent(self)
				image.AddFlag("not_pick")
				image.LoadImage(self.IMAGES[position][state])
				image.Hide()

	def __RefreshButton(self):
		for position, imageDictByState in self.__dictImages.items():
			for state, image in imageDictByState.items():
				if state != self.GetState():
					image.Hide()
				else:
					image.Show()
		self.UpdateTextColor()

	def GetState(self):
		return self.__state

	def SetState(self, state):
		self.__state = state
		self.__RefreshButton()

	def Enable(self, enabled = True):
		self.SetState(_ButtonState.NORMAL)

	def Disable(self, enabled = True):
		self.SetState(_ButtonState.DISABLED)

	def IsDisabled(self):
		return self.GetState() == _ButtonState.DISABLED

	def SetWidth(self, width):
		width = max(self.WIDTH['LEFT'] + self.WIDTH['RIGHT'], width)
		self.width = width
		self.SetSize(width, self.HEIGHT)

		for image in self.__dictImages['CENTER'].values():
			image.SetPosition(self.WIDTH['LEFT'], 0)
			rect = float(width - (self.WIDTH['LEFT'] + self.WIDTH['RIGHT'])) / float(self.WIDTH['CENTER'])
			if self.WIDTH_TYPE == _BaseButton.WidthType.STRETCH:
				image.SetScale(rect, 1.0)
			else:
				image.SetRenderingRect(0.0, 0.0, -1.0 + rect, 0.0)

		for image in self.__dictImages['RIGHT'].values():
			image.SetPosition(width - self.WIDTH['RIGHT'], 0)

		self.UpdateText()

	def SetText(self, text):
		if not self.__txtText:
			self.__txtText = TextLine()
			self.__txtText.SetParent(self)
			self.__txtText.AddFlag("not_pick")
			if self.TEXT_ALIGN == "CENTER":
				self.__txtText.SetHorizontalAlignCenter()
			elif self.TEXT_ALIGN == "LEFT":
				self.__txtText.SetHorizontalAlignLeft()
			elif self.TEXT_ALIGN == "RIGTH":
				self.__txtText.SetHorizontalAlignRight()
			self.__txtText.SetVerticalAlignCenter()
			self.__txtText.Show()

			self.UpdateText()
			self.UpdateTextColor()

		self.__txtText.SetText(text)

	def GetText(self):
		if not self.__txtText:
			return ""
		return self.__txtText.GetText()

	def UpdateText(self):
		if not self.__txtText:
			return

		if self.TEXT_ALIGN == "CENTER":
			self.__txtText.SetPosition(self.GetWidth() / 2 - 1, self.GetHeight() / 2 + self.TEXT_Y)
		elif self.TEXT_ALIGN == "LEFT":
			self.__txtText.SetPosition(self.TEXT_X, self.GetHeight() / 2 + self.TEXT_Y)

	def UpdateTextColor(self):
		if not self.__txtText:
			return

		self.__txtText.SetPackedFontColor(self.TEXT_COLOR[self.GetState()])

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:
			toolTip = createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip
		self.ToolTipText.SetText(text)

	def SetToolTipWindow(self, toolTip):
		self.ToolTipText = toolTip
		self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x = 0, y = -19):
		self.SetFormToolTipText("TEXT", text, x, y)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def SetEvent(self, func, *args):
		if func:
			self.eventFunc = __mem_func__(func)
			self.eventArgs = args
		else:
			self.eventFunc = None
			self.eventArgs = None

	def CallEvent(self):
		snd.PlaySound("sound/ui/click.wav")

		if self.eventFunc:
			self.eventFunc(*self.eventArgs)

	def OnMouseOverIn(self):
		if self.IsDisabled():
			return
		self.SetState(1)
		self.ShowToolTip()

	def OnMouseOverOut(self):
		if self.IsDisabled():
			return
		self.SetState(0)
		self.ShowToolTip()

	def OnMouseLeftButtonDown(self):
		if self.IsDisabled():
			return
		self.SetState(2)

	def OnMouseLeftButtonUp(self):
		if self.IsDisabled():
			return
		self.SetState(1)
		self.CallEvent()

class RedButton(_BaseButton):
	BASE_PATH = "interface/controls/common/button"
	IMAGES = {
		'LEFT' : {
			_ButtonState.NORMAL : "%s/left_normal.tga" % BASE_PATH,
			_ButtonState.HOVER : "%s/left_over.tga" % BASE_PATH,
			_ButtonState.ACTIVE : "%s/left_down.tga" % BASE_PATH,
			# _ButtonState.DISABLED : "%s/left_down.tga" % BASE_PATH,
			_ButtonState.DISABLED : "interface/controls/common/button_black/left_normal.tga"
		},
		'CENTER' : {
			_ButtonState.NORMAL : "%s/center_normal.tga" % BASE_PATH,
			_ButtonState.HOVER : "%s/center_over.tga" % BASE_PATH,
			_ButtonState.ACTIVE : "%s/center_down.tga" % BASE_PATH,
			# _ButtonState.DISABLED : "%s/center_down.tga" % BASE_PATH,
			_ButtonState.DISABLED : "interface/controls/common/button_black/center_normal.tga"
		},
		'RIGHT' : {
			_ButtonState.NORMAL : "%s/right_normal.tga" % BASE_PATH,
			_ButtonState.HOVER : "%s/right_over.tga" % BASE_PATH,
			_ButtonState.ACTIVE : "%s/right_down.tga" % BASE_PATH,
			_ButtonState.DISABLED : "interface/controls/common/button_black/right_normal.tga"
			# _ButtonState.DISABLED : "%s/right_down.tga" % BASE_PATH,
		}
	}

	OPACITY = {
		_ButtonState.NORMAL : 1.0,
		_ButtonState.HOVER : 1.0,
		_ButtonState.ACTIVE : 1.0,
		_ButtonState.DISABLED : 0.5
	}

	WIDTH = {
		'LEFT' : 12,
		'CENTER' : 2,
		'RIGHT' : 12
	}

	HEIGHT = 27

	WIDTH_TYPE = _BaseButton.WidthType.REPEAT

	TEXT_COLOR = {
		_ButtonState.NORMAL : 0xFFFFFFFF,
		_ButtonState.HOVER : 0xFFFFF9F4,
		_ButtonState.ACTIVE : 0xFFCAB89F,
		_ButtonState.DISABLED : 0xFFF4E1C4
	}

	TEXT_Y = -1

class Slider(Window):
	BASE_PATH = "interface/controls/common/slider"

	HEIGHT = 17
	MIN_WIDTH = 50

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.curPos = 1.0
		self.pageSize = 1.0
		self.eventChange = None
		self.__CreateUI()

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.__dictImages = {
			'LEFT' : ImageBox(),
			'CENTER' : ExpandedImageBox(),
			'RIGHT' : ImageBox()
		}

		for position, image in self.__dictImages.items():
			image.SetParent(self)
			image.AddFlag("not_pick")
			image.LoadImage("%s/bg_%s.tga" % (self.BASE_PATH, position.lower()))
			image.Show()

		self.__imgRange = ExpandedImageBox()
		self.__imgRange.SetParent(self)
		self.__imgRange.SetPosition(4, ((Slider.HEIGHT-1)/2)-1)
		self.__imgRange.LoadImage("%s/bg_range.tga" % Slider.BASE_PATH)
		self.__imgRange.Hide()

		self.__btnSlider = DragButton()
		self.__btnSlider.SetParent(self)
		self.__btnSlider.AddFlag("movable")
		self.__btnSlider.AddFlag("restrict_y")
		self.__btnSlider.SetPosition(0, 0)
		self.__btnSlider.SetUpVisual("%s/btn_teste.tga" % Slider.BASE_PATH)
		self.__btnSlider.SetOverVisual("%s/btn_teste.tga" % Slider.BASE_PATH)
		self.__btnSlider.SetDownVisual("%s/btn_teste.tga" % Slider.BASE_PATH)
		self.__btnSlider.Show()

		self.__dictImages['LEFT'].SetPosition(0, 6)
		self.__dictImages['CENTER'].SetPosition(3, 6)

		self.__btnSlider.SetMoveEvent(self.__OnMove)

	def SetWidth(self, width):
		width = max(Slider.MIN_WIDTH, width)

		Window.SetSize(self, width, Slider.HEIGHT)
		self.pageSize = width - self.__btnSlider.GetWidth()
		self.__dictImages['CENTER'].SetScale(float(width - (self.__dictImages['LEFT'].GetWidth() + self.__dictImages['RIGHT'].GetWidth())), 1.0)
		self.__dictImages['RIGHT'].SetPosition(width - self.__dictImages['RIGHT'].GetWidth(), 6)

		self.__btnSlider.SetRestrictMovementArea(0, 0, self.GetWidth(), 0)

	def UpdateRangeEffect(self):
		(xLocal, yLocal) = self.__btnSlider.GetLocalPosition()
		self.__imgRange.SetScale(xLocal, 1.0)
		self.__imgRange.Show()

	def __OnMove(self):
		(xLocal, yLocal) = self.__btnSlider.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)
		self.UpdateRangeEffect()
		if self.eventChange:
			self.eventChange()

	def GetPercent(self):
		return int(self.curPos * 100)

	def SetSliderPos(self, pos):
		self.curPos = pos
		self.__btnSlider.SetPosition(int(self.pageSize * pos), 0)
		self.UpdateRangeEffect()

	def GetSliderPos(self):
		return self.curPos

	def SetEvent(self, event):
		self.eventChange = __mem_func__(event)

	def Enable(self):
		self.__btnSlider.Show()
		self.__imgRange.Show()

	def Disable(self):
		self.__btnSlider.Hide()
		self.__imgRange.Hide()

#################################################################################################################################
### THINBOARD ### THINBOARD ### THINBOARD ### THINBOARD ### THINBOARD ### THINBOARD ### THINBOARD ### THINBOARD ### THINBOARD ###
#################################################################################################################################
class ThinBoard(Window):
	CORNER_WIDTH = 21
	CORNER_HEIGHT = 21
	LINE_WIDTH = 21
	LINE_HEIGHT = 21
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.63)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "interface/controls/common/thinboard_transparent/corner_"+dir+".tga" for dir in ["lefttop","leftbottom","righttop","rightbottom"] ]
		LineFileNames = [ "interface/controls/common/thinboard_transparent/bar_"+dir+".tga" for dir in ["left","right","top","bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	if app.ENABLE_SEND_TARGET_INFO:
		def ShowCorner(self, corner):
			self.Corners[corner].Show()
			self.SetSize(self.GetWidth(), self.GetHeight())

		def HideCorners(self, corner):
			self.Corners[corner].Hide()
			self.SetSize(self.GetWidth(), self.GetHeight())

		def ShowLine(self, line):
			self.Lines[line].Show()
			self.SetSize(self.GetWidth(), self.GetHeight())

		def HideLine(self, line):
			self.Lines[line].Hide()
			self.SetSize(self.GetWidth(), self.GetHeight())

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class New_ThinScrollBar(ScrollBar):
	interface = "interface/controls/common/scrollbar/"
	fill = "interface/controls/special/whisper/fill.tga"
	INTERFACE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
	def CreateScrollBar(self):
		barSlot = ExpandedImageBox()
		barSlot.SetParent(self)
		barSlot.LoadImage(self.fill)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(self.OnMove)
		middleBar.Show()
		middleBar.SetUpVisual(self.interface + "btn_thinboard_middle_01_normal.tga")
		middleBar.SetOverVisual(self.interface + "btn_thinboard_middle_02_hover.tga")
		middleBar.SetDownVisual(self.interface + "btn_thinboard_middle_03_active.tga")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual(self.interface + "btn_up_01_normal.tga")
		upButton.SetOverVisual(self.interface + "btn_up_02_hover.tga")
		upButton.SetDownVisual(self.interface + "btn_up_03_active.tga")
		upButton.SetEvent(self.OnUp)
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual(self.interface + "btn_down_01_normal.tga")
		downButton.SetOverVisual(self.interface + "btn_down_02_hover.tga")
		downButton.SetDownVisual(self.interface + "btn_down_03_active.tga")
		downButton.SetEvent(self.OnDown)
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton
		self.barSlot = barSlot
		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(2, self.SCROLLBAR_BUTTON_HEIGHT-2)
		self.barSlot.SetScale(self.GetWidth()-4, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2+4)

class New_ScrollBar(Window):
	PACH = "interface/controls/common/scrollbar/"
	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 5
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE
	INTERFACE_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

	class MiddleBar(DragButton):
		PACH = "interface/controls/common/scrollbar/"

		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self):
			self.top = ImageBox()
			self.top.SetParent(self)
			self.top.LoadImage(self.PACH + "btn_board_middle_top_01_normal" + ".tga")
			self.top.SetPosition(1, 0)
			self.top.AddFlag("not_pick")
			self.top.Show()

			self.bottom = ImageBox()
			self.bottom.SetParent(self)
			self.bottom.LoadImage(self.PACH + "btn_board_middle_bottom_01_normal" + ".tga")
			self.bottom.AddFlag("not_pick")
			self.bottom.Show()

			self.middle = ExpandedImageBox()
			self.middle.SetParent(self)
			self.middle.LoadImage(self.PACH + "btn_board_middle_center_01_normal" + ".tga")
			self.middle.SetPosition(1, 4)
			self.middle.AddFlag("not_pick")
			self.middle.Show()

			self.marcador = ImageBox()
			self.marcador.SetParent(self)
			self.marcador.LoadImage(self.PACH + "btn_board_middle_grip_01_normal" + ".tga")
			self.marcador.AddFlag("not_pick")
			self.marcador.Show()

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)
			self.bottom.SetPosition(1, height-4)
			self.marcador.SetPosition(1, (height/2)-3)

			height -= 4*3
			self.height = height
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

		def OnMouseOverOut(self):
			self.top.LoadImage(self.PACH + "btn_board_middle_top_01_normal" + ".tga")
			self.bottom.LoadImage(self.PACH + "btn_board_middle_bottom_01_normal" + ".tga")
			self.middle.LoadImage(self.PACH + "btn_board_middle_center_01_normal" + ".tga")
			self.middle.SetRenderingRect(0, 0, 0, float(self.height)/4.0)
			self.marcador.LoadImage(self.PACH + "btn_board_middle_grip_01_normal" + ".tga")

		def OnMouseOverIn(self):
			self.top.LoadImage(self.PACH + "btn_board_middle_top_02_hover" + ".tga")
			self.bottom.LoadImage(self.PACH + "btn_board_middle_bottom_02_hover" + ".tga")
			self.middle.LoadImage(self.PACH + "btn_board_middle_center_02_hover" + ".tga")
			self.middle.SetRenderingRect(0, 0, 0, float(self.height)/4.0)
			self.marcador.LoadImage(self.PACH + "btn_board_middle_grip_02_hover" + ".tga")

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.lockFlag = False
		self.scrollStep = 0.20

		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = Bar()
		barSlot.SetColor(self.INTERFACE_COLOR)
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(self.OnMove)
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(self.OnUp)
		upButton.SetUpVisual(self.PACH + "btn_up_01_normal" + ".tga")
		upButton.SetOverVisual(self.PACH + "btn_up_02_hover" + ".tga")
		upButton.SetDownVisual(self.PACH + "btn_up_03_active" + ".tga")
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(self.OnDown)
		downButton.SetUpVisual(self.PACH + "btn_down_01_normal" + ".tga")
		downButton.SetOverVisual(self.PACH + "btn_down_02_hover" + ".tga")
		downButton.SetDownVisual(self.PACH + "btn_down_03_active" + ".tga")
		downButton.Show()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()

	def Destroy(self):
		self.Hide()
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.eventScroll = None

	def SetScrollEvent(self, event):
		self.eventScroll = __mem_func__(event)

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2 - 6
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		newPos = float(self.pageSize) * self.curPos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 0)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)
		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(2, self.SCROLLBAR_BUTTON_HEIGHT)
		self.barSlot.SetSize(self.GetWidth()-4, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):
		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		if self.curPos  ==  float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize):
			return

		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		if self.eventScroll:
			self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

class SlotElipseWindow(Window):
	def __init__(self):
		Window.__init__(self)

		self.StartIndex = 0

		self.eventSelectEmptySlot = None
		self.eventSelectEmptyArgs = None

		self.eventSelectItemSlot = None
		self.eventSelectItemArgs = None

		self.eventUnselectEmptySlot = None
		self.eventUnselectEmptyArgs = None

		self.eventUnselectItemSlot = None
		self.eventUnselectItemArgs = None

		self.eventUseSlot = None
		self.eventUseArgs = None

		self.eventOverInItem = None
		self.eventOverInArgs = None

		self.eventOverOutItem = None
		self.eventOverOutArgs = None

		self.eventPressedSlotButton = None
		self.eventPressedSlotArgs = None

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterSlotWindow(self, layer)

	def SetSlotStyle(self, style):
		wndMgr.SetSlotStyle(self.hWnd, style)

	def HasSlot(self, slotIndex):
		return wndMgr.HasSlot(self.hWnd, slotIndex)

	def SetSlotBaseImage(self, imageFileName, r, g, b, a):
		wndMgr.SetSlotBaseImage(self.hWnd, imageFileName, r, g, b, a)

	folder = "interface/controls/common/slot_ellipse/"
	def SetCoverButton(self, slotIndex, upName = folder+"slot_vazio.tga", overName = folder+"slot_vazio_over.tga", downName = folder+"slot_vazio_down.tga", disableName = folder+"slot_vazio.tga", LeftButtonEnable = False, RightButtonEnable = True):
		wndMgr.SetCoverButton(self.hWnd, slotIndex, upName, overName, downName, disableName, LeftButtonEnable, RightButtonEnable)

	def EnableCoverButton(self, slotIndex):
		wndMgr.EnableCoverButton(self.hWnd, slotIndex)

	def DisableCoverButton(self, slotIndex):
		wndMgr.DisableCoverButton(self.hWnd, slotIndex)

	def SetAlwaysRenderCoverButton(self, slotIndex, bAlwaysRender = True):
		wndMgr.SetAlwaysRenderCoverButton(self.hWnd, slotIndex, bAlwaysRender)

	def AppendSlotButton(self, upName, overName, downName):
		wndMgr.AppendSlotButton(self.hWnd, upName, overName, downName)

	def ShowSlotButton(self, slotNumber):
		wndMgr.ShowSlotButton(self.hWnd, slotNumber)

	def HideSlotButton(self, slotNumber):
		wndMgr.HideSlotButton(self.hWnd, slotNumber)

	def HideAllSlotButton(self):
		wndMgr.HideAllSlotButton(self.hWnd)

	def AppendRequirementSignImage(self, filename):
		wndMgr.AppendRequirementSignImage(self.hWnd, filename)

	def ShowRequirementSign(self, slotNumber):
		wndMgr.ShowRequirementSign(self.hWnd, slotNumber)

	def HideRequirementSign(self, slotNumber):
		wndMgr.HideRequirementSign(self.hWnd, slotNumber)

	def ActivateSlot(self, slotNumber):
		wndMgr.ActivateSlot(self.hWnd, slotNumber)

	def DeactivateSlot(self, slotNumber):
		wndMgr.DeactivateSlot(self.hWnd, slotNumber)

	def ShowSlotBaseImage(self, slotNumber):
		wndMgr.ShowSlotBaseImage(self.hWnd, slotNumber)

	def HideSlotBaseImage(self, slotNumber):
		wndMgr.HideSlotBaseImage(self.hWnd, slotNumber)

	def SetButtonEvent(self, button, state, event, *args):
		if "LEFT" == button:
			if "EMPTY" == state:
				self.eventSelectEmptySlot = __mem_func__(event)
				self.eventSelectEmptyArgs = args
			elif "EXIST" == state:
				self.eventSelectItemSlot = __mem_func__(event)
				self.eventSelectItemArgs = args
			elif "ALWAYS" == state:
				self.eventSelectEmptySlot = __mem_func__(event)
				self.eventSelectEmptyArgs = args
				self.eventSelectItemSlot = __mem_func__(event)
				self.eventSelectItemArgs = args
		elif "RIGHT" == button:
			if "EMPTY" == state:
				self.eventUnselectEmptySlot = __mem_func__(event)
				self.eventUnselectEmptyArgs = args
			elif "EXIST" == state:
				self.eventUnselectItemSlot = __mem_func__(event)
				self.eventUnselectItemArgs = args
			elif "ALWAYS" == state:
				self.eventUnselectEmptySlot = __mem_func__(event)
				self.eventUnselectEmptyArgs = args
				self.eventUnselectItemSlot = __mem_func__(event)
				self.eventUnselectItemArgs = args

	def SetSelectEmptySlotEvent(self, event, *args):
		self.eventSelectEmptySlot = __mem_func__(event)
		self.eventSelectEmptyArgs = args

	def SetSelectItemSlotEvent(self, event, *args):
		self.eventSelectItemSlot = __mem_func__(event)
		self.eventSelectItemArgs = args

	def SetUnselectEmptySlotEvent(self, event, *args):
		self.eventUnselectEmptySlot = __mem_func__(event)
		self.eventUnselectEmptyArgs = args

	def SetUnselectItemSlotEvent(self, event, *args):
		self.eventUnselectItemSlot = __mem_func__(event)
		self.eventUnselectItemArgs = args

	def SetUseSlotEvent(self, event, *args):
		self.eventUseSlot = __mem_func__(event)
		self.eventUseArgs = args

	def SetOverInItemEvent(self, event, *args):
		self.eventOverInItem = __mem_func__(event)
		self.eventOverInArgs = args

	def SetOverOutItemEvent(self, event, *args):
		self.eventOverOutItem = __mem_func__(event)
		self.eventOverOutArgs = args

	def SetPressedSlotButtonEvent(self, event, *args):
		self.eventPressedSlotButton = __mem_func__(event)
		self.eventPressedSlotArgs = args

	def GetSlotCount(self):
		return wndMgr.GetSlotCount(self.hWnd)

	def SetUseMode(self, flag):
		wndMgr.SetUseMode(self.hWnd, flag)

	def SetUsableItem(self, flag): 
		wndMgr.SetUsableItem(self.hWnd, flag)

	def SetUsableItem2(self, flag): 
		wndMgr.SetUsableItem(self.hWnd, flag)

	def SetSlotCoolTime(self, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.SetSlotCoolTime(self.hWnd, slotIndex, coolTime, elapsedTime)

	def DisableSlot(self, slotIndex):
		wndMgr.DisableSlot(self.hWnd, slotIndex)

	def EnableSlot(self, slotIndex):
		wndMgr.EnableSlot(self.hWnd, slotIndex)

	def LockSlot(self, slotIndex):
		wndMgr.LockSlot(self.hWnd, slotIndex)

	def UnlockSlot(self, slotIndex):
		wndMgr.UnlockSlot(self.hWnd, slotIndex)

	def RefreshSlot(self):
		wndMgr.RefreshSlot(self.hWnd)

	def ClearSlot(self, slotNumber):
		wndMgr.ClearSlot(self.hWnd, slotNumber)

	def ClearAllSlot(self):
		wndMgr.ClearAllSlot(self.hWnd)

	def AppendSlot(self, index, x, y, width, height):
		wndMgr.AppendSlot(self.hWnd, index, x, y, width, height)

	def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

	def SetSlotCount(self, slotNumber, count):
		wndMgr.SetSlotCount(self.hWnd, slotNumber, count)

	def SetSlotCountNew(self, slotNumber, grade, count):
		wndMgr.SetSlotCountNew(self.hWnd, slotNumber, grade, count)

	def SetItemSlot(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		if 0 == ItemIndex or None == ItemIndex:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		item.SelectItem(ItemIndex)
		itemIcon = item.GetIconImage()

		item.SelectItem(ItemIndex)
		(width, height) = item.GetItemSize()

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)

	def SetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel):
		skillIcon = skill.GetIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, skillLevel)

	def SetSkillSlotNew(self, renderingSlotNumber, skillIndex, skillGrade, skillLevel):
		skillIcon = skill.GetIconImageNew(skillIndex, skillGrade)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)

	def SetEmotionSlot(self, renderingSlotNumber, emotionIndex):
		icon = player.GetEmotionIconImage(emotionIndex)

		if 0 == icon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, emotionIndex, 1, 1, icon)

	def OnSelectEmptySlot(self, slotNumber):
		if self.eventSelectEmptySlot:
			if self.eventSelectEmptyArgs:
				self.eventSelectEmptySlot(*self.eventSelectEmptyArgs)
			else:
				self.eventSelectEmptySlot(slotNumber)

	def OnSelectItemSlot(self, slotNumber):
		if self.eventSelectItemSlot:
			if self.eventSelectItemArgs:
				self.eventSelectItemSlot(*self.eventSelectItemArgs)
			else:
				self.eventSelectItemSlot(slotNumber)

	def OnUnselectEmptySlot(self, slotNumber):
		if self.eventUnselectEmptySlot:
			if self.eventUnselectEmptyArgs:
				self.eventUnselectEmptySlot(*self.eventUnselectEmptyArgs)
			else:
				self.eventUnselectEmptySlot(slotNumber)

	def OnUnselectItemSlot(self, slotNumber):
		if self.eventUnselectItemSlot:
			if self.eventUnselectItemArgs:
				self.eventUnselectItemSlot(*self.eventUnselectItemArgs)
			else:
				self.eventUnselectItemSlot(slotNumber)

	def OnUseSlot(self, slotNumber):
		if self.eventUseSlot:
			if self.eventUseArgs:
				self.eventUseSlot(*self.eventUseArgs)
			else:
				self.eventUseSlot(slotNumber)

	def OnOverInItem(self, slotNumber):
		if self.eventOverInItem:
			if self.eventOverInArgs:
				self.eventOverInItem(*self.eventOverInArgs)
			else:
				self.eventOverInItem(slotNumber)

	def OnOverOutItem(self):
		if self.eventOverOutItem:
			if self.eventOverOutArgs:
				self.eventOverOutItem(*self.eventOverOutArgs)
			else:
				self.eventOverOutItem()

	def OnPressedSlotButton(self, slotNumber):
		if self.eventPressedSlotButton:
			if self.eventPressedSlotArgs:
				self.eventPressedSlotButton(*self.eventPressedSlotArgs)
			else:
				self.eventPressedSlotButton(slotNumber)

	def GetStartIndex(self):
		return 0

class GridSlotElipseWindow(SlotElipseWindow):
	def __init__(self):
		SlotElipseWindow.__init__(self)

		self.startIndex = 0

	def __del__(self):
		SlotElipseWindow.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterGridSlotWindow(self, layer)

	def ArrangeSlot(self, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank):
		self.startIndex = StartIndex

		wndMgr.ArrangeSlot(self.hWnd, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank)
		self.startIndex = StartIndex

	def GetStartIndex(self):
		return self.startIndex

class NewRadioButton(Button):
	interface = "interface/controls/common/radio/"
	tga = ".tga"

	empty = {
		'NORMAL'	: interface+"empty_01_normal"+tga,
		'HOVER'		: interface+"empty_02_hover"+tga,
		'ACTIVE'	: interface+"empty_03_active"+tga
	}

	filled = {
		'NORMAL'	: interface+"filled_01_normal"+tga,
		'HOVER'		: interface+"filled_02_hover"+tga,
		'ACTIVE'	: interface+"filled_03_active"+tga
	}

	STATE = {
		'EMPTY' : 0,
		'FILLED' : 1
	}

	TYPE = 1

	def __init__(self):
		Button.__init__(self)
		self.Status = self.STATE['EMPTY']
		self.__Create_UI(self.Status)
		self.IsEnable = None

	def __del__(self):
		Button.__del__(self)
		self.IsEnable = None

	def __Create_UI(self, status):
		self.Status = status
		if status == self.STATE['EMPTY']:
			self.SetUpVisual(self.empty['NORMAL'])
			self.SetOverVisual(self.empty['HOVER'])
			self.SetDownVisual(self.empty['ACTIVE'])
		elif status == self.STATE['FILLED']:
			self.SetUpVisual(self.filled['NORMAL'])
			self.SetOverVisual(self.filled['HOVER'])
			self.SetDownVisual(self.filled['ACTIVE'])

	def SetType(self, type):
		self.TYPE = type

	def Fill(self):
		self.Status = self.STATE['FILLED']
		self.__Create_UI(self.Status)

	def Empty(self):
		self.Status = self.STATE['EMPTY']
		self.__Create_UI(self.Status)

	def Enable(self):
		if self.TYPE:
			self.Empty()
		self.IsEnable = 0

	def Disable(self):
		if self.TYPE:
			self.Fill()
		self.IsEnable = 1

	def GetStatus(self):
		return self.Status

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterButton(self, layer)

	def CallEvent(self):
		if self.IsEnable == 1:
			return

		if self.TYPE:
			if self.GetStatus() == self.STATE['EMPTY']:
				self.Fill()
			else:
				return

		if self.eventFunc:
			self.eventFunc(*self.eventArgs)

class Ballon(Window):
	BASE_PATH = "interface/controls/common/Ballon"

	WIDTH = {
		'LEFT' : 6,
		'FILL_L' : 1,
		'ARROW' : 22,
		'FILL_R' : 1,
		'RIGHT' : 6
	}

	HEIGHT = 36

	ANIMATED = False
	SHOWED = False
	ALPHA = 0.0

	BallonText = None

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.__CreateUI()
		self.SetWidth(0)
		self.Hide()

	def __del__(self):
		Window.__del__(self)

	def __CreateUI(self):
		self.ANIMATED = False
		self.SHOWED = False
		self.ALPHA = 0.0

		self.__dictImages = {
			'LEFT' : ImageBox(),
			'FILL_L' : ExpandedImageBox(),
			'ARROW' : ImageBox(),
			'FILL_R' : ExpandedImageBox(),
			'RIGHT' : ImageBox()
		}

		for image in self.__dictImages.values():
			image.SetParent(self)
			image.Show()

		self.__dictImages['LEFT'].LoadImage("%s/left.tga" % Ballon.BASE_PATH)
		self.__dictImages['FILL_L'].LoadImage("%s/fill.tga" % Ballon.BASE_PATH)
		self.__dictImages['ARROW'].LoadImage("%s/arrow.tga" % Ballon.BASE_PATH)
		self.__dictImages['FILL_R'].LoadImage("%s/fill.tga" % Ballon.BASE_PATH)
		self.__dictImages['RIGHT'].LoadImage("%s/right.tga" % Ballon.BASE_PATH)

		self.__dictImages['LEFT'].SetPosition(0, 0)
		self.__dictImages['FILL_L'].SetPosition(Ballon.WIDTH['LEFT'], 0)

	def SetWidth(self, width):
		if int(width) % 2 == 1:
			width += 1

		width = max(Ballon.WIDTH['LEFT'] + Ballon.WIDTH['FILL_L'] + Ballon.WIDTH['ARROW'] + Ballon.WIDTH['RIGHT'] + Ballon.WIDTH['FILL_R'], width)
		self.WIDTH = width
		self.SetSize(width, Ballon.HEIGHT)

		self.__dictImages['FILL_L'].SetScale(float(width - (Ballon.WIDTH['LEFT'] + Ballon.WIDTH['RIGHT'] + Ballon.WIDTH['ARROW'])) / float(2), 1.0)
		self.__dictImages['FILL_R'].SetPosition((float(width)/2.0 + (Ballon.WIDTH['ARROW'])/2), 0)
		self.__dictImages['FILL_R'].SetScale(float(width - (Ballon.WIDTH['LEFT'] + Ballon.WIDTH['RIGHT'] + Ballon.WIDTH['ARROW'])) / float(2), 1.0)
		self.__dictImages['ARROW'].SetPosition((float(width)/2.0 - float(Ballon.WIDTH['ARROW'])/2), 0)
		self.__dictImages['RIGHT'].SetPosition((width - Ballon.WIDTH['RIGHT']), 0)

	def SetText(self, text):
		if not self.BallonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.Show()
			self.BallonText = textLine
		self.BallonText.SetFontColor(1.0, 1.0, 1.0)
		self.BallonText.SetText(text)
		(width, heigh) = self.BallonText.GetTextSize()
		self.SetWidth(width + 20)
		self.BallonText.SetVerticalAlignCenter()
		self.BallonText.SetHorizontalAlignCenter()
		self.BallonText.SetPosition(self.GetWidth()/2, self.GetHeight()/2-6)

	def Hide(self):
		if self.ANIMATED:
			self.SHOWED = False
		else:
			Window.Hide(self)

	def Show(self):
		Window.Show(self)
		if self.ANIMATED:
			self.SHOWED = True

	def OnUpdate(self):
		if not self.ANIMATED:
			return

		if self.SHOWED and self.ALPHA < 1.0:
			self.ALPHA += 0.1
			if self.BallonText:
				self.BallonText.Hide()
			for image in self.__dictImages.values():
				image.SetAlpha(self.ALPHA)
		elif self.SHOWED and self.ALPHA >= 1.0:
			if self.BallonText:
				self.BallonText.Show()
		elif self.ALPHA > 0.0 and not self.SHOWED:
			if self.BallonText:
				self.BallonText.Hide()
			self.ALPHA -= 0.2
			for image in self.__dictImages.values():
				image.SetAlpha(self.ALPHA)
		elif self.ALPHA <= 0.0 and not self.SHOWED:
			self.Hide()

class HorizontalSeparator(ExpandedImageBox):
	def __init__(self):
		ExpandedImageBox.__init__(self)
		self.AddFlag("not_pick")
		self.__CreateUI()
		self.SetWidth(1)

	def __del__(self):
		ExpandedImageBox.__del__(self)

	def __CreateUI(self):
		self.LoadImage("interface/controls/common/board_separator/horizontal.tga")

	def SetWidth(self, width):
		if width < 1:
			return

		self.SetScale(float(width), 1.0)

class VerticalSeparator(ExpandedImageBox):
	def __init__(self):
		ExpandedImageBox.__init__(self)
		self.AddFlag("not_pick")
		self.__CreateUI()
		self.SetHeight(1)

	def __del__(self):
		ExpandedImageBox.__del__(self)

	def __CreateUI(self):
		self.LoadImage("interface/controls/common/board_separator/vertical.tga")

	def SetHeight(self, height):
		if height < 1:
			return

		self.SetScale(1.0, float(height))

class BarWithBox(Bar):
	flash_color = None
	overInEvent = None
	overInArgs = None
	overOutEvent = None
	overOutArgs = None

	def __init__(self):
		Bar.__init__(self)

		box = Box()
		box.AddFlag("not_pick")
		box.SetParent(self)
		box.SetPosition(0, 0)
		box.SetColor(0xFFB7766B)
		box.Show()
		self.Box = box

	def SetSize(self, width, height):
		Bar.SetSize(self, width, height)
		self.Box.SetSize(width-1, height-1)

	def SetBoxColor(self, color):
		self.Box.SetColor(color)

	def SetFlashColor(self, color):
		self.flash_color = color

	def OnMouseOverIn(self):
		if self.flash_color:
			wndMgr.SetColor(self.hWnd, self.flash_color)
		if self.overInEvent:
			self.overInEvent(*self.overInArgs)

	def OnMouseOverOut(self):
		if self.color:
			wndMgr.SetColor(self.hWnd, self.color)
		if self.overOutEvent:
			self.overOutEvent(*self.overOutArgs)

	def SetOverInEvent(self, func, *args):
		self.overInEvent = __mem_func__(func)
		self.overInArgs = args

	def SetOverOutEvent(self, func, *args):
		self.overOutEvent = __mem_func__(func)
		self.overOutArgs = args

class InputBar(Bar):
	flash_color = None
	overInEvent = None
	overInArgs = None
	overOutEvent = None
	overOutArgs = None

	def __init__(self):
		Bar.__init__(self)

		box = Box()
		box.AddFlag("not_pick")
		box.SetParent(self)
		box.SetPosition(0, 0)
		box.SetColor(0xFFB7766B)
		box.Show()
		self.Box = box

		box2 = Box()
		box2.AddFlag("not_pick")
		box2.SetParent(self)
		box2.SetPosition(1, 1)
		box2.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 1.0))
		box2.Show()
		self.Box2 = box2

		box3 = Box()
		box3.AddFlag("not_pick")
		box3.SetParent(self)
		box3.SetPosition(-1, -1)
		box3.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 1.0))
		box3.Show()
		self.Box3 = box3

		self.right_deco = MakeImageBox(self, "interface/controls/common/input/right_deco.tga", -9, -11)
		self.right_deco.AddFlag("not_pick")
		self.left_deco = MakeImageBox(self, "interface/controls/common/input/left_deco.tga", 0, 0)
		self.left_deco.AddFlag("not_pick")

		self.right_line = MakeImageBox(self, "interface/controls/common/input/line_right.tga", 0, 0)
		self.right_line.AddFlag("not_pick")
		self.left_line = MakeImageBox(self, "interface/controls/common/input/line_left.tga", 0, 0)
		self.left_line.AddFlag("not_pick")
		self.top_line = MakeImageBox(self, "interface/controls/common/input/line_top.tga", 0, 0)
		self.top_line.AddFlag("not_pick")
		self.button_line = MakeImageBox(self, "interface/controls/common/input/line_button.tga", 0, 0)
		self.button_line.AddFlag("not_pick")

	def SetSize(self, width, height):
		Bar.SetSize(self, width, height)
		self.Box.SetSize(width-1, height-1)
		self.Box2.SetSize(width-3, height-3)
		self.Box3.SetSize(width+1, height+1)
		self.left_deco.SetPosition(width-30, -11)
		self.right_line.SetPosition(width-1, 0)
		self.top_line.SetScale(float(width)/100.0, 1.0)
		self.button_line.SetPosition(0, height-1)
		self.button_line.SetScale(float(width)/100.0, 1.0)

	def SetBoxColor(self, color):
		self.Box.SetColor(color)

	def SetFlashColor(self, color):
		self.flash_color = color

	def OnMouseOverIn(self):
		if self.flash_color:
			wndMgr.SetColor(self.hWnd, self.flash_color)
		if self.overInEvent:
			self.overInEvent(*self.overInArgs)

	def OnMouseOverOut(self):
		if self.color:
			wndMgr.SetColor(self.hWnd, self.color)
		if self.overOutEvent:
			self.overOutEvent(*self.overOutArgs)

	def SetOverInEvent(self, func, *args):
		self.overInEvent = __mem_func__(func)
		self.overInArgs = args

	def SetOverOutEvent(self, func, *args):
		self.overOutEvent = __mem_func__(func)
		self.overOutArgs = args

class EditBoard(InputBar):
	COLOR_BOX = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
	COLOR_INSIDE = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
	COLOR_OVER_IN = grp.GenerateColor(0.1, 0.1, 0.1, 0.8)
	# COLOR_TEXT = grp.GenerateColor(1.0, 0.5, 0.5, 1.0)
	COLOR_TEXT = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	def __init__(self):
		InputBar.__init__(self)
		self.__CreateUI()
		self.SetInterface()

	def __CreateUI(self):
		self.TextInfo = MakeTextLeft(self, 8)
		self.EditLine = MakeEditLine(self, 6)

		self.TextInfo.SetOverInEvent(self.OnMouseOverIn)
		self.TextInfo.SetOverOutEvent(self.OnMouseOverOut)
		self.EditLine.SetOverInEvent(self.OnMouseOverIn)
		self.EditLine.SetOverOutEvent(self.OnMouseOverOut)

		self.EditLine.SetMax(64)

		self.SetInfo = self.TextInfo.SetText
		self.GetInfo = self.TextInfo.GetText
		self.SetInfoFontName = self.TextInfo.SetFontName
		self.SetInfoFontColor = self.TextInfo.SetPackedFontColor

		self.GetText = self.EditLine.GetText
		self.SetText = self.EditLine.SetText
		self.SetTabEvent = self.EditLine.SetTabEvent
		self.SetEscapeEvent = self.EditLine.SetEscapeEvent
		self.SetReturnEvent = self.EditLine.SetReturnEvent
		self.SetEndPosition = self.EditLine.SetEndPosition
		self.SetIMEUpdateEvent = self.EditLine.SetIMEUpdateEvent
		self.SetSecret = self.EditLine.SetSecret
		self.SetNumberMode = self.EditLine.SetNumberMode
		self.SetFontName = self.EditLine.SetFontName
		self.SetPackedFontColor = self.EditLine.SetPackedFontColor
		self.GetTextSize = self.EditLine.GetTextSize
		self.SetMax = self.EditLine.SetMax
		self.SetMouseLeftButtonDownEvent(self.SetFocus)
		self.EditLine.SetKillFocusEvent(self.OnKillFocus)
		self.EditLine.SetFocusEvent(self.TextInfo.Hide)
		self.EditLine.SetIMEUpdateEvent(self.OnInput)
		self.KillFocus = self.EditLine.KillFocus

	def SetInterface(self):
		self.SetColor(self.COLOR_INSIDE)
		self.SetBoxColor(self.COLOR_BOX)
		self.SetFlashColor(self.COLOR_OVER_IN)
		self.SetFontName(localeinfo.UI_DEF_FONT_LARGE)

		self.SetInfoFontColor(self.COLOR_TEXT)
		self.SetPackedFontColor(self.COLOR_TEXT)

	def SetFocus(self):
		self.EditLine.SetFocus()
		self.TextInfo.Hide()

	def OnInput(self):
		self.TextInfo.Hide()
		for item in [" "]:
			if item in self.GetText():
				self.SetText(self.GetText().replace(item, ""))
		if self.EditLine.GetTextSize()[0] > (self.GetWidth() - 15):
			self.SetText(self.GetText()[:-1])

	def OnKillFocus(self):
		if len(self.GetText()) < 1:
			self.TextInfo.Show()

	def SetSize(self, width, height):
		InputBar.SetSize(self, width, height)
		self.EditLine.SetSize(width, height)

class EditBoardFake(InputBar):
	COLOR_BOX = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
	COLOR_INSIDE = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
	COLOR_OVER_IN = grp.GenerateColor(0.1, 0.1, 0.1, 0.8)
	# COLOR_TEXT = grp.GenerateColor(1.0, 0.5, 0.5, 1.0)
	COLOR_TEXT = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

	def __init__(self):
		InputBar.__init__(self)
		self.__CreateUI()
		self.SetInterface()

	def __CreateUI(self):
		self.EditLine = MakeTextLeft(self, 8)

		self.GetText = self.EditLine.GetText
		self.SetText = self.EditLine.SetText
		self.SetFontName = self.EditLine.SetFontName
		self.SetPackedFontColor = self.EditLine.SetPackedFontColor
		self.GetTextSize = self.EditLine.GetTextSize

	def SetTextInCenter(self):
		self.EditLine.SetPosition(0, -2)
		self.EditLine.SetHorizontalAlignCenter()
		self.EditLine.SetWindowHorizontalAlignCenter()

	def SetInterface(self):
		self.SetColor(self.COLOR_INSIDE)
		self.SetBoxColor(self.COLOR_BOX)
		self.SetFlashColor(self.COLOR_OVER_IN)
		self.SetFontName(localeinfo.UI_DEF_FONT_LARGE)
		self.SetPackedFontColor(self.COLOR_TEXT)

	def SetSize(self, width, height):
		InputBar.SetSize(self, width, height)

class DropDown(InputBar):
	COLOR_BOX = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
	COLOR_INSIDE = grp.GenerateColor(0.0, 0.0, 0.0, 0.9)
	COLOR_OVER_IN = grp.GenerateColor(1.0, 1.0, 1.0, 0.1)
	COLOR_TEXT = grp.GenerateColor(1.0, 0.5, 0.5, 1.0)
	COLOR_TOP = grp.GenerateColor(1.0, 1.0, 1.0, 0.05)

	ITEM_HEIGTH = 28
	MAX_HEIGTH = 196
	DROP_HEIGTH = 196

	COUNT_ITEM = 0

	eventOnDrop = None
	eventOnSelect = None

	DROPED = 0
	BLOCKED = 0

	class Item(ListBoxEx.Item):
		def __init__(self, parent, text, value = 0):
			ListBoxEx.Item.__init__(self)
			self.Bar = Bar()
			self.Bar.SetParent(self)
			self.Bar.SetPosition(0, 0)
			self.Bar.SetColor(DropDown.COLOR_OVER_IN)
			self.Bar.AddFlag("not_pick")
			self.Bar.Hide()
			self.textBox = TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.AddFlag("not_pick")
			self.textBox.SetPosition(2, -2)
			self.textBox.SetVerticalAlignCenter()
			self.textBox.SetWindowVerticalAlignCenter()
			self.textBox.SetPackedFontColor(0xffa08784)
			self.textBox.Show()
			self.value = value

		def __del__(self):
			ListBoxEx.Item.__del__(self)

		def SetSize(self, width, height):
			wndMgr.SetWindowSize(self.hWnd, width, height)
			self.Bar.SetSize(width, height)

		def GetValue(self):
			return self.value

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(DropDown.COLOR_OVER_IN)
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

		def OnMouseOverIn(self):
			self.textBox.SetPackedFontColor(0xfff88f90)
			if self.Bar.IsShow():
				return
			self.Bar.Show()

		def OnMouseOverOut(self):
			self.textBox.SetPackedFontColor(0xffa08784)
			if self.Bar.IsShow():
				self.Bar.Hide()

	def __init__(self):
		InputBar.__init__(self)
		self.__CreateUI()
		self.SetInterface()

	def __CreateUI(self):
		bar_top = Bar()
		bar_top.SetParent(self)
		bar_top.AddFlag("not_pick")
		bar_top.SetPosition(1, 1)
		bar_top.SetColor(self.COLOR_TOP)
		bar_top.Show()
		self.bar_top = bar_top

		self.right_line_ = MakeImageBox(self, "interface/controls/common/input/line_right.tga", 0, 0)
		self.right_line_.AddFlag("not_pick")
		self.right_deco_down = MakeImageBox(self, "interface/controls/common/input/right_deco_down.tga", -9, -11)
		self.right_deco_down.AddFlag("not_pick")
		self.left_deco_down = MakeImageBox(self, "interface/controls/common/input/left_deco_down.tga", 0, 0)
		self.left_deco_down.AddFlag("not_pick")

		self.right_deco_down.Hide()
		self.left_deco_down.Hide()

		self.arrow_normal = MakeImageBox(self, "interface/controls/common/dropdown/arrow_normal.tga", 0, 0)
		self.arrow_normal.AddFlag("not_pick")
		self.arrow_over = MakeImageBox(self, "interface/controls/common/dropdown/arrow_over.tga", 0, 0)
		self.arrow_over.AddFlag("not_pick")
		self.arrow_over.Hide()

		self.Text = MakeTextLeft(self, 8)

		self.GetText = self.Text.GetText
		self.SetText = self.Text.SetText
		self.SetFontName = self.Text.SetFontName
		self.SetPackedFontColor = self.Text.SetPackedFontColor

		self.Drop = Bar("TOP_MOST")
		self.Drop.SetPosition(self.GetGlobalLeft(), self.GetGlobalTop() + self.GetHeight())
		self.Drop.SetSize(150, 0)
		self.Drop.SetColor(self.COLOR_INSIDE)

		self.Drop.Time = 0

		self.ScrollBar = New_ThinScrollBar()
		self.ScrollBar.SetParent(self.Drop)
		self.ScrollBar.SetPosition(132, 0)
		self.ScrollBar.SetScrollBarSize(0)

		self.DropList = ListBoxEx()
		self.DropList.SetParent(self.Drop)
		self.DropList.itemHeight = self.ITEM_HEIGTH
		self.DropList.itemStep = self.ITEM_HEIGTH
		self.DropList.SetPosition(0, 0)
		self.DropList.SetSize(132, self.ITEM_HEIGTH)
		self.DropList.SetScrollBar(self.ScrollBar)
		self.DropList.SetSelectEvent(self.SetTitle)
		self.DropList.SetViewItemCount(0)
		self.DropList.Show()

		self.SetMouseLeftButtonDownEvent(self.ShowDrop)
		self.Drop.OnUpdate = __mem_func__(self.OnDropUpdate)

	def SetInterface(self):
		self.SetColor(self.COLOR_INSIDE)
		self.SetBoxColor(self.COLOR_BOX)
		self.SetFlashColor(self.COLOR_OVER_IN)
		self.SetPackedFontColor(self.COLOR_TEXT)

	def SetSize(self, width, height):
		InputBar.SetSize(self, width, height)
		self.bar_top.SetSize(width-2, (height)/2)
		self.right_deco_down.SetPosition(-9, height/2-2)
		self.left_deco_down.SetPosition(width-30, height/2-2)
		self.right_line_.SetPosition(width-32, 0)
		self.arrow_normal.SetPosition(width-24, 8)
		self.arrow_over.SetPosition(width-24, 8)

		self.Drop.SetSize(width, self.Drop.GetHeight())
		self.DropList.SetItemSize(width, self.ITEM_HEIGTH)
		self.DropList.SetSize(width, self.MAX_HEIGTH)
		for x in self.DropList.itemList:
			x.SetSize(width, self.ITEM_HEIGTH)
		self.ScrollBar.SetPosition(width - 17, 0)

	def AppendItem(self, text, value = 0):
		self.COUNT_ITEM += 1
		item = self.Item(self, text, value)

		self.DropList.AppendItem(item)

		self.Drop.SetSize(self.Drop.GetWidth(), min(self.MAX_HEIGTH, self.ITEM_HEIGTH * self.COUNT_ITEM))

		self.AdjustScrollBar()

	def AppendItemAndSelect(self, text, value = 0):
		self.DropList.AppendItem(self.Item(self, text, value))
		self.DropList.__UpdateSize()
		self.DropList.SelectIndex(len(self.DropList.itemList) - 1)

	def AdjustScrollBar(self):
		self.ScrollBar.SetScrollBarSize(self.Drop.GetHeight())
		self.DropList.SetViewItemCount(int(self.Drop.GetHeight()/self.ITEM_HEIGTH))
		self.DropList.SetBasePos(0)
		if ((self.Drop.GetHeight()/self.ITEM_HEIGTH) > self.COUNT_ITEM):
			self.ScrollBar.Show()
			self.DropList.SetItemSize(self.Drop.GetWidth() - 16, self.ITEM_HEIGTH)
			self.DropList.SetSize(self.Drop.GetWidth() - 16, self.MAX_HEIGTH)
			for x in self.DropList.itemList:
				x.SetSize(self.Drop.GetWidth() - 16, self.ITEM_HEIGTH)

	def SelectByAffectId(self, id):
		for x in self.DropList.itemList:
			if int(x.GetValue()) == int(id):
				self.DropList.SelectItem(x)
				self.SetTitle(x)
				break

	def GetSelectedValue(self):
		try:
			return self.DropList.GetSelectedItem().GetValue()
		except BaseException:
			return 0

	def GetSelectedItem(self):
		try:
			return self.DropList.GetSelectedItem()
		except BaseException:
			return 0

	def SetTitle(self, item):
		self.Text.SetText(str(item.textBox.GetText()))
		self.HideDrop()

		if self.eventOnSelect:
			self.eventOnSelect()

	def OnMouseOverIn(self):
		InputBar.OnMouseOverIn(self)
		self.arrow_over.Show()
		self.arrow_normal.Hide()

	def OnMouseOverOut(self):
		InputBar.OnMouseOverOut(self)
		self.arrow_normal.Show()
		self.arrow_over.Hide()

	def Block(self):
		self.BLOCKED = 1
		self.HideDrop()

	def UnBlock(self):
		self.BLOCKED = 0

	def ShowDrop(self):
		if self.BLOCKED:
			return

		if self.eventOnDrop:
			self.eventOnDrop()

		if self.DROPED == 0:
			self.DROPED = 1
			self.Drop.Time = 0
			self.Drop.Show()
		else:
			self.DROPED = 0
			self.Drop.Time = 0
			self.Drop.Hide()

	def HideDrop(self):
		self.Drop.Hide()
		self.DROPED = 0
		self.Drop.Time = 0

	def OnUpdate(self):
		self.Drop.SetPosition(self.GetGlobalLeft(), self.GetGlobalTop() + self.GetHeight() + 1)

	def OnDropUpdate(self):
		if self.Drop.IsInPosition() or self.IsInPosition():
			self.Drop.Time = 0
		else:
			if self.Drop.Time < 60:
				self.Drop.Time += 1
			else:
				self.HideDrop()

class New_TitleBar(Window):
	BASE_PATH = "interface/controls/common/board"

	HEIGHT = 28
	MIN_WIDTH = 100
	BAR_WIDTH = 303
	LEFT_WIDTH = 40
	RIGHT_WIDTH = 40
	SEPARATOR_WIDTH = 1

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.AddFlag("attach")

		self.__dictImages = {
			'LEFT' : ImageBox(),
			'BAR' : ExpandedImageBox(),
			'RIGHT' : ImageBox(),
			'SEPARATOR' : ExpandedImageBox(),
		}

		self.__txtTitle = None

		for image in self.__dictImages.values():
			image.SetParent(self)
			image.AddFlag("attach")
			image.Show()

		self.__dictImages['LEFT'].LoadImage("%s/titlebar_left.tga" % self.BASE_PATH)
		self.__dictImages['BAR'].LoadImage("%s/titlebar.tga" % self.BASE_PATH)
		self.__dictImages['RIGHT'].LoadImage("%s/titlebar_right.tga" % self.BASE_PATH)
		self.__dictImages['SEPARATOR'].LoadImage("interface/controls/common/board_separator/horizontal.tga")

		self.__dictImages['LEFT'].SetPosition(0, 0)
		self.__dictImages['BAR'].SetPosition(self.LEFT_WIDTH, 0)
		self.__dictImages['SEPARATOR'].SetPosition(0, self.HEIGHT)

		self.btnClose = Button()
		self.btnClose.SetParent(self)
		self.btnClose.SetUpVisual("interface/controls/common/board/close_normal.tga")
		self.btnClose.SetOverVisual("interface/controls/common/board/close_over.tga")
		self.btnClose.SetDownVisual("interface/controls/common/board/close_down.tga")
		self.btnClose.Show()

	def __del__(self):
		Window.__del__(self)

	def MakeTitleBar(self, width):
		width = max(64, width)
		self.SetWidth(width)

	def SetWidth(self, width):
		width = max(self.MIN_WIDTH, width)

		self.SetSize(width, self.HEIGHT)

		size = float(width - self.LEFT_WIDTH - self.RIGHT_WIDTH + 1)/float(self.BAR_WIDTH) - 1.0
		self.__dictImages['RIGHT'].SetPosition(width - self.RIGHT_WIDTH, 0)
		self.__dictImages['BAR'].SetRenderingRect(0, 0, size, 0.0)
		self.__dictImages['SEPARATOR'].SetScale(float(width)/float(self.SEPARATOR_WIDTH), 1.0)

		self.UpdateTitlePosition()
		self.UpdateCloseButton()

	def SetTitle(self, title):
		if not self.__txtTitle:
			self.__txtTitle = TextLine()
			self.__txtTitle.SetParent(self)
			self.__txtTitle.SetHorizontalAlignCenter()
			self.__txtTitle.SetVerticalAlignBottom()
			self.__txtTitle.Show()

		self.__txtTitle.SetText(title)
		self.UpdateTitlePosition()

	def UpdateTitlePosition(self):
		if not self.__txtTitle:
			return

		self.__txtTitle.SetPosition(self.GetWidth() / 2, 17)

	def UpdateCloseButton(self):
		if not self.btnClose:
			return

		self.btnClose.SetPosition(self.GetWidth() - self.btnClose.GetWidth(), 0)

	def SetCloseEvent(self, event, args = None):
		self.btnClose.SetEvent(event, args)

#################################################################################################################################

class New_Board(Window):
	CORNER_WIDTH = 86
	CORNER_HEIGHT = 86
	LINE_WIDTH = 4
	LINE_HEIGHT = 4
	FILL_WIDTH = 128
	FILL_HEIGHT = 128

	LEFT_TOP = 0
	LEFT_BUTTON = 1
	RIGHT_TOP = 2
	RIGTH_BUTTON = 3

	LEFT = 0
	RIGHT = 1
	TOP = 2
	BUTTON = 3

	def __init__(self):
		Window.__init__(self)

		self.MakeBoard("interface/controls/common/board/corner_", "interface/controls/common/board/bar_")
		self.MakeBase()

	def MakeBoard(self, cornerPath, linePath):
		CornerFileNames = [ cornerPath+dir+".tga" for dir in ("lefttop", "leftbottom", "righttop", "rightbottom", ) ]
		LineFileNames = [ linePath+dir+".tga" for dir in ("left", "right", "top", "bottom", ) ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(-25, -20)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(-25, -20)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.LEFT].SetPosition(-25, self.CORNER_HEIGHT -20)
		self.Lines[self.TOP].SetPosition(self.CORNER_WIDTH -25, -20)

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("interface/controls/common/board/fill.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(33 -25, 28 -20)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		width = max((self.CORNER_WIDTH -25)* 2, width)
		height = max((self.CORNER_HEIGHT -25) * 2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LEFT_BUTTON].SetPosition(-25, height -self.CORNER_HEIGHT +20)
		self.Corners[self.RIGHT_TOP].SetPosition(width -self.CORNER_WIDTH +25, -20)
		self.Corners[self.RIGTH_BUTTON].SetPosition(width -self.CORNER_WIDTH +25, height -self.CORNER_HEIGHT +20)

		self.Lines[self.RIGHT].SetPosition(width -28 -5 +25, self.CORNER_HEIGHT -20)
		self.Lines[self.BUTTON].SetPosition(self.CORNER_HEIGHT -25, height -28 +20)

		verticalShowingPercentage = float((height - (self.CORNER_HEIGHT -20) * 2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - (self.CORNER_WIDTH -25) * 2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.LEFT].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.RIGHT].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.TOP].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.BUTTON].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		verticalShowingPercentage = float((height - (self.CORNER_HEIGHT -58 -20) * 2) - self.FILL_HEIGHT) / self.FILL_HEIGHT
		horizontalShowingPercentage = float((width - (self.CORNER_WIDTH -53 -25) * 2) - self.FILL_WIDTH) / self.FILL_WIDTH
		self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

#################################################################################################################################

class BoardTransparent(New_Board):
	def __init__(self):
		New_Board.__init__(self)

	def MakeBase(self):
		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("not_pick")
		Base.SetPosition(33 -25, 28 -20)
		Base.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.8))
		Base.Show()
		self.Base = Base

	def SetSize(self, width, height):
		width = max((self.CORNER_WIDTH -25)* 2, width)
		height = max((self.CORNER_HEIGHT -20) * 2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LEFT_BUTTON].SetPosition(-25, height -self.CORNER_HEIGHT +20)
		self.Corners[self.RIGHT_TOP].SetPosition(width -self.CORNER_WIDTH +25, -20)
		self.Corners[self.RIGTH_BUTTON].SetPosition(width -self.CORNER_WIDTH +25, height -self.CORNER_HEIGHT +20)

		self.Lines[self.RIGHT].SetPosition(width -28 -5 +25, self.CORNER_HEIGHT -20)
		self.Lines[self.BUTTON].SetPosition(self.CORNER_HEIGHT -25, height -28 +20)

		verticalShowingPercentage = float((height - (self.CORNER_HEIGHT -20) * 2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - (self.CORNER_WIDTH -25) * 2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.LEFT].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.RIGHT].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.TOP].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.BUTTON].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		y = height - (self.CORNER_HEIGHT -58 -20) * 2
		x = width - (self.CORNER_WIDTH -53 -25) * 2
		self.Base.SetSize(x, y)

#################################################################################################################################

class New_BoardWithTitleBar(New_Board):
	def __init__(self):
		New_Board.__init__(self)

		titleBar = New_TitleBar()
		titleBar.SetParent(self)
		titleBar.SetPosition(7, 8)
		titleBar.Show()

		self.titleBar = titleBar

		self.SetTitle = __mem_func__(self.titleBar.SetTitle)
		self.SetTitleName = __mem_func__(self.titleBar.SetTitle)
		self.SetCloseEvent(self.Hide)

	def __del__(self):
		New_Board.__del__(self)
		self.titleBar = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 14)
		New_Board.SetSize(self, width, height)

	def SetCloseEvent(self, event, args = None):
		self.titleBar.SetCloseEvent(event, args)

class ThinBoardNew(Window):

	CORNER_WIDTH = 17
	CORNER_HEIGHT = 17
	LINE_WIDTH = 1
	LINE_HEIGHT = 1

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.MakeBoard("interface/controls/common/tooltipboard/corner_", "interface/controls/common/tooltipboard/bar_")
		self.MakeBase()

	def MakeBoard(self, cornerPath, linePath):
		CornerFileNames = [ cornerPath+dir+".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]
		LineFileNames = [ linePath+dir+".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("interface/controls/common/tooltipboard/fill.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

##########################################################################################################################
### SCRIPTLOADER ### SCRIPTLOADER ### SCRIPTLOADER ### SCRIPTLOADER ### SCRIPTLOADER ### SCRIPTLOADER ### SCRIPTLOADER ###
##########################################################################################################################
class PythonScriptLoader(object):
	def __init__(self):
		self.Clear()

	def Clear(self):
		self.ScriptDictionary = { "SCREEN_WIDTH" : wndMgr.GetScreenWidth(), "SCREEN_HEIGHT" : wndMgr.GetScreenHeight() }
		self.InsertFunction = 0

	def LoadScriptFile(self, window, FileName):
		self.Clear()

		self.ScriptDictionary["PLAYER_NAME_MAX_LEN"] = 24
		self.ScriptDictionary["LOCALE_PATH"] = app.GetLocalePath()

		if __USE_EXTRA_CYTHON__:
			from os.path import splitext as op_splitext, basename as op_basename, dirname as op_dirname
			def GetModName(filename):
				return op_splitext(op_basename(filename))[0]
			def IsInUiPath(filename):
				def ICmp(s1, s2):
					return s1.lower() == s2.lower()
				return ICmp(op_dirname(filename), "uiscript")
			modname = GetModName(FileName)
			import uiscriptlib
			tpl2Main = (
				"SCREEN_WIDTH",
				"SCREEN_HEIGHT",
				"PLAYER_NAME_MAX_LEN",
				"LOCALE_PATH"
			)
			import builtins as bt
			for idx in tpl2Main:
				tmpVal = self.ScriptDictionary[idx]
				exec("bt.%s = tmpVal" % idx, globals(), locals())

		try:
			if __USE_EXTRA_CYTHON__ and IsInUiPath(FileName) and uiscriptlib.isExist(modname):
				m1 = uiscriptlib.moduleImport(modname)
				self.ScriptDictionary["window"] = m1.window.copy()
				del m1
			else:
				execfile(FileName, self.ScriptDictionary)
		except IOError as err:
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile1")
		except RuntimeError as err:
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile2")
		except BaseException:
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			exception.Abort("LoadScriptFile!!!!!!!!!!!!!!")

		Body = self.ScriptDictionary["window"]

		window.ClearDictionary()
		self.InsertFunction = window.InsertChild
		window.SetPosition(int(Body["x"]), int(Body["y"]))
		window.SetSize(int(Body["width"]), int(Body["height"]))
		if Body.__contains__("style"):
			for StyleList in Body["style"]:
				window.AddFlag(StyleList)

		self.LoadChildren(window, Body)

	def LoadChildren(self, parent, dicChildren):
		if dicChildren.__contains__("style"):
			for style in dicChildren["style"]:
				parent.AddFlag(style)

		if False == dicChildren.__contains__("children"):
			return False

		Index = 0

		ChildrenList = dicChildren["children"]
		parent.Children = []
		for i in range(len(ChildrenList)):
			parent.Children.append(None)

		for ElementValue in ChildrenList:
			if "name" in ElementValue:
				Name = ElementValue["name"]
			else:
				Name = ElementValue["name"] = "NONAME"

			if "type" in ElementValue:
				Type = ElementValue["type"]
			else:
				Type = ElementValue["type"] = "window"

			if Type == "window":
				parent.Children[Index] = ScriptWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)

			elif Type == "button":
				parent.Children[Index] = Button()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "radio_button":
				parent.Children[Index] = RadioButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "toggle_button":
				parent.Children[Index] = ToggleButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "mark":
				parent.Children[Index] = MarkBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMark(parent.Children[Index], ElementValue, parent)

			elif Type == "image":
				parent.Children[Index] = ImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "expanded_image":
				parent.Children[Index] = ExpandedImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExpandedImage(parent.Children[Index], ElementValue, parent)

			elif Type == "ani_image":
				parent.Children[Index] = AniImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementAniImage(parent.Children[Index], ElementValue, parent)

			elif Type == "slot":
				parent.Children[Index] = SlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlot(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_table":
				parent.Children[Index] = GridSlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridTable(parent.Children[Index], ElementValue, parent)

			elif Type == "text":
				parent.Children[Index] = TextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementText(parent.Children[Index], ElementValue, parent)

			elif Type == "editline":
				parent.Children[Index] = EditLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)

			elif Type == "box":
				parent.Children[Index] = Box()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBox(parent.Children[Index], ElementValue, parent)

			elif Type == "bar":
				parent.Children[Index] = Bar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBar(parent.Children[Index], ElementValue, parent)

			elif Type == "line":
				parent.Children[Index] = Line()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLine(parent.Children[Index], ElementValue, parent)

			elif Type == "slotbar":
				parent.Children[Index] = SlotBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlotBar(parent.Children[Index], ElementValue, parent)

			elif Type == "gauge":
				parent.Children[Index] = Gauge()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGauge(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox":
				parent.Children[Index] = ListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox2":
				parent.Children[Index] = ListBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox2(parent.Children[Index], ElementValue, parent)

			elif Type == "listboxex":
				parent.Children[Index] = ListBoxEx()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBoxEx(parent.Children[Index], ElementValue, parent)

				#################################################################################################################################
				### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ### OLD INTERFACE ###
				#################################################################################################################################
			elif Type == "titlebar":
				parent.Children[Index] = TitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board":
				parent.Children[Index] = Board()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar":
				parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard":
				parent.Children[Index] = ThinBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "horizontalbar":
				parent.Children[Index] = HorizontalBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar":
				parent.Children[Index] = ScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "small_thin_scrollbar":
				parent.Children[Index] = SmallThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thin_scrollbar":
				parent.Children[Index] = ThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "sliderbar":
				parent.Children[Index] = SliderBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[Index], ElementValue, parent)

				#################################################################################################################################
				### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ###
				#################################################################################################################################
			elif Type == "new_board":
				if constinfo.NEW_INTERFACE:
					parent.Children[Index] = New_Board()
				else:
					parent.Children[Index] = Board()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "new_board_with_titlebar":
				if constinfo.NEW_INTERFACE:
					parent.Children[Index] = New_BoardWithTitleBar()
				else:
					parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "new_scrollbar":
				parent.Children[Index] = New_ScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "new_thin_scrollbar":
				parent.Children[Index] = New_ThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board_transparent":
				parent.Children[Index] = BoardTransparent()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "slider":
				parent.Children[Index] = Slider()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlider(parent.Children[Index], ElementValue, parent)

			elif Type == "redbutton":
				parent.Children[Index] = RedButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBaseButton(parent.Children[Index], ElementValue, parent)

			elif Type == "verticalseparator":
				parent.Children[Index] = VerticalSeparator()
				parent.Children[Index].SetParent(parent)
				self.LoadElementVerticalSeparator(parent.Children[Index], ElementValue, parent)

			elif Type == "horizontalseparator":
				parent.Children[Index] = HorizontalSeparator()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalSeparator(parent.Children[Index], ElementValue, parent)

			elif Type == "ballon":
				parent.Children[Index] = Ballon()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBallon(parent.Children[Index], ElementValue, parent)

			elif Type == "newradio_button":
				parent.Children[Index] = NewRadioButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "slot_elipse":
				parent.Children[Index] = SlotElipseWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlotElipse(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_table_elipse":
				parent.Children[Index] = GridSlotElipseWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridTableElipse(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboardnew":
				parent.Children[Index] = ThinBoardNew()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardNew(parent.Children[Index], ElementValue, parent)

			elif Type == "barwithbox":
				parent.Children[Index] = BarWithBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBarWithBox(parent.Children[Index], ElementValue, parent)

			elif Type == "editboard":
				parent.Children[Index] = EditBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "editboardfake":
				parent.Children[Index] = EditBoardFake()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditBoardFake(parent.Children[Index], ElementValue, parent)

			elif Type == "dropdown":
				parent.Children[Index] = DropDown()
				parent.Children[Index].SetParent(parent)
				self.LoadElementDropDown(parent.Children[Index], ElementValue, parent)

			else:
				Index += 1
				continue

#################################################################################################################################
### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT ####
#################################################################################################################################
			'''
			elif Type == "candidate_list":
				parent.Children[Index] = CandidateListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCandidateList(parent.Children[Index], ElementValue, parent)

			elif Type == "textlink":
				parent.Children[Index] = TextLink()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLinkText(parent.Children[Index], ElementValue, parent)
			'''

			parent.Children[Index].SetWindowName(Name)
			if 0 != self.InsertFunction:
				self.InsertFunction(Name, parent.Children[Index])

			self.LoadChildren(parent.Children[Index], ElementValue)
			Index += 1

	def LoadDefaultData(self, window, value, parentWindow):
		loc_x = int(value["x"])
		loc_y = int(value["y"])
		if value.__contains__("vertical_align"):
			if "center" == value["vertical_align"]:
				window.SetWindowVerticalAlignCenter()
			elif "bottom" == value["vertical_align"]:
				window.SetWindowVerticalAlignBottom()

		if parentWindow.IsRTL():
			loc_x = int(value["x"]) + window.GetWidth()
			if value.__contains__("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
					loc_x = - int(value["x"])
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignLeft()
					loc_x = int(value["x"]) - window.GetWidth()
			else:
				window.SetWindowHorizontalAlignRight()

			if value.__contains__("all_align"):
				window.SetWindowVerticalAlignCenter()
				window.SetWindowHorizontalAlignCenter()
				loc_x = - int(value["x"])
		else:
			if value.__contains__("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignRight()

		window.SetPosition(loc_x, loc_y)
		if not value.__contains__("hide"):
			window.Show()
		else:
			if 0 == value["hide"]:
				window.Show()

		if value.__contains__("istooltip"):
			parentWindow.SetToolTipWindow(window)

	def LoadElementWindow(self, window, value, parentWindow):
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementButton(self, window, value, parentWindow):
		if value.__contains__("width") and value.__contains__("height"):
			window.SetSize(int(value["width"]), int(value["height"]))

		if value.__contains__("set_type"):
			window.SetType(value["set_type"])
		if value.__contains__("default_image"):
			window.SetUpVisual(value["default_image"])
		if value.__contains__("over_image"):
			window.SetOverVisual(value["over_image"])
		if value.__contains__("down_image"):
			window.SetDownVisual(value["down_image"])
		if value.__contains__("disable_image"):
			window.SetDisableVisual(value["disable_image"])

		if value.__contains__("text"):
			if value.__contains__("text_height"):
				window.SetText(value["text"], value["text_height"])
			else:
				window.SetText(value["text"])

			if value.__contains__("text_color"):
				window.SetTextColor(value["text_color"])

		if value.__contains__("tooltip_text"):
			if value.__contains__("tooltip_x") and value.__contains__("tooltip_y"):
				window.SetToolTipText(value["tooltip_text"], int(value["tooltip_x"]), int(value["tooltip_y"]))
			else:
				window.SetToolTipText(value["tooltip_text"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementMark(self, window, value, parentWindow):
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementImage(self, window, value, parentWindow):
		window.LoadImage(value["image"])

		if value.__contains__("alpha"):
			window.SetAlpha(float(value["alpha"]))

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementAniImage(self, window, value, parentWindow):
		if value.__contains__("delay"):
			window.SetDelay(value["delay"])

		for image in value["images"]:
			window.AppendImage(image)

		if value.__contains__("width") and value.__contains__("height"):
			window.SetSize(value["width"], value["height"])

		if value.__contains__("alpha"):
			window.SetAlpha(float(value["alpha"]))

		if value.__contains__("percent"):
			window.SetPercentageNew(float(value["percent"]))

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementExpandedImage(self, window, value, parentWindow):
		window.LoadImage(value["image"])

		if value.__contains__("width") and value.__contains__("height"):
			window.SetSizeFixed(int(value["width"]), int(value["height"]))

		if value.__contains__("x_origin") and value.__contains__("y_origin"):
			window.SetOrigin(float(value["x_origin"]), float(value["y_origin"]))

		if value.__contains__("x_scale") and value.__contains__("y_scale"):
			window.SetScale(float(value["x_scale"]), float(value["y_scale"]))

		if value.__contains__("rect"):
			RenderingRect = value["rect"]
			window.SetRenderingRect(RenderingRect[0], RenderingRect[1], RenderingRect[2], RenderingRect[3])

		if value.__contains__("mode"):
			mode = value["mode"]
			if "MODULATE" == mode:
				window.SetRenderingMode(wndMgr.RENDERING_MODE_MODULATE)

		if value.__contains__("alpha"):
			window.SetAlpha(float(value["alpha"]))

		if value.__contains__("rotation"):
			window.SetRotation(float(value["rotation"]))

		if value.__contains__("percent"):
			window.SetPercentageNew(float(value["percent"]))

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementSlot(self, window, value, parentWindow):
		global_x = int(value["x"])
		global_y = int(value["y"])
		global_width = int(value["width"])
		global_height = int(value["height"])

		window.SetPosition(global_x, global_y)
		window.SetSize(global_width, global_height)
		window.Show()

		r = 1.0
		g = 1.0
		b = 1.0
		a = 1.0

		if value.__contains__("image_r") and \
			value.__contains__("image_g") and \
			value.__contains__("image_b") and \
			value.__contains__("image_a"):
			r = float(value["image_r"])
			g = float(value["image_g"])
			b = float(value["image_b"])
			a = float(value["image_a"])

		for slot in value["slot"]:
			wndMgr.AppendSlot(window.hWnd, int(slot["index"]), int(slot["x"]), int(slot["y"]), int(slot["width"]), int(slot["height"]))

		if value.__contains__("image"):
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)
		return True

	def LoadElementGridTable(self, window, value, parentWindow):
		xBlank = 0
		yBlank = 0

		if value.__contains__("x_blank"):
			xBlank = int(value["x_blank"])
		if value.__contains__("y_blank"):
			yBlank = int(value["y_blank"])

		window.SetPosition(int(value["x"]), int(value["y"]))
		window.ArrangeSlot(int(value["start_index"]), int(value["x_count"]), int(value["y_count"]), int(value["x_step"]), int(value["y_step"]), xBlank, yBlank)

		if value.__contains__("image"):
			r = 1.0
			g = 1.0
			b = 1.0
			a = 1.0
			if value.__contains__("image_r") and value.__contains__("image_g") and value.__contains__("image_b") and value.__contains__("image_a"):
				r = float(value["image_r"])
				g = float(value["image_g"])
				b = float(value["image_b"])
				a = float(value["image_a"])
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		if value.__contains__("style"):
			if "select" == value["style"]:
				wndMgr.SetSlotStyle(window.hWnd, wndMgr.SLOT_STYLE_SELECT)

		window.Show()
		return True

	def LoadElementText(self, window, value, parentWindow):
		if value.__contains__("fontsize"):
			fontSize = value["fontsize"]

			if "LARGE" == fontSize:
				window.SetFontName(localeinfo.UI_DEF_FONT_LARGE)

		elif value.__contains__("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.__contains__("text_horizontal_align"):
			if "left" == value["text_horizontal_align"]:
				window.SetHorizontalAlignLeft()
			elif "center" == value["text_horizontal_align"]:
				window.SetHorizontalAlignCenter()
			elif "right" == value["text_horizontal_align"]:
				window.SetHorizontalAlignRight()

		if value.__contains__("text_vertical_align"):
			if "top" == value["text_vertical_align"]:
				window.SetVerticalAlignTop()
			elif "center" == value["text_vertical_align"]:
				window.SetVerticalAlignCenter()
			elif "bottom" == value["text_vertical_align"]:
				window.SetVerticalAlignBottom()

		if value.__contains__("limit_width"):
			window.SetLimitWidth(value["limit_width"])

		if value.__contains__("multi_line"):
			if value["multi_line"]:
				window.SetMultiLine()

		if value.__contains__("all_align"):
			window.SetHorizontalAlignCenter()
			window.SetVerticalAlignCenter()
			window.SetWindowHorizontalAlignCenter()
			window.SetWindowVerticalAlignCenter()

		if value.__contains__("r") and value.__contains__("g") and value.__contains__("b"):
			window.SetFontColor(float(value["r"]), float(value["g"]), float(value["b"]))
		elif value.__contains__("color"):
			window.SetPackedFontColor(value["color"])
		else:
			window.SetPackedFontColor(colorinfo.COR_TEXTO_PADRAO)

		if value.__contains__("outline"):
			if value["outline"]:
				window.SetOutline()
		if value.__contains__("text"):
			if value.__contains__("text_limited"):
				window.SetTextLimited(value["text"], int(value["text_limited"]))
			else:
				window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementEditLine(self, window, value, parentWindow):
		if value.__contains__("secret_flag"):
			window.SetSecret(value["secret_flag"])

		if value.__contains__("with_codepage"):
			if value["with_codepage"]:
				window.bCodePage = True

		if value.__contains__("r") and value.__contains__("g") and value.__contains__("b"):
			window.SetFontColor(float(value["r"]), float(value["g"]), float(value["b"]))
		elif value.__contains__("color"):
			window.SetPackedFontColor(value["color"])
		else:
			window.SetFontColor(0.8549, 0.8549, 0.8549)

		if value.__contains__("only_number"):
			if value["only_number"]:
				window.SetNumberMode()

		if value.__contains__("money_mode"):
			if value["money_mode"]:
				window.SetMoneyMode()

		if value.__contains__("enable_codepage"):
			window.SetIMEFlag(value["enable_codepage"])

		if value.__contains__("enable_ime"):
			window.SetIMEFlag(value["enable_ime"])

		if value.__contains__("limit_width"):
			window.SetLimitWidth(value["limit_width"])

		if value.__contains__("multi_line"):
			if value["multi_line"]:
				window.SetMultiLine()

		if value.__contains__("text_horizontal_align"):
			if "left" == value["text_horizontal_align"]:
				window.SetHorizontalAlignLeft()
			elif "center" == value["text_horizontal_align"]:
				window.SetHorizontalAlignCenter()
			elif "right" == value["text_horizontal_align"]:
				window.SetHorizontalAlignRight()

		if value.__contains__("text_vertical_align"):
			if "top" == value["text_vertical_align"]:
				window.SetVerticalAlignTop()
			elif "center" == value["text_vertical_align"]:
				window.SetVerticalAlignCenter()
			elif "bottom" == value["text_vertical_align"]:
				window.SetVerticalAlignBottom()

		if value.__contains__("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.__contains__("all_align"):
			window.SetHorizontalAlignCenter()
			window.SetVerticalAlignCenter()
			window.SetWindowHorizontalAlignCenter()
			window.SetWindowVerticalAlignCenter()

		window.SetMax(int(value["input_limit"]))
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadElementText(window, value, parentWindow)
		return True

	def LoadElementTitleBar(self, window, value, parentWindow):
		window.MakeTitleBar(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementBoard(self, window, value, parentWindow):
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementBoardWithTitleBar(self, window, value, parentWindow):
		window.SetSize(int(value["width"]), int(value["height"]))
		window.SetTitleName(value["title"])
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementThinBoard(self, window, value, parentWindow):
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementBox(self, window, value, parentWindow):
		if value.__contains__("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementBar(self, window, value, parentWindow):
		if value.__contains__("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementLine(self, window, value, parentWindow):
		if value.__contains__("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementSlotBar(self, window, value, parentWindow):
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementGauge(self, window, value, parentWindow):
		window.MakeGauge(value["width"], value["color"])
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementScrollBar(self, window, value, parentWindow):
		window.SetScrollBarSize(value["size"])

		if value.__contains__("midle_size"):
			window.SetMiddleBarSize(value["midle_size"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementSliderBar(self, window, value, parentWindow):
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementListBox(self, window, value, parentWindow):
		if value.__contains__("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementListBox2(self, window, value, parentWindow):
		window.SetRowCount(value.get("row_count", 10))
		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.__contains__("item_align"):
			window.SetTextCenterAlign(value["item_align"])
		return True

	def LoadElementListBoxEx(self, window, value, parentWindow):
		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.__contains__("itemsize_x") and value.__contains__("itemsize_y"):
			window.SetItemSize(int(value["itemsize_x"]), int(value["itemsize_y"]))

		if value.__contains__("itemstep"):
			window.SetItemStep(int(value["itemstep"]))

		if value.__contains__("viewcount"):
			window.SetViewItemCount(int(value["viewcount"]))
		return True

#################################################################################################################################
### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ### NEW INTERFACE ###
#################################################################################################################################
	def LoadElementThinBoardNew(self, window, value, parentWindow):
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementBaseButton(self, window, value, parentWindow):
		if value.__contains__("width"):
			window.SetWidth(int(value["width"]))

		if value.__contains__("text"):
			if value.__contains__("text_height"):
				window.SetText(value["text"], value["text_height"])
			else:
				window.SetText(value["text"])

		if value.__contains__("tooltip_text"):
			if value.__contains__("tooltip_x") and value.__contains__("tooltip_y"):
				window.SetToolTipText(value["tooltip_text"], int(value["tooltip_x"]), int(value["tooltip_y"]))
			else:
				window.SetToolTipText(value["tooltip_text"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementVerticalSeparator(self, window, value, parentWindow):
		window.SetHeight(int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementBallon(self, window, value, parentWindow):
		if value.__contains__("width"):
			window.SetWidth(int(value["width"]))
		if value.__contains__("text"):
			window.SetText(value["text"])
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementHorizontalSeparator(self, window, value, parentWindow):
		window.SetWidth(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementSlotElipse(self, window, value, parentWindow):
		global_x = int(value["x"])
		global_y = int(value["y"])
		global_width = int(value["width"])
		global_height = int(value["height"])

		window.SetPosition(global_x, global_y)
		window.SetSize(global_width, global_height)
		window.Show()

		r = 1.0
		g = 1.0
		b = 1.0
		a = 1.0

		if value.__contains__("image_r") and \
			value.__contains__("image_g") and \
			value.__contains__("image_b") and \
			value.__contains__("image_a"):
			r = float(value["image_r"])
			g = float(value["image_g"])
			b = float(value["image_b"])
			a = float(value["image_a"])

		for slot in value["slot"]:
			wndMgr.AppendSlot(window.hWnd, int(slot["index"]), int(slot["x"]), int(slot["y"]), int(slot["width"]), int(slot["height"]))

		if value.__contains__("image"):
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		wndMgr.SetSlotType(window.hWnd, 1)

		return True

	def LoadElementGridTableElipse(self, window, value, parentWindow):
		xBlank = 0
		yBlank = 0

		if value.__contains__("x_blank"):
			xBlank = int(value["x_blank"])
		if value.__contains__("y_blank"):
			yBlank = int(value["y_blank"])

		window.SetPosition(int(value["x"]), int(value["y"]))
		window.ArrangeSlot(int(value["start_index"]), int(value["x_count"]), int(value["y_count"]), int(value["x_step"]), int(value["y_step"]), xBlank, yBlank)

		if value.__contains__("image"):
			r = 1.0
			g = 1.0
			b = 1.0
			a = 1.0
			if value.__contains__("image_r") and \
				value.__contains__("image_g") and \
				value.__contains__("image_b") and \
				value.__contains__("image_a"):
				r = float(value["image_r"])
				g = float(value["image_g"])
				b = float(value["image_b"])
				a = float(value["image_a"])
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		if value.__contains__("style"):
			if "select" == value["style"]:
				wndMgr.SetSlotStyle(window.hWnd, wndMgr.SLOT_STYLE_SELECT)

		wndMgr.SetSlotType(window.hWnd, 1)

		window.Show()
		return True

	def LoadElementSlider(self, window, value, parentWindow):
		window.SetWidth(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementBarWithBox(self, window, value, parentWindow):
		if value.__contains__("color"):
			window.SetColor(value["color"])

		if value.__contains__("box_color"):
			window.SetBoxColor(value["box_color"])

		if value.__contains__("flash_color"):
			window.SetFlashColor(value["flash_color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementEditBoard(self, window, value , parentWindow):
		if value.__contains__("color"):
			window.SetColor(value["color"])
		if value.__contains__("box_color"):
			window.SetBoxColor(value["box_color"])
		if value.__contains__("flash_color"):
			window.SetFlashColor(value["flash_color"])

		if value.__contains__("fontsize"):
			fontSize = value["fontsize"]
			if "LARGE" == fontSize:
				window.SetFontName(localeinfo.UI_DEF_FONT_LARGE)

		elif value.__contains__("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.__contains__("infosize"):
			fontSize = value["infosize"]
			if "LARGE" == fontSize:
				window.SetInfoFontName(localeinfo.UI_DEF_FONT_LARGE)

		if value.__contains__("info_color"):
			window.SetInfoFontColor(value["info_color"])
		if value.__contains__("info_font"):
			window.SetInfoFontName(value["info_font"])
		if value.__contains__("info"):
			window.SetInfo(value["info"])

		if value.__contains__("secret_flag"):
			window.SetSecret(value["secret_flag"])
		if value.__contains__("only_number"):
			if value["only_number"]:
				window.SetNumberMode()
		if value.__contains__("text_color"):
			window.SetPackedFontColor(value["text_color"])
		if value.__contains__("text"):
			window.SetText(value["text"])

		if value.__contains__("input_limit"):
			window.SetMax(int(value["input_limit"]))

		if value.__contains__("height"):
			window.SetSize(int(value["width"]), int(value["height"]))
		else:
			window.SetSize(int(value["width"]), 28)

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementEditBoardFake(self, window, value , parentWindow):
		if value.__contains__("color"):
			window.SetColor(value["color"])
		if value.__contains__("box_color"):
			window.SetBoxColor(value["box_color"])
		if value.__contains__("flash_color"):
			window.SetFlashColor(value["flash_color"])

		if value.__contains__("fontsize"):
			fontSize = value["fontsize"]
			if "LARGE" == fontSize:
				window.SetFontName(localeinfo.UI_DEF_FONT_LARGE)

		elif value.__contains__("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.__contains__("text_color"):
			window.SetPackedFontColor(value["text_color"])
		if value.__contains__("text"):
			window.SetText(value["text"])
		if value.__contains__("text_center"):
			window.SetTextInCenter()

		if value.__contains__("height"):
			window.SetSize(int(value["width"]), int(value["height"]))
		else:
			window.SetSize(int(value["width"]), 28)

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementDropDown(self, window, value , parentWindow):
		if value.__contains__("color"):
			window.SetColor(value["color"])
		if value.__contains__("box_color"):
			window.SetBoxColor(value["box_color"])
		if value.__contains__("flash_color"):
			window.SetFlashColor(value["flash_color"])

		if value.__contains__("fontsize"):
			fontSize = value["fontsize"]
			if "LARGE" == fontSize:
				window.SetFontName(localeinfo.UI_DEF_FONT_LARGE)

		if value.__contains__("text_color"):
			window.SetPackedFontColor(value["text_color"])
		if value.__contains__("text"):
			window.SetText(value["text"])

		if value.__contains__("height"):
			window.SetSize(int(value["width"]), int(value["height"]))
		else:
			window.SetSize(int(value["width"]), 28)

		if value.__contains__("itens"):
			for item in value["itens"]:
				window.AppendItem(str(item["text"]), item["value"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementHorizontalBar(self, window, value, parentWindow):
		window.Create(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)
		return True

#################################################################################################################################
### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT USED ### NOT ####
#################################################################################################################################
'''
	def LoadElementLinkText(self, window, value, parentWindow):
		if value.__contains__("all_align"):
			window.SetHorizontalAlignCenter()
			window.SetVerticalAlignCenter()
			window.SetWindowHorizontalAlignCenter()
			window.SetWindowVerticalAlignCenter()

		if value.__contains__("outline"):
			if value["outline"]:
				window.SetOutline()
		if value.__contains__("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementCandidateList(self, window, value, parentWindow):
		window.SetPosition(int(value["x"]), int(value["y"]))
		window.SetItemSize(int(value["item_xsize"]), int(value["item_ysize"]))
		window.SetItemStep(int(value["item_step"]))
		window.Show()
		return True
'''

if OLD_STUFF:
	class ReadingWnd(Bar):
		def __init__(self):
			Bar.__init__(self, "TOP_MOST")
	
			self.__BuildText()
			self.SetSize(80, 19)
			self.Show()
	
		def __del__(self):
			Bar.__del__(self)
	
		def __BuildText(self):
			self.text = TextLine()
			self.text.SetParent(self)
			self.text.SetPosition(4, 3)
			self.text.Show()
	
		def SetText(self, text):
			self.text.SetText(text)
	
		def SetReadingPosition(self, x, y):
			xPos = x + 2
			yPos = y  - self.GetHeight() - 2
			self.SetPosition(xPos, yPos)
	
		def SetTextColor(self, color):
			self.text.SetPackedFontColor(color)

	class EmptyCandidateWindow(Window):
		def __init__(self):
			Window.__init__(self)

		def __del__(self):
			Window.__init__(self)

		def Load(self):
			pass

		def SetCandidatePosition(self, x, y, textCount):
			pass

		def Clear(self):
			pass

		def Append(self, text):
			pass

		def Refresh(self):
			pass

		def Select(self):
			pass

def MakeText(parent, textlineText, x, y, color):
	textline = TextLine()
	if parent != None:
		textline.SetParent(parent)
	textline.SetPosition(x, y)
	if color != None:
		textline.SetFontColor(color[0], color[1], color[2])
	textline.SetText(textlineText)
	textline.Show()
	return textline

def MakeText2(parent, textlineText, x, y, color):
	textline = TextLine()
	if parent != None:
		textline.SetParent(parent)
	textline.SetPosition(x, y)
	if color != None:
		textline.SetPackedFontColor(color)
	textline.SetText(textlineText)
	textline.Show()
	return textline

def MakeThinBoard(parent,  x, y, width, heigh, moveable = False, center = False):
	thin = ThinBoard()
	if parent != None:
		thin.SetParent(parent)
	if moveable == True:
		thin.AddFlag('movable')
		thin.AddFlag('float')
	thin.SetSize(width, heigh)
	thin.SetPosition(x, y)
	if center == True:
		thin.SetCenterPosition()
	thin.Show()
	return thin

def MakeSlotBar(parent, x, y, width, height):
	slotBar = SlotBar()
	slotBar.SetParent(parent)
	slotBar.SetSize(width, height)
	slotBar.SetPosition(x, y)
	slotBar.Show()
	return slotBar

def MakeImageBox(parent, name, x, y):
	image = ExpandedImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	image.Show()
	return image

def MakeTextLine(parent):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetWindowHorizontalAlignCenter()
	textLine.SetWindowVerticalAlignCenter()
	textLine.SetHorizontalAlignCenter()
	textLine.SetVerticalAlignCenter()
	textLine.Show()
	return textLine

def MakeButton(parent, x, y, tooltipText, path, up, over, down):
	button = Button()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetToolTipText(tooltipText)
	button.Show()
	return button

def RenderRoundBox(x, y, width, height, color):
	grp.SetColor(color)
	grp.RenderLine(x+2, y, width-3, 0)
	grp.RenderLine(x+2, y+height, width-3, 0)
	grp.RenderLine(x, y+2, 0, height-4)
	grp.RenderLine(x+width, y+1, 0, height-3)
	grp.RenderLine(x, y+2, 2, -2)
	grp.RenderLine(x, y+height-2, 2, 2)
	grp.RenderLine(x+width-2, y, 2, 2)
	grp.RenderLine(x+width-2, y+height, 2, -2)

def GenerateColor(r, g, b):
	r = float(r) / 255.0
	g = float(g) / 255.0
	b = float(b) / 255.0
	return grp.GenerateColor(r, g, b, 1.0)

def EnablePaste(flag):
	ime.EnablePaste(flag)

def GetHyperlink():
	return wndMgr.GetHyperlink()

def MakeTextLeft(parent, x):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.AddFlag("not_pick")
	textLine.SetPosition(x, -2)
	textLine.SetWindowVerticalAlignCenter()
	textLine.SetVerticalAlignCenter()
	textLine.Show()
	return textLine

def MakeEditLine(parent, x):
	textLine = EditLine()
	textLine.SetParent(parent)
	# textLine.AddFlag("not_pick")
	textLine.SetPosition(x, 4)
	textLine.SetWindowVerticalAlignCenter()
	# textLine.SetVerticalAlignCenter()
	textLine.Show()
	return textLine

def MakeTextRight(parent, x, y):
	textLine = TextLine()
	textLine.SetOutline()
	textLine.SetParent(parent)
	textLine.AddFlag("not_pick")
	textLine.SetPosition(x, y)
	textLine.SetWindowHorizontalAlignRight()
	textLine.SetHorizontalAlignRight()
	textLine.Show()
	return textLine

RegisterToolTipWindow("TEXT", TextLine)