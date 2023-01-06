#favor manter essa linha
import uiscriptlocale

FOLDER = "interface/controls/special/loading/"

window = {
	"x":0,
	"y":0,
	"width":SCREEN_WIDTH,
	"height":SCREEN_HEIGHT,
	"children":
	(
		{
			"name":"BackGround",
			"type":"expanded_image",
			"x":0,
			"y":0,
			"image":FOLDER + "1.jpg",
			"x_scale":float(SCREEN_WIDTH) / 2560.0,
			"y_scale":float(SCREEN_HEIGHT) / 1665.0,
		},
		{
			"name":"Logo",
			"type":"image",
			"x":0,
			"y":SCREEN_HEIGHT - 250 - 140,
			"horizontal_align":"center",
			"image":FOLDER + "aegon2.png",
		},
		{
			"name":"BackGage",
			"type":"expanded_image",
			"x":0,
			"y":SCREEN_HEIGHT - 110,
			"horizontal_align":"center",
			"image":"interface/controls/special/loading/empty.tga",
		},
		{
			"name":"FullGage",
			"type":"expanded_image",
			"x":0,
			"y":SCREEN_HEIGHT - 110,
			"horizontal_align":"center",
			"image":"interface/controls/special/loading/full.tga",
		},
		{
			"name":"LoadingPercent_Text",
			"type":"text",
			"x":0,
			"y":SCREEN_HEIGHT - 55,
			"text":"",
			"horizontal_align":"center",
		},
	),
}
