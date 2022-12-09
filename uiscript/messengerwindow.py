#favor manter essa linha
import uiscriptlocale

PACH_BUTTONS = "interface/controls/special/friendlist/"
BUTTON_START_X_POS = -60
BUTTON_X_STEP = 30
BUTTON_Y = 50

window = {
	"name":"MessengerWindow",
	"x":SCREEN_WIDTH - 200,
	"y":SCREEN_HEIGHT - 400 - 50,
	"style":("movable", "float",),
	"width":200,
	"height":300,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":210,
			"height":300,
			"title":uiscriptlocale.MESSENGER_TITLE,
		},
		{
			"name":"ScrollBar",
			"type":"new_scrollbar",
			"x":172,
			"y":45,
			"size":70,
		},
		{
			"name":"ButtonsSeparator",
			"type":"horizontalseparator",
			"width":186,
			"x":7,
			"y":100,
		},
		{
			"name":"ScrollBarSeparator",
			"type":"verticalseparator",
			"height":213,
			"x":166,
			"y":38,
		},
		{
			"name":"AddFriendButton",
			"type":"button",
			"x":BUTTON_START_X_POS + BUTTON_X_STEP*0,
			"y":BUTTON_Y,
			"horizontal_align":"center",
			"vertical_align":"bottom",
			"default_image":PACH_BUTTONS + "btn_add_01_normal.tga",
			"over_image":PACH_BUTTONS + "btn_add_02_hover.tga",
			"down_image":PACH_BUTTONS + "btn_add_03_active.tga",
			"disable_image":PACH_BUTTONS + "btn_add_05_disabled.tga",
			"children":
			(
				{"name":"","type":"ballon","width":60,"text":uiscriptlocale.MESSENGER_ADD_FRIEND,"x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
			),
		},
		{
			"name":"WhisperButton",
			"type":"button",
			"x":BUTTON_START_X_POS + BUTTON_X_STEP*1,
			"y":BUTTON_Y,
			"horizontal_align":"center",
			"vertical_align":"bottom",
			"default_image":PACH_BUTTONS + "btn_chat_01_normal.tga",
			"over_image":PACH_BUTTONS + "btn_chat_02_hover.tga",
			"down_image":PACH_BUTTONS + "btn_chat_03_active.tga",
			"disable_image":PACH_BUTTONS + "btn_chat_05_disabled.tga",
			"children":
			(
				{"name":"","type":"ballon","width":60,"text":uiscriptlocale.MESSENGER_WHISPER,"x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
			),
		},
		{
			"name":"RemoveButton",
			"type":"button",
			"x":BUTTON_START_X_POS + BUTTON_X_STEP*3,
			"y":BUTTON_Y,
			"horizontal_align":"center",
			"vertical_align":"bottom",
			"default_image":PACH_BUTTONS + "btn_remove_01_normal.tga",
			"over_image":PACH_BUTTONS + "btn_remove_02_hover.tga",
			"down_image":PACH_BUTTONS + "btn_remove_03_active.tga",
			"disable_image":PACH_BUTTONS + "btn_remove_05_disabled.tga",
			"children":
			(
				{"name":"","type":"ballon","width":60,"text":uiscriptlocale.MESSENGER_DELETE_FRIEND,"x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
			),
		},
		{
			"name":"GuildButton",
			"type":"button",
			"x":BUTTON_START_X_POS + BUTTON_X_STEP*4,
			"y":BUTTON_Y,
			"horizontal_align":"center",
			"vertical_align":"bottom",
			"default_image":PACH_BUTTONS + "btn_guild_01_normal.tga",
			"over_image":PACH_BUTTONS + "btn_guild_02_hover.tga",
			"down_image":PACH_BUTTONS + "btn_guild_03_active.tga",
			"disable_image":PACH_BUTTONS + "btn_guild_05_disabled.tga",
			"children":
			(
				{"name":"","type":"ballon","width":60,"text":uiscriptlocale.MESSENGER_OPEN_GUILD,"x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
			),
		},
	),
}
