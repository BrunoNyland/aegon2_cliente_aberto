#favor manter essa linha
LINE = "interface/controls/common/horizontal_bar/center.tga"
HAIR = "interface/controls/special/select/hair/"
SHAPE = "interface/controls/special/select/shape/"

import grp
text_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
box_color = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)

height = 500
board_hair_height = 450
board_shape_height = 350
window = {
	"name":"selectcharacterwindow",
	"x":0,
	"y":0,
	"width":SCREEN_WIDTH,
	"height":SCREEN_HEIGHT,
	"children":
	(
		{
			"name":"BackGround",
			"type":"expanded_image",
			"x":0, "y":0,
			"x_scale":float(SCREEN_WIDTH) / 1366.0,
			"y_scale":float(SCREEN_HEIGHT) / 768.0,
			"image":"interface/controls/special/login/background.tga",
			# "image":"interface/controls/special/login/verde.tga",
			"children":
			(
				{
					"name":"board",
					"type":"board_transparent",
					"width":250,
					"height":height,
					"x":20, "y":SCREEN_HEIGHT - 520,
					"children":
					(
						{
							"name":"name",
							"type": "editboardfake",
							"x": 0, "y": 40,
							"width":180, "height":28,
							"horizontal_align": "center",
							"text":"",
							"fontname":"Verdana:16b",
							"text_center":1,
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Personagem",
									"color":text_color,
									"fontname":"Verdana:12b",
									"x":0, "y":-15,
									"horizontal_align":"center",
									"text_horizontal_align":"center",
								},
							),
						},
						{
							"name":"level",
							"type": "editboardfake",
							"x": 0, "y": 90,
							"width":100, "height":28,
							"horizontal_align": "center",
							"fontname":"Verdana:16b",
							"text":"",
							"text_center":1,
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Level",
									"color":text_color,
									"fontname":"Verdana:12b",
									"x":0, "y":-15,
									"horizontal_align":"center",
									"text_horizontal_align":"center",
								},
							),
						},
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":110,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"guild",
									"type":"text",
									"text":"",
									"fontname":"Verdana:16b",
									"x":20, "y":40,
								},
								{
									"name":"empire",
									"type":"text",
									"text":"",
									"fontname":"Verdana:16b",
									"x":20, "y":40+30,
								},
								{
									"name":"",
									"type":"image",
									"image":LINE,
									"x":0, "y":40+30+10,
									"horizontal_align":"center",
								},
							),
						},

						{
							"name":"playtime",
							"type": "editboardfake",
							"x": 0, "y": 238,
							"width":150, "height":28,
							"horizontal_align": "center",
							"fontname":"Verdana:16b",
							"text":"",
							"text_center":1,
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Tempo de Jogo",
									"color":text_color,
									"fontname":"Verdana:12b",
									"x":0, "y":-15,
									"horizontal_align":"center",
									"text_horizontal_align":"center",
								},
							),
						},

						{
							"name":"select_hair_btn",
							"type":"button",
							"default_image": "interface/controls/special/select/hair/hair_man_normal.tga",
							"over_image": "interface/controls/special/select/hair/hair_man_over.tga",
							"down_image": "interface/controls/special/select/hair/hair_man_normal.tga",
							"disable_image": "interface/controls/special/select/hair/hair_man_disabled.tga",
							"horizontal_align":"center",
							"x": -56,
							"y":281 - 10 + 26,
						},
						{
							"name":"show_hide_hair",
							"type":"newradio_button",
							"set_type":0,
							"x":-56 + 40,
							"y":280 + 26,
							"horizontal_align":"center",
						},

						{
							"name":"select_shape_btn",
							"type":"button",
							"default_image": "interface/controls/special/select/shape/shape1_normal.tga",
							"over_image": "interface/controls/special/select/shape/shape1_over.tga",
							"down_image": "interface/controls/special/select/shape/shape1_normal.tga",
							"disable_image": "interface/controls/special/select/shape/shape_disabled.tga",
							"horizontal_align":"center",
							"x": 40 -16,
							"y":281 - 10 + 26,
						},
						{
							"name":"show_hide_shape",
							"type":"newradio_button",
							"set_type":0,
							"x":40 + 30 - 6,
							"y":280 + 26,
							"horizontal_align":"center",
						},

						{
							"name":"delete_button",
							"type":"redbutton",
							"x":-55, "y":135,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 100,
							"text_color":0xffc8aa80,
							"text":"Deletar",
						},
						{
							"name":"select_button",
							"type":"redbutton",
							"x":55, "y":135,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 100,
							"text_color":0xffc8aa80,
							"text":"Selecionar",
						},
						{
							"name":"create_button",
							"type":"redbutton",
							"x":0, "y":135,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 130,
							"text_color":0xffc8aa80,
							"text":"Novo Personagem",
						},
						{
							"name":"exit_button",
							"type":"button",
							"type":"redbutton",
							"x":0, "y":105,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 50,
							"text_color":0xffc8aa80,
							"text":"Voltar",
						},
						{
							"name":"left_button",
							"type":"button",
							"x":-55, "y":90,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"default_image":"interface/controls/special/login/left_0.png",
							"over_image":"interface/controls/special/login/left_1.png",
							"down_image":"interface/controls/special/login/left_2.png",
						},
						{
							"name":"right_button",
							"type":"button",
							"x":55, "y":90,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"default_image":"interface/controls/special/login/right_0.png",
							"over_image":"interface/controls/special/login/right_1.png",
							"down_image":"interface/controls/special/login/right_2.png",
						},

						{
							"name":"flag_board",
							"type":"box",
							"color":box_color,
							"x":0,
							"y":-50,
							"width":113+1,
							"height":62+1,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"EmpireFlag_A",
									"type":"image",
									"x":0,
									"y":1,
									"horizontal_align":"center",
									"vertical_align":"center",
									"image":"interface/controls/special/empire_select/flag_1.tga",
								},
								{
									"name":"EmpireFlag_B",
									"type":"image",
									"x":0,
									"y":1,
									"horizontal_align":"center",
									"vertical_align":"center",
									"image":"interface/controls/special/empire_select/flag_2.tga",
								},
								{
									"name":"EmpireFlag_C",
									"type":"image",
									"x":0,
									"y":1,
									"horizontal_align":"center",
									"vertical_align":"center",
									"image":"interface/controls/special/empire_select/flag_3.tga",
								},
							),
						},

					),
				},
