#favor manter essa linha

import colorinfo

box_color = colorinfo.COR_INPUT_BOX

WIDTH = 176
HEIGHT = 581
EQUIPMENT_START_INDEX = 200

SLOT = "interface/controls/common/slot_rectangle/slot.tga"
EQUIP = "interface/controls/special/inventory/inventory_m.tga"
INVENTORY = "interface/controls/special/inventory/"
BOARD = "interface/controls/common/board/"

TABx = 151-117
TABy = 240 - 5
TABd = 30

window = {
	"name":"InventoryWindow",
	"x":SCREEN_WIDTH - WIDTH,
	"y":(SCREEN_HEIGHT - HEIGHT)/2,
	"style":("movable", "float",),
	"width":WIDTH,
	"height":HEIGHT,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"style":("attach",),
			"title":"Inventário",
			"x":0,
			"y":0,
			"width":WIDTH,
			"height":HEIGHT,
			"children":
			(
				{
					"name":"costume_button_hide",
					"type":"button",
					"x": 6,
					"y": 8,
					"default_image":BOARD+"expand_normal.tga",
					"over_image":BOARD+"expand_over.tga",
					"down_image":BOARD+"expand_down.tga",
					"hide":1,
				},
				{
					"name":"costume_button",
					"type":"button",
					"x": 6,
					"y": 8,
					"default_image":BOARD+"retract_normal.tga",
					"over_image":BOARD+"retract_over.tga",
					"down_image":BOARD+"retract_down.tga",
				},
				{
					"name":"Equipment_Base",
					"type":"expanded_image",
					"style":("movable","float","attach",),
					"x":0,
					"y":39,
					"horizontal_align":"center",
					"image":EQUIP,
					"children":
					(
						{
							"name":"EquipmentSlot",
							"type":"slot",
							"x":3,
							"y":3,
							"width":150,
							"height":182,
							"slot":
							(
								{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":38, "width":32, "height":64},			#ARMADURA
								{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":1, "width":32, "height":32},			#ELMO
								{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":147, "width":32, "height":32},		#BOTA
								{"index":EQUIPMENT_START_INDEX+3, "x":77, "y":71, "width":32, "height":32},			#BRACELETE
								{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":0, "width":32, "height":96},			#ARMA
								{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":71, "width":32, "height":32},		#COLAR
								{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":39, "width":32, "height":32},		#BRINCO
								{"index":EQUIPMENT_START_INDEX+7, "x":114, "y":109, "width":32, "height":32},		#SUPORT 1
								{"index":EQUIPMENT_START_INDEX+8, "x":114, "y":147, "width":32, "height":32},		#SUPORT 2
								{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":0, "width":32, "height":32},			#FLECHA
								{"index":EQUIPMENT_START_INDEX+10, "x":77, "y":39, "width":32, "height":32},		#ESCUDO
								{"index":EQUIPMENT_START_INDEX+14, "x":77, "y":103, "width":32, "height":32},		#CINTO
								{"index":EQUIPMENT_START_INDEX+15, "x":77, "y":0, "width":32, "height":32},			#PET
							),
						},
					),
				},
				{"name":"","type":"horizontalseparator","width":WIDTH-14,"x":7,"y":227,},
				{
					"name":"ItemSlot",
					"type":"grid_table",
					"x":8,
					"y":230,
					"start_index":0,
					"x_count":5,
					"y_count":10,
					"x_step":32,
					"y_step":32,
					"image":SLOT,
				},
				{"name":"","type":"horizontalseparator","width":WIDTH-14,"x":7,"y":HEIGHT - 38 -5 +12,},
				{
					"name":"Money_Slot",
					"type":"barwithbox",
					"x": 0,
					"y": HEIGHT - 38 + 12,
					"color": box_color,
					"flash_color": box_color,
					"box_color": box_color,
					"width":156,
					"height":28-12,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"Money",
							"type":"text",
							"style":("not_pick",),
							"x":5,
							"y":-1,
							"vertical_align":"center",
							"text_vertical_align":"center",
							"horizontal_align":"right",
							"text_horizontal_align":"right",
							"text":"999.999.999.999 G",
						},
					),
				},
			),
		},
	),
}