#favor manter essa linha
import uiscriptlocale
import _grp as grp

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
			"name":"","type":"text", "color":text_color, "x":20, "y":y+3, "text":"Data","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":70+10, "y":y+3, "text":"Vencedora","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":176+10, "y":y+3, "text":"Pontos","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":176+40+10, "y":y+3, "text":"Online","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":264+15, "y":y+3, "text":"Perderora","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":264+106+15, "y":y+3, "text":"Pontos","outline":1,
		},
		{
			"name":"","type":"text", "color":text_color, "x":264+106+40+15, "y":y+3, "text":"Online","outline":1,
		},
#####################################################################################################################################
		{
			"name":"slot0","type":"barwithbox","color":normal_color,"x":0,"y":33+18*0,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_0_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_0_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_0_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_0_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_0_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_0_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_0_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot1","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*1,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_1_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_1_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_1_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_1_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_1_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_1_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_1_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot2","type":"barwithbox","color":normal_color,"x":0,"y":33+18*2,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_2_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_2_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_2_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_2_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_2_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_2_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_2_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot3","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*3,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_3_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_3_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_3_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_3_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_3_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_3_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_3_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot4","type":"barwithbox","color":normal_color,"x":0,"y":33+18*4,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_4_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_4_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_4_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_4_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_4_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_4_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_4_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot5","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*5,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_5_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_5_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_5_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_5_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_5_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_5_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_5_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot6","type":"barwithbox","color":normal_color,"x":0,"y":33+18*6,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_6_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_6_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_6_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_6_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_6_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_6_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_6_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot7","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*7,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_7_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_7_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_7_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_7_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_7_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_7_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_7_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot8","type":"barwithbox","color":normal_color,"x":0,"y":33+18*8,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_8_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_8_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_8_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_8_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_8_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_8_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_8_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot9","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*9,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_9_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_9_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_9_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_9_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_9_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_9_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_9_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot10","type":"barwithbox","color":normal_color,"x":0,"y":33+18*10,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_10_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_10_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_10_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_10_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_10_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_10_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_10_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot11","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*11,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_11_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_11_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_11_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_11_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_11_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_11_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_11_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot12","type":"barwithbox","color":normal_color,"x":0,"y":33+18*12,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_12_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_12_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_12_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_12_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_12_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_12_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_12_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot13","type":"barwithbox","color":normal_color2,"x":0,"y":33+18*13,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_13_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_13_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_13_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_13_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_13_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_13_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_13_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{
			"name":"slot14","type":"barwithbox","color":normal_color,"x":0,"y":33+18*14,"height":18,"width":width-20,"flash_color": flash_color,"box_color": normal_color2,
			"children":
			(
				{"name":"W_14_Data","type":"text","text":"","x":1, "y":2, "color":online_color,"style":("not_pick",),},
				{"name":"W_14_Guild1","type":"text","text":"","x":70+10, "y":2, "color":winner_color,"style":("not_pick",),},
				{"name":"W_14_Guild1_Pontos","type":"text","text":"","x":192+10, "y":2, "color":winner_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_14_Guild1_Online","type":"text","text":"","x":230+10, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_14_Guild2","type":"text","text":"","x":264+15, "y":2, "color":box_color,"style":("not_pick",),},
				{"name":"W_14_Guild2_Pontos","type":"text","text":"","x":386+15, "y":2, "color":box_color,"text_horizontal_align":"center","style":("not_pick",),},
				{"name":"W_14_Guild2_Online","type":"text","text":"","x":424+15, "y":2, "color":online_color,"text_horizontal_align":"center","style":("not_pick",),},
			),
		},
		{"name":"","type":"verticalseparator", "height":height-31, "x":width-22-187*2 -16, "y":32,},
		{"name":"","type":"verticalseparator", "height":height-31, "x":width-22-187 - 4, "y":32,},
		{"name":"","type":"verticalseparator", "height":height-31, "x":width-22, "y":32,},
	),
}
