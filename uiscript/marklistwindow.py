#favor manter essa linha
import uiscriptlocale
height = 320
width  = 210

window = {
	"name":"MarkListWindow",
	"x":SCREEN_WIDTH - 170,
	"y":SCREEN_HEIGHT - 400 - 50,
	"style":("movable", "float",),
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":uiscriptlocale.MARKLIST_TITLE,
			"children":
			(
				{
					"name":"horizontal_separator",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 55,
				},
				{
					"name":"verticalseparator",
					"type":"verticalseparator",
					"x":width - 46,
					"y":38,
					"height":height-55-37,
				},
				{
					"name":"ScrollBar",
					"type":"new_scrollbar",
					"x":width - 35,
					"y":43,
					"size":220,
				},
				{
					"name":"ok",
					"type":"redbutton",
					"x":15,
					"y":height-45,
					"width":(width/3)-10,
					"text":uiscriptlocale.OK,
				},
				{
					"name":"cancel",
					"type":"redbutton",
					"x":0,
					"y":height-45,
					"horizontal_align":"center",
					"width":(width/3)-10,
					"text":uiscriptlocale.CANCEL,
				},
				{
					"name":"refresh",
					"type":"redbutton",
					"x":width - 15 - ((width/3)-10),
					"y":height-45,
					"width":(width/3)-10,
					"text":uiscriptlocale.MARKLIST_REFRESH,
				},
			),
		},
	)
}