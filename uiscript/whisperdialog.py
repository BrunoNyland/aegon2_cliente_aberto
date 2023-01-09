#favor manter essa linha
import uiscriptlocale
import _chr as chr
import _app as app

whisper = "interface/controls/special/whisper/"

width = 280
height = 200

window = {
	"name":"WhisperDialog",
	"style":("movable", "float",),
	"x":0,
	"y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"board_transparent",
			"style":("attach",),
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"name_slot",
					"type":"expanded_image",
					"style":("attach",),
					"x":15,
					"y":10,
					"x_scale":110,
					"y_scale":20,
					"image":whisper+"fill.tga",
					"children":
					(
						{
							"name":"left",
							"type":"image",
							"image":whisper + "name_left.tga",
							"x":-5,
							"y":0,
						},
						{
							"name":"right",
							"type":"image",
							"image":whisper + "name_right.tga",
							"x":110,
							"y":0,
						},
						{
							"name":"titlename",
							"type":"text",
							"x":0,
							"y":3,
							"r":1.0,
							"g":0.85,
							"b":0.65,
							"text":"",
						},
						{
							"name":"titlename_edit",
							"type":"editline",
							"x":0,
							"y":3+6,
							"width":120,
							"height":17,
							"text_vertical_align":"center",
							"r":1.0,
							"g":0.85,
							"b":0.65,
							"input_limit":chr.PLAYER_NAME_MAX_LEN,
							"text":"",
						},
					),
				},
				#DIGITANDO
				{
					"name":"yaziyor",
					"type":"text",
					"x":87-9,
					"y":10+3,
					"text":"",
				},
				#FINAL DIGITANDO
				{
					"name":"gamemastermark",
					"type":"expanded_image",
					"style":("attach",),
					"x":120,
					"y":10,
					"x_scale":0.2,
					"y_scale":0.2,
					"image":app.GetLocalePath() + "/effect/gm.png",
				},
				{
					"name":"negociarbutton",
					"type":"button",
					"x":width - 81,
					"y":13,
					"default_image":"interface/controls/common/board/exchange_normal.png",
					"over_image":"interface/controls/common/board/exchange_over.png",
					"down_image":"interface/controls/common/board/exchange_down.png",
				},
				{
					"name":"addbutton",
					"type":"button",
					"x":width - 63,
					"y":13,
					"default_image":"interface/controls/common/board/add_friend_normal.png",
					"over_image":"interface/controls/common/board/add_friend_over.png",
					"down_image":"interface/controls/common/board/add_friend_down.png",
				},
				{
					"name":"minimizebutton",
					"type":"button",
					"x":width - 45,
					"y":13,
					"default_image":"interface/controls/common/board/minimize_normal.tga",
					"over_image":"interface/controls/common/board/minimize_over.tga",
					"down_image":"interface/controls/common/board/minimize_down.tga",
				},
				{
					"name":"closebutton",
					"type":"button",
					"x":42,
					"y":2,
					"default_image":"interface/controls/common/board/close_normal.tga",
					"over_image":"interface/controls/common/board/close_over.tga",
					"down_image":"interface/controls/common/board/close_down.tga",
				},
				{
					"name":"scrollbar",
					"type":"new_thin_scrollbar",
					"x":width - 25,
					"y":35,
					"size":width - 165,
				},
				{
					"name":"editbar",
					"type":"expanded_image",
					"image":whisper + "fill.tga",
					"x":10,
					"y":60,
					"children":
					(
						{
							"name":"left_editbar",
							"type":"image",
							"image":whisper + "input_left.tga",
							"x":-5,
							"y":0,
							"x_scale":1,
							"y_scale":50,
						},
						{
							"name":"chatline",
							"type":"editline",
							"x":0,
							"y":5+6+2,
							"width":width - 70,
							"text_vertical_align":"center",
							"height":40,
							"x":0,
							"y":6,
							"r":1.0,
							"with_codepage":1,
							"input_limit":66,
							"limit_width":width - 90,
							"multi_line":1,
						},
					),
				},
				{
					"name":"sendbutton",
					"type":"button",
					"x":width - 80,
					"y":50,
					"text":uiscriptlocale.WHISPER_SEND,
					"default_image":whisper + "send_01_normal.tga",
					"over_image":whisper + "send_02_hover.tga",
					"down_image":whisper + "send_03_active.tga",
				},
			),
		},
	),
}
