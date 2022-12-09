#favor manter essa linha
import uiscriptlocale
import grp

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
normal_color2 = grp.GenerateColor(0.05, 0.0, 0.0, 0.0)

text_color = grp.GenerateColor(1.0, 1.0, 1.0, 1.0)
hover_color = grp.GenerateColor(0.05, 0.05, 0.05, 1.0)
hover_color2 = grp.GenerateColor(0.1, 0.1, 0.1, 0.8)

width = 356
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
			"name":"Ranking_ScrollBar",
			"type":"new_scrollbar",
			"x":338,
			"y":34,
			"size":268,
		},
		{"name":"","type":"horizontalseparator", "width":width+2, "x":-1, "y":30,},
		{
			"name":"","type":"text", "color":box_color, "x":2, "y":y, "text":"N°.","fontsize":"LARGE","outline":1,
		},
		{
			"name":"","type":"text", "color":box_color, "x":33, "y":y, "text":"Nome","fontsize":"LARGE","outline":1,
		},
		{
			"name":"","type":"text", "color":box_color, "x":134+15+6, "y":y+3, "text":"Pontos","outline":1,
		},
		{
			"name":"","type":"text", "color":box_color, "x":178+15+4, "y":y+3, "text":"Vitórias","outline":1,
		},
		{
			"name":"","type":"text", "color":box_color, "x":227+15+2, "y":y+3, "text":"Empates","outline":1,
		},
		{
			"name":"","type":"text", "color":box_color, "x":280+15, "y":y+3, "text":"Derrotas","outline":1,
		},
#####################################################################################################################################
		{
			"name":"slot0","type":"bar","color":normal_color,"x":0,"y":33+18*0,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_0_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_0_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_0_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_0_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_0_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_0_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot2","type":"bar","color":normal_color2,"x":0,"y":33+18*1,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_1_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_1_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_1_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_1_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_1_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_1_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot3","type":"bar","color":normal_color,"x":0,"y":33+18*2,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_2_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_2_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_2_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_2_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_2_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_2_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot4","type":"bar","color":normal_color2,"x":0,"y":33+18*3,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_3_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_3_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_3_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_3_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_3_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_3_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot5","type":"bar","color":normal_color,"x":0,"y":33+18*4,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_4_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_4_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_4_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_4_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_4_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_4_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot6","type":"bar","color":normal_color2,"x":0,"y":33+18*5,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_5_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_5_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_5_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_5_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_5_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_5_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot7","type":"bar","color":normal_color,"x":0,"y":33+18*6,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_6_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_6_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_6_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_6_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_6_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_6_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot8","type":"bar","color":normal_color2,"x":0,"y":33+18*7,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_7_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_7_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_7_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_7_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_7_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_7_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot9","type":"bar","color":normal_color,"x":0,"y":33+18*8,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_8_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_8_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_8_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_8_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_8_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_8_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot10","type":"bar","color":normal_color2,"x":0,"y":33+18*9,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_9_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_9_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_9_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_9_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_9_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_9_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot11","type":"bar","color":normal_color,"x":0,"y":33+18*10,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_10_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_10_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_10_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_10_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_10_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_10_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot12","type":"bar","color":normal_color2,"x":0,"y":33+18*11,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_11_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_11_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_11_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_11_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_11_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_11_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot13","type":"bar","color":normal_color,"x":0,"y":33+18*12,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_12_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_12_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_12_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_12_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_12_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_12_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot14","type":"bar","color":normal_color2,"x":0,"y":33+18*13,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_13_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_13_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_13_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_13_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_13_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_13_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{
			"name":"slot15","type":"bar","color":normal_color,"x":0,"y":33+18*14,"height":18,"width":width-20,
			"children":
			(
				{"name":"RK_14_Pos","type":"text","text":"","x":1, "y":2, "color":0xffffffff,},
				{"name":"RK_14_Nome","type":"text","text":"","x":33, "y":2, "color":0xffffffff,},
				{"name":"RK_14_Pontos","type":"text","text":"","x":151+15+6, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_14_Vitorias","type":"text","text":"","x":199+15+4, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_14_Empates","type":"text","text":"","x":249+15+2, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
				{"name":"RK_14_Derrotas","type":"text","text":"","x":300+15, "y":2, "color":0xffffffff,"text_horizontal_align":"center",},
			),
		},
		{"name":"","type":"verticalseparator", "height":height-31, "x":width-22, "y":32,},
	),
}
