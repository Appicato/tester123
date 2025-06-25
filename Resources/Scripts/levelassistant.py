YOUNG_HEROES_WEAPON_ACTIVE = 0
YOUNG_HEROES_WEAPON_QUEST_NAME = 'young hero'
YOUNG_HEROES_WEAPON_WARRIOR = 0
YOUNG_HEROES_WEAPON_ASSASSIN = 0
YOUNG_HEROES_WEAPON_SURA = 0
YOUNG_HEROES_WEAPON_SHAMAN = 0
YOUNG_HEROES_WEAPON_WOLFMAN = 0
YOUNG_HEROES_OPEN_ONLY_AFTER_USE = 0
LEVEL_CHEST_ACTIVE = 0

POTION_OF_WISDOM_USE_ONE_HOUR = 0
POTION_OF_WISDOM_USE_THREE_HOURS = 0

EQUIPMENT_WEAPON = 0
EQUIPMENT_BODY = 0
EQUIPMENT_HEAD = 0
EQUIPMENT_SHIELD = 0
EQUIPMENT_JEWELRY = 0

DEBUG = False

import chat
import chr
import event
import net
import player
import playerSettingModule
import quest
import item


def Log(message):
	chat.AppendChat(7, "|ccc888888[Level Assistant] - |ccc00ff00" + message)


def GetSlots():
	return player.GetExtendInvenMax() if hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 else player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT


