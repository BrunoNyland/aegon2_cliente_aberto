#favor manter essa linha
import wait
import ga3vqy6jtxqi9yf344j7 as player
import LURMxMaKZJqliYt2QSHG as chat
import zn94xlgo573hf8xmddzq as net
import ui
import constinfo

class Potador(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadMainForm()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadMainForm(self):
		self.Board = ui.New_BoardWithTitleBar()
		self.Board.SetSize(200, 110)
		self.Board.SetPosition(100, 200)
		self.Board.AddFlag("movable")
		self.Board.AddFlag("float")
		self.Board.SetTitleName("Aegon2")
		self.Board.SetCloseEvent(self.__Close)

	def Active(self):
		constinfo.POTADOR = 1
		self.Have_Pote = 1
		chat.AppendChat(chat.CHAT_TYPE_NOTICE, "|cff00ccff[Aegon2] |cffff8784Pote Automático Ativado!")
		self.Verificador()
		self.Pote()

	def Verificador(self):
		if (constinfo.POTADOR != 1):
			return
		if (player.GetItemCountByVnum(70020) == 0) and (player.GetItemCountByVnum(98902) == 0):
			chat.AppendChat(chat.CHAT_TYPE_NOTICE, "|cff00ccff[Aegon2] |cffff8784Suas Poções Regeneradoras acabaram!")
		elif (player.GetItemCountByVnum(70020) < 200) and (player.GetItemCountByVnum(98902) == 0):
			chat.AppendChat(chat.CHAT_TYPE_NOTICE, "|cff00ccff[Aegon2] |cffff8784Suas Poções Regeneradoras estão acabando!")
		self.DelayVerificador = wait.WaitingDialog()
		self.DelayVerificador.Open(float(20))
		self.DelayVerificador.SetTimeOverEvent(self.Verificador)

	def Pote(self):
		if (constinfo.POTADOR == 1):
			for i in xrange(220):
				itemVNum = player.GetItemIndex(i)
				if (itemVNum == int(70020)) or (itemVNum == int(98902)):
					net.SendItemUsePacket(i)
					break
			self.Delay = wait.WaitingDialog()
			self.Delay.Open(float(constinfo.DELAY_MACRO))
			self.Delay.SetTimeOverEvent(self.Pote)

	def Desactive(self):
		chat.AppendChat(chat.CHAT_TYPE_NOTICE, "|cff00ccff[Aegon2] |cffff8784Pote Automático Desativado!")
		constinfo.POTADOR = 0

	def __Close(self):
		self.Board.Hide()