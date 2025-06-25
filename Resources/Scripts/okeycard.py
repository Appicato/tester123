import mt2py
import mt2pyv
mt2py.SetMt2Py(str(1))

DEBUG = False
DEBUGStatus = True
DELAY = 0.25
import dbg
import sys
import chat
import net
import thread
import time, uiMiniGameRumi
import traceback
import player
import mt2pyv

def Log(message):
	chat.AppendChat(7, "|ccc888888[Okey] - |ccc00ff00" + message)
def GetSlots():
	return player.GetExtendInvenMax() if hasattr(player, 'GetExtendInvenMax') and player.GetExtendInvenMax() > 0 else player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
def OutputHand():
	#Log(str(mt2pyv.HAND))
	pass

def setupIfNeeded():
	doHook = False
	try:
		str(mt2pyv.HOOKED)
	except:
		doHook = True
		
	if doHook == True:
		mt2pyv.HOOKED = True
		mt2pyv.inGame = False
		mt2pyv.nxtFinish = False
		
		mt2pyv.COLORS = {
			10: "Red",
			20: "Blue",
			30: "Yellow"
		}

		mt2pyv.HAND = {
			1: None,
			2: None,
			3: None,
			4: None,
			5: None
		}
		mt2pyv.CARDS = 24
		mt2pyv.USED_CARDS = []
		mt2pyv.windowShown = False
		mt2pyv.cardsPulled = False
		mt2pyv.waitForCardsPulled = False
		
		mt2pyv.CardHandTmp = uiMiniGameRumi.RumiGamePage.MoveCardDeckToHand
		def MyCardHand(*args):
			mt2pyv.HAND[args[2][1] + 1] = {
				"color": args[2][2],
				"number": args[2][3]
			}

			mt2pyv.CardHandTmp(*args)
			mt2pyv.cardsPulled = True
			mt2pyv.waitForCardsPulled = True
			
		uiMiniGameRumi.RumiGamePage.MoveCardDeckToHand = DoDetour(MyCardHand)
		
		mt2pyv.CardShowTmp = uiMiniGameRumi.RumiGamePage.Show
		def MyCardShow(*args):

			mt2pyv.CardShowTmp(*args)
			mt2pyv.windowShown = True
		uiMiniGameRumi.RumiGamePage.Show = DoDetour(MyCardShow)
		
		#chat.AppendChat(0, 'Okey-Bot initialized')

def Finish():
	net.SendMiniGameRumiExit()
	mt2pyv.inGame = False
	mt2pyv.windowShown = False
	mt2pyv.nxtFinish = False

	mt2pyv.HAND = {
		1: None,
		2: None,
		3: None,
		4: None,
		5: None
	}
	mt2pyv.USED_CARDS = []
	if DEBUGStatus:
		Log('Finished the round')
	mt2py.SetMt2Py(str(0))

def PullCardsFromDeck():
	mt2pyv.waitForCardsPulled = True
	net.SendMiniGameRumiDeckCardClick()
	#time.sleep(DELAY)

def MoveCardHandToField(slot):
	net.SendMiniGameRumiHandCardClick(1, slot - 1)

	if DEBUG:
		Log("Placed a card (Slot: %d, Color: %s, Number: %d) - Cards left: %d" % (slot, mt2pyv.COLORS[mt2pyv.HAND[slot]["color"]], mt2pyv.HAND[slot]["number"], CardsLeft() - 1))

	mt2pyv.USED_CARDS.append({"color": mt2pyv.HAND[slot]["color"], "number": mt2pyv.HAND[slot]["number"]})
	mt2pyv.HAND[slot] = None

def MoveCardHandToGrave(slot):
	net.SendMiniGameRumiHandCardClick(0, slot - 1)

	if DEBUG:
		Log("Discarded a card (Slot: %d, Color: %s, Number: %d) - Cards left: %d" % (slot, mt2pyv.COLORS[mt2pyv.HAND[slot]["color"]], mt2pyv.HAND[slot]["number"], CardsLeft() - 1))

	mt2pyv.USED_CARDS.append({"color": mt2pyv.HAND[slot]["color"], "number": mt2pyv.HAND[slot]["number"]})
	mt2pyv.HAND[slot] = None

