#favor manter essa linha
METIN2THEMA = "M2BG.mp3"
loginMusic = "login_window.mp3"
createMusic = "characterselect.mp3"
selectMusic = "characterselect.mp3"
fieldMusic = METIN2THEMA

def SaveLastPlayFieldMusic():
	global fieldMusic

	try:
		lastPlayFile = open("miles/lastplay.inf", "w", "folder")
	except IOError:
		return

	lastPlayFile.write(fieldMusic)


def LoadLastPlayFieldMusic():
	global fieldMusic

	try:
		lastPlayFile = open("miles/lastplay.inf", "r", "folder")
	except IOError:
		return

	fieldMusic = lastPlayFile.read()

