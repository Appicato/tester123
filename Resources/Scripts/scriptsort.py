import chat, player, item, math, net, sys, chr
SORT_TYPE = 3
SLOTS = player.GetExtendInvenMax() if hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 else player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
SLOTS_PER_PAGE = player.INVENTORY_PAGE_SIZE
class Chat:
    @staticmethod
    def info(string):
        return 0
        chat.AppendChat(3, string)
      
class Item:
    def __init__(self, id, slot, size, name):
        self.id = id
        self.slot = slot
        self.size = size
        self.name = name
    def move(self, slot):
        Chat.info("===> The item " + str(self.name) + " has been moved to slot " + str(slot))
        net.SendItemMovePacket(self.slot, slot, 0)
        self.slot = slot
        
class ItemHandler:
    def __init__(self):
        self.list = []
        self.placed = []
    
    def retrieveItems(self):
        Chat.info("========= Retrieving item list ==========")
        
        for slot in range(SLOTS):
            item_id = player.GetItemIndex(slot)
            if item_id != 0:
                item.SelectItem(item_id)
                self.list.append(Item(item_id, slot, int(item.GetItemSize()[1]), item.GetItemName()))
        
        Chat.info("========= Retrieving successful ==========")
                
    def sortByID(self):
        chat.AppendChat(3, "========= Sorting items by ID ==========")
        
        self.list.sort(key=lambda item: item.id, reverse=False)
        
        Chat.info("========= Sorting successful ==========")
        
    def sortByName(self):
        chat.AppendChat(3, "========= Sorting items by NAME ==========")
        
        self.list.sort(key=lambda item: item.name, reverse=False)
        
        Chat.info("========= Sorting successful ==========")
        
    def sortBySizeAndID(self):
        chat.AppendChat(3, "========= Sorting items by Size ==========")
        
        self.list.sort(key=lambda item: (-item.size, item.id), reverse=False)
        
        Chat.info("========= Sorting successful ==========")
    
    def sortBySizeReversed(self):
        chat.AppendChat(3, "========= Sorting items by Size Reversed ==========")
        
        self.list.sort(key=lambda item: item.size, reverse=False)
        
        Chat.info("========= Sorting successful ==========")
        
    def getNextSlot(self, size):
        for page in range(int(math.ceil(SLOTS / SLOTS_PER_PAGE))):
            LAST_SLOT_THIS_PAGE = min((page + 1) * SLOTS_PER_PAGE, SLOTS)
            for slot in range(page * SLOTS_PER_PAGE, LAST_SLOT_THIS_PAGE):
                if slot + 5 * (size - 1) < LAST_SLOT_THIS_PAGE:
                    good = True
                    
                    for i in range(size):
                        if (slot + 5 * i) in self.placed:
                            good = False
                    
                    if good:
                        Chat.info("===> Best slot found is " + str(slot))
                        return slot
        
        Chat.info("===> No free slots found of size " + str(size))
        return -1
        
    def itemsInSlot(self, slot, size):
        items = []
        for i in range(size):
            cur_slot = slot + i * 5
            it = [x for x in self.list if x.slot == cur_slot or (x.size == 2 and x.slot + 5 == cur_slot or False) or (x.size == 3 and (x.slot + 10 == cur_slot or x.slot + 5 == cur_slot) or False) ]
            
            if len(it) > 0 and it[0] not in items:
                Chat.info("=====> The item " + str(it[0].name) + " is in the way" + str(size))
                items.append(it[0])
        
        return items
    
    def getNextFreeSlot(self, size, skip = []):
        for page in range(int(math.ceil(SLOTS / SLOTS_PER_PAGE))):
            LAST_SLOT_THIS_PAGE = min((page + 1) * SLOTS_PER_PAGE, SLOTS)
            for slot in range(page * SLOTS_PER_PAGE, LAST_SLOT_THIS_PAGE):
                if slot not in skip and len(self.itemsInSlot(slot, size)) == 0 and slot + 5 * (size - 1) < LAST_SLOT_THIS_PAGE:
                    return slot
        
        Chat.info("Could not find any free slot")
        return -1        
    def setItemAsPlaced(self, item):
        Chat.info("===> The item has been placed in the right slot")
        for i in range(item.size):
            self.placed.append(item.slot + 5 * i)
    
    def sort(self):
        self.retrieveItems()
        
        if SORT_TYPE == 1:
            self.sortByID()
        elif SORT_TYPE == 2:
            self.sortByName()
        elif SORT_TYPE == 3:
            self.sortBySizeAndID()
        else:
            self.sortBySizeReversed()
        
        for it in self.list:
            for z in range(1000):
                continue
            Chat.info("Sorting Item " + str(it.name))
            
            next_slot = self.getNextSlot(it.size)
            
            if next_slot == -1:
                continue;
            
            if it.slot == next_slot:
                self.setItemAsPlaced(it)
                continue
            
            occupied_slots = []
            
            for i in range(it.slot):
                occupied_slots.append(next_slot + 5 * i)
            
            for in_way_item in self.itemsInSlot(next_slot, it.size):
                next_free_slot = self.getNextFreeSlot(in_way_item.size, occupied_slots)
                
                if next_free_slot == -1:
                    continue
                    
                in_way_item.move(next_free_slot)
                
            it.move(next_slot)
            self.setItemAsPlaced(it)
handler = ItemHandler()
handler.sort()
chr.Refresh()