def GetPointsByCombination(cards):
	_sameNumbers = {
		"1-1-1": 20,
		"2-2-2": 30,
		"3-3-3": 40,
		"4-4-4": 50,
		"5-5-5": 60,
		"6-6-6": 70,
		"7-7-7": 80,
		"8-8-8": 90
	}

	_sameColors = {
		"1-2-3": 50,
		"2-3-4": 60,
		"3-4-5": 70,
		"4-5-6": 80,
		"5-6-7": 90,
		"6-7-8": 100
	}

	_differentColors = {
		"1-2-3": 10,
		"2-3-4": 20,
		"3-4-5": 30,
		"4-5-6": 40,
		"5-6-7": 50,
		"6-7-8": 60
	}

	_matchingCards = []
	_color = 0
	_sameColor = False

	for _card in cards:
		_matchingCards.append(_card["number"])

		if _color == 0:
			_color = _card["color"]
		else:
			if _color == _card["color"]:
				_sameColor = True

	_matchingCards.sort()

	_matchingCardsString = "%d-%d-%d" % (_matchingCards[0], _matchingCards[1], _matchingCards[2])

	if _matchingCardsString in _sameNumbers:
		return _sameNumbers[_matchingCardsString]

	if _sameColor:
		return _sameColors[_matchingCardsString]
	else:
		return _differentColors[_matchingCardsString]

def GetPossibilities():
	_possibilities = []

	for _slot, _card in mt2pyv.HAND.items():
		if not _card:
			continue

		if DEBUG:
			Log("Found a %d, checking for color matching cards" % _card["number"])

		_matchingCards = GetColorMatchingCards(_card, 6) if _card["number"] == 7 else GetColorMatchingCards(_card, 5) if _card["number"] == 6 else GetColorMatchingCards(_card, 1, 6)

		if len(_matchingCards) < 2:
			continue

		if DEBUG:
			Log("Found color matching cards (%s)" % str(_matchingCards))

		_possibleCards = {_slot: _card}

		for _matchingSlot, _matchingCard in _matchingCards.items():
			_possibleCards[_matchingSlot] = _matchingCard

		_possibilities.append({"cards": _possibleCards, "points": GetPointsByCombination(_possibleCards.values())})

		if _card["number"] <= 5:
			if DEBUG:
				Log("Checking for matching cards")

			_matchingCards = GetMatchingCards(_card, 1, 5)

			if len(_matchingCards) >= 2:
				if DEBUG:
					Log("Found matching cards (%s)" % str(_matchingCards))

				_possibleCards = {_slot: _card}

				for _matchingSlot, _matchingCard in _matchingCards.items():
					_possibleCards[_matchingSlot] = _matchingCard

				_possibilities.append({"cards": _possibleCards, "points": GetPointsByCombination(_possibleCards.values())})

	return _possibilities

def GetPointsForPossibility(cards):
	num = [cards[0]["number"], cards[1]["number"], cards[2]["number"]]
	color = [cards[0]["color"], cards[1]["color"], cards[2]["color"]]
	if num[0] == num[1] and num[1] == num[2]:
		n = num[0]
		if n == 1:
			return 20
		if n == 2:
			return 30
		if n == 3:
			return 40
		if n == 4:
			return 50
		if n == 5:
			return 60
		if n == 6:
			return 70
		if n == 7:
			return 80
		if n == 8:
			return 90
	sameColor = False
	if color[0] == color[1] and color[1] == color[2]:
		sameColor = True
	num.sort()
	if num[0] == 1 and num[1] == 2 and num[2] == 3:
		if sameColor == True:
			return 50
		else:
			return 10
	if num[0] == 2 and num[1] == 3 and num[2] == 4:
		if sameColor == True:
			return 60
		else:
			return 20
	if num[0] == 3 and num[1] == 4 and num[2] == 5:
		if sameColor == True:
			return 70
		else:
			return 30
	if num[0] == 4 and num[1] == 5 and num[2] == 6:
		if sameColor == True:
			return 80
		else:
			return 40
	if num[0] == 5 and num[1] == 6 and num[2] == 7:
		if sameColor == True:
			return 90
		else:
			return 50
	if num[0] == 6 and num[1] == 7 and num[2] == 8:
		if sameColor == True:
			return 100
		else:
			return 60
	return 0
		
