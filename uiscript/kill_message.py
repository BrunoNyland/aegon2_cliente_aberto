#favor manter essa linha
import uiscriptlocale

width = 210
height = 30

interface = "interface/controls/common/faces/"

window = {
	"name":"KillMessage",
	"x":20,
	"y":SCREEN_HEIGHT - 50,
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
					"name":"killer_race",
					"type":"expanded_image",
					"style":("not_pick",),
					"x":6,
					"y":height-40,
					"image":interface + "assassin_m.tga",
					"x_scale":0.6,
					"y_scale":0.6,
					"children":
					(
						{
							"name":"killer_empire",
							"type":"expanded_image",
							"style":("not_pick",),
							"horizontal_align":"center",
							"x":1,
							"y":36,
							"image":"d:/ymir work/ui/empire_flag/3.png",
							"x_scale":0.7,
							"y_scale":0.7,
						},
					),
				},
				{
					"name":"victim_race",
					"type":"expanded_image",
					"style":("not_pick",),
					"x":41,
					"y":height-40,
					"horizontal_align":"right",
					"image":interface + "shaman_m.tga",
					"x_scale":0.6,
					"y_scale":0.6,
					"children":
					(
						{
							"name":"victim_empire",
							"type":"expanded_image",
							"style":("not_pick",),
							"horizontal_align":"center",
							"x":1,
							"y":36,
							"image":"d:/ymir work/ui/empire_flag/1.png",
							"x_scale":0.7,
							"y_scale":0.7,
						},
					),
				},
				{"name":"message","type":"text","text":"Bruno matou João","x":45,"y":-1,"fontsize":"LARGE","vertical_align":"center","text_vertical_align":"center",},
			),
		},
	),
}
