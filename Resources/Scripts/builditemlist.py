import item, skill, nonplayer, dbg, app
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
filename = ''
VWKIds = [101, 171, 102, 172, 103, 173, 104, 174, 108, 178, 105, 175, 110, 180, 106, 176, 114, 184, 112, 182, 113, 5101, 5102, 451, 401, 402, 501, 551, 502, 552, 602, 631, 651, 701, 751, 5111, 2001, 2051, 2052, 2002, 2154, 2151, 5121, 771, 731, 2061, 2302, 1601, 1402, 1403]
s = ""
finished = 't'

try:
	oldTime = app.GetGlobalTimeStamp()
	for i in xrange(0,200000):
		e = str(app.GetGlobalTimeStamp() - oldTime)
		if e == '15' or e == '16' or e == '17' or e == '18':
			finished = 'f'
			break
		if i <= 100200 or i % 100 == 0:
			item.SelectItem(i)
			if item.GetItemType() != 6:
				n = item.GetItemName()
				if str(n) != "" and str(n) != "Galle" and str(n) != "Gall" and str(ord(n[0])) != '175':
					s += (n + "\n" + str(i) + "\n")
except:
	pass

if finished == 't':
	item.SelectItem(50300) #FB
	for i in xrange(1,176):
		try:
			s += (skill.GetSkillName(i) + " " + item.GetItemName() + "\n" + str(10000+i) + "\n")
		except:
			pass

	item.SelectItem(70037) #BdV
	for i in xrange(1,176):
		try:
			s += (skill.GetSkillName(i) + " " + item.GetItemName() + "\n" + str(35000+i) + "\n")
		except:
			pass

	item.SelectItem(71093) #VWK
	for id in VWKIds:
		try:
			s += (nonplayer.GetMonsterName(id) + " " + item.GetItemName() + "\n" + str(20000+id) + "\n")
		except:
			pass
	try:
		f = open(filename,'w+')
		f.write(s)
		f.close()
	except:
		pass
finished = 'f'
