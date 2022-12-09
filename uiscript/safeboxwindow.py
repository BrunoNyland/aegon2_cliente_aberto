#favor manter essa linha
import uiscriptlocale

width = 176
height = 418

window = {
	"name":"SafeboxWindow",
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
			"title":uiscriptlocale.SAFE_TITLE,
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"ChangePasswordButton",
					"type":"redbutton",
					"x":13,
					"y":45,
					"width":90,
					"text":"Trocar Senha",
					"horizontal_align":"left",
					"vertical_align":"bottom",
					"children":
					(
						{
							"name":"horizontal_separator",
							"type":"horizontalseparator",
							"width":width - 14,
							"x":-6,
							"y":-10,
						},
						{
							"name":"top",
							"type":"horizontalseparator",
							"width":width - 14,
							"x":-6,
							"y":-46,
						},
					),
				},
				{
					"name":"ExitButton",
					"type":"redbutton",
					"x":65,
					"y":45,
					"width":50,
					"text":uiscriptlocale.CLOSE,
					"horizontal_align":"right",
					"vertical_align":"bottom",
				},
			),
		},
	),
}