####################################################################################################
				{
					"name":"board_shape",
					"type":"board_transparent",
					"width":250,
					"height":board_shape_height,
					"x":20, "y":0,
					"vertical_align":"center",
					"hide":1,
					"children":
					(
						{
							"name":"shape_btn_0",
							"type":"button",
							"x":-55, "y":35,
							"horizontal_align":"center",
							"default_image": SHAPE + "btn_shape_bg_normal.png",
							"over_image": SHAPE + "btn_shape_bg_over.png",
							"down_image": SHAPE + "btn_shape_bg_normal.png",
							"disable_image": SHAPE + "btn_shape_bg_over.png",
							"children":
							(
								{
									"name":"shape_image_0",
									"type":"image",
									"style":("not_pick",),
									"x":1, "y":-10,
									"image": SHAPE + "warrior_m/00.png",
									"horizontal_align":"center",
								},
							)
						},
						{
							"name":"shape_btn_1",
							"type":"button",
							"x":55, "y":35,
							"horizontal_align":"center",
							"default_image": SHAPE + "btn_shape_bg_normal.png",
							"over_image": SHAPE + "btn_shape_bg_over.png",
							"down_image": SHAPE + "btn_shape_bg_normal.png",
							"disable_image": SHAPE + "btn_shape_bg_over.png",
							"children":
							(
								{
									"name":"shape_image_1",
									"type":"image",
									"style":("not_pick",),
									"x":1, "y":-10,
									"image": SHAPE + "warrior_m/01.png",
									"horizontal_align":"center",
								},
							)
						},
####################################################################################################
						{
							"name":"shape_cancel_btn",
							"type":"redbutton",
							"x":-55, "y":55,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 100,
							"text_color":0xffc8aa80,
							"text":"Retornar",
						},
						{
							"name":"shape_save_btn",
							"type":"redbutton",
							"x":55, "y":55,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 100,
							"text_color":0xffc8aa80,
							"text":"Escolher",
						},
					),
				},
