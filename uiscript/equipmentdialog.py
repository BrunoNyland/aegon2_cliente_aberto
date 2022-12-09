#favor manter essa linha
width = 172
height = 235

window = {
	"name":"EquipmentDialog",
	"style":("movable", "float",),
	"x":0,
	"y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":"Character Name",
			"children":
			(
				{
					"name":"EquipmentBaseImage",
					"type":"image",
					"style":("attach",),
					"x":8,
					"y":39,
					"image":"interface/controls/special/inventory/inventory_m.tga",
					"children":
					(
						{
							"name":"EquipmentSlot",
							"type":"slot",
							"x":0,
							"y":0,
							"width":150,
							"height":182,
							"slot":
							(
								{"index":0, "x":42, "y":40, "width":32, "height":64},  #ARMADURA
								{"index":1, "x":42, "y":4, "width":32, "height":32},   #ELMO
								{"index":2, "x":42, "y":150, "width":32, "height":32}, #BOTA
								{"index":3, "x":80, "y":74, "width":32, "height":32},  #BRACELETE
								{"index":4, "x":3, "y":3, "width":32, "height":96},    #ARMA
								{"index":5, "x":117, "y":74, "width":32, "height":32}, #COLAR
								{"index":6, "x":117, "y":42, "width":32, "height":32}, #BRINCO
								{"index":7, "x":117, "y":112, "width":32, "height":32},#SUPORT 1
								{"index":8, "x":117, "y":150, "width":32, "height":32},#SUPORT 2
								{"index":9, "x":117, "y":3, "width":32, "height":32},  #FLECHA
								{"index":10, "x":80, "y":42, "width":32, "height":32}, #ESCUDO,
								{"index":15, "x":82, "y":102, "width":32, "height":32},#CINTO,
							),
						},
					),
				},
			),
		},
	),
}