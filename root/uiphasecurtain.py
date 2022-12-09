#favor manter essa linha
import ui
import grp
import wndMgr

class PhaseCurtain(ui.Bar):
	def __init__(self):
		ui.Bar.__init__(self, "CURTAIN")
		self.speed = 0.05
		self.curAlpha = 0.0
		self.event = 0
		self.args = -1
		self.FadeInFlag = False
		self.SetWindowName("PhaseCurtain")
		self.AddFlag("float")

	def __del__(self):
		ui.Bar.__del__(self)

	def FadeOut(self, event, args = -1):
		self.curAlpha = 0.0
		self.SetAlpha(self.curAlpha)
		self.Show()
		self.event = ui.__mem_func__(event)
		self.args = args

	def FadeIn(self):
		self.event = 0
		self.FadeInFlag = True

	def SetAlpha(self, alpha):
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		color = grp.GenerateColor(0.0, 0.0, 0.0, alpha)
		self.SetColor(color)

	def OnUpdate(self):
		if self.event:
			self.curAlpha += self.speed
			if self.curAlpha >= 1.0:
				self.curAlpha = 1.0
				event = self.event
				self.event = 0

				if -1 != self.args:
					event(self.args)
				else:
					event()

		elif self.FadeInFlag:
			self.curAlpha -= self.speed
			if self.curAlpha <= 0.0:
				self.curAlpha = 0.0
				self.eventFadeIn = 0
				self.FadeInFlag = False
				self.Hide()

		self.SetAlpha(self.curAlpha)