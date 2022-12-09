#favor manter essa linha
import uiscriptlocale
import grp

width = 356
height = 303

x_count = 11
y_count = 8

out_color = grp.GenerateColor(0.078, 0.043, 0.039, 1.0)
win_color = grp.GenerateColor(0.02, 0.02, 0.02, 1.0)
pass_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
hover_color = grp.GenerateColor(0.1, 0.1, 0.1, 0.8)
hover_color2 = grp.GenerateColor(0.05, 0.05, 0.05, 1.0)
text_color = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
color_quest = grp.GenerateColor(0.0, 0.0, 0.0, 0.2)

input_color = normal_color
flash_color = hover_color

SLOT = "interface/controls/common/slot_rectangle/slot.tga"

recuo = 7

window = {
	"name":"SafeboxWindow",
	"x":0,
	"y":0,
	"style":("float",),
	"width":width,
	"height":height,
	"children":
	(
		{"name":"", "type":"horizontalseparator", "width":width+2, "x":-1, "y":200+32*2-recuo,},
		{
			"name":"Slots",
			"type":"grid_table",
			"start_index":0,
			"x":2,
			"y":0,
			"x_count":x_count,
			"y_count":y_count,
			"x_step":32,
			"y_step":32,
			"x_blank":0,
			"y_blank":0,
			"image":SLOT,
		},
#### TABs #### TABs #### TABs #### TABs #### TABs #### TABs #### TABs #### TABs #### TABs ####
		{
			"name":"Tab_01",
			"type":"redbutton",
			"width":26,
			"text":"I",
			"x":4,
			"y":267,
		},
		{
			"name":"Tab_02",
			"type":"redbutton",
			"width":26,
			"text":"II",
			"x":4+28*1,
			"y":267,
		},
#### GOLD #### GOLD #### GOLD #### GOLD #### GOLD #### GOLD #### GOLD #### GOLD #### GOLD ####
		{
			"name":"Money_Slot",
			"type":"barwithbox",
			"x":100, "y":268,
			"width":150+87,
			"height":25,
			"color": input_color,
			"flash_color":flash_color,
			"box_color": box_color,
			"children":
			(
				{
					"name":"Money",
					"type":"text",
					"x":5,
					"y":5,
					"color":0xffa07970,
					"horizontal_align":"right",
					"text_horizontal_align":"right",
					"text":"100.000.000 Gold",
					"style":("not_pick",),
				},
				{
					"name":"tipmoney",
					"type":"thinboardnew",
					"width":200,
					"height":44,
					"x":0,
					"y":-44,
					"horizontal_align":"center",
					"style":("not_pick",),
					"hide":1,
					"children":
					(
						{
							"name":"tipmoney_text",
							"type":"text",
							"x":14,
							"y":15,
							"color":0xFFF5CDB9,
							"text":"Apróx. 100x Anéis de 14 Quilates",
						},
					),
				},
			),
		},
		{
			"name":"MoneyInputBoard",
			"type":"new_board_with_titlebar",
			"title":"Banco da Guild",
			"width":300,
			"height":180,
			"x":0, "y":0,
			"horizontal_align":"center", "vertical_align":"center",
			"hide":1,
			"children":
			(
				{
					"name":"horizontal_separator",
					"type":"horizontalseparator",
					"width":300-24,
					"x":12,
					"y":180-60,
				},
				{
					"name":"MoneyInputButton",
					"type":"redbutton",
					"width":150,
					"text":"Efetuar Operação",
					"x":45,
					"y":180 - 47,
					"horizontal_align":"center",
				},
				{
					"name":"MoneyCancelButton",
					"type":"redbutton",
					"width":80,
					"text":"Cancelar",
					"x":-80,
					"y":180 - 47,
					"horizontal_align":"center",
				},
				{
					"name":"BarInputMoney",
					"type":"barwithbox",
					"x":0, "y":50,
					"width":150+87,
					"height":25,
					"color": input_color,
					"flash_color":flash_color,
					"box_color": box_color,
					"horizontal_align":"center",
					"children":
					(
						{
							"name":"LineInputMoney",
							"type":"editline",
							"x":5,
							"y":6,
							"width":200,
							"height":18,
							"input_limit":22,
							# "only_number":1,
							"money_mode":1,
							"color":0xfff8d090,
							"text":"",
							"style":("not_pick",),
						},
						{
							"name":"TextInputMoney",
							"type":"text",
							"x":5,
							"y":5,
							"color":0xffa07970,
							"text":"Insira aqui o valor desejado...",
							"style":("not_pick",),
						},
						{
							"name":"CopyPasteButton",
							"type":"button",
							"default_image":"interface/controls/special/bank/paste.tga",
							"over_image":"interface/controls/special/bank/paste_up.tga",
							"down_image":"interface/controls/special/bank/paste_down.tga",
							"x":25,
							"y":1,
							"horizontal_align":"right",
							"vertical_align":"center",
							"children":
							(
								{"name":"","type":"ballon","width":60,"text":"Copiar Valor","x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
							),
						},
					),
				},
				{
					"name":"Deposito",
					"type":"newradio_button",
					"x":-50,"y":85,
					"horizontal_align":"center",
					"children":
					(
						{"name":"","type":"text","color":0xffa08784,"text":"Depositar:","x":-5,"y":2,"text_horizontal_align":"right",},
					),
				},
				{
					"name":"Saque",
					"type":"newradio_button",
					"x":50,"y":85,
					"horizontal_align":"center",
					"children":
					(
						{"name":"","type":"text","color":0xffa08784,"text":"Retirar:","x":-5,"y":2,"text_horizontal_align":"right",},
					),
				},
			),
		},
	),
}