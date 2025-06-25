import mt2py
import mt2pyv, chrmgr, chat, item, net, player, shop
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
MaxLvl = 0
MaxPlus = 0
HoldBonus = 0
SellOther = 0
SellFB = 0
BuyRedPottsk = 0
BuyBluePottsk = 0
BuyRedPottsm = 0
BuyBluePottsm = 0
BuyRedPottsg = 0
BuyBluePottsg = 0
BuyRedPottsxxl = 0
BuyBluePottsxxl = 0
dontsell = [2, 3, 4]
alwayssell = [2, 3, 4]
SellPotts = 0
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
RotePottval1 = 27001
RotePottval2 = 27002
RotePottval3 = 27003
RotePottval4 = 27007
BlauePottval1 = 27004
BlauePottval2 = 27005
BlauePottval3 = 27006
BlauePottval4 = 27008
#####INTELLECTUAL PROPERTY - COPYRIGHT ALL RIGHTS RESERVED#####
InventorySize = hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 and player.GetExtendInvenMax() or player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT

def MySendDropPacket(slot):
	net.SendItemDropPacketNew(slot, 200)
			
def MyGetItemIndex(i):
	id = player.GetItemIndex(i)
	try:
		if id == 50300:
			return player.GetItemMetinSocket(i, 0) + 10000
		if id == 71092:
			return player.GetItemMetinSocket(i, 0) + 20000
		if id >= 70104 and id <= 70106:
			return player.GetItemMetinSocket(i, 0) + 20000
		if id == 70037:
			return player.GetItemMetinSocket(i, 0) + 35000
	except:
		return id
	return id

