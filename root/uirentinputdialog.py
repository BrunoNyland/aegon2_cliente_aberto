#favor manter essa linha
import zn94xlgo573hf8xmddzq as net
import ga3vqy6jtxqi9yf344j7 as player
import XXjvumrgrYBZompk3PS8 as item
import ui

class RentTimeDialog(ui.ScriptWindow):

	min = 5 * 60
	max = (60 * 60 * 24 * 30) - min

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/rent_time_input_dialog.py")
		self.attachedInvenType = 0
		self.SrcSlotNumber = 0
		self.DstSlotNumber = 0

	def Open(self, attachedInvenType, SrcSlotNumber, DstSlotNumber):
		itemVnum = player.GetItemIndex(attachedInvenType, SrcSlotNumber)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		if not (item.GetItemType() == item.ITEM_TYPE_ARMOR or (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() != item.WEAPON_ARROW)):
			return

		self.attachedInvenType = attachedInvenType
		self.SrcSlotNumber = SrcSlotNumber
		self.DstSlotNumber = DstSlotNumber

		get = self.GetChild

		get("Slider").SetSliderPos(0.0)
		get("Slider").SetEvent(self.SetTimeText)

		get("accept_button").SetEvent(self.OnAccept)
		get("cancel_button").SetEvent(self.Hide)
		self.Show()
		self.SetTop()
		self.SetFocus()

	def SetTimeText(self):
		get = self.GetChild

		time = self.min + int(self.max * get("Slider").GetSliderPos())
		txt = "Tempo definido: "
		m = (time / (60 * 60 * 24 * 30))
		d = (time - (m * 60 * 60 * 24 * 30)) / (60 * 60 * 24)
		h = (time - (m * 60 * 60 * 24 * 30) - (d * 60 * 60 * 24)) / (60 * 60)
		min = (time - (m * 60 * 60 * 24 * 30) - (d * 60 * 60 * 24) - (h * 60 * 60)) / 60
		if m > 0:
			if m > 1:
				txt = txt + str(m) + " meses "
			else:
				txt = txt + str(m) + " mês "
		if d > 0:
			if d > 1:
				txt = txt + str(d) + " dias "
			else:
				txt = txt + str(d) + " dia "
		if h > 0:
			if h > 1:
				txt = txt + str(h) + " horas "
			else:
				txt = txt + str(h) + " hora "
		if min > 0:
			if min > 1:
				txt = txt + str(min) + " minutos"
			else:
				txt = txt + str(min) + " minuto"

		get("Slider_title").SetText(txt)


	def OnAccept(self):
		get = self.GetChild

		time = self.min + int(self.max * get("Slider").GetSliderPos())
		net.SendExchangeItemAddPacket(self.attachedInvenType, self.SrcSlotNumber, self.DstSlotNumber, time)

		self.Hide()

# x = RentTimeDialog()
# x.Open(0,0,0)