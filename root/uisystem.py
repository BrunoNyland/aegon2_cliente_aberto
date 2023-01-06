#favor manter essa linha
import _net as net
import _app as app
import _chat as chat
import _player as player
import ui
import uiscriptlocale
import networkmodule
import constinfo
import _event as event
import uicommon
import uiconfig

class SystemDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()

	def __Initialize(self):
		self.gameOptionDlg = None
		self.interface = None

	def LoadDialog(self):
		self.gameOptionDlg = uiconfig.GameOptions()

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/systemdialog.py")

		self.GetChild("game_option_button").SetEvent(self.__ClickGameOptionButton)
		self.GetChild("change_button").SetEvent(self.__ClickChangeCharacterButton)
		self.GetChild("logout_button").SetEvent(self.__ClickLogOutButton)
		self.GetChild("exit_button").SetEvent(self.__ClickExitButton)

		if self.interface:
			self.GetChild("inventory_button").SetEvent(self.ShowInventory)
			self.GetChild("messenger_button").SetEvent(self.ShowMessenger)
			self.GetChild("whisper_button").SetEvent(self.ShowWhisper)
			self.GetChild("boot_button").SetEvent(self.ShowBot)
			self.GetChild("guild_button").SetEvent(self.ShowGuild)
			self.GetChild("character_button").SetEvent(self.ShowCharacter)

	def ShowGuild(self):
		if self.interface:
			self.interface.ToggleGuildWindow()
		self.Close()

	def ShowBot(self):
		if self.interface:
			self.interface.OpenWndBot()
		self.Close()

	def ShowCharacter(self):
		if self.interface:
			self.interface.ToggleCharacterWindow()
		self.Close()

	def ShowWhisper(self):
		if self.interface:
			self.interface.OpenWhisperDialogWithoutTarget()
		self.Close()

	def ShowInventory(self):
		if self.interface:
			self.interface.ToggleInventoryWindow()
		self.Close()

	def ShowMessenger(self):
		if self.interface:
			self.interface.ToggleMessenger()
		self.Close()

	def SetInterface(self, interface):
		from weakref import proxy
		self.interface = proxy(interface)

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

		if self.gameOptionDlg:
			self.gameOptionDlg.Destroy()

		self.__Initialize()

	def OpenDialog(self):
		self.Show()

	def __ClickChangeCharacterButton(self):
		self.Close()
		net.ExitGame()

	def __OnClosePopupDialog(self):
		self.popup = None

	def __ClickLogOutButton(self):
		self.Close()
		net.LogOutGame()

	def __ClickExitButton(self):
		questionDialog = uicommon.QuestionDialog()
		questionDialog.SetText("Você quer fechar o jogo?")
		questionDialog.SetAcceptEvent(self.Yes)
		questionDialog.SetCancelEvent(self.No)
		questionDialog.Open()
		self.questionDialog = questionDialog

	def Yes(self):
		app.Exit()

	def No(self):
		self.Close()
		self.questionDialog.Close()

	def __ClickGameOptionButton(self):
		self.Close()

		if self.gameOptionDlg:
			self.gameOptionDlg.Show()

	def Close(self):
		self.Hide()
		return True

	def OnBlockMode(self, mode):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnBlockMode(mode)

	def OnChangePKMode(self):
		if self.gameOptionDlg:
			self.gameOptionDlg.OnChangePKMode()

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True