#favor manter essa linha
import uiscriptlocale
import grp

box_color = grp.GenerateColor(0.208, 0.142, 0.126, 1.0)
win_color = grp.GenerateColor(0.02, 0.02, 0.02, 1.0)
pass_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
input_color = 0xc0000000
flash_color = 0xc00a0a0a

width = 356
height = 303

window = {
	"name":"GuildWindow_Safebox",
	"x":8,
	"y":39,
	"width":width,
	"height":height,
	"children":
	(
######### PASSWORD ######### PASSWORD ######### PASSWORD ######### PASSWORD ######### PASSWORD #########
		{
			"name":"password_board",
			"type":"barwithbox",
			"horizontal_align":"center",
			"x":0, "y":15,
			"width":width - width/4,
			"height":100,
			"color": win_color,
			"box_color": pass_color,
			"hide":1,
			"children":
			(
				{
					"name":"text1", "type":"text",
					"color":0xffa07970,
					"text":"Digite a senha para abrir o Baú de Guild:",
					"x":0, "y":12,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"fontsize":"LARGE",
					"style":("not_pick",),
				},
				{
					"name":"box_password",
					"type":"barwithbox",
					"horizontal_align":"center",
					"x":0, "y":40,
					"width":97,
					"height":40,
					"color": input_color,
					"flash_color":flash_color,
					"box_color": box_color,
					"children":
					(
						{
							"name":"input_password", "type":"editline",
							"input_limit":6,
							"color":box_color,
							"x":15, "y":4,
							"width":97,
							"height":40,
							"fontname":"Verdana:32",
							"style":("not_pick",),
						},
						{
							"name":"loading",
							"type":"ani_image",
							"x":97 + 10,
							"y":5,
							"delay":3,
							"images":
							(
								"interface/controls/special/boot/ani_big/01.tga",
								"interface/controls/special/boot/ani_big/02.tga",
								"interface/controls/special/boot/ani_big/03.tga",
								"interface/controls/special/boot/ani_big/04.tga",
								"interface/controls/special/boot/ani_big/05.tga",
								"interface/controls/special/boot/ani_big/06.tga",
								"interface/controls/special/boot/ani_big/07.tga",
								"interface/controls/special/boot/ani_big/08.tga",
								"interface/controls/special/boot/ani_big/09.tga",
								"interface/controls/special/boot/ani_big/10.tga",
								"interface/controls/special/boot/ani_big/11.tga",
								"interface/controls/special/boot/ani_big/12.tga",
								"interface/controls/special/boot/ani_big/13.tga",
								"interface/controls/special/boot/ani_big/14.tga",
								"interface/controls/special/boot/ani_big/15.tga",
								"interface/controls/special/boot/ani_big/16.tga",
								"interface/controls/special/boot/ani_big/17.tga",
								"interface/controls/special/boot/ani_big/18.tga",
								"interface/controls/special/boot/ani_big/19.tga",
								"interface/controls/special/boot/ani_big/20.tga",
								"interface/controls/special/boot/ani_big/21.tga",
								"interface/controls/special/boot/ani_big/22.tga",
								"interface/controls/special/boot/ani_big/23.tga",
								"interface/controls/special/boot/ani_big/24.tga",
								"interface/controls/special/boot/ani_big/25.tga",
								"interface/controls/special/boot/ani_big/26.tga",
								"interface/controls/special/boot/ani_big/27.tga",
								"interface/controls/special/boot/ani_big/28.tga",
								"interface/controls/special/boot/ani_big/29.tga",
								"interface/controls/special/boot/ani_big/30.tga",
								"interface/controls/special/boot/ani_big/31.tga",
								"interface/controls/special/boot/ani_big/32.tga",
							),
						},
					),
				},
			),
		},
######## NEW PASSWORD ######## NEW PASSWORD ######## NEW PASSWORD ######## NEW PASSWORD ######## NEW PASSWORD ########
		{
			"new_password_board"
			"type":"window",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"hide":1,
			"children":
			(
				{
					"name":"",
					"type":"barwithbox",
					"horizontal_align":"center",
					"x":0, "y":15,
					"width":width - width/4,
					"height":190,
					"color": win_color,
					"box_color": pass_color,
					"children":
					(
						{
							"name":"new_password_text", "type":"text",
							"color":0xffa07970,
							"text":"Digite a nova senha com 6 dígitos:",
							"x":0, "y":12,
							"horizontal_align":"center",
							"text_horizontal_align":"center",
							"fontsize":"LARGE",
							"style":("not_pick",),
						},
						{
							"name":"box_new_password",
							"type":"barwithbox",
							"horizontal_align":"center",
							"x":0, "y":40,
							"width":97,
							"height":40,
							"color": input_color,
							"flash_color":flash_color,
							"box_color": box_color,
							"children":
							(
								{
									"name":"input_new_password", "type":"editline",
									"input_limit":6,
									"color":box_color,
									"x":15, "y":4,
									"width":97,
									"height":40,
									"fontname":"Verdana:32",
									"style":("not_pick",),
								},
							),
						},
						{
							"name":"box_repeat_password",
							"type":"barwithbox",
							"horizontal_align":"center",
							"x":0, "y":90,
							"width":97,
							"height":40,
							"color": input_color,
							"flash_color":flash_color,
							"box_color": box_color,
							"children":
							(
								{
									"name":"input_repeat_password", "type":"editline",
									"input_limit":6,
									"color":box_color,
									"x":15, "y":4,
									"width":97,
									"height":40,
									"fontname":"Verdana:32",
									"style":("not_pick",),
								},
							),
						},
					),
				},
				{
					"name":"change_password_button",
					"type":"redbutton",
					"width":90,
					"x":-55,
					"y":170,
					"horizontal_align":"center",
					"text":"Trocar Senha",
				},
				{
					"name":"cancel_new_password_button",
					"type":"redbutton",
					"width":90,
					"x":55,
					"y":170,
					"horizontal_align":"center",
					"text":"Cancelar",
				},
			),
		},
	),
}
