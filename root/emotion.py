#favor manter essa linha
import localeinfo
import _player as player
import _app as app

EMOTION_CLAP			= 1
EMOTION_CONGRATULATION	= 2
EMOTION_FORGIVE			= 3
EMOTION_ANGRY			= 4
EMOTION_ATTRACTIVE		= 5
EMOTION_SAD				= 6
EMOTION_SHY				= 7
EMOTION_CHEERUP			= 8
EMOTION_BANTER			= 9
EMOTION_JOY				= 10
EMOTION_CHEERS_1		= 11
EMOTION_CHEERS_2		= 12
EMOTION_DANCE_1			= 13
EMOTION_DANCE_2			= 14
EMOTION_DANCE_3			= 15
EMOTION_DANCE_4			= 16
EMOTION_DANCE_5			= 17
EMOTION_DANCE_6			= 18
EMOTION_KISS			= 51
EMOTION_FRENCH_KISS		= 52
EMOTION_SLAP			= 53

if app.ENABLE_EXPRESSING_EMOTION:
	EMOTICON_NEXT		= 12
	EMOTION_PUSHUP		= app.SLOT_EMOTION_START
	EMOTION_DANCE_7		= app.SLOT_EMOTION_START+1
	EMOTION_EXERCISE	= app.SLOT_EMOTION_START+2
	EMOTION_DOZE		= app.SLOT_EMOTION_START+3
	EMOTION_SELFIE		= app.SLOT_EMOTION_START+4
	EMOTION_CHARGING	= app.SLOT_EMOTION_START+5
	EMOTION_NOSAY		= app.SLOT_EMOTION_START+6
	EMOTION_WEATHER_1	= app.SLOT_EMOTION_START+7
	EMOTION_WEATHER_2	= app.SLOT_EMOTION_START+8
	EMOTION_WEATHER_3	= app.SLOT_EMOTION_START+9
	EMOTION_HUNGRY		= app.SLOT_EMOTION_START+10
	EMOTION_SIREN		= app.SLOT_EMOTION_START+11
	EMOTION_ALCOHOL		= app.SLOT_EMOTION_START+12
	EMOTION_CALL		= app.SLOT_EMOTION_START+13
	EMOTION_CELEBRATION = app.SLOT_EMOTION_START+14
	EMOTION_LETTER		= app.SLOT_EMOTION_START+15
	EMOTION_BUSY		= app.SLOT_EMOTION_START+16
	EMOTION_WHIRL		= app.SLOT_EMOTION_START+17

EMOTION_DICT = {
	EMOTION_CLAP			:{"name": localeinfo.EMOTION_CLAP,				"command":"/clap"},
	EMOTION_DANCE_1			:{"name": localeinfo.EMOTION_DANCE_1,			"command":"/dance1"},
	EMOTION_DANCE_2			:{"name": localeinfo.EMOTION_DANCE_2,			"command":"/dance2"},
	EMOTION_DANCE_3			:{"name": localeinfo.EMOTION_DANCE_3,			"command":"/dance3"},
	EMOTION_DANCE_4			:{"name": localeinfo.EMOTION_DANCE_4,			"command":"/dance4"},
	EMOTION_DANCE_5			:{"name": localeinfo.EMOTION_DANCE_5,			"command":"/dance5"},
	EMOTION_DANCE_6			:{"name": localeinfo.EMOTION_DANCE_6,			"command":"/dance6"},
	EMOTION_CONGRATULATION	:{"name": localeinfo.EMOTION_CONGRATULATION,	"command":"/congratulation"},
	EMOTION_FORGIVE			:{"name": localeinfo.EMOTION_FORGIVE,			"command":"/forgive"},
	EMOTION_ANGRY			:{"name": localeinfo.EMOTION_ANGRY,				"command":"/angry"},
	EMOTION_ATTRACTIVE		:{"name": localeinfo.EMOTION_ATTRACTIVE,		"command":"/attractive"},
	EMOTION_SAD				:{"name": localeinfo.EMOTION_SAD,				"command":"/sad"},
	EMOTION_SHY				:{"name": localeinfo.EMOTION_SHY,				"command":"/shy"},
	EMOTION_CHEERUP			:{"name": localeinfo.EMOTION_CHEERUP,			"command":"/cheerup"},
	EMOTION_BANTER			:{"name": localeinfo.EMOTION_BANTER,			"command":"/banter"},
	EMOTION_JOY				:{"name": localeinfo.EMOTION_JOY,				"command":"/joy"},
	EMOTION_CHEERS_1		:{"name": localeinfo.EMOTION_CHEERS_1,			"command":"/cheer1"},
	EMOTION_CHEERS_2		:{"name": localeinfo.EMOTION_CHEERS_2,			"command":"/cheer2"},
	EMOTION_KISS			:{"name": localeinfo.EMOTION_CLAP_KISS,			"command":"/kiss"},
	EMOTION_FRENCH_KISS		:{"name": localeinfo.EMOTION_FRENCH_KISS,		"command":"/french_kiss"},
	EMOTION_SLAP			:{"name": localeinfo.EMOTION_SLAP,				"command":"/slap"}
}


