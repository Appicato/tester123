YANG = 40000
LEVEL = 26
WEAPON_Upgrade_Count = 4
ARMOR_Upgrade_Count = 0
HELMET_Upgrade_Count = 0
SHIELD_Upgrade_Count = 0
JEWELRY_Upgrade_Count = 0
Buy_WEAPON = 1
Buy_ARMOR = 0
Buy_HELMET = 0
Buy_SHIELD = 0
Buy_JEWELRY = 0
npcVID = 1774
checkingMode = 1

import mt2py
import mt2pyv
import player, chat, chr, shop, item, playerSettingModule, event, net, game, dbg
import background
mt2py.SetMt2Py(str(1))
		
INVENTORY = hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 and player.GetExtendInvenMax() or player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT	# INVENTORY RANGE

def isCorrectWeaponLevel(itemid):
	if itemid <= 0: return True
	item.SelectItem(itemid)
	v1, level = item.GetLimit(0)
	if chr.GetRace() == playerSettingModule.RACE_WOLFMAN_M:
		return True
	if chr.GetRace() == playerSettingModule.RACE_SHAMAN_W or chr.GetRace() == playerSettingModule.RACE_SHAMAN_M:
		if level < 5 and player.GetStatus(player.LEVEL) >= 5: return False
		if level < 15 and player.GetStatus(player.LEVEL) >= 15: return False
		if level < 32 and player.GetStatus(player.LEVEL) >= 32: return False
		return True
	##All other races
	if level < 5 and player.GetStatus(player.LEVEL) >= 5: return False
	if level < 15 and player.GetStatus(player.LEVEL) >= 15: return False
	if level < 25 and player.GetStatus(player.LEVEL) >= 25: return False
	if level < 36 and player.GetStatus(player.LEVEL) >= 36: return False
	return True

def GetWeaponSubType(): # CHECK CHARACTER Weapon SubType # Sword = 0 , Knife = 1 , Bow  = 2 , Two hand = 3 , Bell	 = 4,Fan = 5 , Lycan = 8
        if chr.GetRace() == playerSettingModule.RACE_WARRIOR_M or chr.GetRace() == playerSettingModule.RACE_WARRIOR_W:
            return item.WEAPON_TWO_HANDED
			#return item.WEAPON_SWORD
        elif chr.GetRace() == playerSettingModule.RACE_ASSASSIN_W or chr.GetRace() == playerSettingModule.RACE_ASSASSIN_M:
            return item.WEAPON_SWORD
			#return item.WEAPON_DAGGER
			#return item.WEAPON_BOW
        elif chr.GetRace() == playerSettingModule.RACE_SURA_M or chr.GetRace() == playerSettingModule.RACE_SURA_W:
            return item.WEAPON_SWORD
        elif chr.GetRace() == playerSettingModule.RACE_SHAMAN_W or chr.GetRace() == playerSettingModule.RACE_SHAMAN_M:
            return item.WEAPON_FAN
			#return item.WEAPON_BELL
        elif chr.GetRace() == playerSettingModule.RACE_WOLFMAN_M:
            return 8

        return None
	

def GetAntiflag(): # CHECK CHARACTER COMPATIBILITY FOR EQUIPMENT
        if chr.GetRace() == playerSettingModule.RACE_WARRIOR_M or chr.GetRace() == playerSettingModule.RACE_WARRIOR_W:
            return item.ITEM_ANTIFLAG_WARRIOR
        elif chr.GetRace() == playerSettingModule.RACE_ASSASSIN_W or chr.GetRace() == playerSettingModule.RACE_ASSASSIN_M:
            return item.ITEM_ANTIFLAG_ASSASSIN
        elif chr.GetRace() == playerSettingModule.RACE_SURA_M or chr.GetRace() == playerSettingModule.RACE_SURA_W:
            return item.ITEM_ANTIFLAG_SURA
        elif chr.GetRace() == playerSettingModule.RACE_SHAMAN_W or chr.GetRace() == playerSettingModule.RACE_SHAMAN_M:
            return item.ITEM_ANTIFLAG_SHAMAN
        elif chr.GetRace() == playerSettingModule.RACE_WOLFMAN_M:
            return item.ITEM_ANTIFLAG_WOLFMAN

        return None

