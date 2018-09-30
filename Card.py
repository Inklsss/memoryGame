from abc import ABCMeta, abstractmethod
from collections import deque
import random
import pygame
from pygame.locals import *

class memoryGame:
    reveal_MAX = 2
    selectedCard = []
    unMatched = []
    matched = []


    def __init__(self, givenDeck, matchingRule):
        self.deck = givenDeck
        self.deck.shuffle()
        for x in range(self.deck.cardCount()):
            self.unMatched.append(self.deck.deal())
        self.rule = matchingRule

    def isWin(self):
        return len(self.unMatched) == 0

    def select(self,card):
        if card in self.unMatched:
          self.selectedCard.append(card)
        #Check if the two selected card is matching once we have two cards selected
          if len(self.selectedCard) == 2:
            #If matched, remove the selected card from unmached and added to matched
            isMatch = self.rule.isMatching(self.selectedCard[0], self.selectedCard[1])
            print(isMatch)
            if isMatch:
                self.unMatched.remove(self.selectedCard[0])
                self.unMatched.remove(self.selectedCard[1])
                self.matched.append(self.selectedCard[0])
                self.matched.append(self.selectedCard[1])
            #no matter mateched or not, we are done with the current selected cards
            del self.selectedCard[:]


class matchingRule:
    __metaclass__ = ABCMeta
    @abstractmethod
    def isMatching(self, card1, card2):
        pass

#An easier version. Only need the value to be matching
class easyPokerRule(matchingRule):
    def isMatching(self,card1, card2):
        if(card1.getValue() == card2.getValue()):
            return True
        else:
            return False

#A harder version. Need both the color and value to be matching
class hardPokerRule(matchingRule):
    def isMatching(self,card1, card2):
        if(card1.getValue() == card2.getValue() and
        (card1.getSuit() == "S" and card2.getSuit == "C" or
        card1.getSuit() == "C" and card2.getSuit == "S" or
        card1.getSuit() == "H" and card2.getSuit == "D" or
        card1.getSuit() == "D" and card2.getSuit == "H")):
            return True
        else:
            return False

class Deck:
    __metaclass__ = ABCMeta
    @abstractmethod
    def shuffle(self):
        pass

    def deal(self):
        pass

    def isEmpty(self):
        pass

    def cardCount(self):
        pass

#@Deck.register
class pokerDeck(Deck):
    cardHolder = deque([])
    def __init__(self):
        for suit in ["S", "D", "H", "C"]:
            for value in range(1, 14):
                card = pokerCard(suit + str(value))
                self.cardHolder.append(card)

    def isEmpty(self):
        return len(self.cardHolder) == 0

    def deal(self):
        if self.isEmpty():
            print("Out of cards")

        else:
            return self.cardHolder.popleft()



    def shuffle(self):
        for x in range(self.cardCount()-1 ):
            card = self.cardHolder[x]
            newIndex = random.randint(x, self.cardCount() -1)

            self.cardHolder[x] = self.cardHolder[newIndex]
            self.cardHolder[newIndex] = card


    def cardCount(self):
        return len(self.cardHolder)

    def printDeck(self):
        for card in self.cardHolder:
            print card.printAll()


class pokerCard:

    # Expect input such as "S13", "D2"
    def __init__(self, value):
        self.suit = value[0]
        self.value = int(value[1:])

    def getSuit(self):
        return self.suit

    def getValue(self):
        return self.value

    def printAll(self):
        return self.suit + str(self.value)

def main(winstyle = 0):
    pygame.init()
    clock = pygame.time.Clock()
    flip = True

    winstyle = 0
    screen = pygame.display.set_mode((500,500))
    crashed = False

    color1 = (0,0,0)
    color2 = (222,222,222)
    color = True

    #Divide the screen into 
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if color:
                    screen.fill(color1)
                else:
                    screen.fill(color2)
                color = not color#print(pygame.mouse.get_pos())
                print color
        pygame.display.update()
        clock.tick(40)
# Deckk = pokerDeck()
# rule1 = easyPokerRule()
#
# game = memoryGame(Deckk, rule1)
#
# while not game.isWin():
#     print("This is unMatched:\n")
#     for x in game.unMatched:
#         print(x.printAll())
#     print("This is matched:\n")
#     for y in game.matched:
#         print(y.printAll())
#
#     print("This is selected:\n")
#     for z in game.selectedCard:
#         print(z.printAll())
#     print("Enter index: ")
#     index = input()
#     #print(type(game.unMatched[0]))
#     game.select(game.unMatched[int(index)])



#print("\n")
#print(Deckk.cardCount())
#Deckk.shuffle()
#print(Deckk.printDeck())

if __name__ == '__main__': main()
