#favor manter essa linha
import uiscriptlocale
import _grp as grp

COLOR_BG = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)

width = 508
height = 396

window = {
	"name":"Boot",
	"style":("movable", "float",),
	"x":0, "y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"MainBoard",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":"Boot de Melhorar Itens",
			"children":
			(
				{
					"name":"Button_Active_All",
					"type":"redbutton",
					"x":6+83-1, "y":8,
					"width":83,
					"text":"Ativar Todos",
				},
				{
					"name":"Button_Deactive_All",
					"type":"redbutton",
					"x":6, "y":8,
					"width":83,
					"text":"Parar Todos",
				},
				{
					"name":"Button_Minimize",
					"type":"button",
					"default_image": "interface/controls/common/board/minimize_normal.tga",
					"over_image": "interface/controls/common/board/minimize_over.tga",
					"down_image": "interface/controls/common/board/minimize_down.tga",
					"x": width - 58, "y":8,
					# "children":
					# (
						# {"name":"","type":"ballon","width":60,"text":"Minimizar","x":0,"y":-38,"horizontal_align":"center","hide":1,"istooltip":1,},
					# ),
				},
				{
					"name":"",
					"type":"horizontalseparator",
					"width":width - 14,
					"x":7,
					"y":150+3,
				},
				{
					"name":"",
					"type":"bar",
					"color":COLOR_BG,
					"height":height-165,
					"width":width-20+4,
					"x":10-2, "y":156,
				},
				{
					"name":"Options_Page",
					"type":"window",
					"height":height-165,
					"width":width-20,
					"x":0, "y":150,
					"hide":1,
					"children":
					(
						{
							"name":"slider",
							"type":"slider",
							"width":230,
							"x":0, "y":190,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"box",
									"style":("not_pick",),
									"color":0xffa08784,
									"width":width-60, "height":45, 
									"x":0, "y":0,
									"horizontal_align":"center",
									"vertical_align":"center",
								},
								{"name":"slider_title","type":"text","text":"Velocidade:","color":0xffa08784,"x":-45, "y":-2, "text_horizontal_align":"center","fontsize":"LARGE"},
								{"name":"slider_number","type":"text","text":"100%","color":0xffa08784,"x":260, "y":-2, "text_horizontal_align":"center","fontsize":"LARGE"},
							),
						},
					),
				},
			),
		},
	),
}
