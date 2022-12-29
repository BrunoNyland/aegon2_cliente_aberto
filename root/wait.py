#favor manter essa linha
import ui
import time

class WaitingDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.eventTimeOver = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self, waitTime):
		curTime = time.perf_counter_ns()
		self.endTime = curTime + waitTime
		self.Show()

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()

	def SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def OnUpdate(self):
		lastTime = max(0, self.endTime - time.perf_counter_ns())
		if 0 == lastTime:
			self.Close()
			if self.eventTimeOver:
				self.eventTimeOver()