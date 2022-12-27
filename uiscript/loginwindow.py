#favor manter essa linha
import grp
import colorinfo
from _uiscript_helper import *

box_color = colorinfo.COR_TEXTO_PADRAO
text_color = colorinfo.COR_TEXTO_PADRAO

saved_accounts_window_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
saved_accounts_button_color = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

FOLDER = 'interface/controls/special/login/'
LINE = 'interface/controls/common/horizontal_bar/center.tga'

window_save_height = 270
window_save_width = 300

painel_height = 270
painel_width = 300

config_height = 600 - 100
config_width = 800 - 100

window = {
	name:'LoginWindow',
	'sytle':('movable',),
	'x':0,
	'y':0,
	'width':SCREEN_WIDTH,
	'height':SCREEN_HEIGHT,
	'children':
	(
		{
			name:'bg',
			type:types.expanded_image,
			expanded_image.x:0,
			expanded_image.y:0,
			expanded_image.horizontal_align:horizontal_align.center,
			expanded_image.x_scale:float(SCREEN_HEIGHT) / 988.0,
			expanded_image.y_scale:float(SCREEN_HEIGHT) / 988.0,
			expanded_image.image:'interface/controls/special/loading/2.jpg',
		},
#################################################################################################################
### LOGIN BOARD ### LOGIN BOARD ### LOGIN BOARD ### LOGIN BOARD ### LOGIN BOARD ### LOGIN BOARD ### LOGIN BOARD #
#################################################################################################################
		{
			name:'LoginBoard',
			type:types.board_transparent,
			x:(SCREEN_WIDTH/2) - (painel_width/2),
			y:(SCREEN_HEIGHT/2) - (painel_height/2) + 20 + 70,
			height:painel_height,
			width:painel_width,
			children:
			(
				{
					name:'Logo',
					type:types.image,
					image.x: 0,
					image.y: -200 - 60,
					image.horizontal_align:align.horizontal.center,
					image.image:'interface/controls/special/loading/aegon2.png',
				},
				{
					name:'Title',
					type:types.text,
					text.text:'Entrar no Jogo',
					text.align.horizontal:'center',
					text.x: 0,
					text.y: 40,
					text.horizontal_align:'center',
					text.fontname:'Verdana:16b',
				},
				{
					name:'ID_EditLine',
					type:'editboard',
					'x': 0, 'y': 100,
					'width':235, 'height':28,
					'horizontal_align':'center',
					'info':'Digite seu Login...',
					'input_limit':16,
					'children':
					(
						{
							name:'Title_ID_EditLine_BG',
							type:types.text,
							text.text:'Conta',
							text.fontname:'Verdana:12b',
							text.align.horizontal:'center',
							text.horizontal_align:'center',
							text.x: 0,
							text.y: -15,
						},
					),
				},
				{
					name:'Password_EditLine',
					type:'editboard',
					'x': 0,
					'y': 100 + 28 + 25,
					'width':235,
					'height':28,
					'horizontal_align':'center',
					'secret_flag':1,
					'info':'Digite sua Senha...',
					'children':
					(
						{
							name:'Title_Password_EditLine_BG',
							type:types.text,
							text.text:'Senha',
							text.align.horizontal:'center',
							text.horizontal_align:'center',
							text.x: 0,
							text.y: -15,
						},
					),
				},
				{
					name:'LoginButton',
					type:'redbutton',
					'x': 60,
					'y': 100 + (28 + 25)*2,
					'horizontal_align':'center',
					'width': 100,
					'text':'Logar',
				},
				{
					name:'LoginExitButton',
					type:'redbutton',
					'x': -60,
					'y': 100 + (28 + 25)*2,
					'horizontal_align':'center',
					'width': 100,
					'text':'Fechar',
				},
			),
		},
#################################################################################################################
### AUTO LOGIN ### AUTO LOGIN ### AUTO LOGIN ### AUTO LOGIN ### AUTO LOGIN ### AUTO LOGIN ### AUTO LOGIN ########
#################################################################################################################
		{
			name:'SavedAccountsWindow',
			type:'barwithbox',
			'box_color': saved_accounts_window_color,
			'color': saved_accounts_window_color,
			'flash_color': saved_accounts_window_color,
			'x': -160,
			'y': -2,
			'width':162, 'height':SCREEN_HEIGHT + 4,
			'children':
			(
				{
					name:'no_one_saved',
					type:'text',
					'color':box_color,
					'text':'Sem contas salvas',
					'x':-2, 'y':20,
					'horizontal_align':'center',
					'align.horizontal':'center',
					'fontname':'Arial:20',
					'outline':1,
					'style':('not_pick',),
					'hide':1,
				},
				{
					name:'account0',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account0_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account0_line2',type:'text','text':'Tecla de Atalho: [F1]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account1',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account1_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account1_line2',type:'text','text':'Tecla de Atalho: [F2]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account2',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*2,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account2_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account2_line2',type:'text','text':'Tecla de Atalho: [F3]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account3',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*3,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account3_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account3_line2',type:'text','text':'Tecla de Atalho: [F4]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account4',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*4,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account4_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account4_line2',type:'text','text':'Tecla de Atalho: [F5]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account5',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*5,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account5_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account5_line2',type:'text','text':'Tecla de Atalho: [F6]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account6',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*6,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account6_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account6_line2',type:'text','text':'Tecla de Atalho: [F7]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account7',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*7,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account7_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account7_line2',type:'text','text':'Tecla de Atalho: [F8]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account8',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*8,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account8_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account8_line2',type:'text','text':'Tecla de Atalho: [F9]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account9',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*9,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account9_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account9_line2',type:'text','text':'Tecla de Atalho: [F10]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account10',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*10,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account10_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account10_line2',type:'text','text':'Tecla de Atalho: [F11]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'account11',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 5 + 43*11,
					'width':155, 'height':40,
					'hide':1,
					'children':
					(
						{name:'account11_line1',type:'text','text':'Conta:','color':box_color,'x':5,'y':5},
						{name:'account11_line2',type:'text','text':'Tecla de Atalho: [F12]','color':box_color,'x':5,'y':12+9},
					)
				},
				{
					name:'AddAccountButton',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 162 - 44,
					'y': SCREEN_HEIGHT - 50,
					'width':40, 'height':40,
					'children':
					(
						{
							name:'text1', type:'text',
							'color':box_color,
							'text':'Adicionar Conta',
							'x':5, 'y':-2,
							'vertical_align':'center',
							'text_vertical_align':'center',
							'fontname':'Verdana:16b',
							'style':('not_pick',),
							'hide':1,
						},
					),
				},
				{
					name:'plus_image',
					type:'image',
					'sytle':('not_pick',),
					'image':'interface/controls/special/autologin/plus_hover.tga',
					'x': 162 - 34 -7,
					'y': SCREEN_HEIGHT - 35 -13,
				},
			),
		},
#################################################################################################################
### WINDOW SAVE ACCOUNT ### WINDOW SAVE ACCOUNT ### WINDOW SAVE ACCOUNT ### WINDOW SAVE ACCOUNT ### WINDOW SAVE #
#################################################################################################################
		{
			name:'SaveAccountBoard',
			type:'new_board_with_titlebar',
			'title':'Salvar Conta',
			'x':(SCREEN_WIDTH/2) - (window_save_width/2),
			'y':(SCREEN_HEIGHT/2) - (window_save_height/2) + 60,
			'width':window_save_width,
			'height':window_save_height,
			'hide':1,
			'children':
			(
				{
					name:'',
					type:'text',
					'text':'Salvando sua conta você vai poder',
					'x':0,'y':45,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'',
					type:'text',
					'text':'entrar no jogo sem digitar seus dados',
					'x':0,'y':45+15,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'',
					type:'text',
					'text':'utilizando a tecla de atalho ou pelo',
					'x':0,'y':45+15*2,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'',
					type:'text',
					'text':'Painel que fica na esquerda desta Tela',
					'x':0,'y':45+15*3,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'SaveAccountID_EditLine',
					type:'editboard',
					'x': 0, 'y': window_save_height - 130,
					'width':235, 'height':28,
					'horizontal_align':'center',
					'info':'Digite seu Login...',
				},
				{
					name:'SaveAccountPassword_EditLine',
					type:'editboard',
					'x': 0, 'y': window_save_height - 85,
					'width':235, 'height':28,
					'horizontal_align':'center',
					'secret_flag':1,
					'info':'Digite sua Senha...',
				},
				{
					name:'SaveAccountButton',
					type:'redbutton',
					'x': 60,
					'y': window_save_height - 40,
					'horizontal_align':'center',
					'width': 100,
					'text':'Salvar',
				},
				{
					name:'SaveAccountCancelButton',
					type:'redbutton',
					'x': -60,
					'y': window_save_height - 40,
					'horizontal_align':'center',
					'width': 100,
					'text':'Cancelar',
				},
			),
		},
#################################################################################################################
### EDIT SAVED ACCOUNT ### EDIT SAVED ACCOUNT ### EDIT SAVED ACCOUNT ### EDIT SAVED ACCOUNT ### EDIT SAVED ACC ##
#################################################################################################################
		{
			name:'EditAccountsMenuBar',
			type:'barwithbox',
			'box_color': saved_accounts_window_color,
			'color': saved_accounts_window_color,
			'flash_color': saved_accounts_window_color,
			'x': 200,
			'y': 200,
			'width':120-50, 'height':60-2,
			'hide':1,
			'children':
			(
				{
					name:'EditAccountButton',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 3,
					'width':114-50, 'height':25,
					'children':
					(
						{name:'',type:'text','text':'Editar','color':box_color,'x':5,'y':5},
					)
				},
				{
					name:'DeleteAccountButton',
					type:'barwithbox',
					'box_color': box_color,
					'color': saved_accounts_window_color,
					'flash_color': saved_accounts_button_color,
					'x': 3,
					'y': 3 + 2 + 25,
					'width':114-50, 'height':25,
					'children':
					(
						{name:'',type:'text','text':'Excluir','color':box_color,'x':5,'y':5},
					)
				},
			),
		},
#################################################################################################################
		{
			name:'DeleteAccountBoard',
			type:'new_board_with_titlebar',
			'title':'Remover conta salva',
			'x':(SCREEN_WIDTH/2) - (300/2),
			'y':(SCREEN_HEIGHT/2) - (80/2) + 20,
			'width':300,
			'height':80,
			'hide':1,
			'children':
			(
				{name:'',type:'text','text':'Tem certeza que deseja remover a conta abaixo?','x':0,'y':42,'horizontal_align':'center','align.horizontal':'center',},
				{name:'DeleteAccountBoardAccount',type:'text','text':'','x':0,'y':42+15,'horizontal_align':'center','align.horizontal':'center','fontsize':'LARGE',},
				{
					name:'DeleteAccountBoardYes',
					type:'redbutton',
					'x': 50,
					'y': 85,
					'horizontal_align':'center',
					'width': 80,
					'text':'Sim',
				},
				{
					name:'DeleteAccountBoardNo',
					type:'redbutton',
					'x': -50,
					'y': 85,
					'horizontal_align':'center',
					'width': 80,
					'text':'Não',
				},
			),
		},
#################################################################################################################
		{
			name:'EditAccountBoard',
			type:'new_board_with_titlebar',
			'title':'Editar conta salva',
			'x':(SCREEN_WIDTH/2) - (window_save_width/2),
			'y':(SCREEN_HEIGHT/2) - (window_save_height/2) + 60,
			'width':window_save_width,
			'height':window_save_height,
			'hide':1,
			'children':
			(
				{
					name:'',
					type:'text',
					'text':'Altere a senha ou conta para',
					'x':0,'y':45,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'',
					type:'text',
					'text':'entrar no jogo sem digitar seus dados',
					'x':0,'y':45+15,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'',
					type:'text',
					'text':'utilizando a tecla de atalho ou pelo',
					'x':0,'y':45+15*2,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'',
					type:'text',
					'text':'Painel que fica na esquerda desta Tela',
					'x':0,'y':45+15*3,
					'horizontal_align':'center',
					'align.horizontal':'center',
				},
				{
					name:'EditAccountBoardID_EditLine',
					type:'editboard',
					'x': 0, 'y': window_save_height - 130,
					'width':235, 'height':28,
					'horizontal_align':'center',
					'info':'Digite seu Login...',
				},
				{
					name:'EditAccountBoard_EditLine',
					type:'editboard',
					'x': 0, 'y': window_save_height - 85,
					'width':235, 'height':28,
					'horizontal_align':'center',
					'secret_flag':1,
					'info':'Digite sua Senha...',
				},
				{
					name:'EditAccountBoardSave',
					type:'redbutton',
					'x': 43,
					'y': window_save_height - 40,
					'horizontal_align':'center',
					'width': 80,
					'text':'Salvar',
				},
				{
					name:'EditAccountBoardCancel',
					type:'redbutton',
					'x': -43,
					'y': window_save_height - 40,
					'horizontal_align':'center',
					'width': 80,
					'text':'Cancelar',
				},
			),
		},
#################################################################################################################
### LINKS ### LINKS ### LINKS ### LINKS ### LINKS ### LINKS ### LINKS ### LINKS ### LINKS ### LINKS ### LINKS ###
#################################################################################################################
		{
			name:'btn_config',
			type:types.button,
			button.x: SCREEN_WIDTH - 38 - 12,
			button.y: SCREEN_HEIGHT - 38 - 12,
			button.default_image:FOLDER + 'config.tga',
			button.over_image:FOLDER + 'config_hover.tga',
			button.down_image:FOLDER + 'config_active.tga',
		},
		{
			name:'board_config',
			type:'new_board_with_titlebar',
			'title':'Configurações',
			'x':(SCREEN_WIDTH/2) - (config_width/2),
			'y':(SCREEN_HEIGHT/2) - (config_height/2),
			'width':config_width,
			'height':config_height,
			'hide':1,
			'children':
			(
				{
					name:'image_1',
					type:'expanded_image',
					'x':40,
					'y':60,
					'horizontal_align':'center',
					'width': 160,
					'height': 120,
					'image':'interface/controls/special/loading/1.jpg',
					'alpha': 0.8,
				},
				# {
					# imagem 2
					# 'x_scale':float(SCREEN_HEIGHT) / 988.0,
					# 'y_scale':float(SCREEN_HEIGHT) / 988.0,
					#types.image:'interface/controls/special/loading/2.jpg',
					# imagem 3
					# 'x_scale':float(SCREEN_HEIGHT) / 1080.0,
					# 'y_scale':float(SCREEN_HEIGHT) / 1080.0,
					#types.image:'interface/controls/special/loading/3.jpg',
				# },
			),
		},
#################################################################################################################
### LOADING FILES### LOADING FILES### LOADING FILES### LOADING FILES### LOADING FILES### LOADING FILES### LOADING
#################################################################################################################
		{
			name:'loadind_files',
			type:types.barwithbox,
			barwithbox.box_color: saved_accounts_window_color,
			barwithbox.color: saved_accounts_window_color,
			barwithbox.flash_color: saved_accounts_window_color,
			barwithbox.x:20,
			barwithbox.y:-50,
			# 'horizontal_align':'center',
			'width':300,
			'height':50,
			# 'hide':1,
			'children':
			(
				{
					name:'in_process',
					type:types.ani_image,
					ani_image.x:5,
					ani_image.y:5,
					ani_image.delay:10,
					ani_image.images:
					(
						FOLDER + 'login/1.png',
						FOLDER + 'login/2.png',
						FOLDER + 'login/3.png',
						FOLDER + 'login/4.png',
						FOLDER + 'login/5.png',
						FOLDER + 'login/6.png',
						FOLDER + 'login/7.png',
						FOLDER + 'login/8.png',
						FOLDER + 'login/9.png',
						FOLDER + 'login/10.png',
						FOLDER + 'login/11.png',
						FOLDER + 'login/12.png',
						FOLDER + 'login/13.png',
						FOLDER + 'login/14.png',
						FOLDER + 'login/15.png',
						FOLDER + 'login/16.png',
					),
				},
				{
					name:'',
					type:types.text,
					text.outline:1,
					text.text:'Carregando proteção...',
					text.fontname:'Verdana:22b',
					text.x:50,
					text.y:-2,
					text.vertical_align:'center',
					text.align.vertical:'center',
				},
			),
		},
	),
}