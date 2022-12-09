#favor manter essa linha
import uiscriptlocale

interface = "interface/controls/special/guild/"
LINE = "interface/controls/common/horizontal_bar/center.tga"

width = 356
height = 303

window = {
	"name":"GuildWindow_GuildSkillPage",
	"x":8,
	"y":39,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Active_Skill_Title",
			"type":"expanded_image",
			"image":LINE,
			"x":0,
			"y":15,
			"x_scale":1.2,
			"y_scale":1.0,
			"horizontal_align":"center",
			"children":
			(
				{
					"name":"Active_Skill_Title_Text",
					"type":"text",
					"text":"Habilidades da Guild",
					"color":0xfff8d090,
					"x":0,
					"y":-5,
					"all_align":"center",
				},
			),
		},
		{
			"name":"Skill_Plus_Value",
			"type":"text",
			"x":0,
			"y":55,
			"text":"99",
			"color": 0xffa08784,
			"horizontal_align":"center",
			"text_horizontal_align":"center",
		},
		{
			"name":"slots_skills_images",
			"type":"window",
			"width":0,
			"height":0,
			"x":65,
			"y":85,
			"children":
			(
				{"name":"","type":"image","image":"interface/controls/common/slot_ellipse/slot.tga","x":0,"y":0,},
				{"name":"","type":"image","image":"interface/controls/common/slot_ellipse/slot.tga","x":41,"y":0,},
				{"name":"","type":"image","image":"interface/controls/common/slot_ellipse/slot.tga","x":82,"y":0,},
				{"name":"","type":"image","image":"interface/controls/common/slot_ellipse/slot.tga","x":123,"y":0,},
				{"name":"","type":"image","image":"interface/controls/common/slot_ellipse/slot.tga","x":164,"y":0,},
				{"name":"","type":"image","image":"interface/controls/common/slot_ellipse/slot.tga","x":205,"y":0,},
			),
		},
		{
			"name":"Active_Skill_Slot_Table",
			"type":"grid_table_elipse",
			"x":65+4,
			"y":85+4,
			"start_index":210,
			"x_count":6,
			"y_count":1,
			"x_step":41,
			"y_step":41,
			"image":"interface/controls/common/slot_ellipse/slot_vazio.tga"
		},
## SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES ##
		{"name":"", "type":"horizontalseparator", "width":width+2, "x":-1, "y":140,},
## GAUGE ENERGIA #### GAUGE ENERGIA #### GAUGE ENERGIA #### GAUGE ENERGIA #### GAUGE ENERGIA #### GAUGE ENERGIA ##
		{
			"name":"Dragon_God_Power_Title",
			"type":"expanded_image",
			"image":LINE,
			"x":0,
			"y":155,
			"x_scale":1.2,
			"y_scale":1.0,
			"horizontal_align":"center",
			"children":
			(
				{
					"name":"Dragon_God_Power_Title_Text",
					"type":"text",
					"text":"Energia",
					"color":0xfff8d090,
					"x":0,
					"y":-5,
					"all_align":"center",
				},
			),
		},
		{
			"name":"Dragon_God_Power_Value",
			"type":"text",
			"x":0,
			"y":195,
			"color": 0xffa08784,
			"horizontal_align":"center",
			"text_horizontal_align":"center",
			"text":"3000 / 3000",
		},
		{
			"name":"Dragon_God_Power_Gauge_Slot",
			"type":"image",
			"x":0,
			"y":220,
			"horizontal_align":"center",
			"image":interface + "energy_gauge_empty.tga",
			"children":
			(
				{
					"name":"Dragon_God_Power_Gauge",
					"type":"expanded_image",
					"x":0,
					"y":0,
					"image":interface + "energy_gauge_full.tga",
				},
			),
		},
## SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES #### SEPARADORES ##
		# {"name":"", "type":"horizontalseparator", "width":width+2, "x":-1, "y":250,},
		{
			"name":"Heal_GSP_Button",
			"type":"redbutton",
			"width":100,
			"x":0,
			"y":265,
			"horizontal_align":"center",
			"text":uiscriptlocale.GUILD_SKIlL_HEAL_GSP,
		},
	),
}