####################################################################################################
				{
					"name":"board_hair",
					"type":"board_transparent",
					"width":250,
					"height":board_hair_height,
					"x":20, "y":0,
					"vertical_align":"center",
					"hide":1,
					"children":
					(
						{
							"name":"hair_btn_0",
							"type":"button",
							"x":-55, "y":35,
							"horizontal_align":"center",
							"default_image": HAIR + "btn_hair_bg_normal.png",
							"over_image": HAIR + "btn_hair_bg_over.png",
							"down_image": HAIR + "btn_hair_bg_normal.png",
							"disable_image": HAIR + "btn_hair_bg_over.png",
							"children":
							(
								{
									"name":"hair_image_0",
									"type":"image",
									"style":("not_pick",),
									"x":1, "y":0,
									"image": HAIR + "ninja_m/1.png"
								},
							)
						},
						{
							"name":"hair_btn_1",
							"type":"button",
							"x":55, "y":35,
							"horizontal_align":"center",
							"default_image": HAIR + "btn_hair_bg_normal.png",
							"over_image": HAIR + "btn_hair_bg_over.png",
							"down_image": HAIR + "btn_hair_bg_normal.png",
							"disable_image": HAIR + "btn_hair_bg_over.png",
							"children":
							(
								{
									"name":"hair_image_1",
									"type":"image",
									"style":("not_pick",),
									"x":1, "y":0,
									"image": HAIR + "ninja_m/13.png"
								},
							)
						},
						{
							"name":"hair_btn_2",
							"type":"button",
							"x":-55, "y":35 + 110,
							"horizontal_align":"center",
							"default_image": HAIR + "btn_hair_bg_normal.png",
							"over_image": HAIR + "btn_hair_bg_over.png",
							"down_image": HAIR + "btn_hair_bg_normal.png",
							"disable_image": HAIR + "btn_hair_bg_over.png",
							"children":
							(
								{
									"name":"hair_image_2",
									"type":"image",
									"style":("not_pick",),
									"x":1, "y":0,
									"image": HAIR + "ninja_m/25.png"
								},
							)
						},
						{
							"name":"hair_btn_3",
							"type":"button",
							"x":55, "y":35 + 110,
							"horizontal_align":"center",
							"default_image": HAIR + "btn_hair_bg_normal.png",
							"over_image": HAIR + "btn_hair_bg_over.png",
							"down_image": HAIR + "btn_hair_bg_normal.png",
							"disable_image": HAIR + "btn_hair_bg_over.png",
							"children":
							(
								{
									"name":"hair_image_3",
									"type":"image",
									"style":("not_pick",),
									"x":1, "y":0,
									"image": HAIR + "ninja_m/37.png"
								},
							)
						},
####################################################################################################
						{
							"name":"hair_color_btn_1",
							"type":"button",
							"x": -14 + 28 * -2,
							"y": 280,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/01_normal.png",
							"over_image": HAIR + "colors/01_over.png",
							"down_image": HAIR + "colors/01_normal.png",
							"disable_image": HAIR + "colors/01_selected.png",
						},
						{
							"name":"hair_color_btn_2",
							"type":"button",
							"x": -14 + 28 * -1,
							"y": 280,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/02_normal.png",
							"over_image": HAIR + "colors/02_over.png",
							"down_image": HAIR + "colors/02_normal.png",
							"disable_image": HAIR + "colors/02_selected.png",
						},
						{
							"name":"hair_color_btn_3",
							"type":"button",
							"x": -14 + 28 * 0,
							"y": 280,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/03_normal.png",
							"over_image": HAIR + "colors/03_over.png",
							"down_image": HAIR + "colors/03_normal.png",
							"disable_image": HAIR + "colors/03_selected.png",
						},
						{
							"name":"hair_color_btn_4",
							"type":"button",
							"x": -14 + 28 * 1,
							"y": 280,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/04_normal.png",
							"over_image": HAIR + "colors/04_over.png",
							"down_image": HAIR + "colors/04_normal.png",
							"disable_image": HAIR + "colors/04_selected.png",
						},
						{
							"name":"hair_color_btn_5",
							"type":"button",
							"x": -14 + 28 * 2,
							"y": 280,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/05_normal.png",
							"over_image": HAIR + "colors/05_over.png",
							"down_image": HAIR + "colors/05_normal.png",
							"disable_image": HAIR + "colors/05_selected.png",
						},
						{
							"name":"hair_color_btn_6",
							"type":"button",
							"x": -14 + 28 * 3,
							"y": 280,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/06_normal.png",
							"over_image": HAIR + "colors/06_over.png",
							"down_image": HAIR + "colors/06_normal.png",
							"disable_image": HAIR + "colors/06_selected.png",
						},
						{
							"name":"hair_color_btn_7",
							"type":"button",
							"x": -14 + 28 * -2,
							"y": 280 + 28,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/07_normal.png",
							"over_image": HAIR + "colors/07_over.png",
							"down_image": HAIR + "colors/07_normal.png",
							"disable_image": HAIR + "colors/07_selected.png",
						},
						{
							"name":"hair_color_btn_8",
							"type":"button",
							"x": -14 + 28 * -1,
							"y": 280 + 28,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/08_normal.png",
							"over_image": HAIR + "colors/08_over.png",
							"down_image": HAIR + "colors/08_normal.png",
							"disable_image": HAIR + "colors/08_selected.png",
						},
						{
							"name":"hair_color_btn_9",
							"type":"button",
							"x": -14 + 28 * 0,
							"y": 280 + 28,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/09_normal.png",
							"over_image": HAIR + "colors/09_over.png",
							"down_image": HAIR + "colors/09_normal.png",
							"disable_image": HAIR + "colors/09_selected.png",
						},
						{
							"name":"hair_color_btn_10",
							"type":"button",
							"x": -14 + 28 * 1,
							"y": 280 + 28,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/10_normal.png",
							"over_image": HAIR + "colors/10_over.png",
							"down_image": HAIR + "colors/10_normal.png",
							"disable_image": HAIR + "colors/10_selected.png",
						},
						{
							"name":"hair_color_btn_11",
							"type":"button",
							"x": -14 + 28 * 2,
							"y": 280 + 28,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/11_normal.png",
							"over_image": HAIR + "colors/11_over.png",
							"down_image": HAIR + "colors/11_normal.png",
							"disable_image": HAIR + "colors/11_selected.png",
						},
						{
							"name":"hair_color_btn_12",
							"type":"button",
							"x": -14 + 28 * 3,
							"y": 280 + 28,
							"horizontal_align":"center",
							"default_image": HAIR + "colors/12_normal.png",
							"over_image": HAIR + "colors/12_over.png",
							"down_image": HAIR + "colors/12_normal.png",
							"disable_image": HAIR + "colors/12_selected.png",
						},
####################################################################################################
						{
							"name":"hair_cancel_btn",
							"type":"redbutton",
							"x":-55, "y":55,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 100,
							"text_color":0xffc8aa80,
							"text":"Retornar",
						},
						{
							"name":"hair_save_btn",
							"type":"redbutton",
							"x":55, "y":55,
							"vertical_align":"bottom",
							"horizontal_align":"center",
							"width": 100,
							"text_color":0xffc8aa80,
							"text":"Escolher",
						},
					),
				},
			),
		},
	),
}
