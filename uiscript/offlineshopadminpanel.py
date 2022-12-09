#favor manter essa linha
import uiscriptlocale

width = 200
height = 250
button_w = 170
button_x = 0
button_y = 46
y_step = 32

LINE = "interface/controls/common/horizontal_bar/center.tga"

window = {
	"name":"OfflineShopAdminPanelWindow",
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
			"title":"Loja Offline",
			"style":("attach",),
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"OpenOfflineShopButton",
					"type":"redbutton",
					"x":button_x,
					"y":button_y,
					"width":button_w,
					"text":"Abrir Loja",
					"horizontal_align":"center",
				},
				# Close Offline Shop
				{
					"name":"CloseOfflineShopButton",
					"type":"redbutton",
					"x":button_x,
					"y":button_y+y_step*1,
					"width":button_w,
					"text":"Fechar Loja",
					"horizontal_align":"center",
				},
				# Change Price
				{
					"name":"ChangePriceButton",
					"type":"redbutton",
					"x":button_x,
					"y":button_y+y_step*2,
					"width":button_w,
					"text":"Alterar Preço",
					"horizontal_align":"center",
				},
				# Remove Item
				{
					"name":"RemoveItemButton",
					"type":"redbutton",
					"x":button_x,
					"y":button_y+y_step*3,
					"width":button_w,
					"text":"Remover Item",
					"horizontal_align":"center",
				},
				# Add Item
				{
					"name":"AddItemButton",
					"type":"redbutton",
					"x":button_x,
					"y":button_y+y_step*4,
					"width":button_w,
					"text":"Adicionar Item",
					"horizontal_align":"center",
				},
				# My Bank
				{
					"name":"MyBankButton",
					"type":"redbutton",
					"x":button_x,
					"y":button_y+y_step*5,
					"width":button_w,
					"text":"Meu Banco",
					"horizontal_align":"center",
				},
			),
		},
	),
}