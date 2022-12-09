#favor manter essa linha
import uiscriptlocale
import grp

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
hover_color = grp.GenerateColor(0.1, 0.1, 0.1, 0.8)
hover_color2 = grp.GenerateColor(0.05, 0.05, 0.05, 1.0)
text_color = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
color_quest = grp.GenerateColor(0.0, 0.0, 0.0, 0.2)

width = 356
height = 303
y = 8

window = {
	"name":"PainelStaffWindow_GuerraPage",
	"x":8,
	"y":39,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"",
			"type":"horizontalseparator",
			"width":width+2,
			"x":-1,
			"y":50,
		},
		{
			"name":"ScrollBar",
			"type":"new_scrollbar",
			"x":338,
			"y":50,
			"size":245,
		},
	),
}
