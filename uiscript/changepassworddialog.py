#favor manter essa linha
import uiscriptlocale
width = 220 -12
height = 188+65

window = {
	"name":"ChangePasswordDialog",
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
			"title":uiscriptlocale.CHANGE_PASSWORD_TITLE,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"old_password_value",
					"type":"editboard",
					"x":0,
					"y":55,
					"width":130,
					"input_limit":6,
					"secret_flag":1,
					"info":"Senha Atual...",
					"horizontal_align":"center",
				},
				{
					"name":"new_password_value",
					"type":"editboard",
					"x":0,
					"y":55+45,
					"width":130,
					"input_limit":6,
					"secret_flag":1,
					"info":"Nova Senha...",
					"horizontal_align":"center",
				},
				{
					"name":"new_password_check_value",
					"type":"editboard",
					"x":0,
					"y":55+45*2,
					"width":130,
					"input_limit":6,
					"secret_flag":1,
					"info":"Repita a nova senha...",
					"horizontal_align":"center",
				},
				{
					"name":"horizontal_separator",
					"type":"horizontalseparator",
					"width":width-14,
					"x":7,
					"y":height - 65,
				},
				{
					"name":"accept_button",
					"type":"redbutton",
					"width":81,
					"x":- 61 - 5 + 30-10,
					"y":height-48,
					"horizontal_align":"center",
					"text":"Alterar",
				},
				{
					"name":"cancel_button",
					"type":"redbutton",
					"width":81,
					"x":5 + 30+10,
					"y":height-48,
					"horizontal_align":"center",
					"text":"Cancelar",
				},
			),
		},
	),
}