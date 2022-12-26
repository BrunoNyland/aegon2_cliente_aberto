#favor manter essa linha
LINE = "interface/controls/common/horizontal_bar/center.tga"

interface = "interface/controls/special/create/"

x = 30
X_GAP = 11
Y_GAP = 12

STAT_GAUGE_X = 260
STAT_GAUGE_Y = -150
STAT_GAUGE_BAR_X = 40
STAT_GAUGE_BAR_WIDTH = 105
STAT_GAUGE_GAP = 18
STAT_GAUGE_TEXT_WIDTH = 21
STAT_GAUGE_TEXT_HEIGHT = 13

pos = 30
space = 58

window = {
	"name":"CreateCharacterWindow",
	"x":0, "y":0,
	"width":SCREEN_WIDTH,	"height":SCREEN_HEIGHT,
	"children":(
		{
			"name":"BackGround",
			"type":"expanded_image",
			"x":0, "y":0,
			"x_scale":float(SCREEN_WIDTH) / 1366.0,
			"y_scale":float(SCREEN_HEIGHT) / 768.0,
			"image":"interface/controls/special/login/background.tga",
			"children":
			(
				{
					"name":"board_main",
					"type":"thinboard",
					"x":20, "y":50,
					"y":SCREEN_HEIGHT - 400 -20,
					"width":250,
					"height":400,
					"children":
					(
### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE### FACE
						{
							"name":"boardface",
							"type":"image",
							"image": interface + "character_slot.tga",
							"x": 0,
							"y": -30,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"ImgChar",
									"type":"expanded_image",
									"x":0, "y":-6,
									"image":"interface/icons/faces/warrior_w.tga",
									"vertical_align":"center",
									"horizontal_align":"center",
								},
							),
						},
### NOME DO CHAR ###### NOME DO CHAR ###### NOME DO CHAR ###### NOME DO CHAR ###### NOME DO CHAR ###### NOME DO CHAR ###
						{
							"name"		: 	"Char_line",
							"type"		:	"image",
							"image"		:	LINE,
							"x":0, "y":20+x,
							"horizontal_align":"center",
							"children":
							(
								{
									"name" 	: 	"Char_Title",
									"type"	:	"text",
									"text"	:	"|cfff8d090Digite o Nome",
									"x"		:	0,
									"y"		:	-5,
									"all_align":"center",
								},
							),
						},
						{
							"name":"name_slotbar",
							"type":"image",
							"x":0, "y":55+x,
							"horizontal_align":"center",
							"image":"interface/controls/special/login/slotbar.tga",
							"children":(
								{
									"name":"name",
									"type":"editline",
									"x":12, "y":10,
									"width":200, "height":16,
									"color":0xffc8aa80,
									"input_limit": 16,
									"enable_codepage": 0,
								},
							),
						},
### SEXO ### SEXO ### SEXO ### SEXO ### SEXO ### SEXO ### SEXO ### SEXO ### SEXO ### SEXO ### SEXO ### SEXO 
						{
							"name"		: 	"Sexo_line",
							"type"		:	"image",
							"image"		:	LINE,
							"x":0, "y":100+x,
							"horizontal_align":"center",
							"children":
							(
								{
									"name" 	: 	"Sexo_Title",
									"type"	:	"text",
									"text"	:	"|cfff8d090Defina o Gênero",
									"x"		:	0,
									"y"		:	-5,
									"all_align":"center",
								},
							),
						},
						{
							"name":"gender_man",
							"type":"radio_button",
							"x":-40, "y":130+x,
							"horizontal_align":"center",

							"default_image":interface + "male_normal.tga",
							"over_image":interface + "male.tga",
							"down_image":interface + "male_down.tga",
						},
						{
							"name":"gender_woman",
							"type":"radio_button",
							"x":40, "y":130+x,
							"horizontal_align":"center",
							"default_image":interface + "female_normal.tga",
							"over_image":interface + "female.tga",
							"down_image":interface + "female_down.tga",
						},
### CABELO### CABELO### CABELO### CABELO### CABELO### CABELO### CABELO### CABELO### CABELO### CABELO### CABELO
						{
							"name"		: 	"Cabelo_line",
							"type"		:	"image",
							"image"		:	LINE,
							"x":0, "y":230+x,
							"horizontal_align":"center",
							"children":
							(
								{
									"name" 	: 	"Cabelo_Title",
									"type"	:	"text",
									"text"	:	"|cfff8d090Escolha seu Cabelo",
									"x"		:	0,
									"y"		:	-5,
									"all_align":"center",
								},
							),
						},
						{
							"name":"prev_button_hair",
							"type":"redbutton",
							"x":-40, "y":265+x,
							"width":80,
							"horizontal_align":"center",
							"text":"Anterior",
						},
						{
							"name":"next_button_hair",
							"type":"redbutton",
							"x":40, "y":265+x,
							"width":80,
							"horizontal_align":"center",
							"text":"Próximo",
						},
		### FINALIZAR/CANCELAR### FINALIZAR/CANCELAR### FINALIZAR/CANCELAR### FINALIZAR/CANCELAR### FINALIZAR/CANCELAR### FINALIZAR/CANCELAR
						{
							"name":"create_button",
							"type":"redbutton",
							"x":55, "y":310+x,
							"horizontal_align":"center",
							"width": 110,
							"text":"ACEITAR",
						},
						{
							"name":"cancel_button",
							"type":"redbutton",
							"x":-55, "y":310+x,
							"horizontal_align":"center",
							"width": 110,
							"text":"DESISTIR",
						},
					)
				},
### GIRAR PERSONAGEM### GIRAR PERSONAGEM### GIRAR PERSONAGEM### GIRAR PERSONAGEM### GIRAR PERSONAGEM### GIRAR PERSONAGEM### GIRAR PERSONAGEM### GIRAR PERSONAGEM
				{
					"name":"esquerda_char",
					"type":"button",
					"x":200, "y":5,
					"vertical_align":"center",
					"horizontal_align":"center",
					"default_image":interface+"girar_esquerda_over.tga",
					"over_image":interface+"girar_esquerda.tga",
					"down_image":interface+"girar_esquerda_down.tga",
				},
				{
					"name":"direita_char",
					"type":"button",
					"x":-80, "y":0,
					"vertical_align":"center",
					"horizontal_align":"center",
					"default_image":interface+"girar_direita_over.tga",
					"over_image":interface+"girar_direita.tga",
					"down_image":interface+"girar_direita_down.tga",

				},
			),
		},
		{
			"name":"classe_board",
			"type":"thinboard",
			"width": 250,
			"height": 210,
			"x":270,
			"y":SCREEN_HEIGHT - 210 -20,
			"horizontal_align":"right",
			"children":
			(
				{
					"name":"classe_name",
					"type":"image",
					"horizontal_align":"center",
					"x":0,
					"y":20,
					"image":"interface/controls/special/create/shura.tga",
				},
				{
					"name":"seta_esquerda",
					"type":"button",
					"x":-50, "y":210-100,
					"horizontal_align":"center",
					"default_image":"interface/controls/special/login/left_0.tga",
					"over_image":"interface/controls/special/login/left_1.tga",
					"down_image":"interface/controls/special/login/left_2.tga",
				},
				{
					"name":"seta_direita",
					"type":"button",
					"x":50, "y":210-100,
					"horizontal_align":"center",
					"default_image":"interface/controls/special/login/right_0.tga",
					"over_image":"interface/controls/special/login/right_1.tga",
					"down_image":"interface/controls/special/login/right_2.tga",
				},
			),
		},
	),
}

