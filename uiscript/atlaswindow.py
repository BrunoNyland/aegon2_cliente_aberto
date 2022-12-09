#favor manter essa linha
import uiscriptlocale

width = 350 -12
height = 380 -12

window = {
	"name":"AtlasWindow",
	"style":("movable", "float",),
	"x":0,
	"y":0,
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
			"title":uiscriptlocale.ZONE_MAP,
		},
	),
}
