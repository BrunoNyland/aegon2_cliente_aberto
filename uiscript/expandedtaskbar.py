ROOT = "d:/ymir work/ui/game/"

window = {
	"name" : "ExpandTaskBar",
	"x" : SCREEN_WIDTH/2 - 5,
	"y" : SCREEN_HEIGHT - 74,
	"width" : 37,
	"height" : 37,
	"children" :
	(
		{
			"name" : "ExpanedTaskBar_Board",
			"type" : "window",
			"x" : 0,
			"y" : 0,
			"width" : 37,
			"height" : 37,
			"children" :
			(
				{
					"name" : "DragonSoulButton",
					"type" : "button",
					"x" : 0,
					"y" : 0,
					"width" : 37,
					"height" : 37,
					"default_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_03.tga",
				},
			),
		},
	),
}