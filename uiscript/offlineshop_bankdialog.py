#favor manter essa linha
import uiscriptlocale
import enszxc3467hc3kokdueq as app

width = 250
height = 210

LINE = "interface/controls/common/horizontal_bar/center.tga"

import grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"OfflineShopBankWindow",
	"style":("movable", "float", ),
	"x":0,
	"y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Board",
			"type":"new_board_with_titlebar",
			"style":("attach",),
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":"Banco da Loja Offline",
			"children":
			(
				{
					"name":"",
					"type":"expanded_image",
					"image":LINE,
					"x":0,
					"y":40,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"",
							"type":"text",
							"text":"Saldo Disponível",
							"x":0,
							"y":-5,
							"all_align":"center",
						},
					),
				},
				{
					"name":"saldo_slot",
					"type": "barwithbox",
					"width":198, "height":27,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"x":0,
					"y":65,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"GoldAtualLine",
							"type":"text",
							"x":10,
							"y":6,
							"horizontal_align":"right",
							"text_horizontal_align":"right",
							"text":"0 Gold",
						},
					),
				},
				{
					"name":"",
					"type":"expanded_image",
					"image":LINE,
					"x":0,
					"y":90,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"",
							"type":"text",
							"text":"Digite o Valor para Resgate",
							"x":0,
							"y":-5,
							"all_align":"center",
						},
					),
				},
				{
					"name":"money_slot",
					"x":0,
					"y":115,
					"type": "barwithbox",
					"width":198, "height":27,
					"color": normal_color,
					"flash_color": normal_color,
					"box_color": box_color,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"SacarGoldLine",
							"type":"editline",
							"x":5,
							"y":6,
							"width":200,
							"height":18,
							"input_limit":18,
							"only_number":1,
							"color":0xfff8d090,
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
								{"name":"","type":"ballon","width":60,"text":"Copiar","x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
							),
						},
					),
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 60,
				},
				{
					"name":"acept_button",
					"type":"redbutton",
					"x":-50,
					"y":height - 47,
					"horizontal_align":"center",
					"width":90,
					"text":"Retirar",
				},
				{
					"name":"cancel_button",
					"type":"redbutton",
					"x":50,
					"y":height - 47,
					"horizontal_align":"center",
					"width":90,
					"text":"Cancelar",
				},
			),
		},
	),
}