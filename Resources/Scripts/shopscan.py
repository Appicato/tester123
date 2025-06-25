ScanVID = 1234
filename = 'shop_xxxx.txt'
closeShop = 1

import player
import chr
import chat
import mt2py
import mt2pyv
import net
import shop
import app
import item

try:
	x = str(mt2pyv.waitShop)
except:
	mt2pyv.waitShop = 0
	mt2pyv.waitDelay = 0

bonusEnglish = ["Max. HP" , "Max. MP" , "Vitality" , "Intelligence" , "Strength" , "Agility" , "Attack Speed" , "Movement Speed" , "Spell Speed" , "HP Regeneration" , "SP Regeneration" , "Poisoning Chance" , "Chance for Blackout" , "Slowing Chance" , "Chance of Critical Hit" , "Chance of Piercing Hit" , "Strong against Half Humans" , "Strong against Animals" , "Strong against Orcs" , "Strong against Mystics" , "Strong against Undead" , "Strong against Devil" , "Absorbed by HP" , "Absorbed by SP" , "Chance to rob SP" , "Chance SP Regeneration" , "Chance to avoid Arrows" , "Avoid Arrow Attack" , "Sword Defense" , "Two-Handed Sword Defense" , "Dagger Defense" , "Bell Defense" , "Fan Defense" , "Arrow Resistance" , "Fire Resistance" , "Lightning Resistance" , "Magic Resistance" , "Wind Resistance" , "Reflect Close Combat hits" , "Reflect Curse" , "Poison Resistance" , "Chance to Restore MP" , "Chance for EXP Bonus" , "Chance to drop double Yang" , "Chance to drop double Items" , "Increasing potion effect" , "Chance HP Regeneration" , "Defence against Blackouts" , "Defence against Slowing" , "Defense against falling down" , "APPLY_SKILL" , "Arrow Range" , "Attack Value" , "Defense" , "Magic Value" , "Magic Defense" , "No Name" , "Max. Endurance" , "Strong against Warrior" , "Strong against Ninjas" , "Strong against Sura" , "Strong against Shamans" , "Strong against Monster" , "ItemShop - Attack value" , "ItemShop - Defense" , "ItemShop - EXP-Bonus" , "ItemShop - ItemDrop-Bonus" , "ItemShop - YangDrop-Bonus" , "APPLY_MAX_HP_PCT" , "APPLY_MAX_SP_PCT" , "Skill Damage" , "Average Damage" , "Skill Damage Resistance" , "Average Damage Resistance" , "No Name" , "iCafe EXP-Bonus" , "iCafe Item-Bonus" , "Defense chance against warrior attacks" , "Defense chance against ninjas attacks" , "Defense chance against Sura attacks" , "Defense chance against Shaman attacks"]

if shop.IsOpen() == 0 and ScanVID > 0 and mt2pyv.waitShop < 2:
	if app.GetGlobalTime() - mt2pyv.waitDelay > 1000 and mt2pyv.waitShop == 1:
		net.SendShopEndPacket()
	if app.GetGlobalTime() - mt2pyv.waitDelay > 1000:
		net.SendOnClickPacket(ScanVID)
		mt2pyv.waitShop = 1
		mt2pyv.waitDelay = app.GetGlobalTime()
elif shop.IsOpen() == 1 and mt2pyv.waitShop < 2:
	lengg = 40
	if ScanVID > 0:
		chr.SelectInstance(ScanVID)
		if chr.GetRace(ScanVID) > 30000 and chr.GetRace(ScanVID) <= 30008:
			lengg = 80
	mt2pyv.writeText = ''
	for i in xrange(lengg):
		id = shop.GetItemID(i)
		if id > 0:
			mt2pyv.writeText = mt2pyv.writeText + str(id) + ';'
			mt2pyv.writeText = mt2pyv.writeText + str(shop.GetItemCount(i)) + ';'
			mt2pyv.writeText = mt2pyv.writeText + str(shop.GetItemMetinSocket(i, 0)) + ';'
			mt2pyv.writeText = mt2pyv.writeText + str(shop.GetItemPrice(i, 0)) + ';'
			try:
				mt2pyv.writeText = mt2pyv.writeText + str(shop.GetItemCheque(i)) + ';'
			except:
				mt2pyv.writeText = mt2pyv.writeText + '0;'

			try:
				item.SelectItem(id)
				itemt = item.GetItemType()
				if (itemt >= 1) and (itemt <= 2):
					TempBonusCount = 0
					for BonusCount in range(5):
						BonusValue = shop.GetItemAttribute(i , BonusCount )
						if BonusValue[0] > 0 and BonusValue[0] <= 81:
							mt2pyv.writeText = mt2pyv.writeText +  str(bonusEnglish[int(BonusValue[0]) - 1]) + " " +  str(BonusValue[1]) + " "
							TempBonusCount = TempBonusCount + 1
						else:
							break
					if TempBonusCount > 0:
						mt2pyv.writeText = mt2pyv.writeText + ';'
			except:
				pass
		else:
			mt2pyv.writeText = mt2pyv.writeText + '0;0;0;0;0;'
		mt2pyv.writeText = mt2pyv.writeText + '\n'
	if closeShop == 1:
		net.SendShopEndPacket()
		mt2pyv.waitShop = 2
		mt2pyv.waitDelay = app.GetGlobalTime()
	else:
		f = open(filename,'w+')
		f.write(str(mt2pyv.writeText))
		f.close()
		mt2pyv.waitShop = 0
		mt2pyv.waitDelay = 0
elif mt2pyv.waitShop == 2:
	if shop.IsOpen() == 0:
		f = open(filename,'w+')
		f.write(str(mt2pyv.writeText))
		f.close()
		mt2pyv.waitShop = 0
		mt2pyv.waitDelay = 0
	elif app.GetGlobalTime() - mt2pyv.waitDelay > 1000:
		net.SendShopEndPacket()
		mt2pyv.waitDelay = app.GetGlobalTime()
