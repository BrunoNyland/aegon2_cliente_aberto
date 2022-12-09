#favor manter essa linha
import uiscriptlocale
width = 230
height = 200

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
			"name":"Board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":"Desafiar Guild Inimiga",
			"children":
			(
				{
					"name":"InputValue",
					"type": "editboard",
					"x": 0, "y": 60,
					"width":160, "height":28,
					"horizontal_align": "center",
					"text":"",
					"children":
					(
						{
							"name":"InputName",
							"type":"text",
							"text":"Equipe Inimiga",
							"x":0, "y":-15,
							"color":0xffa08784,
							"horizontal_align":"center",
							"text_horizontal_align":"center",
						},
					),
				},
				{
					"name":"DropDown",
					"type": "dropdown",
					"x": 0, "y": 110,
					"width":160, "height":28,
					"horizontal_align": "center",
					"text":"",
					"children":
					(
						{
							"name":"",
							"type":"text",
							"text":"Tipo de Batalha",
							"x":0, "y":-15,
							"color":0xffa08784,
							"horizontal_align":"center",
							"text_horizontal_align":"center",
						},
					),
					# "itens":
					# (
						# {"text":uiscriptlocale.GUILD_WAR_NORMAL,"value":0},
						# {"text":uiscriptlocale.GUILD_WAR_WARP,"value":1},
						# {"text":uiscriptlocale.GUILD_WAR_CTF,"value":2},
					# ),
				},
				{
					"name":"AcceptButton",
					"type":"redbutton",
					"width":90,
					"x":- 61 - 5 + 30-15,
					"y":height-50,
					"horizontal_align":"center",
					"text":"Desafiar",
				},
				{
					"name":"CancelButton",
					"type":"redbutton",
					"width":90,
					"x":5 + 30+15,
					"y":height-50,
					"horizontal_align":"center",
					"text":"Cancelar",
				},
			),
		},
	),
}
