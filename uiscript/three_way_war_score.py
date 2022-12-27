#favor manter essa linha
import uiscriptlocale

width = 150
height = 210

window = {
	"name":"ThreeWayWarScore",
	"x":SCREEN_WIDTH - width - 3,
	"y":150,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"thinboard",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"Titulo",
					"type":"text",
					"text":"Encruzilhada",
					"x":0,
					"y":10,
					"fontsize":"LARGE","horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"Rodada",
					"type":"text",
					"text":"Primeira Rodada",
					"x":0,
					"y":34,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"Monstros",
					"type":"text",
					"text":"Monstros 0 / 10",
					"x":0,
					"y":58,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"EmpireImage1",
					"type":"image",
					"x":30,
					"y":58,
					"horizontal_align":"left",
					# "vertical_align":"center",
					"image":"D:/ymir work/ui/1.tga",
					"children":
					(
						{
							"name":"Empire1",
							"type":"text",
							"text":"0 / 100",
							"x":-70,
							"y":-1,
							"horizontal_align":"right",
							# "vertical_align":"center",
							"text_horizontal_align":"right",
						},
					),
				},
				{
					"name":"EmpireImage2",
					"type":"image",
					"x":30,
					"y":80,
					"horizontal_align":"left",
					# "vertical_align":"center",
					"image":"D:/ymir work/ui/2.tga",
					"children":
					(
						{
							"name":"Empire2",
							"type":"text",
							"text":"0 / 100",
							"x":-70,
							"y":-1,
							"horizontal_align":"right",
							# "vertical_align":"center",
							"text_horizontal_align":"right",
						},
					),
				},
				{
					"name":"EmpireImage3",
					"type":"image",
					"x":30,
					"y":102,
					"horizontal_align":"left",
					# "vertical_align":"center",
					"image":"D:/ymir work/ui/3.tga",
					"children":
					(
						{
							"name":"Empire3",
							"type":"text",
							"text":"0 / 100",
							"x":-70,
							"y":-1,
							"horizontal_align":"right",
							# "vertical_align":"center",
							"text_horizontal_align":"right",
						},
					),
				},
				{
					"name":"Dead",
					"type":"text",
					"text":"Você morreu 0 / 10",
					"x":0,
					"y":128,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"Tempo",
					"type":"text",
					"text":"Restam: 00 min e 00 sec",
					"x":0,
					"y":150,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
				},
				{
					"name":"Button",
					"type":"redbutton",
					"width":90,
					"x":0,
					"y":170,
					"horizontal_align":"center",
					"text":"Sair",
				},
			),
		},
	),
}