ICON_DICT = {
	EMOTION_CLAP			:"interface/icons/emotion/aplaudir.tga",
	EMOTION_CHEERS_1		:"interface/icons/emotion/grito.tga",
	EMOTION_CHEERS_2		:"interface/icons/emotion/comemorar.tga",
	EMOTION_CONGRATULATION	:"interface/icons/emotion/aplaudir.tga",
	EMOTION_FORGIVE			:"interface/icons/emotion/perdoar.tga",
	EMOTION_ANGRY			:"interface/icons/emotion/enfurecer.tga",
	EMOTION_ATTRACTIVE		:"interface/icons/emotion/seduzir.tga",
	EMOTION_SAD				:"interface/icons/emotion/lamentar.tga",
	EMOTION_SHY				:"interface/icons/emotion/timidez.tga",
	EMOTION_CHEERUP			:"interface/icons/emotion/apoiar.tga",
	EMOTION_BANTER			:"interface/icons/emotion/provocar.tga",
	EMOTION_JOY				:"interface/icons/emotion/alegrar.tga",
	EMOTION_DANCE_1			:"interface/icons/emotion/dance1.tga",
	EMOTION_DANCE_2			:"interface/icons/emotion/dance2.tga",
	EMOTION_DANCE_3			:"interface/icons/emotion/dance3.tga",
	EMOTION_DANCE_4			:"interface/icons/emotion/dance4.tga",
	EMOTION_DANCE_5			:"interface/icons/emotion/dance5.tga",
	EMOTION_DANCE_6			:"interface/icons/emotion/dance6.tga",
	EMOTION_KISS			:"interface/icons/emotion/beijo1.tga",
	EMOTION_FRENCH_KISS		:"interface/icons/emotion/beijo2.tga",
	EMOTION_SLAP			:"interface/icons/emotion/tapa.tga"
}

