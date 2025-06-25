import mt2py
import mt2pyv, chrmgr, chat, item, net, player, shop
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
BuyPaste = 0
BuyWurm = 0
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
Pasteval = 27800
Wurmval = 27801
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
InventorySize = hasattr(player, 'INVENTORY_PAGE_SIZE') and player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT or player.ZEAGII_PENTO_SYNVER * player.INVENTORY_PAGE_COUNT
def MySendShopSellPacket(slot):
	try:
		net.SendShopSellPacket(slot)
	except:
		try:
			net.SendShopSellPacket(1, slot)
		except:
			net.SendShopSellPacketNew(slot, 0, 1)

def SellingMt2Py():
	try:
		for j in xrange(InventorySize):
			i = InventorySize - j - 1
			vid = player.GetItemIndex(i)
			if vid == 40001 or vid == 50002 or vid == 50008 or vid == 50009 or vid == 80008:#Unbekannter Goldring, Goldring, mehrere Schluessel
				MySendShopSellPacket(i)
		mt2py.SetMt2Py(str(1))
		mt2py.SetMt2Py(str(2))
		for i in xrange(40):
			shopitemid = shop.GetItemID(i)
			shopitemcount = shop.GetItemCount(i)
			if shopitemid == Pasteval and shopitemcount == 50:
				ShopPasteSlot = i
			if shopitemid == Wurmval and shopitemcount == 50:
				ShopWurmSlot = i
		koedercountvalue = int(player.GetItemCountByVnum(int(Pasteval)))
		for i in xrange(BuyPaste):
			if koedercountvalue >= int(BuyPaste * 50):
				break
			net.SendShopBuyPacket(int(ShopPasteSlot))
			koedercountvalue = koedercountvalue + 50
		koedercountvalue = int(player.GetItemCountByVnum(int(Wurmval)))
		for i in xrange(BuyWurm):
			if koedercountvalue >= int(BuyWurm * 50):
				break
			net.SendShopBuyPacket(int(ShopWurmSlot))
			koedercountvalue = koedercountvalue + 50
	except:
		useless = 1
SellingMt2Py()