class weapon:
	ONE_HAND = 0
	TWO_HAND = 1
	DAGGER = 1
	BOW = 2
	BELL = 0
	FAN = 1
	CLAW = 0

	WARRIOR = [
		[21900, 21910, 21920, 21930, 21940, 21950, 21960, 21970],  # one hand
		[21903, 21913, 21923, 21933, 21943, 21953, 21963, 21973]  # two hand
	]

	ASSASSIN = [
		[21900, 21910, 21920, 21930, 21940, 21950, 21960, 21970],  # one hand
		[21901, 21911, 21921, 21931, 21941, 21951, 21961, 21971],  # dagger
		[21902, 21912, 21922, 21932, 21942, 21952, 21962, 21972]  # bow
	]

	SURA = [
		[21900, 21910, 21920, 21930, 21940, 21950, 21960, 21970]  # one hand
	]

	SHAMAN = [
		[21904, 21914, 21924, 21934, 21944, 21954, 21964, 21974],  # bell
		[21905, 21915, 21925, 21935, 21945, 21955, 21965, 21975]  # fan
	]

	WOLFMAN = [
		[21906, 21916, 21926, 21936, 21946, 21956, 21966, 21976]  # claw
	]

	QUEST_ID = None

	@classmethod
	def IsQuestOpen(cls):
		maxc = quest.GetQuestCount()
		if maxc < 280:
			maxc = 280
		for i in xrange(maxc):
			try:
				if quest.GetQuestData(i) == None or str(quest.GetQuestData(i)[0]).lower().find(setting.YOUNG_HEROES_WEAPON.QUEST_NAME.lower()) == -1:
					continue

				weapon.QUEST_ID = quest.GetQuestIndex(i)

				return True
			except:
				pass

		return False

	@staticmethod
	def Receive():
		if not weapon.QUEST_ID:
			return

		event.QuestButtonClick(weapon.QUEST_ID)
		event.SelectAnswer(1, 254)

		if chr.GetRace() == playerSettingModule.RACE_WARRIOR_M or chr.GetRace() == playerSettingModule.RACE_WARRIOR_W:
			event.SelectAnswer(1, setting.YOUNG_HEROES_WEAPON.WARRIOR)
		elif chr.GetRace() == playerSettingModule.RACE_ASSASSIN_W or chr.GetRace() == playerSettingModule.RACE_ASSASSIN_M:
			event.SelectAnswer(1, setting.YOUNG_HEROES_WEAPON.ASSASSIN)
		elif chr.GetRace() == playerSettingModule.RACE_SURA_M or chr.GetRace() == playerSettingModule.RACE_SURA_W:
			event.SelectAnswer(1, setting.YOUNG_HEROES_WEAPON.SURA)
		elif chr.GetRace() == playerSettingModule.RACE_SHAMAN_W or chr.GetRace() == playerSettingModule.RACE_SHAMAN_M:
			event.SelectAnswer(1, setting.YOUNG_HEROES_WEAPON.SHAMAN)
		elif chr.GetRace() == playerSettingModule.RACE_WOLFMAN_M:
			event.SelectAnswer(1, setting.YOUNG_HEROES_WEAPON.WOLFMAN)

	@staticmethod
	def GetVnums():
		if chr.GetRace() == playerSettingModule.RACE_WARRIOR_M or chr.GetRace() == playerSettingModule.RACE_WARRIOR_W:
			return weapon.WARRIOR[setting.YOUNG_HEROES_WEAPON.WARRIOR]
		elif chr.GetRace() == playerSettingModule.RACE_ASSASSIN_W or chr.GetRace() == playerSettingModule.RACE_ASSASSIN_M:
			return weapon.ASSASSIN[setting.YOUNG_HEROES_WEAPON.ASSASSIN]
		elif chr.GetRace() == playerSettingModule.RACE_SURA_M or chr.GetRace() == playerSettingModule.RACE_SURA_W:
			return weapon.SURA[setting.YOUNG_HEROES_WEAPON.SURA]
		elif chr.GetRace() == playerSettingModule.RACE_SHAMAN_W or chr.GetRace() == playerSettingModule.RACE_SHAMAN_M:
			return weapon.SHAMAN[setting.YOUNG_HEROES_WEAPON.SHAMAN]
		elif chr.GetRace() == playerSettingModule.RACE_WOLFMAN_M:
			return weapon.WOLFMAN[setting.YOUNG_HEROES_WEAPON.WOLFMAN]

		return None
		
	@staticmethod
	def HasAnyWeaponEquipped():
		itemID = player.GetItemIndex(2, item.EQUIPMENT_WEAPON)
		if itemID in weapon.WARRIOR[0]: return True
		if itemID in weapon.WARRIOR[1]: return True
		if itemID in weapon.ASSASSIN[0]: return True
		if itemID in weapon.ASSASSIN[1]: return True
		if itemID in weapon.ASSASSIN[2]: return True
		if itemID in weapon.SURA[0]: return True
		if itemID in weapon.SHAMAN[0]: return True
		if itemID in weapon.SHAMAN[1]: return True
		if itemID in weapon.WOLFMAN[0]: return True
		return False
		
	@staticmethod
	def HasAnyWeapon():
		itemID = player.GetItemIndex(2, item.EQUIPMENT_WEAPON)
		if itemID in weapon.WARRIOR[0]: return True
		if itemID in weapon.WARRIOR[1]: return True
		if itemID in weapon.ASSASSIN[0]: return True
		if itemID in weapon.ASSASSIN[1]: return True
		if itemID in weapon.ASSASSIN[2]: return True
		if itemID in weapon.SURA[0]: return True
		if itemID in weapon.SHAMAN[0]: return True
		if itemID in weapon.SHAMAN[1]: return True
		if itemID in weapon.WOLFMAN[0]: return True
		return False

	@staticmethod
	def HasWeapon():
		vnums = weapon.GetVnums()
		if not weapon.GetVnums():
			return False
		vnums = vnums[::-1]
		
		itemID = player.GetItemIndex(2, item.EQUIPMENT_WEAPON)
		if itemID in vnums: return True
		
		for vnum in vnums:
			for _slot in xrange(GetSlots()):
				if player.GetItemIndex(_slot) == vnum:
					return True

		return False

	@staticmethod
	def Equip():
		vnums = weapon.GetVnums()
		vnums = vnums[::-1]
		if not vnums:
			return

		itemID = player.GetItemIndex(2, item.EQUIPMENT_WEAPON)
		wIndex = 99
		
		for index in range(len(vnums)):
			if itemID == vnums[index]:
				wIndex = index

		for index in range(len(vnums)):
			if index < wIndex:
				for _slot in xrange(GetSlots()):
					if player.GetItemIndex(_slot) == vnums[index]:
						item.SelectItem(vnums[index])

						if DEBUG:
							Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _slot))

						net.SendItemUsePacket(_slot)
						return

