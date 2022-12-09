#favor manter essa linha
import XXjvumrgrYBZompk3PS8 as item

COSTUME_START_INDEX = item.COSTUME_SLOT_START

width = 129
height = 145

window = {
	"name":"CostumeWindow",
	"x":SCREEN_WIDTH - 175 - 140,
	"y":SCREEN_HEIGHT - 37 - 565,
	"style":("movable", "float",),
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board",
			"style":("attach",),
			"title":"Costumes",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"Costume_Base",
					"type":"image",
					"x":8,
					"y":8,
					"image":"interface/controls/special/inventory/costume_m.tga",
					"children":
					(
						{
							"name":"CostumeSlot",
							"type":"slot",
							"x":3,
							"y":3,
							"width":127,
							"height":145,
							"slot":
							(
								{"index":COSTUME_START_INDEX+0, "x":46, "y":40, "width":32, "height":64}, #Armadura
								{"index":COSTUME_START_INDEX+1, "x":46, "y":2, "width":32, "height":32},  #Cabelo
								{"index":COSTUME_START_INDEX+2, "x":7, "y":8, "width":32, "height":96},  #Arma
							),
						},
					),
				},

			),
		},
	),
}