def GetBestPossibility():
	cards = [0, 0, 0]
	maxPoints = 0
	for i in xrange(1, 6):
		if i <= len(mt2pyv.HAND):
			card1 = mt2pyv.HAND[i]
			if not card1:
				continue
			for j in xrange(1, 6):
				if j == i:
					continue
				if j <= len(mt2pyv.HAND):
					card2 = mt2pyv.HAND[j]
					if not card2:
						continue
					for k in xrange(1, 6):
						if k == i or k == j:
							continue
						if k <= len(mt2pyv.HAND):
							card3 = mt2pyv.HAND[k]
							if not card3:
								continue
							if GetPointsForPossibility([card1, card2, card3]) > maxPoints:
								maxPoints = GetPointsForPossibility([card1, card2, card3])
								cards[0] = i
								cards[1] = j
								cards[2] = k
	return cards

def GetPointsForPossibility678(cards):
	num = [cards[0]["number"], cards[1]["number"], cards[2]["number"]]
	color = [cards[0]["color"], cards[1]["color"], cards[2]["color"]]
	sameColor = False
	if color[0] == color[1] and color[1] == color[2]:
		sameColor = True
	num.sort()
	if num[0] == 6 and num[1] == 7 and num[2] == 8:
		if sameColor == True:
			return 100
		else:
			return 0 #Not here
	if num[0] == 5 and num[1] == 6 and num[2] == 7:
		if sameColor == True:
			return 90
		else:
			return 0 #Not here
	return 0

def GetBestPossibility678():
	cards = [0, 0, 0]
	maxPoints = 0
	for i in xrange(1, 6):
		if i <= len(mt2pyv.HAND):
			card1 = mt2pyv.HAND[i]
			if not card1:
				continue
			for j in xrange(1, 6):
				if j == i:
					continue
				if j <= len(mt2pyv.HAND):
					card2 = mt2pyv.HAND[j]
					if not card2:
						continue
					for k in xrange(1, 6):
						if k == i or k == j:
							continue
						if k <= len(mt2pyv.HAND):
							card3 = mt2pyv.HAND[k]
							if not card3:
								continue
							if GetPointsForPossibility678([card1, card2, card3]) > maxPoints:
								maxPoints = GetPointsForPossibility678([card1, card2, card3])
								cards[0] = i
								cards[1] = j
								cards[2] = k
	return cards

def GetPointsForPossibilityNot678(cards):
	num = [cards[0]["number"], cards[1]["number"], cards[2]["number"]]
	color = [cards[0]["color"], cards[1]["color"], cards[2]["color"]]
	if num[0] == num[1] and num[1] == num[2]:
		n = num[0]
		if n == 1:
			return 20
		if n == 2:
			return 30
		if n == 3:
			return 40
		if n == 4:
			return 50
		if n == 5:
			return 60
	sameColor = False
	if color[0] == color[1] and color[1] == color[2]:
		sameColor = True
	num.sort()
	if num[0] == 1 and num[1] == 2 and num[2] == 3:
		if sameColor == True:
			return 50
		else:
			return 10
	if num[0] == 2 and num[1] == 3 and num[2] == 4:
		if sameColor == True:
			return 60
		else:
			return 20
	if num[0] == 3 and num[1] == 4 and num[2] == 5:
		if sameColor == True:
			return 70
		else:
			return 30
	return 0
		
def GetBestPossibilityNot678():
	cards = [0, 0, 0]
	maxPoints = 0
	for i in xrange(1, 6):
		if i <= len(mt2pyv.HAND):
			card1 = mt2pyv.HAND[i]
			if not card1:
				continue
			for j in xrange(1, 6):
				if j == i:
					continue
				if j <= len(mt2pyv.HAND):
					card2 = mt2pyv.HAND[j]
					if not card2:
						continue
					for k in xrange(1, 6):
						if k == i or k == j:
							continue
						if k <= len(mt2pyv.HAND):
							card3 = mt2pyv.HAND[k]
							if not card3:
								continue
							if GetPointsForPossibilityNot678([card1, card2, card3]) > maxPoints:
								maxPoints = GetPointsForPossibilityNot678([card1, card2, card3])
								cards[0] = i
								cards[1] = j
								cards[2] = k
	return cards