def Get_ITEM_ID(INVENTORY,SLOT):	# GET ITEM ID 
	return player.GetItemIndex ( INVENTORY , SLOT )

def Get_Defance(INVENTORY,SLOT): 	# GET ITEM DEFANCE 
	item.SelectItem( Get_ITEM_ID( INVENTORY , SLOT ) )	
	return ( item.GetValue(1) + (item.GetValue(5) * 2) )

def Get_Grade(INVENTORY,SLOT):		# GET ITEM GRADE 
	return player.GetItemGrade( INVENTORY , SLOT )
	
def Upgrade(slot): #  UPGRADE
	NpcStatus = shop.IsOpen()	# CHECK IF SHOP PANEL IS OPEN
	if NpcStatus == 0 :	# IF SHOP IS CLOSED
		net.SendRefinePacket(slot, 0)
	else:
		net.SendShopEndPacket()	# CLOSE SHOP PANEL
	
def Use_ITEM(slot):	# USE ITEM
	net.SendItemUsePacket(slot)

def Buy_ITEM(ItemSubType):	# BUY BEST ITEM FROM NPC FOR ItemSubType VALUE; IF NO ITEM, TURN BACK TO -1
	defance = -1
	buy_slot = -1
	for slot in xrange(shop.SHOP_SLOT_COUNT):	# GET SHOP SLOT COUNT
	
		item.SelectItem( shop.GetItemID( slot ) ) 
		selected_defance = item.GetValue(1) + (item.GetValue(5) * 2)	# GET WHOLE DEFANCE
		v1, v2 = item.GetLimit(0)	# get item characterstics

		if (player.GetStatus(player.LEVEL) >= v2 and item.IsAntiFlag(GetAntiflag()) == 0 and item.GetItemType() == item.ITEM_TYPE_ARMOR and item.GetItemSubType() == ItemSubType and selected_defance > defance): # IF LEVEL SUITABLE AND IF CHARACTER SUITABLE  AND  IF EQUIPABLE EQUIPMENT AND IF ItemSubType SUITABLE	AND IF DEFANCE IS HIGHER THEN LAST VALUE	

			defance = selected_defance	# GET ITEM WITH HIGHER DEFANCE
			buy_slot = slot				# GET SLOT
			
	net.SendShopBuyPacket(buy_slot)		# GET BEST EQUIPMENT FROM NPC
	net.SendShopEndPacket()				# CLOSE SHOP PANEL

def Buy_ITEM_Weapon(ItemSubType):	# BUY BEST ITEM FROM NPC FOR ItemSubType VALUE; IF NO ITEM, TURN BACK TO -1
	attack = -1
	buy_slot = -1
	for slot in xrange(shop.SHOP_SLOT_COUNT):	# GET SHOP SLOT COUNT
	
		item.SelectItem( shop.GetItemID( slot ) ) 
		selected_attack = item.GetValue(4) + (item.GetValue(5) )	# GET MAX ATTACK + UPGRADE ATTACK
		v1, v2 = item.GetLimit(0)	# get item characterstics
		
		if (player.GetStatus(player.LEVEL) >= v2 and item.IsAntiFlag(GetAntiflag()) == 0 and item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == ItemSubType and selected_attack > attack): # IF LEVEL SUITABLE AND IF CHARACTER SUITABLE  AND  IF EQUIPABLE EQUIPMENT AND IF ItemSubType SUITABLE	AND IF ATTACK IS HIGHER THEN LAST VALUE	
			
			attack = selected_attack	# GET ITEM WITH HIGHER ATTACK
			buy_slot = slot				# GET SLOT

	net.SendShopBuyPacket(buy_slot)		# GET BEST EQUIPMENT FROM NPC
	net.SendShopEndPacket()				# CLOSE SHOP PANEL

