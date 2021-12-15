import random
import handTypes
#constants
RANKS = [2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K", "A"]
SUITS = ["H", "D", "S", "C"]
BLIND = 20
CHIPSHEETPATH = "D:\python\python_poker\chips_sheet.txt"

def readChipSheet():
    with open(CHIPSHEETPATH,"rt") as chipSheet:
        chipSheetAraay = []
        for line in chipSheet:
            chipSheetAraay.append(line.split())
        return chipSheetAraay

def readSearch(name,chipSheetArray):
    i = len(chipSheetArray)//2
    start = 0
    stop = len(chipSheetArray)-1
    while start!=stop:
        i = (start+stop)//2
        if name <= chipSheetArray[i][0]:
            stop = i
        else:
            start= i+1
    if chipSheetArray[start][0] == name:
        return start
    else:
        return False

def validateCreds(name,password):
    chipSheetArray = readChipSheet()
    playerPos = readSearch(name,chipSheetArray)
    if isinstance(playerPos,int):
        if chipSheetArray[playerPos][1] == password and int(chipSheetArray[playerPos][3]):
            chipSheetArray[playerPos][3] = "0"
            saveChipSheet(chipSheetArray)
            return int(chipSheetArray[playerPos][2])
    return False

def savePlayer(name,chips):
    chipSheetArray = readChipSheet()
    playerPos = readSearch(name,chipSheetArray)
    chipSheetArray[playerPos][3] = "1"
    chipSheetArray[playerPos][2] = str(chips)
    saveChipSheet(chipSheetArray)

def saveChipSheet(sheet):
    midArray=[]
    for line in sheet:
        midArray.append(" ".join(line))
    out = "\n".join(midArray)
    with open(CHIPSHEETPATH,"wt") as chipSheet:
        chipSheet.write(out)
    


    

#Queue data structure
class Queue:
    
    #queue initialise 
    def __init__(self,size,array=None):

        #queue atributres
        if array == None:
            self.array= []
        else:
            self.array = array
        self.size =size

    #enqueue method (adds to queue)  
    def enqueue(self,data):
        if not(self.isFull()):
            self.array.append(data)
        else:
            raise Exception("queue full")
    
    #dequeue method (returns front of queue and removes it from queue)
    def dequeue(self):
        if not(self.isEmpty()):
            data = self.array[0]
            del self.array[0]
            return data
        else:
            raise Exception("queue empty")
    
    #peek method (returns front of queue)
    def peek(self):
        if not(self.isEmpty()):
            return self.array[0]
        else:
            return None
    
    #isEmpty method (checks if queue is empty)
    def isEmpty(self):
        if len(self.array) == 0:
            return True
        else:
            return False
        
    #isFull method (checks if queue is full)
    def isFull(self):
        if len(self.array) == self.size:
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
        if isinstance(self.rank,int):
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
        self.connected = True

    def __del__(self):
        savePlayer(self.name,self.chips)

    
    #Player newGame method (takes in deck resets players hand and deals first two cards)
    def newGame(self,deck):
        self.hand = Hand()
        self.hand.genCards(2,deck)    
        self.sendMsg(f"{self.name} : {self.hand}\n")
        
    def sendMsg(self,msg):
        try:
            self.client.sendMsg(msg)
        except Exception:
            self.connected = False
            self.sittingOut = True
    def recive(self):
        try: 
            msg = self.client.recive()
        except Exception:
            self.connected = False
            self.sittingOut = True
            msg = False

        return msg

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
            self.sendMsg(f"{self.name} chips: {self.chips}  >>>  Call:{betamt}   Raise  Fold  <<< : ")
            opt = self.recive()
            if opt == False:
                break
            elif opt.upper() =="CALL":
                self.chips -= betamt
                self.bet = current
                if self.chips >= 0:
                    return betamt
                else:
                    self.sittingOut=True
                    return False

            elif opt.upper() =="RAISE":
                for x in range(3):
                    try:
                        self.sendMsg(f"{self.name}  >>> Amount to raise from [{current}] <<< : ")
                        amt = int(self.recive())
                        if amt >= 0:
                            break
                        raise Exception
                    except Exception:
                        self.sendMsg(f"{self.name}  >>> Amount must be positve interger You have {2-x} more attemps\n")
                        amt = None
                
                if isinstance(amt,int):
                    betamt = current + amt
                    self.chips -= betamt - self.bet
                    self.bet = betamt
                    if self.chips >= 0:
                        return betamt
                    else:
                        self.sittingOut=True
                        return False
                else:
                    self.sendMsg(f"{self.name}  >>> Raise failed choose again\n")
                    
            elif opt.upper() == "FOLD":
                self.sittingOut=True
                return
                
            elif i<2:
                self.sendMsg(f"{self.name}  >>>  Choice is not option try again \n")
            else:
                self.sendMsg(f"{self.name}  >>>  Too many failed attemps \n")
                self.sittingOut=True

            



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
        self.seats.append(client)

    #Table removePlayer method (takes seatNumber and removes)
    def removePlayer(self,seat):
        del self.seats[seat]

    #Table sendAll method(takes message and sends to all clients)
    def sendAll(self,msg):
        for i in self.seats:
            if i.connected:
                i.sendMsg(msg)
                if not(i.connected):
                    self.sittingOutCount +=1
    def sendMsg(self,player,msg):
        if player.connected:
                player.sendMsg(msg)
                if not(player.connected):
                    self.sittingOutCount +=1

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
        endp = (self.dealer + 2) % len(self.seats)
        self.takeBets(BLIND,i,endp)

        for i in self.seats:
            i.bet = 0
        
        
    #Table one card method (takes in name eg/turn or river and deals one card)
    def dealCards(self,name,amt):
        self.common.genCards(amt,self.deck)
        self.sendAll(f"\nTHE {name} : {self.common.cards}\n\n")
        i = (self.dealer+1) % len(self.seats)
        endp = (i+1) % len(self.seats)
        self.takeBets(0,i,endp)

    def takeBets(self,currentBet,i,endp):
        loopComplete = False
        while (self.seats[i].bet != currentBet or self.seats[i].sittingOut or not(loopComplete)) and self.inPlay:
            if not(self.seats[i].sittingOut):
                    #bust handling
                bet = self.seats[i].callRaiseFold(currentBet)
                if bet:
                    self.pool += bet
                    self.sendAll(f"Pool : {self.pool}\n")
                
                else:
                    if self.seats[i].sittingOut:
                        self.sittingOutCount += 1

                if self.seats[i].bet > currentBet:
                    currentBet = self.seats[i].bet
            if i == endp:
                loopComplete = True
            if self.sittingOutCount >= len(self.seats)-1:
                self.inPlay=False
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
            self.sendAll(f"{finishers[0].name} Won {self.pool} !!! with {finishers[0].hand.hand}\n")
            finishers[0].chips += self.pool
        else:
            print("Error")

        self.end()
    #Table end method(runs end of game resets)
    def end(self):
        self.cleanUp()
        for i in self.seats:
            self.sendMsg(i,f"Balance : {i.chips}\n\n")
            i.sittingOut = False
        self.inPlay=True
        self.sittingOutCount = 0 
        self.pool = 0
        self.dealer= self.dealer+1 % len(self.seats)
        self.deck= Deck()
        self.common = Common()
    def cleanUp(self):
        for seat ,i in enumerate(self.seats):
            if not(i.connected):
                self.removePlayer(seat)
                
    #Table foldedEnd(ends game when winner is only none folded player)
    def foldedEnd(self):
        winner = None
        for i in self.seats:
            if not(i.sittingOut):
                winner = i
                break
        if winner:
            winner.chips += self.pool
            self.sendAll(f"{winner.name} Won {self.pool} chips !!! As everyone folded. \n")
        self.end()

    

        
        



        