def HandOnlyHas678():
	for _slot, _card in mt2pyv.HAND.items():
		if not _card:
			continue
		if _card['number'] < 6:
			return False
	return True

def CardsExist(cards):
	for _card in cards:
		_discarded = False

		for _usedCard in mt2pyv.USED_CARDS:
			if _card["color"] != _usedCard["color"] or _card["number"] != _usedCard["color"]:
				continue

			_discarded = True

		if _discarded:
			return False

	return True

def CardsLeft():
	_cards = 0

	for _card in mt2pyv.HAND.values():
		if not _card:
			continue

		_cards += 1

	return mt2pyv.CARDS - len(mt2pyv.USED_CARDS) - _cards

def GetMatchingCards(data, min=None, max=None):
	if min is None:
		min = 0

	if max is None:
		max = 8

	_matchingCards = {}

	for _slot, _card in mt2pyv.HAND.items():
		if not _card:
			continue

		if _card["number"] < min:
			continue

		if _card["number"] > max:
			continue

		if data["number"] == _card["number"] and data["color"] == _card["color"]:
			continue

		if data["number"] != _card["number"] and data["number"] - 1 != _card["number"] and data["number"] + 1 != _card["number"]:
			continue

		_matchingCards[_slot] = _card

	_matchingCardsChecked = {}

	_cardPlusOne = None
	_cardPlusOneSlot = None
	_cardMinusOne = None
	_cardMinusOneSlot = None

	for _slot, _card in _matchingCards.items():
		if data["number"] + 1 == _card["number"]:
			if not _cardPlusOne:
				_cardPlusOne = _card
				_cardPlusOneSlot = _slot

		if data["number"] - 1 == _card["number"]:
			if not _cardMinusOne:
				_cardMinusOne = _card
				_cardMinusOneSlot = _slot

	if _cardPlusOne and _cardPlusOneSlot and _cardMinusOne and _cardMinusOneSlot:
		_matchingCardsChecked = {
			_cardPlusOneSlot: _cardPlusOne,
			_cardMinusOneSlot: _cardMinusOne
		}
	else:
		_firstCard = None
		_firstCardSlot = None
		_secondCard = None
		_secondCardSlot = None

		for _slot, _card in _matchingCards.items():
			if data["number"] == _card["number"]:
				if not _firstCard:
					_firstCard = _card
					_firstCardSlot = _slot
				else:
					_secondCard = _card
					_secondCardSlot = _slot

		if _firstCard and _firstCardSlot and _secondCard and _secondCardSlot:
			_matchingCardsChecked = {
				_firstCardSlot: _firstCard,
				_secondCardSlot: _secondCard
			}

	return _matchingCardsChecked

def GetColorMatchingCards(data, min=None, max=None):
	if min is None:
		min = 0

	if max is None:
		max = 8

	_matchingCards = {}

	for _slot, _card in mt2pyv.HAND.items():
		if not _card:
			continue

		if _card["number"] < min:
			continue

		if _card["number"] > max:
			continue

		if data["color"] != _card["color"]:
			continue

		if data["number"] == _card["number"]:
			continue

		if data["number"] - 1 != _card["number"] and data["number"] + 1 != _card["number"]:
			continue

		_matchingCards[_slot] = _card

	return _matchingCards

def GetLowestCard(handitems):
	_lowestCard = {
		"slot": 0,
		"number": 0
	}

	for _slot, _card in handitems.items():
		if not _card:
			continue

		if _card["number"] > _lowestCard["number"] != 0:
			continue

		_lowestCard = {
			"slot": _slot,
			"number": _card["number"]
		}

	return _lowestCard

