#favor manter essa linha
import uiscriptlocale

default = "interface/controls/common/button/stats_increase_01_normal.tga"
over = "interface/controls/common/button/stats_increase_02_hover.tga"
down = "interface/controls/common/button/stats_increase_03_active.tga"

adjust = 80

window = {
	"name":"GameWindow",
	"style":("not_pick",),
	"x":0,
	"y":0,
	"width":SCREEN_WIDTH,
	"height":SCREEN_HEIGHT,
	"children":
	(
		{
			"name":"QuestButton",
			"type":"button",
			"x":SCREEN_WIDTH-50-32,
			"y":SCREEN_HEIGHT-170-adjust,
			"default_image":default,
			"over_image":over,
			"down_image":down,
			"children":
			(
				{
					"name":"QuestButtonLabel",
					"type":"text",
					"x": 16,
					"y": 40,
					"text":uiscriptlocale.GAME_QUEST,
					"r":1.0, "g":1.0, "b":1.0, "a":1.0,
					"text_horizontal_align":"center"
				},
			),
		},
		{
			"name":"StatusPlusButton",
			"type":"button",
			"x":50,
			"y":SCREEN_HEIGHT-100-adjust,
			"default_image":default,
			"over_image":over,
			"down_image":down,

			"children":
			(
				{
					"name":"StatusPlusLabel",
					"type":"text",
					"x":16,
					"y":40,
					"text":uiscriptlocale.GAME_STAT_UP,
					"r":1.0, "g":1.0, "b":1.0, "a":1.0,
					"text_horizontal_align":"center"
				},
			),
		},
		{
			"name":"SkillPlusButton",
			"type":"button",
			"x":50,
			"y":SCREEN_HEIGHT-100-adjust-70,
			"default_image":default,
			"over_image":over,
			"down_image":down,
			"children":
			(
				{
					"name":"SkillPlusLabel",
					"type":"text",
					"x": 16,
					"y": 40,
					"text":uiscriptlocale.GAME_SKILL_UP,
					"r":1.0, "g":1.0, "b":1.0, "a":1.0,
					"text_horizontal_align":"center"
				},
			),
		},
		{
			"name":"ExitObserver",
			"type":"button", 
			"x":SCREEN_WIDTH-50-32,
			"y":SCREEN_HEIGHT-170-adjust,
			"default_image":default,
			"over_image":over,
			"down_image":down,
			"children":
			(
				{ 
					"name":"ExitObserverButtonName",
					"type":"text",
					"x": 16,
					"y": 40,
					"text": uiscriptlocale.GAME_EXIT_OBSERVER,
					"r":1.0, "g":1.0, "b":1.0, "a":1.0,
					"text_horizontal_align":"center"
				},
			),
		},
	),
}
