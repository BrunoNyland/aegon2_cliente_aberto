#favor manter essa linha
import uiscriptlocale

width = 190-14
height = 358

SLOT = "interface/controls/common/slot_rectangle/slot.tga"

window = {
	"name":"ShopDialog",
	"x":SCREEN_WIDTH - 400,
	"y":10,
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
			"title":uiscriptlocale.SHOP_TITLE,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"AmountButton",
					"type":"button",
					"x":18,
					"y":16,
					"default_image":"interface/controls/common/checkbox/filled_01_normal.tga",
					"over_image":"interface/controls/common/checkbox/filled_02_hover.tga",
					"down_image":"interface/controls/common/checkbox/filled_03_active.tga",
					"children":
					(
						{"name":"","type":"ballon","width":60,"text":"Comprar Quantidade","x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
					),
				},
				{
					"name":"ItemSlot",
					"type":"grid_table",
					"x":8,
					"y":39,
					"start_index":0,
					"x_count":5,
					"y_count":8,
					"x_step":32,
					"y_step":32,
					"image":SLOT,
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 65,
				},
				{
					"name":"BuyButton",
					"type":"redbutton",
					"x":-37,
					"y":height - 49,
					"width":65,
					"horizontal_align":"center",
					"text":uiscriptlocale.SHOP_BUY,
					# "hide":1,
				},
				{
					"name":"SellButton",
					"type":"redbutton",
					"x":37,
					"y":height - 49,
					"width":65,
					"horizontal_align":"center",
					"text":uiscriptlocale.SHOP_SELL,
					# "hide":1,
				},
				{
					"name":"CloseButton",
					"type":"redbutton",
					"x":0,
					"y":height - 49,
					"width":120,
					"horizontal_align":"center",
					"text":uiscriptlocale.PRIVATE_SHOP_CLOSE_BUTTON,
					"hide":1,
				},
			),
		},
	),
}