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

window = {
	"name":"GuildWindow_BoardPage",
	"x":8,
	"y":39,
	"width":width,
	"height":height,
	"children":
	(
## SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES ##
		{"name":"", "type":"horizontalseparator", "width":width+2, "x":-1, "y":230,},
## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS
		{
			"name":"RefreshButton",
			"type":"button",
			"x":337,
			"y":5,
			"default_image":"d:/ymir work/ui/game/guild/Refresh_Button_01.sub",
			"over_image":"d:/ymir work/ui/game/guild/Refresh_Button_02.sub",
			"down_image":"d:/ymir work/ui/game/guild/Refresh_Button_03.sub",
			"tooltip_text":uiscriptlocale.GUILD_BOARD_REFRESH,
			"hide":1,
		},
## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS## BOTOES ESCONDIDOS
		{
			"name":"PostCommentButton",
			"type":"button",
			"x":337,
			"y":273,
			"default_image":"d:/ymir work/ui/game/taskbar/Send_Chat_Button_01.sub",
			"over_image":"d:/ymir work/ui/game/taskbar/Send_Chat_Button_02.sub",
			"down_image":"d:/ymir work/ui/game/taskbar/Send_Chat_Button_03.sub",
			"tooltip_text":uiscriptlocale.GUILD_GRADE_WRITE,
			"hide":1,
		},
### SCROLBAR ###### SCROLBAR ###### SCROLBAR ###### SCROLBAR ###### SCROLBAR ###### SCROLBAR ###### SCROLBAR ###### SCROLBAR ###
		{
			"name":"CommentScrollBar",
			"type":"new_scrollbar",
			"x":338,
			"y":9,
			"size":215,
		},
### LOCAL DE DIGITAR a MENSAGEM ##### LOCAL DE DIGITAR a MENSAGEM ##### LOCAL DE DIGITAR a MENSAGEM ##### LOCAL DE DIGITAR a MENSAGEM ##
		{
			"name":"CommentSlot",
			"type": "barwithbox",
			"width":345,
			"height":60,
			"color": hover_color2,
			"flash_color": hover_color2,
			"box_color": normal_color,
			"x":0,
			"y":238,
			"horizontal_align":"center",
			"children":
			(
				{
					"name":"Digite",
					"type":"text",
					"text":"Digite aqui sua mensagem...",
					"color":0xffa08784,
					"x":5,
					"y":3,
				},
				{
					"name":"CommentValue",
					"type":"editline",
					"limit_width":340,
					"multi_line":1,
					"color":0xffa08784,
					"text_vertical_align":"center",
					"x":5,
					"y":10,
					"width":330,
					"height":60,
					"input_limit":60,
					"text":"",
				},
			),
		},

	),
}
