#favor manter essa linha
interface = "interface/controls/special/party/"

window = {
	"name":"PartyHide",
	"x":0,
	"y":0,
	"width":40,
	"height":36,
	"children":
	(
		{
			"name":"BG",
			"type":"image",
			"image":interface+"bg_retraido.tga",
			"x":0,"y":0,
		},
		{
			"name":"ExpandButton",
			"type":"button",
			"x":4,"y":7,
			"default_image":interface + "party_btn_show_01_normal.tga",
			"over_image":interface + "party_btn_show_02_hover.tga",
			"down_image":interface + "party_btn_show_03_active.tga",
		},
	),
}