class chest:
	CHESTS = [
		{"vnum": 50188, "amount": 8},
		{"vnum": 50189, "amount": 10},
		{"vnum": 50190, "amount": 7},
		{"vnum": 50191, "amount": 9},
		{"vnum": 50192, "amount": 11},
		{"vnum": 50193, "amount": 11},
		{"vnum": 50194, "amount": 13},
		{"vnum": 50195, "amount": 15},
		{"vnum": 50196, "amount": 10}
	]

	@staticmethod
	def GetChest():
		for _chest in chest.CHESTS:
			for _slot in xrange(GetSlots()):
				if player.GetItemIndex(_slot) != _chest["vnum"]:
					continue

				item.SelectItem(_chest["vnum"])

				if item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
					continue

				return {"vnum": _chest["vnum"], "slot": _slot, "amount": _chest["amount"]}

		return None

	@staticmethod
	def Open():
		_chest = chest.GetChest()

		if not _chest:
			return

		_space = 0

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) != item.ITEM_TYPE_NONE:
				continue

			_space += 1

		if _space < _chest["amount"]:
			return

		item.SelectItem(_chest["vnum"])

		if DEBUG:
			Log("Opened %s (Slot: %d)" % (item.GetItemName(), _chest["slot"]))

		net.SendItemUsePacket(_chest["slot"])


class potion:
	ONE_HOUR = [
		71153
	]

	THREE_HOURS = [
		71155,
		71181,
		38058
	]

	@staticmethod
	def HasAffect():
		return False

	@staticmethod
	def HasPotion():
		for _vnum in potion.THREE_HOURS:
			if player.GetItemIndex(2, 7) != _vnum and player.GetItemIndex(2, 8) != _vnum:
				continue

			return True

		return False

	@classmethod
	def UseOneHour(cls):
		if potion.HasAffect():
			return

		_used = False

		for _vnum in potion.ONE_HOUR:
			for _slot in xrange(GetSlots()):
				if player.GetItemIndex(_slot) != _vnum:
					continue

				item.SelectItem(_vnum)

				potion.ACTIVE_AFFECT = True

				if DEBUG:
					Log("Used %s (Slot: %d)" % (item.GetItemName(), _slot))

				net.SendItemUsePacket(_slot)

				_used = True
				break

			if _used:
				break

	@staticmethod
	def UseThreeHours():
		if potion.HasPotion():
			return

		_used = False

		for _vnum in potion.THREE_HOURS:
			for _slot in xrange(GetSlots()):
				if player.GetItemIndex(_slot) != _vnum:
					continue

				item.SelectItem(_vnum)

				if DEBUG:
					Log("Used %s (Slot: %d)" % (item.GetItemName(), _slot))

				net.SendItemUsePacket(_slot)

				_used = True
				break

			if _used:
				break