if app.ENABLE_EXPRESSING_EMOTION:
	ICON_DICT[EMOTION_PUSHUP]				= "interface/icons/emotion/pushup.tga"
	ICON_DICT[EMOTION_DANCE_7]				= "interface/icons/emotion/dance7.tga"
	ICON_DICT[EMOTION_EXERCISE]				= "interface/icons/emotion/exercise.tga"
	ICON_DICT[EMOTION_DOZE]					= "interface/icons/emotion/doze.tga"
	ICON_DICT[EMOTION_SELFIE]				= "interface/icons/emotion/selfie.tga"
	ICON_DICT[EMOTION_CHARGING]				= "interface/icons/emotion/charging.tga"
	ICON_DICT[EMOTION_NOSAY]				= "interface/icons/emotion/nosay.tga"
	ICON_DICT[EMOTION_WEATHER_1]			= "interface/icons/emotion/weather1.tga"
	ICON_DICT[EMOTION_WEATHER_2]			= "interface/icons/emotion/weather2.tga"
	ICON_DICT[EMOTION_WEATHER_3]			= "interface/icons/emotion/weather3.tga"
	ICON_DICT[EMOTION_HUNGRY]				= "interface/icons/emotion/hungry.tga"
	ICON_DICT[EMOTION_SIREN]				= "interface/icons/emotion/siren.tga"
	ICON_DICT[EMOTION_ALCOHOL]				= "interface/icons/emotion/alcohol.tga"
	ICON_DICT[EMOTION_CALL]					= "interface/icons/emotion/call.tga"
	ICON_DICT[EMOTION_CELEBRATION]			= "interface/icons/emotion/celebration.tga"
	ICON_DICT[EMOTION_LETTER]				= "interface/icons/emotion/letter.tga"
	ICON_DICT[EMOTION_BUSY]					= "interface/icons/emotion/busy.tga"
	ICON_DICT[EMOTION_WHIRL]				= "interface/icons/emotion/whirl.tga"

if app.ENABLE_EXPRESSING_EMOTION:
	command_emotion = {
		EMOTION_PUSHUP			:{"name": localeinfo.EMOTION_PUSH_UP,			"command":"/pushup"},
		EMOTION_DANCE_7			:{"name": localeinfo.EMOTION_DANCE_7,			"command":"/dance_7"},
		EMOTION_EXERCISE		:{"name": localeinfo.EMOTION_EXERCISE,			"command":"/exercise"},
		EMOTION_DOZE			:{"name": localeinfo.EMOTION_DOZE,				"command":"/doze"},
		EMOTION_SELFIE			:{"name": localeinfo.EMOTION_SELFIE,			"command":"/selfie"},
		EMOTION_CHARGING		:{"name": localeinfo.EMOTION_CHARGING,			"command":EMOTICON_NEXT},
		EMOTION_NOSAY			:{"name": localeinfo.EMOTION_NOSAY,				"command":EMOTICON_NEXT+1},
		EMOTION_WEATHER_1		:{"name": localeinfo.EMOTION_WEATHER_1,			"command":EMOTICON_NEXT+2},
		EMOTION_WEATHER_2		:{"name": localeinfo.EMOTION_WEATHER_2,			"command":EMOTICON_NEXT+3},
		EMOTION_WEATHER_3		:{"name": localeinfo.EMOTION_WEATHER_3,			"command":EMOTICON_NEXT+4},
		EMOTION_HUNGRY			:{"name": localeinfo.EMOTION_HUNGRY,			"command":EMOTICON_NEXT+5},
		EMOTION_SIREN			:{"name": localeinfo.EMOTION_SIREN,				"command":EMOTICON_NEXT+6},
		EMOTION_ALCOHOL			:{"name": localeinfo.EMOTION_ALCOHOL,			"command":EMOTICON_NEXT+7},
		EMOTION_CALL			:{"name": localeinfo.EMOTION_CALL,				"command":EMOTICON_NEXT+8},
		EMOTION_CELEBRATION		:{"name": localeinfo.EMOTION_CELEBRATION,		"command":EMOTICON_NEXT+9},
		EMOTION_LETTER			:{"name": localeinfo.EMOTION_LETTER,			"command":EMOTICON_NEXT+10},
		EMOTION_BUSY			:{"name": localeinfo.EMOTION_BUSY,				"command":EMOTICON_NEXT+11},
		EMOTION_WHIRL			:{"name": localeinfo.EMOTION_WHIRL,				"command":EMOTICON_NEXT+12}
	}

def RegisterEmotionIcons():
	for key, val in ICON_DICT.items():
		player.RegisterEmotionIcon(key, val)
