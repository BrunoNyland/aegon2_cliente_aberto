#favor manter essa linha
import enszxc3467hc3kokdueq as app

CODEPAGE = str(app.GetDefaultCodePage())

def LoadLocaleFile(srcFileName, localeDict):
	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("Load uiscript/LocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		tokens = line[:-1].split("\t")
		if len(tokens) >= 2:
			localeDict[tokens[0]] = tokens[1]
		else:
			print(len(tokens), lines.index(line), line)

name = app.GetLocalePath()
LOCALE_UISCRIPT_PATH = "%s/ui/" % (name)
LOGIN_PATH = "%s/ui/login/" % (name)
EMPIRE_PATH = "%s/ui/empire/" % (name)
SELECT_PATH = "%s/ui/select/" % (name)
MAPNAME_PATH = "%s/ui/mapname/" % (name)
WINDOWS_PATH = "%s/ui/windows/" % (name)

JOBDESC_WARRIOR_PATH = "%s/jobdesc_warrior.txt" % (name)
JOBDESC_ASSASSIN_PATH = "%s/jobdesc_assassin.txt" % (name)
JOBDESC_SURA_PATH = "%s/jobdesc_sura.txt" % (name)
JOBDESC_SHAMAN_PATH = "%s/jobdesc_shaman.txt" % (name)

EMPIREDESC_A = "%s/empiredesc_a.txt" % (name)
EMPIREDESC_B = "%s/empiredesc_b.txt" % (name)
EMPIREDESC_C = "%s/empiredesc_c.txt" % (name)

LOCALE_INTERFACE_FILE_NAME = "%s/locale_interface.txt" % (name)

LoadLocaleFile(LOCALE_INTERFACE_FILE_NAME, locals())