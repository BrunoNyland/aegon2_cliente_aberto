#favor manter essa linha
import uiscriptlocale
import _grp as grp

normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

interface = "interface/controls/special/guild/"
icons = "interface/icons/special/"

CHARACTER = "interface/controls/special/character/"
interface = "interface/controls/special/guild/"
LINE = "interface/controls/common/horizontal_bar/center.tga"

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
hover_color = grp.GenerateColor(0.1, 0.1, 0.1, 0.8)
hover_color2 = grp.GenerateColor(0.05, 0.05, 0.05, 1.0)
text_color = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
color_quest = grp.GenerateColor(0.0, 0.0, 0.0, 0.2)


width = 356
height = 303

window = {
	"name":"GuildWindow_GuildInfoPage",
	"x":8,
	"y":39,
	"width":width,
	"height":height,
	"children":
	(
		# {"name":"","type":"bar","x":0,"y":0,"width":width,"height":height,"color":normal_color,},
## SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES ##
		{"name":"", "type":"horizontalseparator", "width":width+2, "x":-1, "y":85,},
		{"name":"", "type":"horizontalseparator", "width":width+2, "x":-1, "y":165,},
## BANDEIRA #### BANDEIRA #### BANDEIRA #### BANDEIRA #### BANDEIRA #### BANDEIRA #### BANDEIRA #### BANDEIRA ##
		{
			"name":"LargeGuildMarkSlot",
			"type": "barwithbox",
			"width":56, "height":44,
			"color": normal_color,
			"flash_color": hover_color,
			"box_color": box_color,
			"x":5,
			"y":5,
			"children":
			(
				{
					"name":"LargeGuildMark",
					"type":"mark",
					"x":4,
					"y":4,
				},
				{
					"name":"UploadGuildMarkButton",
					"type":"button",
					"default_image":interface+"changemark.tga",
					"over_image":interface+"changemark1.tga",
					"down_image":interface+"changemark2.tga",
					"x":0,"y":0,
				},
			),
		},
## NOME GUILD #### NOME GUILD #### NOME GUILD #### NOME GUILD #### NOME GUILD #### NOME GUILD #### NOME GUILD ##
		{
			"name":"GuildNameSlot",
			"type": "barwithbox",
			"width":140,
			"height":27,
			"color": normal_color,
			"flash_color": hover_color,
			"box_color": box_color,
			"x":66,
			"y":10,
			"children":
			(
				{"name":"GuildNameValue", "type":"text", "color":text_color, "text":uiscriptlocale.GUILD_INFO_NAME_VALUE, "x":0, "y":-1, "all_align":"center"},
			),
		},
## NOME LIDER #### NOME LIDER #### NOME LIDER #### NOME LIDER #### NOME LIDER #### NOME LIDER #### NOME LIDER ##
		{
			"name":"GuildMasterNameSlot",
			"type": "barwithbox",
			"width":140,
			"height":27,
			"color": normal_color,
			"flash_color": hover_color,
			"box_color": box_color,
			"x":211,
			"y":10,
			"children":
			(
				{
					"name":"GuildLeaderMark",
					"type":"image",
					"image":interface + "leader.tga",
					"x":7,"y":-1,
					"vertical_align":"center",
				},
				{"name":"line","type":"line","width":0.5,"height":27,"x":28,"y":0,"color":box_color,},
				{"name":"GuildMasterNameValue", "type":"text", "color":text_color, "text":uiscriptlocale.GUILD_INFO_MASTER_VALUE, "x":14, "y":-1, "all_align":"center"},
			),
		},
## GUILD LEVEL #### GUILD LEVEL #### GUILD LEVEL #### GUILD LEVEL #### GUILD LEVEL #### GUILD LEVEL #### GUILD LEVEL ##
		{
			"name":"GuildLevelSlot",
			"type": "barwithbox",
			"width":56,
			"height":27,
			"color": normal_color,
			"flash_color": normal_color,
			"box_color": box_color,
			"x":5,
			"y":54,
			"children":
			(
				{"name":"GuildLevelValue", "type":"text", "color":box_color, "text":"30", "x":0, "y":-1, "all_align":"center"},
			),
		},
## GUILD EXP #### GUILD EXP #### GUILD EXP #### GUILD EXP #### GUILD EXP #### GUILD EXP #### GUILD EXP #### GUILD EXP ##
		{
			"name":"ExpImgEmpty",
			"type":"image",
			"x":100,
			"y":62,
			"image":CHARACTER+"exp_gauge_empty.tga",
			"children":
			(
				{
					"name":"ExpImgFull",
					"type":"expanded_image",
					"x":0,
					"y":0,
					"image": CHARACTER+"exp_gauge_full.tga",
				},
				{"name":"PercentExp","type":"text","color":text_color,"text":"100%","x":0,"y":-14,"fontsize":"LARGE",},
				{"name":"Exp_Value","type":"text","color":box_color,"text":"","x":90-35,"y":-12,},
			),
		},
### QT DE MEMBROS ###### QT DE MEMBROS ###### QT DE MEMBROS ###### QT DE MEMBROS ###### QT DE MEMBROS ###### QT DE MEMBROS ###
		{
			"name":"GuildMemberCount", "type":"text", "color":text_color, "x":13, "y":105, "text":uiscriptlocale.GUILD_INFO_MEMBER_NUM+":",
			"children":
			(
				{
					"name":"GuildMemberCountSlot",
					"type": "barwithbox",
					"width":56,
					"height":25,
					"color": normal_color,
					"flash_color": hover_color,
					"box_color": normal_color,
					"x":55,
					"y":-5,
					"children":
					(
						{"name":"GuildMemberCountValue", "type":"text", "color":text_color, "text":"30 / 32", "x":0, "y":-1, "all_align":"center"},
					),
				},
			),
		},
### LVL MEDIO ###### LVL MEDIO ###### LVL MEDIO ###### LVL MEDIO ###### LVL MEDIO ###### LVL MEDIO ###### LVL MEDIO ###### LVL MEDIO ###
		{
			"name":"GuildMemberLevelAverage", "type":"text", "color":text_color, "x":13, "y":135, "text":uiscriptlocale.GUILD_INFO_MEMBER_AVG_LEVEL+":",
			"children":
			(
				{
					"name":"GuildMemberLevelAverageSlot",
					"type": "barwithbox",
					"width":37,
					"height":25,
					"color": normal_color,
					"flash_color": hover_color,
					"box_color": normal_color,
					"x":55+19,
					"y":-5,
					"children":
					(
						{"name":"GuildMemberLevelAverageValue", "type":"text", "color":text_color, "text":"53", "x":0, "y":-1, "all_align":"center"},
					),
				},
			),
		},
## DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP #### DOAR XP ##
		{
			"name":"OfferButton",
			"type":"redbutton",
			"width":90,
			"x":210-50,
			"y":95,
			"text":uiscriptlocale.GUILD_INFO_OFFER_EXP,
		},
		{
			"name":"DeclareWarButton",
			"type":"redbutton",
			"width":110,
			"x":200-50,"y":95+30,
			"text":"Declarar Guerra",
		},
		{
			"name":"MeetingButton",
			"type":"redbutton",
			"width":60,
			"x":275,"y":120,
			"text":"Convocar",
			"children":
			(
				{"name":"","type":"text","text":"Reunião de Guild","color": text_color,"x":0,"y":-20,"horizontal_align":"center","text_horizontal_align":"center",},
			),
		},
		{
			"name":"",
			"type":"expanded_image",
			"image":LINE,
			"x":0,
			"y":180,
			"x_scale":1.5,
			"y_scale":1,
			"horizontal_align":"center",
			"children":
			(
				{
					"name":"",
					"type":"text",
					"text":"Mensagem do Líder:",
					"color":text_color,
					"x":0,
					"y":-5,
					"all_align":"center",
				},
			),
		},
		{
			"name":"MessageLeaderButton",
			"type":"button",
			"default_image":icons + "quest_closed.tga",
			"over_image":icons + "quest_closed_hover.tga",
			"down_image":icons + "quest_closed.tga",
			"disable_image":icons + "quest_closed.tga",
			"x":7, "y":175,
		},
		{
			"name":"msg1",
			"type":"text",
			"color":0xffa08784,
			"text":"",
			"x": 0, "y": 210,
			"horizontal_align":"center",
			"text_horizontal_align":"center",
		},
		{
			"name":"msg2",
			"type":"text",
			"color":0xffa08784,
			"text":"",
			"x": 0, "y": 210+15,
			"horizontal_align":"center",
			"text_horizontal_align":"center",
		},
		{
			"name":"msg3",
			"type":"text",
			"color":0xffa08784,
			"text":"",
			"x": 0, "y": 210+15*2,
			"horizontal_align":"center",
			"text_horizontal_align":"center",
		},
		{
			"name":"msg4",
			"type":"text",
			"color":0xffa08784,
			"text":"",
			"x": 0, "y": 210+15*3,
			"horizontal_align":"center",
			"text_horizontal_align":"center",
		},
		{
			"name":"msg5",
			"type":"text",
			"color":0xffa08784,
			"text":"",
			"x": 0, "y": 210+15*4,
			"horizontal_align":"center",
			"text_horizontal_align":"center",
		},
		{
			"name":"MessageLeaderSlot",
			"type": "barwithbox",
			"width":345,
			"height":85,
			"color": hover_color2,
			"flash_color": hover_color2,
			"box_color": normal_color,
			"x":0,
			"y":210,
			"horizontal_align":"center",
			"hide":1,
			"children":
			(
				{
					"name":"smsg1",
					"type":"editline",
					"style":("not_pick",),
					"text_vertical_align":"center",
					"multi_line":1,
					"width":335, "height":80,
					"input_limit":170,
					"limit_width":330,
					"color":0xffa08784,
					"text":"",
					"x": 5, "y": 10,
				},
			),
		},
	),
}
