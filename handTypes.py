

#scoreHand function(takes in hand type and cards returns a hashed value)
def scoreHand(handTypeValue,c1,c2,c3,c4,c5):
    return 759375*handTypeValue+50625*c1+3375*c2+225*c3+15*c4+c5

#HighCard object (5 different cards)
class HighCard:
    def __init__(self,cards):
        self.cards = cards
        self.value = 0
    def score(self):
        return scoreHand(self.value,self.cards[0].value,self.cards[1].value,self.cards[2].value,self.cards[3].value,self.cards[4].value)
    def __repr__(self):
        string = "HIGHCARD "
        for i in self.cards:
            string += " "+str(i)
        return string
#OnePair object (2 cards same rank rest different)
class OnePair:
    def __init__(self,pairCard,cards):
        self.pairCard = pairCard
        self.cards = cards
        self.value=1
    def score(self):
        return scoreHand(self.value,self.pairCard[0].value,self.pairCard[1].value,self.cards[0].value,self.cards[1].value,self.cards[2].value,)
    def __repr__(self):
        string = f"ONEPAIR {self.pairCard}"
        for i in self.cards:
            string += " "+str(i)
        return string

#TwoPair object(2 sets of 2 cards same rank)
class TwoPair:
    def __init__(self,pairCard1,pairCard2,card):
        self.pairCard1 = pairCard1
        self.pairCard2 = pairCard2
        self.card = card
        self.value=2
    def score(self):
        return scoreHand(self.value,self.pairCard1[0].value,self.pairCard1[1].value,self.pairCard2[0].value,self.pairCard2[1].value,self.card.value)
    def __repr__(self):
        string = f"TWOPAIR {self.pairCard1} {self.pairCard2} {self.card}"
        return string

#ThreePair object(3 cards same rank rest different)
class ThreeOfAKind:
    def __init__(self,threeCard,cards):
        self.threeCard = threeCard
        self.cards = cards
        self.value=3
    def score(self):
        return scoreHand(self.value,self.threeCard[0].value,self.threeCard[1].value,self.threeCard[1].value,self.cards[0].value,self.cards[1].value)
    def __repr__(self):
        string = f"THREEOFAKIND {self.threeCard}"
        for i in self.cards:
            string += " "+ str(i)
        return string

#Straight object(5 cards increasing in rank conseculativly)
class Straight:
    def __init__(self,cards):
        self.value = 4
        self.cards = cards
    def score(self):
        return scoreHand(self.value,self.cards[0].value,self.cards[1].value,self.cards[2].value,self.cards[3].value,self.cards[4].value)
    def __repr__(self):
        string = "STRAIGHT"
        for i in self.cards:
            string += " "+ str(i)
        return string

#Flush object(5 cards same suit)
class Flush:
    def __init__(self,cards):
        self.value = 5
        self.cards = cards
    def score(self):
        return scoreHand(self.value,self.cards[0].value,self.cards[1].value,self.cards[2].value,self.cards[3].value,self.cards[4].value)
    def __repr__(self):
        string = "FLUSH"
        for i in self.cards:
            string += " "+ str(i)
        return string

#FullHouse object (3 cards same rank and 2 cards same rank )
class FullHouse:
    def __init__(self,threeCard,pairCard):
        self.pairCard = pairCard
        self.threeCard = threeCard
        self.value=6
    def score(self):
        return scoreHand(self.value,self.threeCard[0].value,self.threeCard[1].value,self.threeCard[2].value,self.pairCard[0].value,self.pairCard[1].value)
    def __repr__(self):
        string = f"FULLHOUSE {self.threeCard} {self.pairCard}"
        return string
    
#FourOfAKind object (4 cards same rank)
class FourOfAKind:
    def __init__(self,fourCard,card):
        self.fourCard = fourCard
        self.card = card
        self.value=7
    def score(self):
        return scoreHand(self.value,self.fourCard[0].value,self.fourCard[1].value,self.fourCard[2].value,self.fourCard[3].value,self.card.value)

    def __repr__(self):
        string = f"FOUROFAKIND {self.fourCard} {self.card}"
        return string

#StraightFlush object (5 cards same suit and increasing conseculatively)
class StraightFlush:
    def __init__(self,cards):
        self.value = 8
        self.cards = cards
    def score(self):
        return scoreHand(self.value,self.cards[0].value,self.cards[1].value,self.cards[2].value,self.cards[3].value,self.cards[4].value)
    def __repr__(self):
        string = "STAIGHTFLUSH"
        for i in self.cards:
            string += " "+ str(i)
        return string



#checkHand function (takes list of cards returns highest scoring hand object) 
def checkHand(cards):
    
    tempCards = cards.copy()
    rankCount = {"A":[],"K":[],"Q":[],"J":[],"T":[],9:[],8:[],7:[],6:[],5:[],4:[],3:[],2:[]}
    suits = {"H":[],"S":[],"D":[],"C":[]}
    straight = []
    scheck = False
    best = None
    bestHand = []
    amounts = {4:[],3:[],2:[],1:[],0:[]}
    pairCounts = {2:0,3:0,4:0}

    #count cards ranks and suits
    for i in tempCards:
        rankCount[i.rank].append(i)
        suits[i.suit].append(i)
        
    cardCount=0
    #striaght check and amounts
    for i in rankCount:
        rlen = len(rankCount[i])
        amounts[rlen].append(rankCount[i])
        if rlen > 0 and not(scheck):
            straight.append(rankCount[i][0])
            if len(straight) == 5:
                scheck = True
        elif not(scheck):
            straight= []

    #check 4s
    if (amounts[4]):
            bestHand.append(amounts[4][0])
            pairCounts[4]+=1
            cardCount+=4

    #check 3s
    if cardCount <= 2:
        if (amounts[3]):
            bestHand.append(amounts[3][0])
            pairCounts[3]+=1
            cardCount+=3

    #check 2s
    if cardCount <= 3:
        for i in amounts[2]:
            if cardCount >3:
                break
            bestHand.append(i)
            pairCounts[2]+=1
            cardCount+=2

    #add single cards
    if cardCount <= 4:
        for i in amounts[1]:
            if cardCount ==5:
                break        
            bestHand.append(i[0])
            cardCount+=1

    #Construct best
    if pairCounts[2]==1:
        if pairCounts[3]==1:
            best = FullHouse(bestHand[0],bestHand[1])
        else:
            best = OnePair(bestHand[0],bestHand[1:])
    elif pairCounts[2]==2:
        best = TwoPair(bestHand[0],bestHand[1],bestHand[2])
    elif pairCounts[3]==1:
        best = ThreeOfAKind(bestHand[0],bestHand[1:])
    elif pairCounts[4]==1:
        best = FourOfAKind(bestHand[0],bestHand[1])
    else:
        best=HighCard(bestHand)
    if scheck and best.score()<3037500:
        best = Straight(straight)

    for i in suits:
        if len(suits[i])==5:
            if scheck and suits[i] == straight:
                best = StraightFlush(suits[i])
            elif best.score() < 3796875:
                best = Flush(suits[i])
                
                
    return best