def GetLowestLonelyCard(handitems):
	_lowestCard = {
		"slot": 0,
		"number": 0,
		"color": 0
	}

	for _slot, _card in handitems.items():
		if not _card:
			continue

		if _card["number"] > _lowestCard["number"] != 0:
			continue

		_sameColor = False

		for _colorCard in mt2pyv.HAND.values():
			if not _colorCard:
				continue

			if _colorCard["color"] == _card["color"] and _colorCard["number"] == _card["number"]:
				continue

			if _colorCard["color"] != _card["color"]:
				continue

			_sameColor = True

		if _sameColor:
			continue

		_lowestCard = {
			"slot": _slot,
			"number": _card["number"],
			"color": _card["color"]
		}

	return _lowestCard

def GetHighestCard():
	_highestCard = {
		"slot": 0,
		"number": 0
	}

	for _slot, _card in mt2pyv.HAND.items():
		if not _card:
			continue

		if _card["number"] < _highestCard["number"] != 0:
			continue

		_highestCard = {
			"slot": _slot,
			"number": _card["number"]
		}

	return _highestCard

def canStartGame():
	__import__('gc')
	for obj in sys.modules['gc'].get_objects():
		if isinstance(obj, uiMiniGameRumi.RumiGamePage):
			return True
	chat.AppendChat(7, 'Could not start game, rules window must be opened')
	return False

