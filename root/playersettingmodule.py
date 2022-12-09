#favor manter essa linha
import Js4k2l7BrdasmVRt8Wem as chr
import L0E5ajNEGIFdtCIFglqo as chrmgr
import enszxc3467hc3kokdueq as app
import ga3vqy6jtxqi9yf344j7 as player

JOB_WARRIOR		= 0
JOB_ASSASSIN	= 1
JOB_SURA		= 2
JOB_SHAMAN		= 3

RACE_WARRIOR_M	= 0
RACE_ASSASSIN_W	= 1
RACE_SURA_M		= 2
RACE_SHAMAN_W	= 3
RACE_WARRIOR_W	= 4
RACE_ASSASSIN_M	= 5
RACE_SURA_W		= 6
RACE_SHAMAN_M	= 7

PASSIVE_GUILD_SKILL_INDEX_LIST = [151,]
ACTIVE_GUILD_SKILL_INDEX_LIST = [152, 153, 154, 155, 156, 157,]

SKILL_INDEX_DICT = {
	JOB_WARRIOR : {
		1 : (1, 2, 3, 4, 5, 6, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (16, 17, 18, 19, 20, 21, 0, 0, 137, 0, 138, 0, 139, 0,),
		"SUPPORT" : (122, 121, 124, 125, 129, 130, 131, 0, 0, 0,),
	},
	JOB_ASSASSIN : {
		1 : (31, 32, 33, 34, 35, 36, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (46, 47, 48, 49, 50, 51, 0, 0, 137, 0, 138, 0, 139, 0,),
		"SUPPORT" : (122, 121, 124, 125, 129, 130, 131, 0, 0, 0,),
	},
	JOB_SURA : {
		1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
		"SUPPORT" : (122, 121, 124, 125, 129, 130, 131, 0, 0, 0,),
	},
	JOB_SHAMAN : {
		1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
		"SUPPORT" : (122, 121, 124, 125, 129, 130, 131, 0, 0, 0,),
	},
}

def RegisterSkill(race, group):
	job = chr.RaceToJob(race)
	if SKILL_INDEX_DICT.has_key(job):
		if SKILL_INDEX_DICT[job].has_key(group):
			activeSkillList = SKILL_INDEX_DICT[job][group]

			for i in xrange(len(activeSkillList)):
				skillIndex = activeSkillList[i]

				if i != 6 and i != 7:
					player.SetSkill(i+1, skillIndex)

			supportSkillList = SKILL_INDEX_DICT[job]["SUPPORT"]

			for i in xrange(len(supportSkillList)):
				player.SetSkill(i+100+1, supportSkillList[i])

	for i in xrange(len(PASSIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(200+i, PASSIVE_GUILD_SKILL_INDEX_LIST[i])

	for i in xrange(len(ACTIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(210+i, ACTIVE_GUILD_SKILL_INDEX_LIST[i])

def LoadGameNPC():
	try:
		lines = pack_open("npclist.txt", "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		tokens = line[:-1].split("\t")
		if len(tokens) == 0 or not tokens[0]:
			continue

		try:
			vnum = int(tokens[0])
		except ValueError:
			import dbg
			dbg.LogBox("LoadGameNPC() - %s - line #%d: %s" % (tokens, lines.index(line), line))
			app.Abort()

		try:
			if vnum:
				chrmgr.RegisterRaceName(vnum, tokens[1].strip())
			else:
				chrmgr.RegisterRaceSrcName(tokens[1].strip(), tokens[2].strip())
		except IndexError:
			import dbg
			dbg.LogBox("LoadGameNPC() - %d, %s - line #%d: %s " % (vnum, tokens, lines.index(line), line))
			app.Abort()