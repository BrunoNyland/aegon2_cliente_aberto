#favor manter essa linha
import uiscriptlocale

interface = "interface/controls/special/party/"

faces = "interface/icons/faces/medium/icon_"
icons_y = 28
icons_x = 75
alpha = 0.8

window = {
	"name":"PartyMemeberInfoBoard",
	"x":0,
	"y":0,
	"width":106,
	"height":55,
	"children":
	(
		{
			"name":"party_bg",
			"type":"image",
			"image":interface + "member_bg_gradient.tga",
			"x":0, "y":0,
			"children":
			(
				{
					"name":"StateButton",
					"type":"button",
					"x":2,
					"y":0,
					"default_image":interface + "party_state_leader_01.tga",
					"over_image":interface + "party_state_leader_02.tga",
					"down_image":interface + "party_state_leader_03.tga",
					"vertical_align":"center",
				},
				{
					"name":"NameSlot",
					"type":"image",
					"image":interface+"member_label_name_left.tga",
					"x":54,"y":3,
					"alpha":alpha,
					"children":
					(
						{
							"name":"NameSlotFill",
							"type":"expanded_image",
							"image":interface+"member_label_name_center.tga",
							"x":0,"y":0,
							"x_scale":54,
							"y_scale":1,
							"horizontal_align":"right",
							"alpha":alpha,
							"children":
							(
								{
									"name":"NameSlotRight",
									"type":"image",
									"image":interface+"member_label_name_right.tga",
									"x":0,"y":0,
									"horizontal_align":"right",
									"alpha":alpha,
								},
								{
									"name":"NamePrint",
									"type":"text",
									"text":uiscriptlocale.PARTY_MEMBER_INFO_NAME,
									"x":3,
									"y":3,
								},
							),
						},
					),
				},
				{
					"name":"MemberLabelIcons",
					"type":"image",
					"image":interface+"member_label_icons.tga",
					"x":54,"y":26,
					"alpha":alpha-0.15,
				},
				{
					"name":"face",
					"type":"image",
					"image":faces + "mwarrior.tga",
					"x":20, "y":0,
					"vertical_align":"center",
					"children":
					(
						{
							"name":"HP_Gauge_Base",
							"type":"image",
							"image":interface + "member_gauge_hp_empty.tga",
							"x":0,
							"y":35,
							"horizontal_align":"center",
							"children":
							(
								{
									"name":"Gauge",
									"type":"expanded_image",
									"image":interface + "member_gauge_hp_fill.tga",
									"x":0,"y":0,
									"percent":50,
								},
							),
						},
						{
							"name":"CompartilharExp",
							"type":"image",
							"image":interface + "member_icon_exp_empty.tga",
							"x":35,"y":0,
						},
						{
							"name":"ExperienceImage",
							"type":"image",
							"x":35,"y":0,
							"image":interface + "member_icon_exp_full.tga",
						},
					),
				},
			),
		},
		{
			"name":"AttackerImage",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"DefenderImage",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"BufferImage",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"SkillMasterImage",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"TimeBonusImage",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"RegenBonus",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"IncreaseArea150",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"IncreaseArea200",
			"type":"image",
			"x":icons_x,
			"y":icons_y,
			"image":	interface + "bonus.tga",
			"hide":1,
		},
		{
			"name":"leader",
			"type":"button",
			"x":icons_x,
			"y":icons_y,
			"default_image":	interface + "leader.tga",
			"over_image":		interface + "leader.tga",
			"down_image":		interface + "leader.tga",
			"hide":1,
			"children":
			(
				{
					"name":"tipleader",
					"type":"thinboardnew",
					"width":60,"height":40,
					"x":20,"y":-5,
					"istooltip":1,"hide":1,
					"children":
					(
						{"name":"tagleader","type":"text","text":"|cffa08784"+"Lider","x":0,"y":-1,"all_align":1,},
					),
				},
			),
		},
	),
}
