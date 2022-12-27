#favor manter essa linha
import uiscriptlocale

width = 260
height = 150

import grp
box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)

window = {
	"name":"RentTime",
	"x":SCREEN_WIDTH/2 - width/2,
	"y":SCREEN_HEIGHT/2 - height,
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
			"title":"Defina o tempo do empréstimo",
			"children":
			(
				# {
					# "name":"DropDown",
					# "type": "dropdown",
					# "x": 0, "y": 55,
					# "width":160, "height":28,
					# "horizontal_align": "center",
					# "text":"",
					# "itens":
					# (
						# {"text":"15 Minutos","value":1},
						# {"text":"30 Minutos","value":2},
						# {"text":"1 Hora","value":3},
						# {"text":"2 Horas","value":4},
						# {"text":"3 Horas","value":5},
						# {"text":"6 Horas","value":6},
						# {"text":"12 Horas","value":7},
						# {"text":"24 Horas","value":8},
						# {"text":"2 Dias","value":9},
						# {"text":"7 Dias","value":10},
						# {"text":"15 Dias","value":11},
					# ),
				# },
				{
					"name":"Slider",
					"type":"slider",
					"width":160,
					"x":0,
					"y":55,
					"horizontal_align":"center",
				},
				{
					"name":"Slider_title",
					"type":"text",
					"text":"5 minutos",
					"x":0,
					"y":55 - 13,
					"text_horizontal_align":"center",
					"horizontal_align":"center",
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 60,
				},
				{
					"name":"accept_button",
					"type":"redbutton",
					"x":(width/5),
					"y":height - 47,
					"horizontal_align":"center",
					"width":75,
					"text":"Aceitar",
				},
				{
					"name":"cancel_button",
					"type":"redbutton",
					"x":-(width/5),
					"y":height - 47,
					"horizontal_align":"center",
					"width":75,
					"text":"Cancelar",
				},
			),
		},
	),
}