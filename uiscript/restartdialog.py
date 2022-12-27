#favor manter essa linha
import uiscriptlocale

width = 200
height = 140

window = {
	"name":"RestartDialog",
	"style":("float",),
	"x":SCREEN_WIDTH/2 - width/2,
	"y":100,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"restart_here_button",
					"type":"redbutton",
					"width":150,
					"x":0,
					"y":20,
					"horizontal_align":"center",
					"text":uiscriptlocale.RESTART_HERE,
				},
				{
					"name":"restart_town_button",
					"type":"redbutton",
					"width":150,
					"x":0,
					"y":20+35,
					"horizontal_align":"center",
					"text":uiscriptlocale.RESTART_TOWN,
				},
				{
					"name":"restart_town_desc",
					"type":"text",
					"text":"Retorno automático em",
					"fontsize":"LARGE",
					"x":0,
					"y":20+35+30,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"restart_town_desc2",
					"type":"text",
					"text":"",
					"color":0xffa07970,
					"fontsize":"LARGE",
					"x":0,
					"y":20+35+35+14,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
			),
		},
	),
}
