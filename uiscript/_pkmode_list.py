#favor manter essa linha
import uiscriptlocale
import _grp as grp

width = 180
height = 87

COLOR_OUT = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
COLOR_NONE = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)

window = {
	"name":"PopupDialog",
	"style":("float",),
	"x":SCREEN_WIDTH - 203,
	"y":SCREEN_HEIGHT - 30 - height,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"barwithbox",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"color": 0xc0000000,
			"box_color": COLOR_OUT,
			"children":
			(
				{
					"name":"button1",
					"type":"barwithbox",
					"x":2,
					"y":2,
					"width":width-4,
					"height":20,
					"flash_color": 0xc0000000,
					"color": 0xc00a0a0a,
					"box_color": COLOR_NONE,
					"children":
					(
						{
							"name":"text1", "type":"text",
							"color":0xffa07970,
							# "color":0xfff8d090,
							"text":"Modo Pacífico",
							"x":5, "y":-2,
							"vertical_align":"center",
							"text_vertical_align":"center",
							"fontsize":"LARGE",
							"style":("not_pick",),
						},
					),
				},
#####################################################################
				{
					"name":"button2",
					"type":"barwithbox",
					"x":2,
					"y":2+21,
					"width":width-4,
					"height":20,
					"flash_color": 0xc0000000,
					"color": 0xc00a0a0a,
					"box_color": COLOR_NONE,
					"children":
					(
						{
							"name":"text2", "type":"text",
							"color":0xffa07970,
							# "color":0xfff8d090,
							"text":"Modo Honra",
							"x":5, "y":-2,
							"vertical_align":"center",
							"text_vertical_align":"center",
							"fontsize":"LARGE",
							"style":("not_pick",),
						},
					),
				},
###############################################################
				{
					"name":"button3",
					"type":"barwithbox",
					"x":2,
					"y":2+21*2,
					"width":width-4,
					"height":20,
					"flash_color": 0xc0000000,
					"color": 0xc00a0a0a,
					"box_color": COLOR_NONE,
					"children":
					(
						{
							"name":"text3", "type":"text",
							"color":0xffa07970,
							# "color":0xfff8d090,
							"text":"Modo Guild",
							"x":5, "y":-2,
							"vertical_align":"center",
							"text_vertical_align":"center",
							"fontsize":"LARGE",
							"style":("not_pick",),
						},
					),
				},
######################################################################
				{
					"name":"button4",
					"type":"barwithbox",
					"x":2,
					"y":2+21*3,
					"width":width-4,
					"height":20,
					"flash_color": 0xc0000000,
					"color": 0xc00a0a0a,
					"box_color": COLOR_NONE,
					"children":
					(
						{
							"name":"text4", "type":"text",
							"color":0xffa07970,
							# "color":0xfff8d090,
							"text":"Modo Livre",
							"x":5, "y":-2,
							"vertical_align":"center",
							"text_vertical_align":"center",
							"fontsize":"LARGE",
							"style":("not_pick",),
						},
					),
				},
#################################################################
			),
		},
	),
}