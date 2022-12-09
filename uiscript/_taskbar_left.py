#favor manter essa linha
interface = "interface/controls/special/taskbar/"

left = interface + "left.tga"

width = 255-30-35
height = 59-30

window = {
	"name":"TaskBar_Right",
	"x":0,
	"y":SCREEN_HEIGHT - height,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Base_Board_Right",
			"type":"image",
			"x":0,
			"y":-30,
			"horizontal_align":"center",
			"image":left,
		},
		{
			"name":"hp_empty",
			"type":"image",
			"image":interface+"hp/empty.png",
			"x":4,
			"y":4,
			"children":
			(
				{
					"name":"hp_mid",
					"type":"expanded_image",
					"image":interface+"hp/midle.png",
					"x":0,"y":0,
					"style":("not_pick",),
				},
				{
					"name":"hp_full",
					"type":"expanded_image",
					"image":interface+"hp/full.png",
					"x":0,"y":0,
					"style":("not_pick",),
				},
				{"name":"tooltip_hp","type":"ballon","width":60,"text":"","x":0,"y":-38,"hide":1,},
			),
		},
		{
			"name":"mp_empty",
			"type":"image",
			"image":interface+"mp/empty.png",
			"x":4,
			"y":4+7,
			"children":
			(
				{
					"name":"mp_mid",
					"type":"expanded_image",
					"image":interface+"mp/midle.png",
					"x":0,"y":0,
					"style":("not_pick",),
				},
				{
					"name":"mp_full",
					"type":"expanded_image",
					"image":interface+"mp/full.png",
					"x":0,"y":0,
					"style":("not_pick",),
				},
				{"name":"tooltip_mp","type":"ballon","width":60,"text":"","x":0,"y":-38,"hide":1,},
			),
		},
		{
			"name":"tp_empty",
			"type":"image",
			"image":interface+"tp/empty.png",
			"x":4,
			"y":4+7*2,
			"children":
			(
				{
					"name":"tp_full",
					"type":"expanded_image",
					"image":interface+"tp/full.png",
					"x":0,"y":0,
					"style":("not_pick",),
				},
				{"name":"tooltip_tp","type":"ballon","width":60,"text":"","x":0,"y":-38,"hide":1,},
			),
		},
	),
}