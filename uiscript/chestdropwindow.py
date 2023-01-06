#favor manter essa linha
import _grp as grp

SLOT = "interface/controls/common/slot_rectangle/slot.tga"

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)

width = 510 -12
height = 257 -12

window = {
	"name":"ChestDropWindow",
	"x":0,
	"y":0,
	"style":("movable", "float",),
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"style":("attach",),
			"x":0,
			"y":0,
			"title": "Drops Possiveis",
			"width":width,
			"height":height,
			"children":
			(
				{ 
					"name":"SlotBG",
					"type":"expanded_image",
					"style":("attach",),
					"x":18,
					"y":204,
					"image":SLOT,
					"children":
					(
						{
							"name":"OpenItemSlot",
							"type":"slot",
							"x":0,
							"y":0,
							"horizontal_align":"center",
							"vertical_align":"center",
							"width":32,
							"height":32,
							"slot":(
								{"index":0, "x":0, "y":0, "width":32, "height":32,},
							),
						},
					),
				},
				{
					"name":"OpenCountController",
					"type":"slider",
					"width":120,
					"x":65,
					"y":213,
				},
				{
					"name":"prev_button", 
					"type":"button",
					"x":404,
					"y":height - 39,
					"default_image":"interface/controls/common/board/retract_normal.tga",
					"over_image":"interface/controls/common/board/retract_over.tga",
					"down_image":"interface/controls/common/board/retract_down.tga",
				},
				{
					"name":"CurrentPageBack",
					"type":"barwithbox",
					"x":430,
					"y":210,
					"color": 0xc0000000,
					"flash_color": 0xc00a0a0a,
					"box_color": 0xc00a0a0a,
					"width":30,
					"height":21,
					"children":
					(
						{
							"name":"CurrentPage",
							"type":"text",
							"x":0,
							"y":0,
							"vertical_align":"center",
							"horizontal_align":"center",
							"text_vertical_align":"center",
							"text_horizontal_align":"center",
							"text":"1",
						},
					),
				},
				{
					"name":"next_button", 
					"type":"button",
					"x":460, 
					"y":height - 39,
					"default_image":"interface/controls/common/board/expand_normal.tga",
					"over_image":"interface/controls/common/board/expand_over.tga",
					"down_image":"interface/controls/common/board/expand_down.tga",
				},
				{
					"name":"ItemSlot",
					"type":"grid_table",
					"x":8,
					"y":40,
					"start_index":0,
					"x_count":15,
					"y_count":5,
					"x_step":32,
					"y_step":32,
					"image":SLOT,
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 45,
				},
				{
					"name":"OpenChestButton",
					"type":"redbutton",
					"width": 110,
					"text":"Abrir",
					"x":290,
					"y":height - 39,
				},
			),
		},
	),
}

