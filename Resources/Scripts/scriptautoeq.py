import net,player,chat,item,chr,app,time,dbg,sys
switchweapon = 0
switcharmor = 0
switchhelm = 0
switchschild = 0
upgradeitems = 0
upgradeitemsgrade = 9
#####INTELLECTUAL PROPERTY - COPYRIGHT 2014 ALL RIGHTS RESERVED#####
InventorySize = player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
"""
try: # only activ this, if you know what you are do !
	del sys.modules["AutoEq"]
except:
	pass
"""
if "AutoEq" not in sys.modules: # init Phase
	class obj: pass
	sys.modules["AutoEq"]=obj()
	import AutoEq
	AutoEq.Done=1
	AutoEq.unhookedUpdate = app.UpdateGame
	def wearList(list,eqweapon=0):
		if len(list)==0: return
		ItemOld=player.GetItemIndex(list[0])
		AutoEq.SendNext=0
		orgPos=tuple([int(i) for i in player.GetMainCharacterPosition()[:2]])
		posi1=tuple([int(i)+1000 for i in orgPos])
		DataTuple=[chr.SetPixelPosition,posi1,chr.SetLoopMotion,chr.MOTION_WAIT,orgPos,None,-1,list,ItemOld]
		del list
		del posi1
		del orgPos
		del ItemOld
		AutoEq.EQedWeapon=1
		AutoEq.shitCounter=0
		vnumWeapon=player.GetItemIndex(94)
		if eqweapon and vnumWeapon:
			AutoEq.EQedWeapon=0
			DataTuple[5]=(lambda bla=net.SendItemUsePacket: bla(94)) # i think it is a little bit faster
			DataTuple[6]=vnumWeapon
		AutoEq.DataTuple=tuple(DataTuple)
		del DataTuple
		def X():
			DataTuple = AutoEq.DataTuple
			try:
				DataTuple[0](*DataTuple[1])
				DataTuple[2](DataTuple[3])
				if AutoEq.EQedWeapon == 0 and DataTuple[5] != None:
					if player.GetItemIndex(94)!=DataTuple[6]:
						AutoEq.EQedWeapon=1
						AutoEq.shitCounter=0
					else:
						DataTuple[5]()
						AutoEq.shitCounter+=1
						if AutoEq.shitCounter>=20:
							AutoEq.shitCounter=0
							AutoEq.EQedWeapon=1
				elif max(0,AutoEq.SendNext-time.clock())==0:
					if player.GetItemIndex(DataTuple[7][0])==DataTuple[8]:
						for id in DataTuple[7]:
							net.SendItemUsePacket(id)
						AutoEq.SendNext=time.clock()+0.75
						AutoEq.shitCounter+=1
						if AutoEq.shitCounter>=6:
							raise IndexError
					else:
						raise IndexError
			except IndexError:
				DataTuple[0](*DataTuple[4])
				app.UpdateGame=AutoEq.unhookedUpdate
				AutoEq.Done=1
			except:
				DataTuple[0](*DataTuple[4])
				app.UpdateGame=AutoEq.unhookedUpdate
				AutoEq.Done=1
				raise sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2] # i'm not sure why raise *(sys.exc_info()) not work :o
			AutoEq.unhookedUpdate()
		AutoEq.flushMotion()
		app.UpdateGame=X
		AutoEq.Done=0
	def GetBonus(slotidx,bonusid):
		var1=0
		var2=0
		getAffect=item.GetAffect
		getAttribute=player.GetItemAttribute
		for AttributeIndex in xrange(5):
			Affect=getAffect(AttributeIndex)
			if Affect and Affect[0] == bonusid:
				var1=Affect[1]
			Affect = getAttribute(slotidx, AttributeIndex)
			if Affect and Affect[0] == bonusid:
				var2=Affect[1]
		return var1+var2
	def CountBonus(slotidx): # unused but bla
		var1=0
		var2=0
		getAffect=item.GetAffect
		getAttribute=player.GetItemAttribute
		for AttributeIndex in xrange(5):
			Affect=getAffect(AttributeIndex)
			if Affect and Affect[0]:
				var1+=1
			Affect = getAttribute(slotidx, AttributeIndex)
			if Affect and Affect[0]:
				var2+=1
		return var1+var2
	AutoEq.GetBonus=GetBonus
	AutoEq.CountBonus=CountBonus
	AutoEq.wearList=wearList
	AutoEq.flushMotion=(lambda bla=chr.SetLoopMotion, bla2=chr.MOTION_WAIT: bla(bla2))
	AutoEq.BoniList=(
		item.APPLY_MAX_HP,
		item.APPLY_RESIST_BOW,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_STR,
	)
	AutoEq.CLASSDICT=(
		item.ITEM_ANTIFLAG_WARRIOR,
		item.ITEM_ANTIFLAG_ASSASSIN,
		item.ITEM_ANTIFLAG_SURA,
		item.ITEM_ANTIFLAG_SHAMAN,
	)
	
else:
	import AutoEq
race = chr.GetRace()
towear=[]
if race>=4:
	race-=4
