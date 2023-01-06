#favor manter essa linha
import uiscriptlocale
import _grp as grp

width = 400 -12
height = 150 -12
box_color = grp.GenerateColor(0.208, 0.142, 0.126, 1.0)

window = {
	"name":"AntiRoboticsWindows",
	"x":SCREEN_WIDTH/2 - width/2,
	"y":SCREEN_HEIGHT/2 - height,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board",
			"style":("attach",),
			"width": width, "height": height,
			"x":0, "y":0,
			"children":
			(
				{
					"name":"text1", "type":"text",
					"color":0xffa07970,
					"text":"Digite os números abaixo para continuar jogando",
					"x":0, "y":23,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"fontsize":"LARGE",
					"style":("not_pick",),
				},
				{
					"name":"horizontal_separator",
					"type":"horizontalseparator",
					"width":width-14,
					"x":7,
					"y":50,
					"style":("not_pick",),
				},
				{
					"name":"number_box",
					"type":"barwithbox",
					"horizontal_align":"center",
					"x":-70, "y":68,
					"width":120,
					"height":60,
					"color": 0xc0000000,
					"flash_color": 0xc00a0a0a,
					"box_color": box_color,
					"children":
					(
						{
							"name":"numbers", "type":"text",
							"color":box_color,
							"text":"1324",
							"x":0, "y":5,
							"fontname":"Verdana:46",
							"horizontal_align":"center",
							"text_horizontal_align":"center",
							"style":("not_pick",),
						},
					),
				},
				{
					"name":"edit_box",
					"type":"barwithbox",
					"horizontal_align":"center",
					"x":70, "y":68,
					"width":120,
					"height":60,
					"color": 0xc0000000,
					"flash_color": 0xc00a0a0a,
					"box_color": box_color,
					"children":
					(
						{
							"name":"input", "type":"editline",
							"input_limit":4,
							"color":box_color,
							"x":10, "y":7,
							"width":120,
							"height":0,
							"only_number":1,
							"fontname":"Verdana:46",
							# "vertical_align":"center",
							# "text_vertical_align":"center",
							"style":("not_pick",),
						},
					),
				},
			),
		},
	),
}