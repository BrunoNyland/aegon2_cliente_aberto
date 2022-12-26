#favor manter essa linha
interface = "interface/controls/special/taskbar/"

center = interface + "center.tga"

slot = "interface/controls/common/slot_ellipse/slot.tga"
slot_vazio = "interface/controls/common/slot_ellipse/slot_vazio.tga"

width = 440
height = 45

x_slot = 13
y_slot = -3

image_mask_left = interface + "mask_left.tga"
image_mask_right = interface + "mask_right.tga"

window = {
	"name":"TaskBar",
	"x":SCREEN_WIDTH/2 - width/2,
	"y":SCREEN_HEIGHT - height,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Base_Board_01",
			"type":"image",
			"x":0,
			"y":-38,
			"horizontal_align":"center",
			"image":center,
			"children":
			(
				{"name":"","type":"image","image":slot,"x":68+x_slot,"y":39+y_slot},
				{"name":"","type":"image","image":slot,"x":68+42+x_slot,"y":39+y_slot},
				{"name":"","type":"image","image":slot,"x":68+42*2+x_slot,"y":39+y_slot},
				{"name":"","type":"image","image":slot,"x":68+42*3+x_slot,"y":39+y_slot},

				{"name":"","type":"image","image":slot,"x":288-x_slot,"y":39+y_slot},
				{"name":"","type":"image","image":slot,"x":288+42-x_slot,"y":39+y_slot},
				{"name":"","type":"image","image":slot,"x":288+42*2-x_slot,"y":39+y_slot},
				{"name":"","type":"image","image":slot,"x":288+42*3-x_slot,"y":39+y_slot},
			),
		},
		{
			"name":"quickslot_board",
			"type":"window",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"quick_slot_1",
					"type":"grid_table_elipse",
					"start_index":0,
					"x":27+4+x_slot,
					"y":1+4+y_slot,
					"x_count":4,
					"y_count":1,
					"x_step":42,
					"y_step":42,
					"image":slot_vazio,
					"image_r":1.0,
					"image_g":1.0,
					"image_b":1.0,
					"image_a":1.0,
					"children":
					(
						{ "name":"slot_1", "type":"image", "x":-1+42*0, "y":-1, "image":"d:/ymir work/ui/game/taskbar/1.sub", },
						{ "name":"slot_2", "type":"image", "x":-1+42*1, "y":-1, "image":"d:/ymir work/ui/game/taskbar/2.sub", },
						{ "name":"slot_3", "type":"image", "x":-1+42*2, "y":-1, "image":"d:/ymir work/ui/game/taskbar/3.sub", },
						{ "name":"slot_4", "type":"image", "x":-1+42*3, "y":-1, "image":"d:/ymir work/ui/game/taskbar/4.sub", },
					),
				},
				{
					"name":"quick_slot_2",
					"type":"grid_table_elipse",
					"start_index":4,
					"x":247+4-x_slot,
					"y":1+4+y_slot,
					"x_count":4,
					"y_count":1,
					"x_step":42,
					"y_step":42,
					"image":slot_vazio,
					"image_r":1.0,
					"image_g":1.0,
					"image_b":1.0,
					"image_a":1.0,
					"children":
					(
						{ "name":"slot_5", "type":"image", "x":-1+42*0, "y":-1, "image":"d:/ymir work/ui/game/taskbar/f1.sub", },
						{ "name":"slot_6", "type":"image", "x":-1+42*1, "y":-1, "image":"d:/ymir work/ui/game/taskbar/f2.sub", },
						{ "name":"slot_7", "type":"image", "x":-1+42*2, "y":-1, "image":"d:/ymir work/ui/game/taskbar/f3.sub", },
						{ "name":"slot_8", "type":"image", "x":-1+42*3, "y":-1, "image":"d:/ymir work/ui/game/taskbar/f4.sub", },
					),
				},
			),
		},