def mainokeyfunc():
	try:
		setupIfNeeded()

		if DEBUG:
			Log("Start Script")
		if mt2pyv.nxtFinish == True:
			Finish()
			return
		if player.GetStatus(player.HP) <= 0:
			if DEBUGStatus:
				Log("Player is dead")
			mt2py.SetMt2Py(str(5))

		if mt2pyv.inGame == False and player.GetStatus(player.HP) > 0:
			_hasCards = False
			for _slot in xrange(GetSlots()):
				if player.GetItemIndex(_slot) != 79506:
					continue
				_hasCards = True
				break
			if _hasCards == True:
				if canStartGame() == True:
					Log("Starting new Game")
					net.SendMiniGameRumiStart()
					mt2pyv.inGame = True
			else:
				if DEBUGStatus:
					Log("No more cards left")
				mt2py.SetMt2Py(str(4))
		elif mt2pyv.windowShown == True and player.GetStatus(player.HP) > 0:
			if DEBUG:
				Log("Checking hand")
			if mt2pyv.waitForCardsPulled == True and mt2pyv.cardsPulled == False:
				pass
			else:
				mt2pyv.cardsPulled = False
				mt2pyv.waitForCardsPulled = False
				
				moved = False
				if moved == False and CardsLeft() > 0:
					possSlots = GetBestPossibility678()
					if possSlots[0] > 0:
						MoveCardHandToField(possSlots[0])
						MoveCardHandToField(possSlots[1])
						MoveCardHandToField(possSlots[2])
						moved = True
				
				if moved == False and CardsLeft() > 0:
					possSlots = GetBestPossibilityNot678()
					if possSlots[0] > 0:
						MoveCardHandToField(possSlots[0])
						MoveCardHandToField(possSlots[1])
						MoveCardHandToField(possSlots[2])
						moved = True

				if moved == False and (HandOnlyHas678() == True or CardsLeft() <= 0):
					possSlots = GetBestPossibility()
					if possSlots[0] > 0:
						MoveCardHandToField(possSlots[0])
						MoveCardHandToField(possSlots[1])
						MoveCardHandToField(possSlots[2])
						moved = True
				
				if None not in mt2pyv.HAND.values():
					if DEBUG:
						Log("No cards missing, discarding a card")

					_discarded = False
					possCards = {
						1: None,
						2: None,
						3: None,
						4: None,
						5: None
					}
					counter = 0

					for _slot, _card in mt2pyv.HAND.items():
						counter = counter + 1
						if _discarded == True:
							continue
						if not _card:
							continue
						_cn = _card["number"]
						_cc = _card["color"]
						
						_cardsExist1 = False
						_cardsExist2 = False
						
						if _cn == 8 or _cn == 7 or _cn == 6:
							if DEBUG:
								Log("Found a %d 678, prediction for matching cards" % _cn)

							_cardsExist1 = CardsExist([
								{"number": 7 if _cn == 8 else 8, "color": _cc},
								{"number": 6 if _cn == 8 else 6 if _cn == 7 else 7, "color": _cc}
							])
						if _cn == 5 or _cn == 6 or _cn == 7:
							if DEBUG:
								Log("Found a %d 567, prediction for matching cards" % _cn)

							_cardsExist2 = CardsExist([
								{"number": 6 if _cn == 7 else 7, "color": _cc},
								{"number": 5 if _cn == 7 else 5 if _cn == 6 else 6, "color": _cc}
							])

						if not _cardsExist1 and not _cardsExist2:
							if DEBUG:
								Log("Discarding a card1 (%s)" % str(_card))

							possCards[counter] = _card
					
					if not _discarded:
						_lowestCard = GetLowestLonelyCard(possCards)

						if _lowestCard["slot"] > 0:
							if DEBUG:
								Log("Discarding a card3 (%s)" % str(_lowestCard))

							_discarded = True
							MoveCardHandToGrave(_lowestCard["slot"])

					if not _discarded:
						_lowestCard = GetLowestCard(possCards)

						if _lowestCard["slot"] > 0:
							if DEBUG:
								Log("Discarding a card2 (%s)" % str(_lowestCard))
							_discarded = True
							MoveCardHandToGrave(_lowestCard["slot"])
					
					if not _discarded:
						_lowestCard = GetLowestLonelyCard(mt2pyv.HAND)

						if _lowestCard["slot"] > 0:
							if _lowestCard["number"] < 5:
								if DEBUG:
									Log("Discarding a card3 (%s)" % str(_lowestCard))

								_discarded = True
								MoveCardHandToGrave(_lowestCard["slot"])

					if not _discarded:
						_lowestCard = GetLowestCard(mt2pyv.HAND)

						if _lowestCard["slot"] > 0:
							if _lowestCard["number"] < 5:
								if DEBUG:
									Log("Discarding a card2 (%s)" % str(_lowestCard))
								_discarded = True
								MoveCardHandToGrave(_lowestCard["slot"])
								
					if not _discarded:
						_lowestCard = GetLowestLonelyCard(mt2pyv.HAND)

						if _lowestCard["slot"] > 0:
							if _lowestCard["number"] < 6:
								if DEBUG:
									Log("Discarding a card3 (%s)" % str(_lowestCard))

								_discarded = True
								MoveCardHandToGrave(_lowestCard["slot"])

					if not _discarded:
						_lowestCard = GetLowestCard(mt2pyv.HAND)

						if _lowestCard["slot"] > 0:
							if _lowestCard["number"] < 6:
								if DEBUG:
									Log("Discarding a card2 (%s)" % str(_lowestCard))
								_discarded = True
								MoveCardHandToGrave(_lowestCard["slot"])
								
					if not _discarded:
						_lowestCard = GetLowestLonelyCard(mt2pyv.HAND)

						if _lowestCard["slot"] > 0:
							if DEBUG:
								Log("Discarding a card3 (%s)" % str(_lowestCard))

							_discarded = True
							MoveCardHandToGrave(_lowestCard["slot"])

					if not _discarded:
						_lowestCard = GetLowestCard(mt2pyv.HAND)

						if _lowestCard["slot"] > 0:
							if DEBUG:
								Log("Discarding a card4 (%s)" % str(_lowestCard))
							_discarded = True
							MoveCardHandToGrave(_lowestCard["slot"])

				if DEBUG:
					Log("Checking if hand has missing cards")
				if None in mt2pyv.HAND.values() and CardsLeft() > 0:
					if DEBUG:
						Log("Cards missing, pulling new ones")

					PullCardsFromDeck()
				else:
					if DEBUG:
						Log("Cards missing, nothing to pull - STOP")

					mt2pyv.nxtFinish = True

				if DEBUG:
					Log("End Script")
			
		OutputHand()
	except:
		if DEBUGStatus:
			Log("An error occured:")
			Log(str(traceback.format_exc()))
		mt2py.SetMt2Py(str(2))
mainokeyfunc()
