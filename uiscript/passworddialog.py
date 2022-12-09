#favor manter essa linha
import uiscriptlocale
CHARACTER = "interface/controls/special/character/"

width = 230
height = 190

window = {
	"name":"PasswordDialog",
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
			"title":uiscriptlocale.PASSWORD_TITLE,
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"horizontal_separator",
					"type":"horizontalseparator",
					"width":width-14,
					"x":7,
					"y":height - 60,
				},
				{
					"name":"text_senha",
					"type":"text",
					"text":"Caso você ainda não tenha alterado",
					"x":23,
					"y":95,
				},
				{
					"name":"text_senha2",
					"type":"text",
					"text":"sua senha, a senha padrão é 000000.",
					"x":20,
					"y":110,
				},
				{
					"name":"password_value",
					"type":"editboard",
					"width":90, "height":28,
					"x":0,
					"y":55,
					"horizontal_align":"center",
					"input_limit":6,
					"secret_flag":1,
					"info":"Digite a senha",
				},
				{
					"name":"accept_button",
					"type":"redbutton",
					"width":80,
					"x":width/2 - 80 - 10,
					"y":height-47,
					"text":uiscriptlocale.OK,
				},
				{
					"name":"cancel_button",
					"type":"redbutton",
					"width":80,
					"x":width/2 + 10,
					"y":height-47,
					"text":uiscriptlocale.CANCEL,
				},
			),
		},
	),
}
