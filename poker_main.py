# Jonathan oakley poker server

#imports modules
import commons
import connHandle
import threading
import time


#the main procudure
def main():
    #start connection handling thread
    queueThread = threading.Thread(target=connHandle.initSocket)
    queueThread.start()
    

    #create the table
    mainTable = commons.Table()
    

    while True:
        mainTable.cleanUp()
        #connect players from queue if seats not full
        if len(mainTable.seats) < 6:
            #loop enough to fill all seats
            for i in range(6-len(mainTable.seats)):
                #check queue
                if not(connHandle.waitingQueue.isEmpty()):
                    #add player from queue
                    mainTable.addPlayer(connHandle.waitingQueue.dequeue())
                else:
                    #break when queue emoty
                    break

        #confirm enough players
        if len(mainTable.seats) >= 2:
            #deal and bets preflop
            mainTable.preFlop()
            #deal and betsflop

            if mainTable.inPlay:
                mainTable.dealCards("FLOP",3)

            #deal and bets turn
            if mainTable.inPlay:
                mainTable.dealCards("TURN",1)

            #deal and bets river
            if mainTable.inPlay:
                mainTable.dealCards("RIVER",1)
            #end the game
            if mainTable.inPlay:
                mainTable.endGame()
            #end the game
            else:
                mainTable.foldedEnd()
        else:
            mainTable.sendAll("waiting for players...\n")
            time.sleep(1)

        #increment dealer seat

#checks if the the name is main. ensure file is being excuted
if __name__ == "__main__":
    #call main
    main()