def Inventory_Control(ItemSubType): # Get best Item for ItemSubType value; if there is no item, turn back to -1  
	defance = -1
	UseSlot = -1
	for slot in xrange(INVENTORY):	# SCAN INVENTORY
	
		item.SelectItem( player.GetItemIndex( slot ) ) # select item [SLOT]
		v1, v2 = item.GetLimit(0)	# GET ITEM CHARACTERISTICS
		selected_defance = item.GetValue(1) + (item.GetValue(5) * 2)	# GET WHOLE DEFANCE VALUE

		if player.GetStatus(player.LEVEL) >= v2 and item.IsAntiFlag(GetAntiflag()) == 0 and item.GetItemType() == item.ITEM_TYPE_ARMOR and item.GetItemSubType() == ItemSubType and selected_defance > defance:	 # IF LEVEL SUITABLE AND IF CHARACTER SUITABLE  AND  IF EQUIPABLE EQUIPMENT AND IF ItemSubType SUITABLE	AND IF DEFANCE IS HIGHER THEN LAST VALUE
			UseSlot = slot				# GET SLOT INFORMATION
			defance = selected_defance	# GET ITEM WITH BETTER DEFANCE
			
	return UseSlot		# IF EQUIPMENT AVAILABLE USE ITEM WITH BEST VALUE , IF NOT -1 

def Inventory_Control_Weapon(ItemSubType): # Get best Item for ItemSubType value; if there is no item, turn back to -1  
	#attack = -1
	UseSlot = -1
	level = 0
	for slot in xrange(INVENTORY):	# SCAN INVENTORY
	
		item.SelectItem( player.GetItemIndex( slot ) ) 
		v1, v2 = item.GetLimit(0)	# GET ITEM CHARACTERISTICS
		#selected_attack = item.GetValue(4) + (item.GetValue(5) )	# GET WHOLE DEFANCE VALUE
		
		if player.GetStatus(player.LEVEL) >= v2 and item.IsAntiFlag(GetAntiflag()) == 0 and item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == ItemSubType:	 # IF LEVEL SUITABLE AND IF CHARACTER SUITABLE  AND  IF EQUIPABLE EQUIPMENT AND IF ItemSubType SUITABLE	AND IF ATTACK IS HIGHER THEN LAST VALUE
			#if selected_attack > attack:
			if v2 > level:
				UseSlot = slot				# GET SLOT INFORMATION
				#attack = selected_attack	# GET ITEM WITH BETTER ATTACK
				level = v2	# GET ITEM WITH higher level

	return UseSlot		# IF EQUIPMENT AVAILABLE USE ITEM WITH BEST VALUE , IF NOT -1 

def Inventory_Control_Weapon2(ItemSubType): # Get best Item for ItemSubType value; if there is no item, turn back to -1  
	#attack = -1
	UseSlot = -1
	level = 0
	for slot in xrange(INVENTORY):	# SCAN INVENTORY
		if player.GetItemIndex( 1 , slot ) >= 21900 and player.GetItemIndex( 1 , slot ) <= 21990:
			continue
		item.SelectItem( player.GetItemIndex( slot ) ) 
		v1, v2 = item.GetLimit(0)	# GET ITEM CHARACTERISTICS
		selected_attack = item.GetValue(4) + (item.GetValue(5) )	# GET WHOLE DEFANCE VALUE
		
		if player.GetStatus(player.LEVEL) >= v2 and item.IsAntiFlag(GetAntiflag()) == 0 and item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == ItemSubType:	 # IF LEVEL SUITABLE AND IF CHARACTER SUITABLE  AND  IF EQUIPABLE EQUIPMENT AND IF ItemSubType SUITABLE	AND IF ATTACK IS HIGHER THEN LAST VALUE
			#if selected_attack > attack:
			if v2 > level:
				UseSlot = slot				# GET SLOT INFORMATION
				#attack = selected_attack	# GET ITEM WITH BETTER ATTACK
				level = v2	# GET ITEM WITH higher level

	return UseSlot		# IF EQUIPMENT AVAILABLE USE ITEM WITH BEST VALUE , IF NOT -1 

