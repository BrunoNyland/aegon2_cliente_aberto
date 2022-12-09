#favor manter essa linha
import uiscriptlocale
height = 135
width = 180

window = {
	"name":"ChangeGradeNameDialog",
	"x":0,
	"y":0,
	"style":("movable", "float",),
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"title":uiscriptlocale.GUILD_GRADE_CHANGE_GRADE_NAME,
			"children":
			(
				{
					"name":"GradeNameValue",
					"type":"editboard",
					"width":120, "height":28,
					"x":0, "y":55,
					"horizontal_align":"center",
					"input_limit":8,
					"info":"Digite aqui...",
				},
				{
					"name":"AcceptButton",
					"type":"redbutton",
					"width":68,
					"x":-40,
					"y":height-45,
					"horizontal_align":"center",
					"text":uiscriptlocale.OK,
				},
				{
					"name":"CancelButton",
					"type":"redbutton",
					"width":68,
					"x":40,
					"y":height-45,
					"horizontal_align":"center",
					"text":uiscriptlocale.CANCEL,
				},
			),
		},
	),
}