#Memory game. Using pygame to render a game of memory with a set of poker cards
#Author: Anthony Yang Xu
#Last Update: Sept 30, 2018


from abc import ABCMeta, abstractmethod
from collections import deque
import random
import pygame
from pygame.locals import *
import os.path

#Find path for images
main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


class memoryGame:
    selectedCard = []
    all = []
    unMatched = []
    matched = []
    cardCount = 0


    def __init__(self, givenDeck, matchingRule):
        self.deck = givenDeck
        self.deck.shuffle()
        for x in range(self.deck.cardCount()):
            self.cardCount = self.cardCount + 1

            self.all.append(self.deck.deal())
            self.unMatched = self.all[:]
        self.rule = matchingRule

    def isWin(self):
        #if not more cards are unmatched, the game is solved
        return len(self.unMatched) == 0

    #select a given unmatched card. If two cards are selected and they are matching,
    #move them to matched list. If two cards are selected and they are not matching,
    #keep display them until the third card is selected. Then remove the first two
    #cards
    def select(self,card):

        #if the card is unmatched and it is not yet been selected
        if card in self.unMatched and card not in self.selectedCard:

            self.selectedCard.append(card)

        #Check if the two selected card is matching once we have two cards selected
            if len(self.selectedCard) == 2:
            #If matched, remove the selected card from unmached and added to matched
                isMatch = self.rule.isMatching(self.selectedCard[0], self.selectedCard[1])
                if isMatch:
                    #remove matched pair from unmatched and move to matched
                    self.unMatched.remove(self.selectedCard[0])
                    self.unMatched.remove(self.selectedCard[1])
                    self.matched.append(self.selectedCard[0])
                    self.matched.append(self.selectedCard[1])
                    del self.selectedCard[:]

            elif len(self.selectedCard) == 3:
                #Remove the previous two cards.
                del self.selectedCard[0:2]





    def getSize(self):
        return self.cardCount

    #Return all contained cards in a list
    #def staringDeck(self):
    #    return self.all[:]


#The rule for what count as a match.
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

    def toString(self):
        for card in self.cardHolder:
            print card.printAll()


class pokerCard:

    # Expect input such as "S13", "D2"
    def __init__(self, value):
        self.suit = value[0]
        self.value = value[1:]

    def getSuit(self):
        return self.suit

    def getValue(self):
        return self.value

    def toString(self):
        return self.suit + str(self.value)

def main(winstyle = 0):
    pygame.init()
    clock = pygame.time.Clock()

    #initialize the game
    Deck = pokerDeck()
    rule = easyPokerRule()
    game = memoryGame(Deck, rule)
    #Set to full screen

    #set up window
    screenHeight = 1000
    screenWidth = 1720
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    #decorate the game window
    icon = load_image('back_cards-07.png')
    icon = pygame.transform.scale(icon, (32,32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Poker Memory')


    #Divide the screen into n parts where n is the size of deck, 4 rows
    #Assuming the deck size is divisable by 4
    cardNum = game.getSize()
    rowNum = 4
    colNum = cardNum/rowNum
    #If the card is not divisable by 4, add another row
    if cardNum%rowNum != 0:
        rowNum += 1

    height = pygame.display.Info().current_h
    width = pygame.display.Info().current_w

    X_dif = width/colNum
    Y_dif = height/rowNum



    crashed = False

    imageList = []
    #Create an array of images that the index is corresponding to the index of cards
    #in game
    for card in game.all:
        suit = card.getSuit()
        value = card.getValue()
        if value == "1":
            value = "A"
        elif value == "11":
            value = "J"
        elif value == "12":
            value = "Q"
        elif value == "13":
            value = "K"

        cardImgName = value + suit + ".png"

        cardImg = load_image(cardImgName)
        cardImg = pygame.transform.scale(cardImg, (X_dif, Y_dif))
        imageList.append(cardImg)

    #Load card back image
    backImg = load_image("blue_back.png")
    backImg = pygame.transform.scale(backImg, (X_dif, Y_dif))

    font = pygame.font.SysFont("comicsansms", 72)

    winText = font.render("Congraduation! ", True, (128, 0, 0))
    loseText = font.render("A shame! Maybe next time?", True, (128, 0, 0))

    while not crashed and not game.isWin():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #find out the corresponding grid to get correct card
                coord = pygame.mouse.get_pos()
                col = coord[0]/X_dif
                row = coord[1]/Y_dif

                index = col + row * colNum

                #not the best implementation
                game.select(game.all[index])


            #use the index to find out the correct render position
            for unMatchedCard in game.unMatched:
                index = game.all.index(unMatchedCard)
                colCoord = index%13 * X_dif
                rowCoord = index/13 * Y_dif


                screen.blit(backImg, (colCoord, rowCoord))




            for matchedCard in game.matched:
                index = game.all.index(matchedCard)
                colCoord = index%13 * X_dif
                rowCoord = index/13 * Y_dif
                screen.blit(imageList[index], (colCoord, rowCoord))
            for selectedCard in game.selectedCard:
                index = game.all.index(selectedCard)
                colCoord = index%13 * X_dif
                rowCoord = index/13 * Y_dif
                screen.blit(imageList[index], (colCoord, rowCoord))


        pygame.display.update()
        clock.tick(40)

    #Display win/lose text. Quit after 5 second
    if game.isWin():
        screen.blit(winText,
        (100, 300))

    else:
        screen.blit(loseText,
        (100, 300))
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()


if __name__ == '__main__': main()