def Scan_Npc(): # Npc vid Scan
	if checkingMode == 1:
		return -1
	return npcVID

def Open_Npc(vid):

	net.SendOnClickPacket(vid)
	event.SelectAnswer(event.BUTTON_TYPE_NEXT, 254)
	event.SelectAnswer(event.BUTTON_TYPE_NEXT, 254)
	event.SelectAnswer(1, 0)

	net.SendOnClickPacket(vid)
	event.SelectAnswer(1, 0)
	event.SelectAnswer(event.BUTTON_TYPE_NEXT, 254)
	event.SelectAnswer(1, 1)
	event.SelectAnswer(1, 0)
	net.SendOnClickPacket(vid)
	event.SelectAnswer(1, 1)
	event.SelectAnswer(event.BUTTON_TYPE_NEXT, 254)
	event.SelectAnswer(1, 1)
	event.SelectAnswer(1, 0)
	net.SendOnClickPacket(vid)

	net.SendOnClickPacket(vid)
	event.SelectAnswer(1, 0)
	event.SelectAnswer(event.BUTTON_TYPE_NEXT, 254)
	event.SelectAnswer(1, 0)
	event.SelectAnswer(1, 0)
	net.SendOnClickPacket(vid)
	event.SelectAnswer(1, 1)
	event.SelectAnswer(event.BUTTON_TYPE_NEXT, 254)
	event.SelectAnswer(1, 0)
	event.SelectAnswer(1, 0)
	net.SendOnClickPacket(vid)

def InstallPopupHook():
	
	try:
		if mt2pyv.Popup == "":
		
			mt2pyv.Popup = game.GameWindow.PopupMessage
			
	except:
	
		mt2pyv.Popup = ""
	
	if mt2pyv.Popup == "":
	
		mt2pyv.Popup = game.GameWindow.PopupMessage
		
	game.GameWindow.PopupMessage = None
	
def UnHookPopup():
	game.GameWindow.PopupMessage = mt2pyv.Popup


