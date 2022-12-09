#favor manter essa linha
import uiscriptlocale

interface = "interface/controls/special/minimap/"
minimap = interface + "minimap.tga"

width = 136
height = 137
taskbar_width = 440
image_width = 226
image_heigth = 158

window = {
	"name":"MiniMap",
	"y":0,
	"x":SCREEN_WIDTH - width,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"MiniMapShowButton",
			"type":"button",
			"hide":1,
			"x":0,
			"y":0,
			"default_image":interface + "show_button_normal.tga",
			"over_image":interface + "show_button_over.tga",
			"down_image":interface + "show_button_down.tga",
		},
		{
			"name":"OpenWindow",
			"type":"window",
			"x":0,
			"y":0,
			"width":width,
			"height":height,
			"children":
			(
				{
					"name":"OpenWindowBGI",
					"type":"image",
					"x":0,
					"y":0,
					"image":minimap,
				},
				{
					"name":"MiniMapWindow",
					"type":"window",
					"x":19,
					"y":-2,
					"width":128,
					"height":128,
				},
				{
					"name":"ScaleUpButton",
					"type":"button",
					"x":101,
					"y":118,
					"default_image":interface + "btn_zoomin_01_normal.tga",
					"over_image":interface + "btn_zoomin_02_hover.tga",
					"down_image":interface + "btn_zoomin_03_active.tga",
				},
				{
					"name":"ScaleDownButton",
					"type":"button",
					"x":115,
					"y":104,
					"default_image":interface + "btn_zoomout_01_normal.tga",
					"over_image":interface + "btn_zoomout_02_hover.tga",
					"down_image":interface + "btn_zoomout_03_active.tga",
				},
				{
					"name":"MiniMapHideButton",
					"type":"button",
					"x":111,
					"y":6,
					"default_image":interface + "btn_close_normal.tga",
					"over_image":interface + "btn_close_over.tga",
					"down_image":interface + "btn_close_down.tga",
				},
				{
					"name":"AtlasShowButton",
					"type":"button",
					"x":12,
					"y":12,
					"default_image":interface + "btn_atlas_01_normal.tga",
					"over_image":interface + "btn_atlas_02_hover.tga",
					"down_image":interface + "btn_atlas_03_active.tga",
				},
				{
					"name":"ServerInfo",
					"type":"text",
					"text_horizontal_align":"center",
					"outline":1,
					"x":70,
					"y":140,
					"text":"",
					"hide":1,
				},
				{
					"name":"PositionInfo",
					"type":"text",
					"text_horizontal_align":"center",
					"outline":1,
					"x":70,
					"y":160,
					"text":"",
					"hide":1,
				},
				{
					"name":"ObserverCount",
					"type":"text",
					"text_horizontal_align":"center",
					"outline":1,
					"x":70,
					"y":180,
					"text":"",
				},
				{
					"name":"MastWindow",
					"type":"thinboard",
					"x":35,
					"y":160,
					"width":105,
					"height":37,
					"children":
					(
						{
							"name":"MastText",
							"type":"text",
							"text_horizontal_align":"center",
							"x":35,
							"y":8,
							"text":uiscriptlocale.DEFANCE_WAWE_MAST_TEXT,
						},
						{
							"name":"MastHp",
							"type":"gauge",
							"x":10,
							"y":23,
							"width":85,
							"color":"red",
							"tooltip_text":uiscriptlocale.DEFANCE_WAWE_GAUGE_TOOLTIP,
						},
					),
				},
			),
		},
	),
}