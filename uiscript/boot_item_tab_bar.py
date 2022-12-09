#favor manter essa linha
import uiscriptlocale
import grp

width = 500
height = 116

window = {
	"name":"ItemTabBar",
	"x":0, "y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Arrow",
			"type":"image",
			"image":"interface/controls/special/boot/arrow_top.tga",
			"x":10, "y":0,
			"vertical_align":"center",
		},
		{
			"name":"Explain",
			"type":"thinboardnew",
			"style":("not_pick",),
			"width": 330,
			"height": height-40,
			"x":110, "y":0,
			"vertical_align":"center",
			"children":
			(
				{
					"name":"", "type":"text", "text":"Arraste o Ítem que voce Deseja Melhorar",
					"color":0xfff88f90, "x":0, "y":-10,
					"text_vertical_align":"center", "vertical_align":"center",
					"text_horizontal_align":"center", "horizontal_align":"center",
					"fontsize":"LARGE",
				},
				{
					"name":"", "type":"text", "text":"e Solte Aqui...",
					"color":0xfff88f90, "x":0, "y":7,
					"text_vertical_align":"center", "vertical_align":"center",
					"text_horizontal_align":"center", "horizontal_align":"center",
					"fontsize":"LARGE",
				},
			),
		},
		{"name":"", "type":"verticalseparator", "height":height, "x":width-45, "y":3,},
		{
			"name":"Config_Button",
			"type":"image",
			"image":"interface/controls/special/boot/configs_button.tga",
			"x": width - 42,
			"y": 4,
			"children":
			(
				{"name":"Select", "type":"image", "image":"interface/controls/special/boot/select.tga", "x":0, "y":height+2-4, "horizontal_align":"center","style":("not_pick",), "hide":1,},
				{
					"name":"configs_text",
					"style":("not_pick",),
					"type":"image",
					"image":"interface/controls/special/boot/configurar_normal.tga",
					"x":0, "y":0,
					"vertical_align":"center",
					"horizontal_align":"center",
				},
			),
		},
	),
}
