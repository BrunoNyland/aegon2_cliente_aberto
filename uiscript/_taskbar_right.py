#favor manter essa linha
import grp
interface = "interface/controls/special/taskbar/"
buttons = "interface/controls/common/button/"

right = interface + "right.tga"

width = 255-30-35
height = 59-30

box_color = grp.GenerateColor(0.602362, 0.177165, 0.177165, 1.0)
# box_color = grp.GenerateColor(0.4, 0.4, 0.4, 1.0)
normal_color = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
hover_color = grp.GenerateColor(0.1, 0.1, 0.1, 0.5)

window = {
	"name":"TaskBar_Right",
	"x":SCREEN_WIDTH - width,
	"y":SCREEN_HEIGHT - height,
	"width":width,
	"height":height,
	"children":
	(
		{
			"name":"Base_Board_Right",
			"type":"image",
			"x":0,
			"y":-30,
			"horizontal_align":"center",
			"image":right,
		},
		{
			"name":"Button_Menu",
			# "type":"redbutton",
			# "text":"Menu",
			# "width":50,
			"type":"button",
			"default_image":buttons + "configs/normal.tga",
			"over_image":buttons + "configs/over.tga",
			"down_image":buttons + "configs/down.tga",
			"x":width - 27 - 1,
			"y":2,
		},
		{
			"name":"Button_Friends",
			"type":"button",
			"default_image":buttons + "friends/normal.tga",
			"over_image":buttons + "friends/over.tga",
			"down_image":buttons + "friends/down.tga",
			"x":width - 27 * 2 - 1,
			"y":2,
		},
		{
			"name":"Button_Inventory",
			"type":"button",
			"default_image":buttons + "inventory/normal.tga",
			"over_image":buttons + "inventory/over.tga",
			"down_image":buttons + "inventory/down.tga",
			"x":width - 27 * 3 - 1,
			"y":2,
		},
		{
			"name":"Button_Player",
			"type":"button",
			"default_image":buttons + "player/normal.tga",
			"over_image":buttons + "player/over.tga",
			"down_image":buttons + "player/down.tga",
			"x":width - 27 * 4 - 1,
			"y":2,
		},
		{
			"name":"Button_PKmode",
			"type":"button",
			"default_image":buttons + "pkmode/normal.tga",
			"over_image":buttons + "pkmode/over.tga",
			"down_image":buttons + "pkmode/down.tga",
			"x":width - 27 * 5 - 1,
			"y":2,
		},
		{
			"name":"GoldSlot",
			"type": "barwithbox",
			"width":120, "height":19,
			"color": normal_color,
			"flash_color": hover_color,
			"box_color": box_color,
			"y":6,
			"x":18,
			"children":
			(
				{
					"name":"Gold_Text",
					"type":"text",
					"text":"",
					"x":4,
					"y":-1,
					"horizontal_align":"right",
					"text_horizontal_align":"right",
					"vertical_align":"center",
					"text_vertical_align":"center",
					"style":("not_pick",),
				},
				{"name":"tooltip_gold","type":"ballon","width":60,"text":"","x":0,"y":-38,"hide":1,},
			),
		},
	),
}