raceflag=AutoEq.CLASSDICT[race]
if upgradeitems == 1:
	for slot in xrange(InventorySize):
		if player.GetElk() > 40000:
			item.SelectItem(player.GetItemIndex(slot))
			v1, v2 = item.GetLimit(0)
			if player.GetStatus(player.LEVEL) >= v2:	
				if item.IsWearableFlag(item.WEARABLE_HEAD) or item.IsWearableFlag(item.WEARABLE_SHIELD) or item.IsWearableFlag(item.WEARABLE_WEAPON) or item.IsWearableFlag(item.WEARABLE_BODY):
					if player.GetItemGrade(slot) < upgradeitemsgrade:
						if race == 0:
							if item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR) == 0:
								net.SendRefinePacket(slot, 0)
						elif race == 1:
							if item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN) == 0:
								net.SendRefinePacket(slot, 0)
						elif race == 2:
							if item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA) == 0:
								net.SendRefinePacket(slot, 0)
						elif race == 3:
							if item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN) == 0:
								net.SendRefinePacket(slot, 0)
"""
Truhen:
Lehrlingstruhe 1 50187
Lehrlingstruhe 2 50188
Lehrlingstruhe 3 50189
Meistertruhe   1 50193
Meistertruhe   2 50194
Meistertruhe   3 50195
Expertentruhe  1 50190
Expertentruhe  2 50191
Expertentruhe  3 50192
"""
Data=[]
#Data.append([                  0, "slot","bestofvalue","WearSlot","getvalue","Slotsize",("level","grade")])
if switcharmor:
	Data.append([item.WEARABLE_BODY,  90,  -1, None, "item.GetValue(1)+item.GetValue(5)*2",0,(0,-1)]) # rüstung
if switchhelm:
	Data.append([item.WEARABLE_HEAD,  91,  -1, None, "item.GetValue(1)+item.GetValue(5)*2",0,(0,-1)]) # helm
if switchschild:
	Data.append([item.WEARABLE_SHIELD,100, -1, None, "item.GetValue(1)+item.GetValue(5)*2",0,(0,-1)]) # schild
if switchweapon:
	Data.append([item.WEARABLE_WEAPON,94,  -1, None, "((item.GetValue(3)+item.GetValue(4)+2*item.GetValue(5))/2.0)",0,(0,-1)]) # waffe ## for dss add '/100*(AutoEq.GetBonus(slot,AutoEq.BoniList[2])+100)'
if 0: # hier variable :P
	Data.append([item.WEARABLE_FOOTS, 92,  -1, None, "AutoEq.GetBonus(slot,AutoEq.BoniList[0])",0,(0,-1)]) # schuhe
if 0: # hier variable :P
	Data.append([item.WEARABLE_NECK,  95,  -1, None, "AutoEq.GetBonus(slot,AutoEq.BoniList[0])",0,(0,-1)]) # halskette
if 0: # hier variable :P
	Data.append([item.WEARABLE_EAR,   96,  -1, None, "AutoEq.GetBonus(slot,AutoEq.BoniList[1])",0,(0,-1)]) # ohrringe
if 0: # hier variable :P
	Data.append([item.WEARABLE_WRIST, 93,  -1, None, "AutoEq.GetBonus(slot,AutoEq.BoniList[0])",0,(0,-1)]) # armband

CanWearFlag=item.IsWearableFlag
CantWearFlag=item.IsAntiFlag
IsWearable=lambda WearFlag,raceflag=raceflag,CanWearFlag=CanWearFlag,CantWearRace=CantWearFlag: (CanWearFlag(WearFlag) and not CantWearRace(raceflag))
del raceflag,CanWearFlag,CantWearFlag
Select=item.SelectItem
GetLimit=item.GetLimit
GetVnum=player.GetItemIndex
for glied in Data:
	slot=glied[1]
	vnum=GetVnum(slot)
	if vnum != 0:	
		Select(vnum)
		exec ('glied[2]=%s'%(glied[4]))
		glied[5]=item.GetItemSize()[1]
		glied[6]=(GetLimit(0)[1],player.GetItemGrade(slot))

pLEVEL=player.GetStatus(player.LEVEL)
wearWeapon=0
for slot in xrange(InventorySize):
	vnum=GetVnum(slot)
	if not vnum:
		continue
	Select(vnum)
	for glied in Data:
		if IsWearable(glied[0]) and int(str(vnum)[:3])!=274:
			Grades=(GetLimit(0)[1],player.GetItemGrade(slot))
			if pLEVEL >= Grades[0]:
				exec ('ValueOfWaffe=%s'%(glied[4]))
				if (ValueOfWaffe > glied[2]):
					if glied[1]==94:
						wearWeapon=1
					glied[2]=ValueOfWaffe
					glied[3]=slot
					glied[6]=Grades
					break

for glied in Data:
	slotnum=glied[3]
	if slotnum!=None:
		towear.append(slotnum)
if AutoEq.Done:
	AutoEq.wearList(towear,wearWeapon)