class equipment:
	@staticmethod
	def GetAntiflag():
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

	@staticmethod
	def GetItemDamage(inventory, slot):
		_vnum = player.GetItemIndex(inventory, slot)

		if not _vnum:
			return 0

		item.SelectItem(_vnum)

		_dmg = item.GetValue(3) + item.GetValue(5)

		for _i in xrange(0, 3):
			if item.GetAffect(_i)[0] == item.APPLY_MALL_ATTBONUS:
				_dmg += float(_dmg) * item.GetAffect(_i)[1] / 100

		for _i in xrange(0, 7):
			if player.GetItemAttribute(inventory, slot, _i)[0] == item.APPLY_NORMAL_HIT_DAMAGE_BONUS:
				_dmg += float(_dmg) * player.GetItemAttribute(inventory, slot, _i)[1] / 100

		return _dmg

	@staticmethod
	def GetItemDef(inventory, slot):
		_vnum = player.GetItemIndex(inventory, slot)

		if not _vnum:
			return 0

		item.SelectItem(_vnum)

		return item.GetValue(1) + (item.GetValue(5) * 2)

	@staticmethod
	def GetItemHP(inventory, slot):
		_vnum = player.GetItemIndex(inventory, slot)

		if not _vnum:
			return 0

		_hp = 0

		item.SelectItem(_vnum)

		for _i in xrange(0, 3):
			if item.GetAffect(_i)[0] == item.APPLY_MAX_HP:
				_hp += item.GetAffect(_i)[1]

		for _i in xrange(0, 7):
			if player.GetItemAttribute(inventory, slot, _i)[0] == item.APPLY_MAX_HP:
				_hp += player.GetItemAttribute(inventory, slot, _i)[1]

		return _hp

	@staticmethod
	def EquipWeapon():
		if not equipment.GetAntiflag():
			return

		if weapon.HasWeapon():
			return

		if player.GetItemIndex(2, item.EQUIPMENT_WEAPON) in weapon.GetVnums():
			return

		_dmg = equipment.GetItemDamage(2, item.EQUIPMENT_WEAPON)
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE or player.GetItemIndex(_slot) in weapon.GetVnums():
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.GetItemType() != item.ITEM_TYPE_WEAPON:
				continue

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if _dmg >= equipment.GetItemDamage(1, _slot):
				continue

			_dmg = equipment.GetItemDamage(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)

	@staticmethod
	def EquipBody():
		if not equipment.GetAntiflag():
			return

		_def = equipment.GetItemDef(2, item.EQUIPMENT_BODY)
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE:
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.GetItemType() != item.ITEM_TYPE_ARMOR or item.GetItemSubType() != item.ARMOR_BODY:
				continue

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if _def >= equipment.GetItemDef(1, _slot):
				continue

			_def = equipment.GetItemDef(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)

	@staticmethod
	def EquipHead():
		if not equipment.GetAntiflag():
			return

		_def = equipment.GetItemDef(2, item.EQUIPMENT_HEAD)
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE:
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.GetItemType() != item.ITEM_TYPE_ARMOR or item.GetItemSubType() != item.ARMOR_HEAD:
				continue

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if _def >= equipment.GetItemDef(1, _slot):
				continue

			_def = equipment.GetItemDef(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)

	@staticmethod
	def EquipShield():
		if not equipment.GetAntiflag():
			return

		_def = equipment.GetItemDef(2, 10)  # no item.EQUIPMENT_SHIELD or anything similar found lol
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE:
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.GetItemType() != item.ITEM_TYPE_ARMOR or item.GetItemSubType() != item.ARMOR_SHIELD:
				continue

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if _def >= equipment.GetItemDef(1, _slot):
				continue

			_def = equipment.GetItemDef(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)

	@staticmethod
	def EquipWrist():
		if not equipment.GetAntiflag():
			return

		_hp = equipment.GetItemHP(2, item.EQUIPMENT_WRIST)
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE:
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR or item.GetItemSubType() != item.ARMOR_WRIST:
				continue

			if _hp >= equipment.GetItemHP(1, _slot) and player.GetItemIndex(2, item.EQUIPMENT_WRIST) != item.ITEM_TYPE_NONE:
				continue

			_hp = equipment.GetItemHP(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)

	@staticmethod
	def EquipEar():
		if not equipment.GetAntiflag():
			return

		_hp = equipment.GetItemHP(2, item.EQUIPMENT_EAR)
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE:
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR or item.GetItemSubType() != item.ARMOR_EAR:
				continue

			if _hp >= equipment.GetItemHP(1, _slot) and player.GetItemIndex(2, item.EQUIPMENT_EAR) != item.ITEM_TYPE_NONE:
				continue

			_hp = equipment.GetItemHP(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)

	@staticmethod
	def EquipNeck():
		if not equipment.GetAntiflag():
			return

		_hp = equipment.GetItemHP(2, item.EQUIPMENT_NECK)
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE:
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR or item.GetItemSubType() != item.ARMOR_NECK:
				continue

			if _hp >= equipment.GetItemHP(1, _slot) and player.GetItemIndex(2, item.EQUIPMENT_NECK) != item.ITEM_TYPE_NONE:
				continue

			_hp = equipment.GetItemHP(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)

	@staticmethod
	def EquipFoots():
		if not equipment.GetAntiflag():
			return

		_hp = equipment.GetItemHP(2, item.EQUIPMENT_SHOES)
		_equipSlot = None

		for _slot in xrange(GetSlots()):
			if player.GetItemIndex(_slot) == item.ITEM_TYPE_NONE:
				continue

			item.SelectItem(player.GetItemIndex(_slot))

			if item.IsAntiFlag(equipment.GetAntiflag()):
				continue

			if item.GetLimit(0)[0] == item.LIMIT_LEVEL and item.GetLimit(0)[1] > player.GetStatus(player.LEVEL):
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				continue

			if item.GetItemType() != item.ITEM_TYPE_ARMOR or item.GetItemSubType() != item.ARMOR_FOOTS:
				continue

			if _hp >= equipment.GetItemHP(1, _slot) and player.GetItemIndex(2, item.EQUIPMENT_SHOES) != item.ITEM_TYPE_NONE:
				continue

			_hp = equipment.GetItemHP(1, _slot)
			_equipSlot = _slot

		if _equipSlot is not None:
			item.SelectItem(player.GetItemIndex(_equipSlot))

			if DEBUG:
				Log("Equipped %s (Slot: %d)" % (item.GetItemName(), _equipSlot))

			net.SendItemUsePacket(_equipSlot)