def Start():
	weapon_ok = 1
	armor_ok = 1
	helmet_ok = 1
	shield_ok = 1
	jewelry_ok = 1
	
	WEAPON_Status = 0	# VARIABLE FOR WEAPON VALUE (not included currently)	
	ARMOR_Status = 0	# VARIABLE FOR ARMOR VALUE
	HELMET_Status = 0	# VARIABLE FOR HELMET VALUE
	SHIELD_Status = 0	# VARIABLE FOR SHIELD VALUE
	JEWELRY_Status = 0	# VARIABLE FOR JEWELRY VALUE (not included currently)		
	InstallPopupHook()


	#######################################################################################################
	
	if Buy_WEAPON:	# IF BUY Weapon ACTIVE
		weapon_ok = 0
		
		Weapon_Subtype = GetWeaponSubType()
		
		if Get_ITEM_ID(2,item.EQUIPMENT_WEAPON) == 0: #IF NO EQUIPPET Weapon
			
			Slot = Inventory_Control_Weapon(Weapon_Subtype) #SEARCH Weapon IN INVENTORY
			if Slot != -1 and isCorrectWeaponLevel(player.GetItemIndex(Slot)) == True: # IF Weapon AVAILABLE
			
				Weapon_Grade = Get_Grade(1,Slot) #GET GRADE OF ITEM
				
				if Weapon_Grade >= WEAPON_Upgrade_Count : #IF NEEDED OR HIGHER GRADE Weapon IS AVAILABLE
					Use_ITEM(Slot)	# use item					
					#WEAPON_Status  = 1 # Weapon value 1
					
				elif Weapon_Grade < WEAPON_Upgrade_Count : # lower then needed grade
					ID = Get_ITEM_ID(1,Slot)
					if ID >=21900 and ID <= 21969 :
						item.SelectItem(player.GetItemIndex(1,Slot))
						v1, v2 = item.GetLimit(0)
						if player.GetStatus(player.LEVEL) - v2 >= 10:
							Slot = Inventory_Control_Weapon2(Weapon_Subtype)
							Weapon_Grade = Get_Grade(1,Slot)
							if Slot == -1:
								NpcStatus = shop.IsOpen()	# CHECK IF SHOP PANEL IS OPEN
								if NpcStatus == 0 :	# IF SHOP IS CLOSED
									vid_NPC = Scan_Npc()	# check vid of Armour Shop Dealer , ( Armour Shop Dealer part have to change for different countrys  , itÂ´s for TR Server )
									vid_NPC = vid_NPC - 1
									if vid_NPC != -1:	# IF ARMOUR SHOP DEALER FOUND
										Open_Npc( vid_NPC ) # OPEN ARMOUR SHOP DEALER PANEL
								else:
									Slot = Inventory_Control_Weapon2(Weapon_Subtype)
									if Slot == -1:
										Buy_ITEM_Weapon(Weapon_Subtype)	# IF ARMOUR SHOP DEALER PANEL IS OPEN, BUY CHEAPEST Weapon
							else:
								if Weapon_Grade < WEAPON_Upgrade_Count :
									net.SendShopEndPacket()
									Upgrade(Slot)
								else:
									Use_ITEM(Slot)	# use item					
									#WEAPON_Status  = 1 # Weapon value 1
						else: # BEST LEVEL WEAPON
							Use_ITEM(Slot)
							#WEAPON_Status = 1   # EN IYI LEVEL SILAHI
					else:
						net.SendShopEndPacket()
						Upgrade(Slot)	# upgrade Weapon
					
			else: # ENVANTERDE DE Silah YOKSA
				NpcStatus = shop.IsOpen()	# CHECK IF SHOP PANEL IS OPEN
				if NpcStatus == 0 :	# IF SHOP IS CLOSED
					vid_NPC = Scan_Npc()	# check vid of Armour Shop Dealer , ( Armour Shop Dealer part have to change for different countrys  , itÂ´s for TR Server )
					vid_NPC = vid_NPC - 1
					if vid_NPC != -1:	# IF ARMOUR SHOP DEALER FOUND
						Open_Npc( vid_NPC ) # OPEN ARMOUR SHOP DEALER PANEL
						
				else:
					Buy_ITEM_Weapon(Weapon_Subtype)	# IF ARMOUR SHOP DEALER PANEL IS OPEN, BUY CHEAPEST Weapon
					
		else: # TAKILI SÄ°LAH VARSA
			Weapon_Grade = Get_Grade(2,item.EQUIPMENT_WEAPON) #GET GRADE OF EQUIPPET Weapon
			if isCorrectWeaponLevel(player.GetItemIndex(2,item.EQUIPMENT_WEAPON)) and Weapon_Grade >= WEAPON_Upgrade_Count: # if needed grad OR higher Weapon existing
			
				WEAPON_Status = 1	# Weapon value 1
				#Use_ITEM(Slot)	# use item	
				
			else:
				ID = Get_ITEM_ID(2,item.EQUIPMENT_WEAPON)
				if ID >=21900 and ID <= 21969 :
					item.SelectItem(player.GetItemIndex(2,item.EQUIPMENT_WEAPON))
					v1, v2 = item.GetLimit(0)
					if player.GetStatus(player.LEVEL) - v2 >= 10:
						net.SendShopEndPacket()
						net.SendItemUsePacket(2,item.EQUIPMENT_WEAPON) # FARK 10DAN FAZLA LEVEL SILAHINI CIKART
					else: # BEST LEVEL WEAPON
						WEAPON_Status = 1   # EN IYI LEVEL SILAHI
				else:
					net.SendShopEndPacket()
					net.SendItemUsePacket(2,item.EQUIPMENT_WEAPON)
					
		if WEAPON_Status :	# IF Weapon PROCESS WAS COMPLETED SUCCESSFULLY, WRITE CHAT MESSAGE
			#chat.AppendChat(4,"WEAPON OKAY")
			weapon_ok = 1

	####################################################################################################### 
	
	if Buy_ARMOR:	# IF BUY ARMOR ACTIVE
		armor_ok = 0
	
		if Get_ITEM_ID(2,item.EQUIPMENT_BODY) == 0: #IF NO EQUIPPET ARMOR
		
			Slot = Inventory_Control(item.ARMOR_BODY) #SEARCH ARMOR IN INVENTORY
			
			if Slot != -1: # IF ARMOR AVAILABLE
			
				Armor_Grade = Get_Grade(1,Slot) #GET GRADE OF ITEM
				
				if Armor_Grade >= ARMOR_Upgrade_Count : #IF NEEDED OR HIGHER GRADE ARMOR IS AVAILABLE
					
					Use_ITEM(Slot)	# use item
					
					#ARMOR_Status  = 1 # ARMOR value 1
					
				elif Armor_Grade < ARMOR_Upgrade_Count : # lower then needed grade
					net.SendShopEndPacket()
					Upgrade(Slot)	# upgrade armor
					
			else: # ENVANTERDE DE ZIRH YOKSA
				NpcStatus = shop.IsOpen()	# CHECK IF SHOP PANEL IS OPEN
				if NpcStatus == 0 :	# IF SHOP IS CLOSED
					
					vid_NPC = Scan_Npc()	# check vid of Armour Shop Dealer , ( Armour Shop Dealer part have to change for different countrys  , itÂ´s for TR Server )
					if vid_NPC != -1:	# IF ARMOUR SHOP DEALER FOUND
						Open_Npc( vid_NPC ) # OPEN ARMOUR SHOP DEALER PANEL
						
				else:
					Buy_ITEM(item.ARMOR_BODY)	# IF ARMOUR SHOP DEALER PANEL IS OPEN, BUY CHEAPEST ARMOR
					
		else: # TAKILI ZIRH VARSA
			Armor_Grade = Get_Grade(2,item.EQUIPMENT_BODY) #GET GRADE OF EQUIPPET ARMOR
			
			if Armor_Grade >= ARMOR_Upgrade_Count: # if needed grad OR higher armor existing
				ARMOR_Status = 1	# ARMOR value 1
				
				
			else:
				
				net.SendShopEndPacket()
				net.SendItemUsePacket(2,item.EQUIPMENT_BODY)
				
		if ARMOR_Status :	# IF ARMOR PROCESS WAS COMPLETED SUCCESSFULLY, WRITE CHAT MESSAGE
			#chat.AppendChat(4,"ARMOR OKAY")
			armor_ok = 1
		
			
		