###################################################################################################
### MASCARA DAS OPÇÕES DE MOUSE ### MASCARA DAS OPÇÕES DE MOUSE ### MASCARA DAS OPÇÕES DE MOUSE ###
###################################################################################################
		{
			"name":"mask_left",
			"type":"image",
			"x":39,
			"y":-5,
			"image":image_mask_left,
			"hide":1,
			"children":
			(
				{
					"name":"Camera",
					"type":"button",
					"default_image":interface + "btn_camera_01_normal.tga",
					"over_image":interface + "btn_camera_02_hover.tga",
					"down_image":interface + "btn_camera_03_active.tga",
					"x":35*3,
					"y":0,
					"vertical_align":"center",
					"children":
					(
						{"name":"","type":"ballon","width":70,"text":"Girar Câmera","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
					),
				},
				{
					"name":"AtqNormal",
					"type":"button",
					"default_image":interface + "btn_attacknormal_01_normal.tga",
					"over_image":interface + "btn_attacknormal_02_hover.tga",
					"down_image":interface + "btn_attacknormal_03_active.tga",
					"x":35*2,
					"y":0,
					"vertical_align":"center",
					"children":
					(
						{"name":"","type":"ballon","width":70,"text":"Ataque Normal","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
					),
				},
				{
					"name":"AtqAuto",
					"type":"button",
					"default_image":interface + "btn_attackauto_01_normal.tga",
					"over_image":interface + "btn_attackauto_02_hover.tga",
					"down_image":interface + "btn_attackauto_03_active.tga",
					"x":35*1,
					"y":0,
					"vertical_align":"center",
					"children":
					(
						{"name":"","type":"ballon","width":70,"text":"Ataque Automático","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
					),
				},
			),
		},
##################################################################################################################
		{
			"name":"mask_right",
			"type":"image",
			"x":233,
			"y":-5,
			"hide":1,
			"image":image_mask_right,
			"children":
			(
				{
					"name":"1",
					"type":"button",
					"default_image":interface + "btn_slotpageone_01_normal.tga",
					"over_image":interface + "btn_slotpageone_02_hover.tga",
					"down_image":interface + "btn_slotpageone_03_active.tga",
					"x":167 - 35 - 5,
					"y":0,
					"vertical_align":"center",
					"children":
					(
						{"name":"","type":"ballon","width":70,"text":"Slots 1","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
					),
				},
				{
					"name":"2",
					"type":"button",
					"default_image":interface + "btn_slotpagetwo_01_normal.tga",
					"over_image":interface + "btn_slotpagetwo_02_hover.tga",
					"down_image":interface + "btn_slotpagetwo_03_active.tga",
					"x":167 - 35*2 - 5,
					"y":0,
					"vertical_align":"center",
					"children":
					(
						{"name":"","type":"ballon","width":70,"text":"Slots 2","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
					),
				},
				{
					"name":"3",
					"type":"button",
					"default_image":interface + "btn_slotpagethree_01_normal.tga",
					"over_image":interface + "btn_slotpagethree_02_hover.tga",
					"down_image":interface + "btn_slotpagethree_03_active.tga",
					"x":167 - 35*3 - 5,
					"y":0,
					"vertical_align":"center",
					"children":
					(
						{"name":"","type":"ballon","width":70,"text":"Slots 3","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
					),
				},
				{
					"name":"4",
					"type":"button",
					"default_image":interface + "btn_slotpagefour_01_normal.tga",
					"over_image":interface + "btn_slotpagefour_02_hover.tga",
					"down_image":interface + "btn_slotpagefour_03_active.tga",
					"x":167 - 35*4 - 5,
					"y":0,
					"vertical_align":"center",
					"children":
					(
						{"name":"","type":"ballon","width":70,"text":"Slots 4","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
					),
				},
			),
		},
##################################################################################################################
		{
			"name":"ChatButton",
			"type":"button",
			"x":0,
			"y":12,
			"default_image":interface + "chat_button_normal.tga",
			"over_image":interface + "chat_button_over.tga",
			"down_image":interface + "chat_button_down.tga",
			"horizontal_align":"center",
			"children":
			(
				{"name":"tipchat","type":"ballon","width":70,"text":"Abrir Chat","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
			),
		},
		{
			"name":"QuickSlotNumberButton",
			"type":"button",
			"x":194,
			"y":12,
			"default_image":interface + "btn_slotpageone_01_normal.tga",
			"over_image":interface + "btn_slotpageone_02_hover.tga",
			"down_image":interface + "btn_slotpageone_03_active.tga",
			"horizontal_align":"center",
			"children":
			(
				{"name":"","type":"ballon","width":70,"text":"Páginas de Slots","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
			),
		},
		{
			"name":"LeftMouseButtonNew",
			"type":"button",
			"x":-194,
			"y":12,
			"default_image":interface + "btn_attacknormal_01_normal.tga",
			"over_image":interface + "btn_attacknormal_02_hover.tga",
			"down_image":interface + "btn_attacknormal_03_active.tga",
			"horizontal_align":"center",
			"children":
			(
				{"name":"","type":"ballon","width":70,"text":"Ação do Mouse","x":0,"y":-40,"horizontal_align":"center","istooltip":1,"hide":1,},
			),
		},
	),
}
