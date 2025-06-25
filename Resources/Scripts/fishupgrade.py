doAction = 0 #1 = checkUpgrade, 2 = doUpgrade, 3 = buyRod, 4 = equipBest
npcVID = 0
upgradeUntil = 0


RodIDs = [27400,27410,27420,27430,27440,27450,27460,27470,27480,27490,27500,27510,27520,27530,27540,27550,27560,27570,27580,27590]
Points = [10,20,40,80,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,421]
import mt2py
import mt2pyv, chrmgr, chat, item, net, player, shop, event
mt2py.SetMt2Py(str(9))

#if npcVID == 0:
#	npcVID = player.GetTargetVID()

def Point_Control(ITEM_ID, CURRENT_POINT):
	Upgrade = 0
	for i in range(20):
		if ITEM_ID == RodIDs[i] and CURRENT_POINT == Points[i]:
			Upgrade = 1
	return Upgrade

def doCheckUpdate(inv, index):
	ITEM_ID = player.GetItemIndex(inv, index)
	if ITEM_ID in RodIDs:
		point = player.GetItemMetinSocket(inv, index, 0)
		return Point_Control(ITEM_ID, point)
	return 0

def doEquipBest():
	best = -1
	point = -1
	INVENTORY = hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 and player.GetExtendInvenMax() or player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
	for slot in xrange(INVENTORY):
		ITEM_ID = player.GetItemIndex(slot)
		if ITEM_ID == 27591: #Carbon rod
			best = slot
			break
		if ITEM_ID in RodIDs:
			if player.GetItemIndex(best) < ITEM_ID:
				best = slot
				point = player.GetItemMetinSocket(1, slot, 0)

			if player.GetItemIndex(best) == ITEM_ID :
				if point < player.GetItemMetinSocket(1, slot, 0):
					best = slot
					point = player.GetItemMetinSocket(1, slot, 0)

	equipped = player.GetItemIndex(2, item.EQUIPMENT_WEAPON)
	if best != -1 and equipped != 27591: #Carbon rod
		ITEM_ID = player.GetItemIndex(best)
		if ITEM_ID > equipped:
			net.SendItemUsePacket(1, best)
		elif ITEM_ID == equipped:
			if point > player.GetItemMetinSocket(2, item.EQUIPMENT_WEAPON, 0):
				net.SendItemUsePacket(1, best)

def doUpgradeFunc():
	if npcVID <= 0: return
	INVENTORY = hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 and player.GetExtendInvenMax() or player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
	for i in xrange(INVENTORY):
		if doCheckUpdate(1, i) == 1:	
			net.SendGiveItemPacket(npcVID, i, 1)
			event.SelectAnswer(0, 0)
			return 1
	return 0

def buyRodFunc():
	if shop.IsOpen() == False: return 0
	for i in xrange(40):
		if shop.GetItemID(i) == 27400:
			net.SendShopBuyPacket(i)
			return 1
	return 0

try:
	if doAction == 1:
		status = doCheckUpdate(2, item.EQUIPMENT_WEAPON)
		mt2py.SetMt2Py(str(status))
		chat.AppendChat(7, str(doAction) + '__' + str(status))
	if doAction == 2:
		status = doUpgradeFunc()
		mt2py.SetMt2Py(str(status))
		chat.AppendChat(7, str(doAction) + '__' + str(status))
	if doAction == 3:
		status = buyRodFunc()
		mt2py.SetMt2Py(str(status))
		chat.AppendChat(7, str(doAction) + '__' + str(status))
	if doAction == 4:
		doEquipBest()
		mt2py.SetMt2Py(str(1))
		chat.AppendChat(7, str(doAction) + '__' + str(1))
except:
	mt2py.SetMt2Py(str(8))