class setting:
	class YOUNG_HEROES_WEAPON:
		ACTIVE = YOUNG_HEROES_WEAPON_ACTIVE
		QUEST_NAME = YOUNG_HEROES_WEAPON_QUEST_NAME
		WARRIOR = YOUNG_HEROES_WEAPON_WARRIOR
		ASSASSIN = YOUNG_HEROES_WEAPON_ASSASSIN
		SURA = YOUNG_HEROES_WEAPON_SURA
		SHAMAN = YOUNG_HEROES_WEAPON_SHAMAN
		WOLFMAN = YOUNG_HEROES_WEAPON_WOLFMAN

	class LEVEL_CHEST:
		ACTIVE = LEVEL_CHEST_ACTIVE

	class POTION_OF_WISDOM:
		USE_ONE_HOUR = POTION_OF_WISDOM_USE_ONE_HOUR
		USE_THREE_HOURS = POTION_OF_WISDOM_USE_THREE_HOURS

	class EQUIPMENT:
		USE_WEAPON = EQUIPMENT_WEAPON
		USE_BODY = EQUIPMENT_BODY
		USE_HEAD = EQUIPMENT_HEAD
		USE_SHIELD = EQUIPMENT_SHIELD
		USE_JEWELRY = EQUIPMENT_JEWELRY


class LevelUp:
	def __init__(self):
		if DEBUG:
			Log("Initialized")
			
		if player.GetStatus(player.HP) <= 0:
			return
		
		if setting.YOUNG_HEROES_WEAPON.ACTIVE:
			if YOUNG_HEROES_OPEN_ONLY_AFTER_USE == False or weapon.HasAnyWeapon() == False:
				if weapon.IsQuestOpen():
					weapon.Receive()
			weapon.Equip()

		if setting.LEVEL_CHEST.ACTIVE:
			chest.Open()

		if setting.POTION_OF_WISDOM.USE_ONE_HOUR:
			potion.UseOneHour()

		if setting.POTION_OF_WISDOM.USE_THREE_HOURS:
			potion.UseThreeHours()

		if setting.EQUIPMENT.USE_WEAPON:
			equipment.EquipWeapon()

		if setting.EQUIPMENT.USE_BODY:
			equipment.EquipBody()

		if setting.EQUIPMENT.USE_HEAD:
			equipment.EquipHead()

		if setting.EQUIPMENT.USE_SHIELD:
			equipment.EquipShield()

		if setting.EQUIPMENT.USE_JEWELRY:
			equipment.EquipWrist()
			equipment.EquipEar()
			equipment.EquipNeck()
			equipment.EquipFoots()


LevelUp()
