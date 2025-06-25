import ui, chat, uiToolTip
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
##
filename = ''
out = open(filename,'w+')
rubbishbonis = [40, 46, 50, 52, 54, 58, 64, 65, 66, 67, 68, 69, 70, 73, 74, 75, 76, 82, 84, 86, 89, 90, 91, 92, 93, 94, 100, 102]
try:
	AFFECT_DICT = uiToolTip.ItemToolTip.AFFECT_DICT
except:
	pass
s = ''
try:
	for x in AFFECT_DICT:
		try:
			if x in rubbishbonis:
				continue
			s += str(AFFECT_DICT[x](999999) +  '\n' + str(x)) + '\n'
		except:
			pass
except:
	pass
try:
	s = s.replace('999999.0', "")
	s = s.replace('999999', "")
	s = s.replace('()', "")
	out.write(s)
	out.close()
except:
	pass
