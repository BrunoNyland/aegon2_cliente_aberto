#favor manter essa linha
import uiscriptlocale
import grp

COLOR_INACTIVE = grp.GenerateColor(1.0, 0.0, 0.0, 0.2)
COLOR_INACTIVE_RARE = grp.GenerateColor(1.0, 0.2, 0.0, 0.2)
COLOR_BG = grp.GenerateColor(0.0, 0.0, 0.0, 0.5)
COLOR_BLACK = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)

width = 62
height = 116

window = {
	"name":"ItemTabBar",
	"x":0, "y":0,
	"width":width,
	"height":height,
	"children":
	(
		{"name":"","type":"bar","x":0,"y":4,"color":COLOR_BLACK,"width":width,"height":15,},
		{"name":"","type":"verticalseparator","height":height,"x":width,"y":3,},
		{"name":"Select", "type":"image", "image":"interface/controls/special/boot/select.tga", "x":28, "y":height+2, "style":("not_pick",),},
		{
			"name":"Close_Button",
			"type":"button",
			"default_image": "interface/controls/special/boot/button_close.tga",
			"over_image": "interface/controls/special/boot/button_close_3.tga",
			"down_image": "interface/controls/special/boot/button_close_2.tga",
			"x": width - 15,
			"y":4,
		},
		{
			"name":"Slot_Name",
			"type":"text",
			"text":"",
			"color":0xfff8d090,
			"x": 1,
			"y": 4,
		},
		{
			"name":"in_process",
			"type":"ani_image",
			"x":17,
			"y":40,
			"delay":4,
			"images":
			(
				"interface/controls/special/boot/ani_big/01.tga",
				"interface/controls/special/boot/ani_big/02.tga",
				"interface/controls/special/boot/ani_big/03.tga",
				"interface/controls/special/boot/ani_big/04.tga",
				"interface/controls/special/boot/ani_big/05.tga",
				"interface/controls/special/boot/ani_big/06.tga",
				"interface/controls/special/boot/ani_big/07.tga",
				"interface/controls/special/boot/ani_big/08.tga",
				"interface/controls/special/boot/ani_big/09.tga",
				"interface/controls/special/boot/ani_big/10.tga",
				"interface/controls/special/boot/ani_big/11.tga",
				"interface/controls/special/boot/ani_big/12.tga",
				"interface/controls/special/boot/ani_big/13.tga",
				"interface/controls/special/boot/ani_big/14.tga",
				"interface/controls/special/boot/ani_big/15.tga",
				"interface/controls/special/boot/ani_big/16.tga",
				"interface/controls/special/boot/ani_big/17.tga",
				"interface/controls/special/boot/ani_big/18.tga",
				"interface/controls/special/boot/ani_big/19.tga",
				"interface/controls/special/boot/ani_big/20.tga",
				"interface/controls/special/boot/ani_big/21.tga",
				"interface/controls/special/boot/ani_big/22.tga",
				"interface/controls/special/boot/ani_big/23.tga",
				"interface/controls/special/boot/ani_big/24.tga",
				"interface/controls/special/boot/ani_big/25.tga",
				"interface/controls/special/boot/ani_big/26.tga",
				"interface/controls/special/boot/ani_big/27.tga",
				"interface/controls/special/boot/ani_big/28.tga",
				"interface/controls/special/boot/ani_big/29.tga",
				"interface/controls/special/boot/ani_big/30.tga",
				"interface/controls/special/boot/ani_big/31.tga",
				"interface/controls/special/boot/ani_big/32.tga",
			),
		},
		# {
			# "name":"warning",
			# "type":"button",
			# "default_image":"interface/controls/special/boot/ani/exclamation.tga",
			# "over_image":"interface/controls/special/boot/ani/exclamation.tga",
			# "down_image":"interface/controls/special/boot/ani/exclamation.tga",
			# "x":5,
			# "y":30,
			# "children":
			# (
				# {
					# "name":"msg",
					# "style":("not_pick",),
					# "type":"thinboardnew",
					# "width":150, "height":50,
					# "x": 0, 
					# "y": -35,
					# "istooltip":1,
					# "hide":1,
					# "horizontal_align":"center",
				# },
			# ),
		# },
		{"name":"ItemIcon","type":"image","x":0,"y": 0,"horizontal_align":"center","vertical_align":"center","image":"icon/item/00010.tga"},
		{
			"name":"StatusBar",
			"type":"bar", "color":COLOR_INACTIVE,
			"style":("not_pick",),
			"height":11, "width":width,
			"x":0, "y":10,
			"vertical_align":"bottom",
			"children":
			(
				{
					"name":"StatusText",
					"type":"text",
					"style":("not_pick",),
					"text":"Inativo",
					"x":0, "y": -1,
					"color":0xffa08784,
				},
				{
					"name":"",
					"type":"box", "color":COLOR_BLACK,
					"style":("not_pick",),
					"height":11, "width":width-1,
					"x":0, "y":0,
				},
			),
		},
		{
			"name":"StatusBar_rare",
			"style":("not_pick",),
			"type":"bar", "color":COLOR_INACTIVE_RARE,
			"height":11, "width":width,
			"x":0, "y":11*2,
			"vertical_align":"bottom",
			"hide":1,
			"children":
			(
				{
					"name":"StatusText_rare",
					"type":"text",
					"style":("not_pick",),
					"text":"Inativo",
					"x":0, "y": -1,
					"color":0xfff8d090,
				},
				{
					"name":"",
					"type":"box", "color":COLOR_BLACK,
					"style":("not_pick",),
					"height":11, "width":width-1,
					"x":0, "y":0,
				},
			),
		},
	),
}
