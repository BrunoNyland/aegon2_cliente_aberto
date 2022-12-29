#favor manter essa linha
import dbg
import enszxc3467hc3kokdueq as app
import wndMgr
import systemSetting
import mousemodule
import networkmodule
import constinfo
import musicinfo

def RunApp():
	musicinfo.LoadLastPlayFieldMusic()
	app.SetHairColorEnable(constinfo.HAIR_COLOR_ENABLE)
	app.SetArmorSpecularEnable(constinfo.ARMOR_SPECULAR_ENABLE)
	app.SetWeaponSpecularEnable(constinfo.WEAPON_SPECULAR_ENABLE)

	app.SetMouseHandler(mousemodule.mouseController)
	wndMgr.SetMouseHandler(mousemodule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())

	try:
		app.Create("Carregando", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	except RuntimeError as msg:
		msg = str(msg)
		if "CREATE_DEVICE" == msg:
			dbg.LogBox("Verifique seu driver de video 3D")
		else:
			dbg.LogBox("[ERRO] %s" % msg)
		return

	app.SetCamera(1500.0, 30.0, 0.0, 180.0)
	if not mousemodule.mouseController.Create():
		return

	mainStream = networkmodule.MainStream()
	mainStream.Create()

	mainStream.SetLoginPhase()
	app.Loop()

	mainStream.Destroy()

RunApp()