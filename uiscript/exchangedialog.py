#favor manter essa linha
import uiscriptlocale
import localeinfo
CHARACTER = "interface/icons/faces/medium/" 
EXCHANGE = "interface/controls/special/exange/" 
SLOT = "interface/controls/common/slot_rectangle/slot.tga"
CHECKBOX = "interface/controls/common/checkbox/"
SLOTGOLD = EXCHANGE + "slot_gold.tga"
width = 490
height = 318
a = 5
b = 2
x_count = 7
y_count = 4

window = {
	"name":"ExchangeDialog",
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
			"title": uiscriptlocale.EXCHANGE_TITLE,
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":8,
					"y":height - 60,
				},
				{
					"name":"verticalseparator",
					"type":"verticalseparator",
					"x":0,
					"y":38,
					"horizontal_align":"center",
					"height":height-24-25-43-5,
				},
				{
					"name":"Owner",
					"type":"window",
					"x":width/2,
					"y":39,
					"width":width/2-10,
					"height":height-90,
					"children":
					(
						{
							"name":"Owner_Slot",
							"type":"grid_table",
							"start_index":0,
							"x":6,
							"y":0,
							"x_count":x_count,
							"y_count":y_count,
							"x_step":32,
							"y_step":32,
							"x_blank":0,
							"y_blank":0,
							"image":SLOT,
						},
						{
							"name":"Owner_Money",
							"type":"button",
							"x":6,
							"y":103+35,
							"default_image":SLOTGOLD,
							"over_image":SLOTGOLD,
							"down_image":SLOTGOLD,
							"children":
							(
								{
									"name":"Owner_Accept_Light",
									"type":"button",
									"x":207,
									"y":0,
									"vertical_align":"center",
									"default_image":CHECKBOX + "empty_01_normal.tga",
									"over_image": CHECKBOX + "empty_02_hover.tga",
									"down_image": CHECKBOX + "filled_01_normal.tga",
									"disable_image": CHECKBOX + "empty_01_normal.tga",
								},
								{
									"name":"Owner_Money_Value",
									"type":"text",
									"x":25,
									"y":3,
									"color":0xfff8d090,
									"text":"999.999.999 G",
									"text_horizontal_align":"right",
									"horizontal_align":"right",
								},
							),
						},
						{
							"name":"owner_face",
							"type":"button",
							"default_image":CHARACTER+ "icon_mwarrior.tga",
							"over_image":CHARACTER + "on/icon_mwarrior.tga",
							"down_image":CHARACTER + "on/icon_mwarrior.tga",
							"x": 135+41,
							"y": 138+25,
							"children":
							(
								{
									"name":"owner_tooltip",
									"type":"image",
									"style":("not_pick",),
									"image": EXCHANGE + "slot_data.tga",
									"x":-166,
									"y":0,
									"vertical_align":"center",
									"children":
									(
										{"name":"owner_name","type":"text","color":0xfff8d090,"text":"Nome: |cfff88f90Teste", "x":2, "y": 12*0+3,},
										{"name":"owner_lvl","type":"text","color":0xfff8d090,"text":"Level: |cfff88f90 99", "x":2, "y": 12*1+3,},
										{"name":"owner_guild","type":"text","color":0xfff8d090,"text":"Guild: |cfff88f90Teste", "x":2, "y": 12*2+3,},
									),
								},
							),
						},
					),
				},
				{
					"name":"Owner_Accept_Button",
					"type":"redbutton",
					"text":uiscriptlocale.EXCHANGE_ACCEPT,
					"x":width/4,
					"y":height - 47,
					"horizontal_align":"center",
					"width":100,
				},
				{
					"name":"Owner_Decline_Button",
					"type":"redbutton",
					"text":"Recusar",
					"x":-(width/4),
					"y":height - 47,
					"horizontal_align":"center",
					"width":100,
				},
				{
					"name":"Target",
					"type":"window",
					# "type":"thinboard",
					"x":10,
					"y":39,
					"width":width/2-10,
					"height":height-90,
					"children":
					(
						{
							"name":"Target_Slot",
							"type":"grid_table",
							"start_index":0,
							"x":6,
							"y":0,
							"x_count":x_count,
							"y_count":y_count,
							"x_step":32,
							"y_step":32,
							"x_blank":0,
							"y_blank":0,
							"image":SLOT,
						},
						{
							"name":"Target_Money",
							"type":"expanded_image",
							"x":6,
							"y":103+35,
							"image":SLOTGOLD,
							"children":
							(
								{
									"name":"Target_Accept_Light",
									"type":"button",
									"x":207,
									"y":0,
									"vertical_align":"center",
									"default_image":CHECKBOX + "empty_01_normal.tga",
									"over_image": CHECKBOX + "empty_02_hover.tga",
									"down_image": CHECKBOX + "filled_01_normal.tga",
									"disable_image": CHECKBOX + "empty_01_normal.tga",
								},
								{
									"name":"Target_Money_Value",
									"type":"text",
									"x":25,
									"y":3,
									"color":0xfff8d090,
									"text":"999.999 Gold",
									"text_horizontal_align":"right",
									"horizontal_align":"right",
								},
							),
						},
						{
							"name":"target_face",
							"type":"button",
							"default_image":CHARACTER+ "icon_wsura.tga",
							"over_image":CHARACTER + "on/icon_wsura.tga",
							"down_image":CHARACTER + "on/icon_wsura.tga",
							"x": 135+41,
							"y": 138+25,
							"children":
							(
								{
									"name":"target_tooltip",
									"type":"image",
									"style":("not_pick",),
									"image": EXCHANGE + "slot_data.tga",
									"x":-166,
									"y":0,
									"vertical_align":"center",
									"children":
									(
										{"name":"target_name","type":"text","color":0xfff8d090,"text":"Nome: |cfff88f90Teste", "x":2, "y": 13*0+3,},
										{"name":"target_lvl","type":"text","color":0xfff8d090,"text":"Level: |cfff88f9099", "x":2, "y": 13*1+3,},
										{"name":"target_guild","type":"text","color":0xfff8d090,"text":"Guild: |cfff88f90Guild", "x":2, "y": 13*2+3,},
									),
								},
							),
						},
					),
				},
			),
		},
	),
}