#########################################################################################	HELMET		SAME STRUCTURE AS ARMOR
	
	if Buy_HELMET:
		helmet_ok = 0
	
		if Get_ITEM_ID(2,item.EQUIPMENT_HEAD) == 0:
			
			Slot = Inventory_Control(item.ARMOR_HEAD)
				
			if Slot != -1:
				
				Helmet_Grade = Get_Grade(1,Slot)
					
				if Helmet_Grade >= HELMET_Upgrade_Count :
						
					Use_ITEM(Slot)
						
					#HELMET_Status  = 1
						
				elif Helmet_Grade < HELMET_Upgrade_Count :
					net.SendShopEndPacket()
					Upgrade(Slot)
						
			else:
				NpcStatus = shop.IsOpen()
					
				if NpcStatus == 0 :
					vid_NPC = Scan_Npc()
					if vid_NPC != -1:
						Open_Npc( vid_NPC )
							
				else:
					Buy_ITEM(item.ARMOR_HEAD)
						
		else:
			Helmet_Grade = Get_Grade(2,item.EQUIPMENT_HEAD)
				
			if Helmet_Grade >= HELMET_Upgrade_Count:
				HELMET_Status = 1
					
					
			else:
				
				net.SendShopEndPacket()
				net.SendItemUsePacket(2,item.EQUIPMENT_HEAD)

		if HELMET_Status :
			#chat.AppendChat(4,"HELMET OKAY")
			helmet_ok = 1


