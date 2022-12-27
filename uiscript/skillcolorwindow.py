#favor manter essa linha

BOARD_WIDTH = 325 -14
BOARD_HEIGHT = 340 + 14 + 24

THINBOARD_WIDTH = 310
THINBOARD_HEIGHT = 280 + 14

BUTTON_GAP = 12.5

COLOR_PICKER_WIDTH = 256
COLOR_PICKER_HEIGHT = 256

window = {
	"name":"SkillColorWindow",
	"style":("movable", "float",),
	"x":(SCREEN_WIDTH - BOARD_WIDTH) / 2,
	"y":(SCREEN_HEIGHT - BOARD_HEIGHT) / 2,
	"width":BOARD_WIDTH,
	"height":BOARD_HEIGHT,
	"children":
	(
		{
			"name":"Board",
			"type":"new_board_with_titlebar",
			"style":("attach",),
			"x":0,
			"y":0,
			"width":BOARD_WIDTH,
			"height":BOARD_HEIGHT,
			"title":"Escolher Cor da Habilidade",
			"children":
			(
				{
					"name":"ThinBoard",
					"type":"window",
					"x":13-5,
					"y":35+4,
					"width":THINBOARD_WIDTH - 15,
					"height":THINBOARD_HEIGHT - 15,
					"children":
					(
						{
							"name":"BGColorBar",
							"type":"bar",
							"x":0,
							"y":0,
							"width":THINBOARD_WIDTH - 15,
							"height":THINBOARD_HEIGHT - 15,
							"color":0xff303030,
						},
						{
							"name":"BGImage",
							"type":"image",
							"x":2.5,
							"y":2.5,
							"image":"interface/controls/special/skillcolor/background_expanded.tga",
						},
						{
							"name":"BGColorPickerImage",
							"type":"image",
							"x":0,
							"y":15-2,
							"horizontal_align":"center",
							"image":"interface/controls/special/skillcolor/box.tga",
						},
						{
							"name":"BGColorPickerImage",
							"type":"image",
							"x":0,
							"y":15,
							"horizontal_align":"center",
							"width":COLOR_PICKER_WIDTH,
							"height":COLOR_PICKER_HEIGHT,
							"image":"interface/controls/special/skillcolor/color_picker_background.tga",
							"children":
							(
								{
									"name":"BGColorPickerButton",
									"type":"button",
									"x":0,
									"y":0,
									"width":COLOR_PICKER_WIDTH,
									"height":COLOR_PICKER_HEIGHT,
								},
								{
									"name":"BGColorPickerDotImage",
									"type":"image",
									"x":0,
									"y":0,
									"width":12,
									"height":12,
									"image":"interface/controls/special/skillcolor/color_picker_dot.tga",
								},
							),
						},
						{
							"name":"BG2Image",
							"type":"image",
							"x":2.5,
							"y":2.5,
							"image":"interface/controls/special/skillcolor/background_expanded.tga",
							"children":
							(
								{
									"name":"BG2Window",
									"type":"window",
									"x":70 + 1,
									"y":30,
									"width":150,
									"height":172.5,
									"children":
									(
										{
											"name":"BG2ColorPresetSlotImage",
											"type":"expanded_image",
											"style":("attach",),
											"x":0,
											"y":0,
											"width":COLOR_PICKER_WIDTH,
											"height":COLOR_PICKER_HEIGHT,
											"image":"interface/controls/special/skillcolor/pet_incu.tga",
											"children":
											(
												{
													"name":"BG2ColorPresetTitle",
													"type":"text",
													"x":0,
													"y":-10,
													"text":"CORES SALVAS",
													"fontname":"Verdana:12b",
													"all_align":"center"
												},
												{
													"name":"BG2ColorPresetEditLine",
													"type":"button",
													"x":13,
													"y":26,
													"width":136,
													"height":16,
													"text":"Selecione uma cor",
												},
												{
													"name":"BG2ColorPresetButton",
													"type":"button",
													"x":124,
													"y":31,
													"default_image":"interface/controls/special/skillcolor/arrow_left_normal.tga",
													"over_image":"interface/controls/special/skillcolor/arrow_left_over.tga",
													"down_image":"interface/controls/special/skillcolor/arrow_left_down.tga",
												},
											),
										},
										{
											"name":"BG2ColorPresetSaveButton",
											"type":"redbutton",
											"width":75,
											"x":42,
											"y":60,
											"horizontal_align":"center",
											"text":"Salvar Cor",
										},
										{
											"name":"BG2ColorPresetClearButton",
											"type":"redbutton",
											"width":75,
											"x":-42,
											"y":60,
											"horizontal_align":"center",
											"text":"Excluir Cor",
										},
										{
											"name":"BG2CustomColorInputSlotImage",
											"type":"expanded_image",
											"style":("attach",),
											"x":0,
											"y":120,
											"width":COLOR_PICKER_WIDTH,
											"height":COLOR_PICKER_HEIGHT,
											"image":"interface/controls/special/skillcolor/pet_incu.tga",
											"children":
											(
												{
													"name":"BG2CustomColorTitle",
													"type":"text",
													"x":0,
													"y":-10,
													"text":"CÓDIGO DA COR",
													"fontname":"Verdana:12b",
													"all_align":"center"
												},
												{
													"name":"BG2CustomColorEditLine",
													"type":"editline",
													"x":13,
													"y":30-2,
													"width":136,
													"height":15,
													"text":"",
													"input_limit":7,
												},
											),
										},
									),
								},
								{
									"name":"DefaultButton",
									"type":"redbutton",
									"width":148,
									"x":70 + 1.5,
									"y":THINBOARD_HEIGHT - 85,
									"text":"Usar cor padrão",
								},
							),
						},
					),
				},
				{
					"name":"ColorLayer1Button",
					"type":"redbutton",
					"width":27,
					"x":BUTTON_GAP + 62.5 + 35 * 0,
					"y":BOARD_HEIGHT - 95,
					"text":"1",
				},
				{
					"name":"ColorLayer2Button",
					"type":"redbutton",
					"width":27,
					"x":BUTTON_GAP + 62.5 + 35 * 1,
					"y":BOARD_HEIGHT - 95,
					"text":"2",
				},
				{
					"name":"ColorLayer3Button",
					"type":"redbutton",
					"width":27,
					"x":BUTTON_GAP + 62.5 + 35 * 2,
					"y":BOARD_HEIGHT - 95,
					"text":"3",
				},
				{
					"name":"ColorLayer4Button",
					"type":"redbutton",
					"width":27,
					"x":BUTTON_GAP + 62.5 + 35 * 3,
					"y":BOARD_HEIGHT - 95,
					"text":"4",
				},
				{
					"name":"ColorLayer5Button",
					"type":"redbutton",
					"width":27,
					"x":BUTTON_GAP + 62.5 + 35 * 4,
					"y":BOARD_HEIGHT - 95,
					"text":"5",
				},
				{
					"name":"PrevPageButton",
					"type":"button",
					"x": 22,
					"y":(COLOR_PICKER_HEIGHT / 2) + 40,
					"default_image":"interface/controls/special/skillcolor/arrow_right_normal.tga",
					"over_image":"interface/controls/special/skillcolor/arrow_right_over.tga",
					"down_image":"interface/controls/special/skillcolor/arrow_right_down.tga",
				},
				{
					"name":"NextPageButton",
					"type":"button",
					"x":COLOR_PICKER_WIDTH + 21,
					"y":(COLOR_PICKER_HEIGHT / 2) + 40,
					"default_image":"interface/controls/special/skillcolor/arrow_left_normal.tga",
					"over_image":"interface/controls/special/skillcolor/arrow_left_over.tga",
					"down_image":"interface/controls/special/skillcolor/arrow_left_down.tga",
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":BOARD_WIDTH - 14,
					"x":7,
					"y":BOARD_HEIGHT - 60,
				},
				{
					"name":"ConfirmButton",
					"type":"redbutton",
					"width":131,
					"x": -71,
					"y":BOARD_HEIGHT - 46,
					"horizontal_align":"center",
					"text":"Alterar Cor",
				},
				{
					"name":"CancelButton",
					"type":"redbutton",
					"width":131,
					"x": 71,
					"y":BOARD_HEIGHT - 46,
					"horizontal_align":"center",
					"text":"Cancelar",
				},
				{
					"name":"BG2ColorPresetWindow",
					"type":"window",
					"x":91,
					"y":117,
					"width":131,
					"height":0,
				},
			)
		},
	),
}