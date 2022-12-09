#favor manter essa linha
import uiscriptlocale

width = 240
height = 180

refine = "interface/controls/special/refine/"

import grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"InputDialog",
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
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":"Insira o Valor",
			"children":
			(
				{
					"name":"InputSlot",
					"type": "barwithbox",
					"width":198, "height":22,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":42,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"InputValue",
							"type":"editline",
							"x":1,
							"y":8,
							"width":200,
							"height":18,
							"input_limit":20,
							# "only_number":1,
							"money_mode":1,
							"text":"",
							"vertical_align":"center",
							"text_vertical_align":"center",
						},
						{
							"name":"CopyPasteButton",
							"type":"button",
							"default_image":"interface/controls/special/bank/paste.tga",
							"over_image":"interface/controls/special/bank/paste_up.tga",
							"down_image":"interface/controls/special/bank/paste_down.tga",
							"x":176,
							"y":1,
							"vertical_align":"center",
							"children":
							(
								{"name":"","type":"ballon","width":60,"text":"Copiar Preço Médio","x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
							),
						},
					),
				},
				{
					"name":"InputSlotButton",
					"type": "barwithbox",
					"width":198, "height":22,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":42,
					"horizontal_align":"center",
					"x":0,
					"y":42,
					"hide":1,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"MoneyValue",
							"type":"text",
							"style":("not_pick",),
							"horizontal_align":"right",
							"text_horizontal_align":"right",
							"x":5,
							"y":5,
							"width":200,
							"height":18,
							"text":"999.999.999.999 Gold",
						},
					)
				},
				{
					"name":"",
					"type":"thinboardnew",
					"x":0,
					"y":60,
					"width":width-30,
					"height":height-110,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"ItemSlot",
							"type":"image",
							"image":refine+"slot.tga",
							"x":0,"y":0,
							"vertical_align":"center",
							"children":
							(
								{"name": "ItemIcon","type": "expanded_image","x":0,"y":0,"image":"icon/item/00140.tga","y_scale":0.5,"x_scale":0.5,"horizontal_align":"center","vertical_align":"center",},
							),
						},
						{
							"name":"NameItem",
							"type":"text",
							"style":("not_pick",),
							"x":50,
							"y":12,
							"color":0xfff98784,
							"text":"Espada Teste+9",
							"text_limited":140,
						},
						{
							"name":"",
							"type":"text",
							"style":("not_pick",),
							"x":50,
							"y":5+12*2,
							"color":0xffa08784,
							"text":"Preço Médio de Venda:",
							"text_limited":140,
						},
						{
							"name":"AveragePrice",
							"type":"text",
							"style":("not_pick",),
							"x":50,
							"y":5+12*3,
							"color":0xfff8d090,
							"text":"Carregando Informações...",
							"text_limited":140,
						},
					),
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 55,
				},
				{
					"name":"AcceptButton",
					"type":"redbutton",
					"width": 90,
					"x":-50,
					"y":height-45,
					"horizontal_align":"center",
					"text":uiscriptlocale.OK,
				},
				{
					"name":"CancelButton",
					"type":"redbutton",
					"width": 90,
					"x":50,
					"y":height-45,
					"horizontal_align":"center",
					"text":uiscriptlocale.CANCEL,
				},
			),
		},
	),
}