#########################################################################################	SHIELD		SAME STRUCTURE AS ARMOR

	if Buy_SHIELD:
		shield_ok = 0
	
		if Get_ITEM_ID(2,10) == 0:
		
			Slot = Inventory_Control(item.ARMOR_SHIELD)
			
			if Slot != -1:
			
				Shield_Grade = Get_Grade(1,Slot)
				
				if Shield_Grade >= SHIELD_Upgrade_Count :
					
					Use_ITEM(Slot)
					
					#SHIELD_Status  = 1
					
				elif Shield_Grade < SHIELD_Upgrade_Count :
					net.SendShopEndPacket()
					Upgrade(Slot)
					
			else:
				NpcStatus = shop.IsOpen()
				
				if NpcStatus == 0 :
					vid_NPC = Scan_Npc()
					if vid_NPC != -1:
						Open_Npc( vid_NPC )
						
				else:
					Buy_ITEM(item.ARMOR_SHIELD)
					
		else:
			Shield_Grade = Get_Grade(2,10)
			
			if Shield_Grade >= SHIELD_Upgrade_Count:
				SHIELD_Status = 1
				
				
			else:
				
				net.SendShopEndPacket()
				net.SendItemUsePacket(2,10)
				
		if SHIELD_Status:
			#chat.AppendChat(4,"SHIELD OKAY")
			shield_ok = 1
			
#########################################################################################
	undoPopup = False
	if weapon_ok == 1 and armor_ok == 1 and helmet_ok == 1 and shield_ok == 1 and jewelry_ok == 1:
		if Buy_WEAPON == 1 and (Buy_ARMOR == 1 or Buy_HELMET == 1 or Buy_SHIELD == 1 or Buy_JEWELRY == 1):
			undoPopup = True
			chat.AppendChat(0, "Upgrade-EQ: Weapon+Armor+Helmet+Shield Okay!")
		if Buy_WEAPON == 0 and (Buy_ARMOR == 1 or Buy_HELMET == 1 or Buy_SHIELD == 1 or Buy_JEWELRY == 1):
			undoPopup = True
			chat.AppendChat(0, "Upgrade-EQ: Armor+Helmet+Shield Okay!")
		if Buy_WEAPON == 1 and Buy_ARMOR == 0 and Buy_HELMET == 0 and Buy_SHIELD == 0 and Buy_JEWELRY == 0:
			undoPopup = True
			chat.AppendChat(0, "Upgrade-EQ: Weapon Okay!")
		mt2py.SetMt2Py(str(2))
	if weapon_ok == 0:
		chat.AppendChat(0, "Upgrade-EQ: Weapon not okay!")
	if armor_ok == 0:
		chat.AppendChat(0, "Upgrade-EQ: Armor not okay!")
	if helmet_ok == 0:
		chat.AppendChat(0, "Upgrade-EQ: Helmet not okay!")
	if shield_ok == 0:
		chat.AppendChat(0, "Upgrade-EQ: Shield not okay!")
	if jewelry_ok == 0:
		chat.AppendChat(0, "Upgrade-EQ: Jewelry not okay!")
	if undoPopup == True:
		UnHookPopup()

Start()	