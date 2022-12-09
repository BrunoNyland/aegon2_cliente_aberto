#favor manter essa linha
import uiscriptlocale

width = 176
height = 418-36

window = {
	"name":"MallWindow",
	"x":100,
	"y":20,
	"style":("movable", "float",),
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"title":"Retirada de Item",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"ExitButton",
					"type":"redbutton",
					"text":"Fechar",
					"x":0,
					"y":45,
					"width":90,
					"height":0,
					"horizontal_align":"center",
					"vertical_align":"bottom",
				},
				{
					"name":"horizontal_separator",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":13-6,
					"y":55,
					"vertical_align":"bottom",
				},
			),
		},
	),
}
