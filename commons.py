import random
import handTypes
#constants
RANKS = [2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K", "A"]
SUITS = ["H", "D", "S", "C"]
BLIND = 20

#Queue data structure
class Queue:
    
    #queue initialise 
    def __init__(self,size,array=[]):

        #queue atributres
        self.array=array
        self.size =size
        self.head = 0
        self.tail = len(self.array)
        for i in range(size-self.tail):
            self.array.append(None)
        self.gap = self.tail - self.head

    #enqueue method (adds to queue)  
    def enqueue(self,data):
        if not(self.isFull()):
            self.array[self.tail] = data
            self.tail = (self.tail+1)%self.size
            self.gap+=1
        else:
            raise Exception("queue full")
    
    #dequeue method (returns front of queue and removes it from queue)
    def dequeue(self):
        if not(self.isEmpty()):
            data = self.array[self.head]
            self.head = (self.head +1)% self.size
            self.gap-=1
            return data
        else:
            raise Exception("queue empty")
    
    #peek method (returns front of queue)
    def peek(self):
        if not(self.isEmpty()):
            return self.array[self.head]
        else:
            return None
    
    #isEmpty method (checks if queue is empty)
    def isEmpty(self):
        if self.gap == 0:
            return True
        else:
            return False
        
    #isFull method (checks if queue is full)
    def isFull(self):
        if self.gap == self.size:
            return True
        else:
            return False

#card object
class Card:

    #card initialise 
    def __init__(self, suit, rank):
        
        #card attributes
        self.suit = suit
        self.rank = rank
        self.value = self.score()

    #card magic reprsent method
    def __repr__(self):
        return str(self.rank)+str(self.suit)

    #score method (returns interger score of card)
    def score(self):
        if type(self.rank) is int:
            return self.rank
        elif self.rank == "T":
            return 10 
        elif self.rank == "J":
            return 11
        elif self.rank == "Q":
            return 12
        elif self.rank == "K":
            return 13
        elif self.rank == "A":
            return 14
         
        
#Hand object
class Hand:
    
    #Hand initialise
    def __init__(self):

        #Hand attributes
        self.cards = []

    #Hand magic reprsent method
    def __repr__(self):
        string = ""
        for i in self.cards:
            string += str(i) +" "
        return string
    
    #genCards method (takes amount of cards and deck then takes cards of top of deck and adds to hand)
    def genCards(self,amt,deck):
        for i in range(amt):
            self.cards.append(deck.takeCard())

    def checkScore(self,common):
        tempCards = self.cards.copy() + common.cards.copy()
        self.hand = handTypes.checkHand(tempCards)
#Dack object
class Deck:
    
    #Deck initialise
    def __init__(self):

        #Deck attributes
        self.deck=[]
        for rank in RANKS:
            for suit in SUITS:
                self.deck.append(Card(suit,rank))
        #Shuffles deck
        self.shuffle()
    
    #takeCard method(returns top of deck and removes from deck)
    def takeCard(self):
        return self.deck.pop()

    #shuffle method(shuffles the deck)
    def shuffle(self):
        random.shuffle(self.deck)

#Common object
class Common:

    #Common initialise
    def __init__(self):
        #Common atributes
        self.cards=[]

    #Common magic reprsent method (returns string made from cards)
    def __repr__(self):
        string = ""
        for i in self.cards:
            string += str(i) +" "
        return string
    #Common newGame method(takes in deck generates the first 3 cards)
    def newGame(self,deck):
        self.genCards(3,deck)

    #Common turnOrRiver method(takes in deck generates a card)
    def turnORriver(self,deck,):
        self.genCards(1,deck)

    #genCards method (takes amount of cards and deck then deals cards to table)
    def genCards(self,amt,deck):
        for i in range(amt):
            newCard = deck.takeCard()
            self.cards.append(newCard)
            print(f"{newCard} <> Dealt to table")

#Player object
class Player:

    #Player initialise
    def __init__(self,name, chips,client):

        #Player attributes
        self.name = name
        self.client = client
        self.chips = chips
        self.hand = None
        self.bet = 0
        self.sittingOut = False
    
    #Player newGame method (takes in deck resets players hand and deals first two cards)
    def newGame(self,deck):
        self.hand = Hand()
        self.hand.genCards(2,deck)
        self.client.sendMsg((f"{self.name} : {self.hand}"))

    #Player blindBet method (takes the amt to bet removes from player returns False if player doesnt have enough chips else returns the amount bet)
    def blindBet(self,amt):
        self.chips = self.chips-amt
        self.bet += amt
        if self.chips < 0:
            self.sittingOut=True
            return False
        else:
            return amt

    #Player callRaiseFold method (takes in the current bet, then askes player to bet , Returning false if bet cant be made else returning bet amount)
    def callRaiseFold(self,current):
        for i in range(3):
            betamt = current-self.bet
            self.client.sendMsg(f"{self.name}  >>>  Call:{betamt}   Raise  Fold  <<< : ")
            opt = self.client.recive()
            if opt.upper() =="CALL":
                self.chips -= betamt
                self.bet = current
                if self.chips >= 0:
                    return betamt
                else:
                    self.sittingOut=True
                    return False

            elif opt.upper() =="RAISE":
                self.client.sendMsg(f"{self.name}  >>> Amount to raise from [{current}] <<< : ")
                amt = int(self.client.recive())
                betamt = current + amt
                self.chips -= betamt - self.bet
                self.bet = betamt
                if self.chips >= 0:
                    return betamt
                else:
                    self.sittingOut=True
                    return False
                    
            elif opt.upper() == "FOLD":
                self.sittingOut=True
                return
            elif i<2:
                self.client.sendMsg(f"{self.name}  >>>  Choice is not option try again ")
            else:
                self.client.sendMsg(f"{self.name}  >>>  Too many failed attemps ")



#Table object
class Table:

    #Table initialise
    def __init__(self):

        #Table attributes
        self.seats=[]
        self.pool = 0
        self.dealer=0
        self.sittingOutCount = 0
        self.inPlay = True
        self.deck= Deck()
        self.common = Common()

    #Table addPlayer method (takes client connection and creates player on table)
    def addPlayer(self,client):
        self.seats.append(Player("none",1000,client))

    #Table removePlayer method (takes seatNumber and removes)
    def removePlayer(self,seat):
        del self.seats[seat]

    #Table sendAll method(takes message and sends to all clients)
    def sendAll(self,msg):
        for i in self.seats:
            i.client.sendMsg(msg)

    #Table preFlop method(resets table takes blinds and deals preflop)
    def preFlop(self):
        # dev notes # Bust handling needed
        bet = self.seats[(self.dealer+1) % len(self.seats)].blindBet(BLIND//2)

        if bet:
            self.pool += bet
        else:
            self.sittingOutCount +=1

        bet = self.seats[(self.dealer+2) % len(self.seats)].blindBet(BLIND)

        if bet:
            self.pool += bet
        else:
            self.sittingOutCount +=1

        i = (self.dealer+1) % len(self.seats)
        dealCount= 0
        while dealCount < len(self.seats) :
            if not(self.seats[i].sittingOut):
                self.seats[i].newGame(self.deck)
            i = (i+1)%len(self.seats)
            dealCount+=1

        i = (self.dealer+3) % len(self.seats)
        currentBet = BLIND
        bigBlindPlayed = False
        #dev notes # boot dead players needed

        while (self.seats[i].bet != currentBet or self.seats[i].sittingOut or not(bigBlindPlayed)) and self.inPlay:
            if not(self.seats[i].sittingOut):

                #dev notes # bust handling
                bet = self.seats[i].callRaiseFold(currentBet)
                print(bet)
                if bet:
                    self.pool += bet
                    print(f"Pool now: {self.pool}")

                    if self.seats[i].bet > currentBet:
                        currentBet = self.seats[i].bet
                else:
                    if self.seats[i].sittingOut:
                        self.sittingOutCount += 1
                        if self.sittingOutCount >= len(self.seats)-1:
                            self.inPlay=False

            if i == (self.dealer + 2) % len(self.seats):
                bigBlindPlayed = True

            i = (i+1)%len(self.seats)

        for i in self.seats:
            i.bet = 0
        
        


    #Table flop method (deals the flop) 
    def flop(self):
        self.common.newGame(self.deck)
        self.sendAll(f"THE FLOP : {self.common.cards}")
        i = (self.dealer+1) % len(self.seats)
        currentBet = 0
        loopComplete = False
        while (self.seats[i].bet != currentBet or self.seats[i].sittingOut or not(loopComplete)) and self.inPlay:
            if not(self.seats[i].sittingOut):
                    #bust handling      -------------------------------------------------------------<<<<<<
                bet = self.seats[i].callRaiseFold(currentBet)
                if bet:
                    self.pool += bet

                else:
                    if self.seats[i].sittingOut:
                        self.sittingOutCount += 1
                        if self.sittingOutCount >= len(self.seats)-1:
                            self.inPlay=False
                


                if self.seats[i].bet > currentBet:
                    currentBet = self.seats[i].bet
            if i == self.dealer:
                loopComplete = True
            i = (i+1)%len(self.seats)
        for i in self.seats:
            i.bet = 0

        
    #Table one card method (takes in name eg/turn or river and deals one card)
    def oneCard(self,name):
        self.common.turnORriver(self.deck)
        self.sendAll(f"THE {name} : {self.common.cards}")
        i = (self.dealer+1) % len(self.seats)
        currentBet = 0
        loopComplete = False
        while (self.seats[i].bet != currentBet or self.seats[i].sittingOut or not(loopComplete)) and self.inPlay:
            if not(self.seats[i].sittingOut):
                    #bust handling
                bet = self.seats[i].callRaiseFold(currentBet)
                if bet:
                    self.pool += bet
                    print(f"Pool now: {self.pool}")
                
                else:
                    if self.seats[i].sittingOut:
                        self.sittingOutCount += 1
                        if self.sittingOutCount >= len(self.seats)-1:
                            self.inPlay=False

                if self.seats[i].bet > currentBet:
                    currentBet = self.seats[i].bet
            if i == self.dealer:
                loopComplete = True
            i = (i+1)%len(self.seats)

        for i in self.seats:
            i.bet = 0
        
    #Table endGame method (ends the game and sorts winners)
    def endGame(self):
        finishers = []
        for i in self.seats:
            if not(i.sittingOut):
                i.hand.checkScore(self.common)
                finishers.append(i)
        finishers.sort(key = lambda x : x.hand.hand.score(), reverse=True)
        

        if finishers:
            self.sendAll(f"{finishers[0].name} Won!!! with {finishers[0].hand.hand}")
            finishers[0].chips += self.pool
        else:
            print("Error")

        self.end()
    #Table end method(runs end of game resets)
    def end(self):
        for i in self.seats:
            i.sittingOut = False
        self.inPlay=True
        self.sittingOutCount = 0 
        self.pool = 0
        self.dealer= self.dealer+1 % len(self.seats)
        self.deck= Deck()
        self.common = Common()
    
    #Table foldedEnd(ends game when winner is only none folded player)
    def foldedEnd(self):
        winner = None
        for i in self.seats:
            if not(i.sittingOut):
                winner = i
                break
        self.sendAll(f"{winner.name} Won!!! As everyone folded. ")
        self.end()

    

        
        



        