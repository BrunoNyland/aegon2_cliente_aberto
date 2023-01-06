#favor manter essa linha
import uiscriptlocale
import _grp as grp

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
text_color = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)

width = 356
height = 303

y = 15
x = 16
window = {
	"name":"GuildWindow_BoardPage",
	"x":8,
	"y":39,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"BoardScrollBar",
			"type":"new_scrollbar",
			"x":338,
			"y":50,
			"size":245,
		},
		{"name":"", "type":"horizontalseparator", "width":width+2, "x":-1, "y":33,},
		{
			"name":"GradeNumber", "type":"text", "color":box_color, "x":12, "y":y-(x/2), "text":"N°.","fontsize":"LARGE","outline":1,
		},
		{
			"name":"GradeName", "type":"text", "color":box_color, "x":45, "y":y-(x/2), "text":"Posição","fontsize":"LARGE","outline":1,
		},
		{
			"name":"InviteAuthority", "type":"text", "color":box_color, "x":108, "y":y-x, "text":"Recrutar","fontsize":"LARGE","outline":1,
		},
		{
			"name":"DriveOutAuthority", "type":"text", "color":box_color, "x":152, "y":y, "text":"Banir","fontsize":"LARGE","outline":1,
		},
		{
			"name":"NoticeAuthority", "type":"text", "color":box_color, "x":186, "y":y-x, "text":"Postar","fontsize":"LARGE","outline":1,
		},
		{
			"name":"SkillAuthority", "type":"text", "color":box_color, "x":228, "y":y, "text":"Skill","fontsize":"LARGE","outline":1,
		},
		{
			"name":"WarAuthority", "type":"text", "color":box_color, "x":265, "y":y-x, "text":"War","fontsize":"LARGE","outline":1,
		},
		{
			"name":"SafeboxAuthority", "type":"text", "color":box_color, "x":299, "y":y, "text":"Baú","fontsize":"LARGE","outline":1,
		},
	),
}
