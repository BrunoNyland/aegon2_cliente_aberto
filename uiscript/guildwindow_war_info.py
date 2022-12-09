#favor manter essa linha
import uiscriptlocale
import grp

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
winner_color = grp.GenerateColor(0.802362, 0.802362, 0.177165, 1.0)
online_color = grp.GenerateColor(0.177165, 0.602362, 0.177165, 1.0)

normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
normal_color2 = grp.GenerateColor(0.05, 0.0, 0.0, 0.0)

text_color = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
hover_color = grp.GenerateColor(0.05, 0.05, 0.05, 1.0)
hover_color2 = grp.GenerateColor(0.1, 0.1, 0.1, 0.8)
flash_color = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

width = 356 + 128
height = 303

y = 5
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
			"name":"War_ScrollBar",
			"type":"new_scrollbar",
			"x":466,
			"y":34,
			"size":268,
		},
		{"name":"","type":"horizontalseparator", "width":width+2, "x":-1, "y":30,},
		{
			"name":"WINNER","type":"text", "color":winner_color, "x":5, "y":y+3, "text":"","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":145, "y":y+3, "text":"Matou","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":190, "y":y+3, "text":"Morreu","outline":1,
		},
		{
			"name":"LOSER","type":"text", "color":box_color, "x":5+233, "y":y+3, "text":"","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":145+233, "y":y+3, "text":"Matou","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":190+233, "y":y+3, "text":"Morreu","outline":1,
		},
#####################################################################################################################################
		{
			"name":"slot0","type":"barwithbox","color":normal_color,"x":0,"y":33+18*0,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_0_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_0_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_0_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_0_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_0_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_0_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot1","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*1,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_1_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_1_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_1_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_1_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_1_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_1_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot2","type":"barwithbox","color":normal_color,"x":0,"y":33+18*2,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_2_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_2_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_2_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_2_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_2_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_2_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot3","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*3,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_3_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_3_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_3_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_3_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_3_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_3_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot4","type":"barwithbox","color":normal_color,"x":0,"y":33+18*4,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_4_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_4_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_4_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_4_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_4_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_4_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot5","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*5,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_5_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_5_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_5_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_5_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_5_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_5_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot6","type":"barwithbox","color":normal_color,"x":0,"y":33+18*6,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_6_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_6_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_6_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_6_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_6_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_6_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot7","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*7,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_7_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_7_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_7_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_7_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_7_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_7_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot8","type":"barwithbox","color":normal_color,"x":0,"y":33+18*8,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_8_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_8_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_8_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_8_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_8_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_8_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot9","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*9,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_9_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_9_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_9_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_9_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_9_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_9_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot10","type":"barwithbox","color":normal_color,"x":0,"y":33+18*10,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_10_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_10_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_10_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_10_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_10_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_10_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot11","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*11,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_11_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_11_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_11_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_11_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_11_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_11_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot12","type":"barwithbox","color":normal_color,"x":0,"y":33+18*12,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_12_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_12_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_12_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_12_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_12_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_12_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot13","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*13,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_13_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_13_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_13_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_13_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_13_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_13_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot14","type":"barwithbox","color":normal_color,"x":0,"y":33+18*14,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_14_Player1","type":"text","text":"","x":5, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_14_Killed1","type":"text","text":"","x":160, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_14_Died1","type":"text","text":"","x":205, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_14_Player2","type":"text","text":"","x":5+233, "y":2, "color":text_color,"style":("not_pick",),},
				{"name":"W_14_Killed2","type":"text","text":"","x":160+233, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_14_Died2","type":"text","text":"","x":205+233, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{"name":"","type":"verticalseparator", "height":height-31, "x":230, "y":32,},
		{"name":"","type":"verticalseparator", "height":height-31, "x":width-22, "y":32,},
	),
}
