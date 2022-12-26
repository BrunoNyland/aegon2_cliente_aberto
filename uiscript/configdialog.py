#favor manter essa linha
import uiscriptlocale

width = 430
height = 358

CHARACTER = "interface/controls/special/character/"
LINE = "interface/controls/common/horizontal_bar/center.tga"

window = {
	"name":"SystemOptionDialog",
	"style":("movable", "float",),
	"x":0,
	"y":0,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"board",
			"type":"new_board_with_titlebar",
			"x":0,
			"y":0,
			"title":"Configurações",
			"width":width,
			"height":height,
			"children":
			(
###################### SELETOR DE PÁGINA ###################### SELETOR DE PÁGINA ###################### SELETOR DE PÁGINA ######################
				{
					"name":"Options",
					"type":"window",
					"x":width-148,
					"y":35,
					"width":151,
					"height":height-35,
					"children":
					(
						{
							"name":"vertical_separator",
							"type":"verticalseparator",
							"height":height-45,
							"x":1,
							"y":3,
						},
						{
							"name":"Tab_Button_01",
							"type":"redbutton",
							"width":133,
							"text":"Áudio",
							"x":6,
							"y":6,
						},
						{
							"name":"Tab_Button_02",
							"type":"redbutton",
							"width":133,
							"text":"Câmera",
							"x":6,
							"y":6+32,
						},
						{
							"name":"Tab_Button_03",
							"type":"redbutton",
							"width":133,
							"text":"Janela",
							"x":6,
							"y":6+32*2,
						},
						{
							"name":"Tab_Button_04",
							"type":"redbutton",
							"width":133,
							"text":"Exibir",
							"x":6,
							"y":6+32*3,
						},
						{
							"name":"Tab_Button_05",
							"type":"redbutton",
							"width":133,
							"text":"Modo PvP",
							"x":6,
							"y":6+32*4,
						},
						{
							"name":"Tab_Button_06",
							"type":"redbutton",
							"width":133,
							"text":"Permitir",
							"x":6,
							"y":6+32*5,
						},
					),
				},
###################### PAGINA DE AUDIO ###################### PAGINA DE AUDIO ###################### PAGINA DE AUDIO ######################
				{
					"name":"Audio_Page",
					"type":"window",
					"width":width-156-12,
					"height":height - 35,
					"x":12-5,
					"y":35,
					"children":
					(
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":10,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Configurações de Aúdio",
									"x":0,
									"y":-5,
									"all_align":"center",
								},
							),
						},
						{
							"name":"vol_audio",
							"type":"window",
							"width":width - 156 - 12,
							"height":50,
							"x":0,
							"y":50,
							"children":
							(
								{"name":"audio_slider","type":"slider","width":160,"x":0,"y":23,"horizontal_align":"center",},
								{"name":"audio_slider_title","type":"text","text":"|cffa08784Volume Geral","x":(width-156-12)/2,"y":10,"text_horizontal_align":"center",},
								{"name":"audio_slider_percent","type":"text","text":"100%","x":width - 156 - 12 - 45,"y":18+3,"fontsize":"LARGE",},
								{"name":"audio_none","type":"image","image":"interface/controls/special/audio/none.tga","x":12,"y":11+4,},
								{"name":"audio_1","type":"image","image":"interface/controls/special/audio/1.tga","x":12,"y":11+4,},
								{"name":"audio_2","type":"image","image":"interface/controls/special/audio/2.tga","x":12,"y":11+4,},
								{"name":"audio_3","type":"image","image":"interface/controls/special/audio/3.tga","x":12,"y":11+4,},
								{"name":"audio_x","type":"image","image":"interface/controls/special/audio/x.tga","x":12,"y":11+4,},
								{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":0,"horizontal_align":"center",},
								{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":50,"horizontal_align":"center",},
							),
						},
						{
							"name":"vol_music",
							"type":"window",
							"width":width - 156 - 12,
							"height":50,
							"x":0,
							"y":100,
							"children":
							(
								{"name":"music_slider","type":"slider","width":130,"x":0,"y":23,"horizontal_align":"center",},
								{"name":"music_slider_title","type":"text","text":"|cffa08784Volume da Música","x":(width-156-12)/2,"y":10,"text_horizontal_align":"center",},
								{"name":"music_slider_percent","type":"text","text":"100%","x":width - 156 - 12 - 45,"y":18+3,"fontsize":"LARGE",},
								{"name":"music_none","type":"image","image":"interface/controls/special/audio/none.tga","x":12,"y":11+4,},
								{"name":"music_1","type":"image","image":"interface/controls/special/audio/1.tga","x":12,"y":11+4,},
								{"name":"music_2","type":"image","image":"interface/controls/special/audio/2.tga","x":12,"y":11+4,},
								{"name":"music_3","type":"image","image":"interface/controls/special/audio/3.tga","x":12,"y":11+4,},
								{"name":"music_x","type":"image","image":"interface/controls/special/audio/x.tga","x":12,"y":11+4,},
								{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":0,"horizontal_align":"center",},
								{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":50,"horizontal_align":"center",},
							),
						},
						{
							"name":"select_music",
							"type":"window",
							"width":width - 156 - 12,
							"height":50,
							"x":0,
							"y":150,
							"children":
							(
								{"name":"","type":"expanded_image","x":95+13-5,"y":16+4,"image":CHARACTER+"text_slot_big.tga","x_scale": 1.5, "y_scale":0.8},
								{"name":"change_music_button","type":"redbutton","text":"Trocar Música","width":95,"x":13+4,"y":7,"vertical_align":"center",},
								{"name":"nome_musica","type":"text","text":"","x":95+13+10,"y":7+16,},
								{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":0,"horizontal_align":"center",},
								{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":50,"horizontal_align":"center",},
							),
						},
					),
				},
###################### PAGINA DE CAMERA ###################### PAGINA DE CAMERA ###################### PAGINA DE CAMERA #########################################
				{
					"name":"Camera_Page",
					"type":"window",
					"width":width-156-12,
					"height":height-35,
					"x":12-5,
					"y":35,
					"children":
					(
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":10,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Configurações da Câmera",
									"x":0,
									"y":-5,
									"all_align":"center",
								},
							),
						},
						{
							"name":"camera_dialog",
							"type":"window",
							"width":width-156-12,
							"height":70,
							"x":0,
							"y":50,
							"children":
							(
								{"name":"camera_max_slider","type":"slider","width":130,"x":0,"y":23,"horizontal_align":"center",},
								{"name":"camera_max_slider_title","type":"text","text":"|cffa08784Distância Máxima","x":(width-156-12)/2,"y":10,"text_horizontal_align":"center",},
								{"name":"camera_max_slider_percent","type":"text","text":"100%","x":width - 156 - 12 - 45,"y":18+3,"fontsize":"LARGE",},
								{"name":"neblina_slider","type":"slider","width":90,"x":0,"y":23+30,"horizontal_align":"center",},
								{"name":"neblina_slider_title","type":"text","text":"|cffa08784Névoa","x":(width-156-12)/2,"y":10+30,"text_horizontal_align":"center",},
								{"name":"neblina_slider_percent","type":"text","text":"100%","x":width - 156 - 12 - 45,"y":18+3+30,"fontsize":"LARGE",},
								{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":70,"horizontal_align":"center",},
							),
						},
						{
							"name":"graficos",
							"type":"window",
							"width":width - 156 - 12,
							"height":200,
							"x":0,
							"y":50+70,
							"children":
							(
								{
									"name":"",
									"type":"image",
									"image":LINE,
									"x":0,
									"y":10,
									"horizontal_align":"center",
									"children":
									(
										{
											"name":"",
											"type":"text",
											"text":"Processamento dos Gráficos",
											"x":0,
											"y":-5,
											"all_align":"center",
										},
									),
								},
								{"name":"gpu_tiling","type":"newradio_button","x":-80+20,"y":45,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784GPU:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"cpu_tiling","type":"newradio_button", "x":0+20,"y":45,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784CPU:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"tiling_apply","type":"redbutton","text":"Aplicar","width":75,"x":80+20,"y":41,"horizontal_align":"center",},
								{
									"name":"",
									"type":"image",
									"image":LINE,
									"x":0,
									"y":75,
									"horizontal_align":"center",
									"children":
									(
										{
											"name":"",
											"type":"text",
											"text":"Qualidade das Sombras",
											"x":0,
											"y":-5,
											"all_align":"center",
										},
									),
								},
								{"name":"sombras_none","type":"newradio_button","x":-60-5,"y":45+75-10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Nenhuma:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"sombras_word","type":"newradio_button", "x":28-5,"y":45+75-10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Baixa:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"sombras_player","type":"newradio_button", "x":120-5,"y":45+75-10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Média:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"sombras_all","type":"newradio_button", "x":-15-5,"y":45+75-10+30,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Alta:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"sombras_all_all","type":"newradio_button", "x":-15-5+92,"y":45+75-10+30,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Altíssima:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
					),
				},
################# PAGINA DE DISPLAY ################# PAGINA DE DISPLAY ################# PAGINA DE DISPLAY ################# PAGINA DE DISPLAY ################# PAGINA DE DISPLAY 
				{
					"name":"Display_Page",
					"type":"window",
					"width":width-156-12,
					"height":height-35,
					"x":12-5,
					"y":35,
					"children":
					(
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":10,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Resolução do Jogo",
									"x":0,
									"y":-5,
									"all_align":"center",
								},
							),
						},
						{"name":"resolucao_slider","type":"slider","width":200,"x":0,"y":40+20,"horizontal_align":"center",},
						{"name":"resolucao_slider_title","type":"text","text":"800:600","x":(width-156-12)/2,"y":40,"text_horizontal_align":"center","fontsize":"LARGE",},
						{"name":"resolucao_imagem","type":"expanded_image","image":"interface/controls/special/config/resolution.tga","x":0,"y":40+40,"horizontal_align":"center","x_scale":0.8,"y_scale":0.8,},
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":170,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Modo da Janela",
									"x":0,
									"y":-5,
									"all_align":"center",
								},
							),
						},
						{"name":"modo_janela","type":"newradio_button","x":-60+20,"y":170+40,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Janela:","x":-5,"y":2,"text_horizontal_align":"right",},),},
						{"name":"modo_fullscreen","type":"newradio_button", "x":60+20,"y":170+40,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Tela Cheia:","x":-5,"y":2,"text_horizontal_align":"right",},),},
						{"name":"aplicar_resolucao","type":"redbutton","text":"Aplicar","width":70,"x":190,"y":180+60+36,},
					),
				},
################# PAGINA DE PLAYER ################# PAGINA DE PLAYER ################# PAGINA DE PLAYER ################# PAGINA DE PLAYER ##################
				{
					"name":"Player_Page",
					"type":"window",
					"width":width - 156 - 12,
					"height":height - 35,
					"x":12-5,
					"y":35,
					"children":
					(
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":10,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Configurações de Exibição",
									"x":0,
									"y":-5,
									"all_align":"center",
								},
							),
						},
						{
							"name": "name_color_config",
							"type": "window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*0,
							"children":
							(
								{"name":"","type":"expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"name_color_text","type":"text","text":"Cor do Nome:","x":0,"y":12,},
								{"name":"name_color_normal","type":"newradio_button","x":20,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Normal:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"name_color_empire","type":"newradio_button","x":110,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Reino:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name": "target_board_config",
							"type": "window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*1,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"target_board_text","type":"text","text":"Mostrar Alvo:","x":0,"y":12,},
								{"name":"target_board_view","type":"newradio_button","x":20,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Exibir:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"target_board_no_view","type":"newradio_button","x":110,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Ocultar:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name": "view_chat_config",
							"type": "window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*2,
							"children":
							(
								{"name":"","type":"expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"view_chat_text","type":"text","text":"Mostrar Chat:","x":0,"y":12,},
								{"name":"view_chat_on_button","type":"newradio_button","x":20,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Exibir:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"view_chat_off_button","type":"newradio_button","x":110,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Ocultar:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"salestext_config",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*3,
							"children":
							(
								{"name":"","type":"expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"salestext_text","type":"text","text":"Mostrar Lojas:","x":0,"y":12,},
								{"name":"salestext_on_button","type":"newradio_button","x":20,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Exibir:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"salestext_off_button","type":"newradio_button","x":110,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Ocultar:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"show_damage_config",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*4,
							"children":
							(
								{"name":"","type":"expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"show_damage_text","type":"text","text":"Mostrar Dano:","x":0,"y":12,},
								{"name":"show_damage_on_button","type":"newradio_button","x":20,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Exibir:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"show_damage_off_button","type":"newradio_button","x":110,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Ocultar:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name": "show_yang_config",
							"type": "window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*5,
							"children":
							(
								{"name":"","type":"expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"show_yang_text","type":"text","text":"Mostrar Yang:","x":0,"y":12,},
								{"name":"show_yang_on_button","type":"newradio_button","x":20,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Exibir:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"show_yang_off_button","type":"newradio_button","x":110,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Ocultar:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name": "always_show_nameconfig",
							"type": "window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*6,
							"children":
							(
								{"name":"","type":"expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"always_show_name_text","type":"text","text":"Mostrar Nomes:","x":0,"y":12,},
								{"name":"always_show_name_on_button","type":"newradio_button","x":20,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Sempre:","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"always_show_name_off_button","type":"newradio_button","x":110,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Tecla Alt:","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":40,"horizontal_align":"center",},
					),
				},
################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE ################# PVP MODE
				{
					"name":"PvP_Page",
					"type":"window",
					"width":width - 156 - 12,
					"height":height - 35,
					"x":12-5,
					"y":35,
					"children":
					(
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":10,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":"Modo de Jogo [PvP Mode]",
									"x":0,
									"y":-5,
									"all_align":"center",
								},
							),
						},
						{
							"name":"pvp_peace","type":"newradio_button","x":10+40*1,"y":60+45*0,
							"children":
							(
								{"name":"","type":"text","text":"|cffa08784Pacífico","x":25,"y":2,"text_horizontal_align":"left",},
								{
									"name":"pvp_peace_descript",
									"type":"thinboardnew",
									"width":width - 156 -10,
									"height":90,
									"x":1-(10+40*1),
									"y":230-(60+45*0),
									"children":
									(
										{"name":"pvp_peace_1","type":"text","x":(width - 156 -10)/2,"y":20-5,"text_horizontal_align":"center","text":"|cfff98784Permite atacar apenas jogadores","fontsize":"LARGE",},
										{"name":"pvp_peace_2","type":"text","x":(width - 156 -10)/2,"y":20*2-5,"text_horizontal_align":"center","text":"|cfff98784dos Reinos Inimigos.","fontsize":"LARGE",},
									),
								},
							),
						},
						{
							"name":"pvp_revenge","type":"newradio_button","x":10+40*2,"y":60+45*1,
							"children":
							(
								{"name":"","type":"text","text":"|cffa08784Vingança","x":25,"y":2,"text_horizontal_align":"left",},
								{
									"name":"pvp_revenge_descript",
									"type":"thinboardnew",
									"width":width - 156 -10,
									"height":90,
									"x":1-(10+40*2),
									"y":230-(60+45*1),
									"children":
									(
										{"name":"pvp_revenge_1","type":"text","x":(width - 156 -10)/2,"y":20-5,"text_horizontal_align":"center","text":"|cfff98784Permite atacar os jogadores","fontsize":"LARGE",},
										{"name":"pvp_revenge_2","type":"text","x":(width - 156 -10)/2,"y":20*2-5,"text_horizontal_align":"center","text":"|cfff98784que estiverem com pontos","fontsize":"LARGE",},
										{"name":"pvp_revenge_3","type":"text","x":(width - 156 -10)/2,"y":20*3-5,"text_horizontal_align":"center","text":"|cfff98784de Honra Negativa.","fontsize":"LARGE",},
									),
								},
							),
						},
						{
							"name":"pvp_guild",	"type":"newradio_button","x":10+40*3,"y":60+45*2,
							"children":
							(
								{"name":"","type":"text","text":"|cffa08784Guild","x":25,"y":2,"text_horizontal_align":"left",},
								{
									"name":"pvp_guild_descript",
									"type":"thinboardnew",
									"width":width - 156 -10,
									"height":90,
									"x":1-(10+40*3),
									"y":230-(60+45*2),
									"children":
									(
										{"name":"pvp_guild_1","type":"text","x":(width - 156 -10)/2,"y":20*1-5,"text_horizontal_align":"center","text":"|cfff98784Permite atacar todos Jogadores","fontsize":"LARGE",},
										{"name":"pvp_guild_2","type":"text","x":(width - 156 -10)/2,"y":20*2-5,"text_horizontal_align":"center","text":"|cfff98784que não forem da sua Guild.","fontsize":"LARGE",},
									),
								},
							),
						},
						{
							"name":"pvp_free","type":"newradio_button","x":10+40*4,"y":60+45*3,
							"children":
							(
								{"name":"","type":"text","text":"|cffa08784Livre","x":25,"y":2,"text_horizontal_align":"left",},
								{
									"name":"pvp_free_descript",
									"type":"thinboardnew",
									"width":width - 156 -10,
									"height":90,
									"x":1-(10+40*4),
									"y":230-(60+45*3),
									"children":
									(
										{"name":"pvp_free_1","type":"text","x":(width - 156 -10)/2,"y":20*1-5,"text_horizontal_align":"center","text":"|cfff98784Permite Atacar a Todos Jogadores","fontsize":"LARGE",},
										{"name":"pvp_free_2","type":"text","x":(width - 156 -10)/2,"y":20*2-5,"text_horizontal_align":"center","text":"|cfff98784Você pode perder Honra.","fontsize":"LARGE",},
									),
								},
							),
						},
					),
				},
################# BLOCK PAGE ################# BLOCK PAGE ################# BLOCK PAGE ################# BLOCK PAGE ################# BLOCK PAGE ################# BLOCK PAGE ################# BLOCK PAGE 
				{
					"name":"Block_Page",
					"type":"window",
					"width":width - 156 - 12,
					"height":height - 35,
					"x":12-5,
					"y":35,
					"children":
					(
						{
							"name":"",
							"type":"image",
							"image":LINE,
							"x":0,
							"y":10,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"",
									"type":"text",
									"text":" Bloquear ou Liberar Solicitações",
									"x":0,
									"y":-5,
									"all_align":"center",
								},
							),
						},
						{
							"name":"BlockExchange",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*0,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"BlockExchange_text","type":"text","text":"Abrir Negociações:","x":0,"y":12,},
								{"name":"BlockExchange_on_button","type":"newradio_button","x":115,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Liberar","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"BlockExchange_off_button","type":"newradio_button","x":45,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Bloquear","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"BlockParty",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*1,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"BlockParty_text","type":"text","text":"Convites para Grupos:","x":0,"y":12,},
								{"name":"BlockParty_on_button","type":"newradio_button","x":115,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Liberar","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"BlockParty_off_button","type":"newradio_button","x":45,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Bloquear","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"BlockGuild",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*3,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"BlockGuild_text","type":"text","text":"Convite para Guilds:","x":0,"y":12,},
								{"name":"BlockGuild_on_button","type":"newradio_button","x":115,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Liberar","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"BlockGuild_off_button","type":"newradio_button","x":45,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Bloquear","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"BlockWhisper",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*4,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"BlockWhisper_text","type":"text","text":"Mensagens Privadas:","x":0,"y":12,},
								{"name":"BlockWhisper_on_button","type":"newradio_button","x":115,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Liberar","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"BlockWhisper_off_button","type":"newradio_button","x":45,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Bloquear","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"BlockFriend",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*5,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"BlockFriend_text","type":"text","text":"Solicitação de Amizade:","x":0,"y":12,},
								{"name":"BlockFriend_on_button","type":"newradio_button","x":115,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Liberar","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"BlockFriend_off_button","type":"newradio_button","x":45,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Bloquear","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"BlockPartyRequest",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*2,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"BlockPartyRequest_text","type":"text","text":"Participar de Grupo:","x":0,"y":12,},
								{"name":"BlockPartyRequest_on_button","type":"newradio_button","x":115,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Liberar","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"BlockPartyRequest_off_button","type":"newradio_button","x":45,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Bloquear","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{
							"name":"VerSet",
							"type":"window",
							"width":width - 156 - 12,
							"height":30,
							"x":5,
							"y":42+39*6,
							"children":
							(
								{"name":"","type": "expanded_image","image":CHARACTER+"quest.tga","x":-10,"y":0,"x_scale":1.23,"y_scale":1,},
								{"name":"VerSet_text","type":"text","text":"Mostrar Equipamentos:","x":0,"y":12,},
								{"name":"VerSet_on_button","type":"newradio_button","x":115,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Liberar","x":-5,"y":2,"text_horizontal_align":"right",},),},
								{"name":"VerSet_off_button","type":"newradio_button","x":45,"y":10,"horizontal_align":"center","children":({"name":"","type":"text","text":"|cffa08784Bloquear","x":-5,"y":2,"text_horizontal_align":"right",},),},
							),
						},
						{"name":"","type":"horizontalseparator","width":width-153,"x":7,"y":40,"horizontal_align":"center",},
					),
				},
			),
		},
	),
}