def DroppingMt2Py():
	try:
		mt2py.SetMt2Py(str(1))
		sold = 0
		#mt2py.SetMt2Py(str(2))
		for j in xrange(InventorySize):
			i = InventorySize - j - 1
			#MySendDropPacket(i)
			#continue
			if sold == 1:
				break
			vid = MyGetItemIndex(i)
			if vid in dontsell:
				continue
			if vid in alwayssell:
				sold = 1
				MySendDropPacket(i)
				continue
			vid = player.GetItemIndex(i)
			if SellPotts == 1:
				if vid == RotePottval1:
					if BuyRedPottsk == 0 or int(player.GetItemCountByVnum(int(RotePottval1))) >= int(BuyRedPottsk * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
				if vid == RotePottval2:
					if BuyRedPottsm == 0 or int(player.GetItemCountByVnum(int(RotePottval2))) >= int(BuyRedPottsm * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
				if vid == RotePottval3:
					if BuyRedPottsg == 0 or int(player.GetItemCountByVnum(int(RotePottval3))) >= int(BuyRedPottsg * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
				if vid == RotePottval4:
					if BuyRedPottsxxl == 0 or int(player.GetItemCountByVnum(int(RotePottval4))) >= int(BuyRedPottsxxl * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
				if vid == BlauePottval1:
					if BuyBluePottsk == 0 or int(player.GetItemCountByVnum(int(BlauePottval1))) >= int(BuyBluePottsk * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
				if vid == BlauePottval2:
					if BuyBluePottsm == 0 or int(player.GetItemCountByVnum(int(BlauePottval2))) >= int(BuyBluePottsm * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
				if vid == BlauePottval3:
					if BuyBluePottsg == 0 or int(player.GetItemCountByVnum(int(BlauePottval3))) >= int(BuyBluePottsg * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
				if vid == BlauePottval4:
					if BuyBluePottsxxl == 0 or int(player.GetItemCountByVnum(int(BlauePottval4))) >= int(BuyBluePottsxxl * 200) + 200:
						sold = 1
						MySendDropPacket(i)
						break
					continue
			if vid == 50300 or vid == 70037 or vid == 70102 or (vid >= 70104 and vid <= 70106) or vid == 71092:#FB||BDV||VWK||VWK||VWK
				sockid = player.GetItemMetinSocket(i, 0)
				nosell = 0
				for NOTSOCKET in dontsell:
					if vid == 50300:#fB
						NOTSOCKET-=10000
						if NOTSOCKET == sockid:
							nosell = 1
							break
					elif vid == 70037:#BDV
						NOTSOCKET-=35000
						if NOTSOCKET == sockid:
							nosell = 1
							break
					else:#VWK
						NOTSOCKET-=20000	
						if NOTSOCKET == sockid:
							nosell = 1
							break
				if nosell == 1:
					continue
			if vid == 0 or vid == RotePottval1 or vid == RotePottval2 or vid == RotePottval3 or vid == RotePottval4 or vid == BlauePottval1 or vid == BlauePottval2 or vid == BlauePottval3 or vid == BlauePottval4:
				continue
			if vid >= 8000 and vid <= 8009:
				if SellOther == 1:
					sold = 1
					MySendDropPacket(i)
					break
				continue
			if vid >= 14040 and vid <= 14049:
				continue
			if (SellFB == 1) and (vid == 50300):
				fbid = player.GetItemMetinSocket(i, 0)
				FBItems = [1,2,5,6,16,17,18,20,21,31,32,33,34,35,36,46,47,48,49,50,51,61,62,64,65,66,76,77,78,79,80,81,91,92,93,95,106,107,108,109,110,111,170,171,172,173,174,175] # USELESS FBs
				for FBItemd in FBItems:
					if fbid == FBItemd:
						sold = 1
						MySendDropPacket(i)
						break
			if SellOther == 1:
				OtherItems = [50307,50308,50318,50319,50315,30003,30004,30024,30026,30027,30028,30029,30037,30041,30044,30069,30070,30092,30151,50420,50432,50434,50435,50446,50447,50449,50461,50464,50466,50476,50478,50479,50481,50491,50493,50495,50506,50507,50508,50509,50510,50511,50002,50006,50007,50701,50702,50703,50704,50705,50706,50708,50721,50722,50723,50724,50725,50726,50728,70015,71088,71089,80003,80004,80005,80006,80007,28030,28031,28032,28033,28034,28035,28036,28037,28038,28039,28040,28041,28042,28043,28130,28131,28132,28133,28134,28135,28136,28137,28138,28139,28140,28141,28142,28143,28230,28231,28232,28233,28234,28235,28236,28237,28238,28239,28240,28241,28242,28334,28336,28339,28340,50302,50303]
				for Itemd in OtherItems:
					if vid == Itemd:
						sold = 1
						MySendDropPacket(i)
						break
			item.SelectItem(player.GetItemIndex(i))
			itemt = item.GetItemType()
			if (itemt >= 1) and (itemt <= 2):
				val1, val2 = player.GetItemAttribute(int(i), int(0))
				v1, v2 = item.GetLimit(0)
				if v2 == 30:
					continue
				if v2 == 33 and (vid < 14100 or vid > 14109) and (vid < 16100 or vid > 16109):#Ebis
					continue
				if v2 <= int(MaxLvl):
					if '+' not in item.GetItemName():
						continue
					if int(item.GetItemName().split('+')[1]) <= int(MaxPlus):
						if HoldBonus == 1:
							bonivalue = -1
							bonicount = 0
							tocontinue = 0
							while bonivalue != 0 and tocontinue != 1:
								val1, val2 = player.GetItemAttribute(int(i), int(bonicount))
								bonivalue = val1
								bonicount = bonicount + 1
								if val1 == 1 and val2 >= 500:
									tocontinue = 1
									break
								if val1 == 4 and val2 >= 6:
									tocontinue = 1
									break
								if val1 == 5 and val2 >= 8:
									tocontinue = 1
									break
								if val1 == 7 and val2 >= 8:
									tocontinue = 1
									break
								if val1 == 8 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 9 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 10 and val2 >= 20:
									tocontinue = 1
									break
								if val1 == 12 and val2 >= 5:
									tocontinue = 1
									break
								if val1 == 13 and val2 >= 5:
									tocontinue = 1
									break
								if val1 == 15 and val2 >= 5:
									tocontinue = 1
									break
								if val1 == 16 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 17 and val2 >= 5:
									tocontinue = 1
									break
								if val1 == 18 and val2 >= 20:
									tocontinue = 1
									break
								if val1 == 19 and val2 >= 20:
									tocontinue = 1
									break
								if val1 == 20 and val2 >= 20:
									tocontinue = 1
									break
								if val1 == 21 and val2 >= 20:
									tocontinue = 1
									break
								if val1 == 22 and val2 >= 20:
									tocontinue = 1
									break
								if val1 == 23 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 24 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 28 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 29 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 30 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 31 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 32 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 33 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 34 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 37 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 41 and val2 >= 8:
									tocontinue = 1
									break
								if val1 == 43 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 44 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 45 and val2 >= 10:
									tocontinue = 1
									break
								if val1 == 48 and val2 >= 0:
									tocontinue = 1
									break
								if val1 == 49 and val2 >= 0:
									tocontinue = 1
									break
								if val1 == 53 and val2 >= 20:
									tocontinue = 1
									break
							if tocontinue == 1:
								continue
							if tocontinue == 0:
								sold = 1
						else:
							sold = 1
			if sold == 1:
				MySendDropPacket(i)
		if sold == 0:
			mt2py.SetMt2Py(str(2))
			
	except:
		useless = 1

DroppingMt2Py()