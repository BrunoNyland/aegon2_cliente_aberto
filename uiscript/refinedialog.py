#favor manter essa linha
import uiscriptlocale
import grp

NEGATIVE_COLOR = grp.GenerateColor(0.999, 0.3, 0.3, 1.0)
POSITIVE_COLOR = grp.GenerateColor(0.5, 0.9058, 0.5, 1.0)

width = 460
height = 390
REFINE = "interface/controls/special/refine/"
BOARD = "interface/controls/common/board/"

CHARACTER = "interface/controls/special/character/"
LINE = "interface/controls/common/horizontal_bar/center.tga"

window = {
	"name":"RefineDialog",
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
			"style":("attach",),
			"title":"Refinar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"Retrair",
					"type":"button",
					"x":width-58,
					"y":8,
					"default_image":BOARD+"retract_normal.tga",
					"over_image":BOARD+"retract_over.tga",
					"down_image":BOARD+"retract_down.tga",
				},
				{
					"name":"Expandir",
					"type":"button",
					"x":width-58,
					"y":8,
					"default_image":BOARD+"expand_normal.tga",
					"over_image":BOARD+"expand_over.tga",
					"down_image":BOARD+"expand_down.tga",
				},
				{
					"name":"",
					"type":"expanded_image",
					"image":LINE,
					"x":230-5,
					"y":40,
					"x_scale":0.8,
					"y_scale":1,
					"children":
					(
						{
							"name":"name_result",
							"type":"text",
							"text":"Nome do Item +9",
							"color":0xfff8d090,
							"x":0,
							"y":-5,
							"all_align":"center",
						},
					),
				},
				{
					"name":"Atributes",
					"type":"window",
					"x":430-5, "y": 40,
					"height":240,
					"width": 170,
					"hide":1,
					"children":
					(
						{
							"name":"add1","type":"image","image":REFINE+"list.tga","x":5,"y":17,
							"children":
							(
								{"name":"add1_1","type":"text","color":0xfff8d090,"text":"Ataque", "x":15, "y":-12,},
								{"name":"add1_2","type":"text","color":0xffa08784,"text":"1000(+15) - 1125(+20)", "x":15,"y":8,},
							),
						},
						{
							"name":"add2","type":"image","image":REFINE+"list.tga","x":5,"y":17 + 46,
							"children":
							(
								{"name":"add2_1","type":"text","color":0xfff8d090,"text":"Ataque Magico", "x":15, "y":-12,},
								{"name":"add2_2","type":"text","color":0xffa08784,"text":"715(+15) - 780(+20)", "x":15,"y":8,},
							),
						},
						{
							"name":"add3","type":"image","image":REFINE+"list.tga","x":5,"y":17 + 46*2,
							"children":
							(
								{"name":"add3_1","type":"text","color":0xfff8d090,"text":"Bonus Contra Humanoides", "x":15, "y":-12,},
								{"name":"add3_2","type":"text","color":0xffa08784,"text":"120%(+20%)", "x":15,"y":8,},
							),
						},
						{
							"name":"add4","type":"image","image":REFINE+"list.tga","x":5,"y":17 + 46*3,
							"children":
							(
								{"name":"add4_1","type":"text","color":0xfff8d090,"text":"Inteligencia", "x":15, "y":-12,},
								{"name":"add4_2","type":"text","color":0xffa08784,"text":"50(+10)", "x":15,"y":8,},
							),
						},
						{
							"name":"add5","type":"image","image":REFINE+"list.tga","x":5,"y":17 + 46*4,
							"children":
							(
								{"name":"add5_1","type":"text","color":0xfff8d090,"text":"Chance de Ataque Critico", "x":15, "y":-12,},
								{"name":"add5_2","type":"text","color":0xffa08784,"text":"15%(+5%)", "x":15,"y":8,},
							),
						},
					),
				},
				{
					"name":"arrow",
					"type":"image",
					"image":REFINE+"seta.tga",
					"x":300-5,
					"y":80,
				},
				{
					"name":"Cost",
					"type":"text",
					"color":0xfff8d090,
					"text":uiscriptlocale.REFINE_COST,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"x":0,
					"y":height - 100,
				},
				{"name":"line","type":"line","width":200,"height":0.5,"x":0,"y":height-80,"horizontal_align":"center","color":0xfff8d090,},
				{
					"name":"SuccessPercentage",
					"type":"text",
					"color":0xfff8d090,
					"text":uiscriptlocale.REFINE_INFO,
					"horizontal_align":"center",
					"text_horizontal_align":"center",
					"x":0,
					"y":height - 75,
				},
				{
					"name":"separator",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":height - 120,
				},
				{
					"name":"AcceptButton",
					"text":uiscriptlocale.OK,
					"type":"redbutton",
					"x":55,
					"y":height - 47,
					"horizontal_align":"center",
					"width":90,
				},
				{
					"name":"CancelButton",
					"text":uiscriptlocale.CANCEL,
					"type":"redbutton",
					"x":-55,
					"y":height - 47,
					"horizontal_align":"center",
					"width":90,
				},
				{
					"name":"bg",
					"type":"image",
					"image":REFINE+"c.tga",
					"x":8,
					"y":50,
					"children":
					(
						{
							"name":"slot_refine1",
							"type":"image",
							"image":REFINE+"slot.tga",
							"x":20, "y":-8,
							"children":
							(
								{"name":"refine1","type":"text","color":0xffa08784,"text":"Perola Escarlate","x":60,"y":10,},
								{"name":"state1","type":"image","image":REFINE+"v.tga","x":45,"y":12,},
								{"name":"","type":"image","image":REFINE+"line.tga","x":50,"y":26,},
								{"name":"","type":"image","image":REFINE+"decoration_line.tga","x":40,"y":29,},
							),
						},
						{
							"name":"slot_refine2",
							"type":"image",
							"image":REFINE+"slot.tga",
							"x":94, "y":35,
							"children":
							(
								{"name":"refine2","type":"text","color":0xffa08784,"text":"Perola Azul","x":60,"y":10,},
								{"name":"state2","type":"image","image":REFINE+"f.tga","x":45,"y":12,},
								{"name":"","type":"image","image":REFINE+"line.tga","x":50,"y":26,},
								{"name":"","type":"image","image":REFINE+"decoration_line.tga","x":50,"y":29,},
							),
						},
						{
							"name":"slot_refine3",
							"type":"image",
							"image":REFINE+"slot.tga",
							"x":114, "y":90,
							"children":
							(
								{"name":"refine3","type":"text","color":0xffa08784,"text":"Perola Branca","x":60,"y":10,},
								{"name":"state3","type":"image","image":REFINE+"v.tga","x":45,"y":12,},
								{"name":"","type":"image","image":REFINE+"line.tga","x":50,"y":26,},
								{"name":"","type":"image","image":REFINE+"decoration_line.tga","x":40,"y":29,},
							),
						},
						{
							"name":"slot_refine4",
							"type":"image",
							"image":REFINE+"slot.tga",
							"x":94, "y":145,
							"children":
							(
								{"name":"refine4","type":"text","color":0xffa08784,"text":"Perola Branca","x":60,"y":10,},
								{"name":"state4","type":"image","image":REFINE+"v.tga","x":45,"y":12,},
								{"name":"","type":"image","image":REFINE+"line.tga","x":50,"y":26,},
								{"name":"","type":"image","image":REFINE+"decoration_line.tga","x":40,"y":29,},
							),
						},
						{
							"name":"slot_refine5",
							"type":"image",
							"image":REFINE+"slot.tga",
							"x":20, "y":200,
							"children":
							(
								{"name":"refine5","type":"text","color":0xffa08784,"text":"Perola Branca","x":60,"y":10,},
								{"name":"state5","type":"image","image":REFINE+"v.tga","x":45,"y":12,},
								{"name":"","type":"image","image":REFINE+"line.tga","x":50,"y":26,},
								{"name":"","type":"image","image":REFINE+"decoration_line.tga","x":40,"y":29,},
							),
						},
						{
							"name":"slot_origem",
							"type":"button",
							"default_image":REFINE+"slot3x.tga",
							"over_image":REFINE+"slot3x.tga",
							"down_image":REFINE+"slot3x.tga",
							"x":20,
							"y":0,
							"vertical_align":"center",
						},
					),
				},
				{
					"name":"slot_result",
					"type":"button",
					"default_image":REFINE+"slot3xR.tga",
					"over_image":REFINE+"slot3xR.tga",
					"down_image":REFINE+"slot3xR.tga",
					"x":360,
					"y":107,
					"children":
					(
						{
							"name":"slot_lvl",
							"type":"image",
							"image":CHARACTER+"level_round.tga",
							"x":-5,
							"y":-15,
							"children":
							({"name":"item_lvl","type":"text","color":POSITIVE_COLOR,"text":"255","x":0,"y":-1,"all_align":"center",},),
						},
					),
				},
			),
		},
	),
}