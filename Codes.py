from random import random
import copy
import time

playCount=100

class ConnectSin:
    YOU = 1
    CPU = -1
    EMPTY = 0
    DRAW = 0
    __CONNECT_NUMBER = 4
    board = None

    def __init__(self, board_size=(6, 7), silent=False,depth=3):
        assert len(board_size) == 2, "board size should be a 1*2 tuple"
        assert board_size[0] > 4 and board_size[1] > 4, "board size should be at least 5*5"

        self.columns = board_size[1]
        self.rows = board_size[0]
        self.silent = silent
        self.board_size = self.rows * self.columns
        self.turnsPlayed=0
        self.depth=depth
        self.choice=-1
        self.turnsPlayed=0
        self.minimaxTempValue=float("-inf")
   
    def run(self, starter=None):
        if (not starter):
            starter = self.__get_random_starter()
        assert starter in [self.YOU, self.CPU], "starter value can only be 1,-1 or None"
        
        self.__init_board()
        turns_played = 0
        current_player = starter
        while(turns_played < self.board_size):
            
            if (current_player == self.YOU):
                self.__print_board()
                player_input = self.get_your_input()
            elif (current_player == self.CPU):
                player_input = self.__get_cpu_input()
            else:
                raise Exception("A problem has happend! contact no one, there is no fix!")
            if (not self.register_input(player_input, current_player)):
                self.__print("this move is invalid!")
                continue
            current_player = self.__change_turn(current_player)
            potential_winner = self.check_for_winners()
            turns_played += 1
            self.turnsPlayed+=1
            if (potential_winner != 0):
                self.__print_board()
                self.__print_winner_message(potential_winner)
                return potential_winner
        self.__print_board()
        self.__print("The game has ended in a draw!")
        return self.DRAW

    def get_your_input(self):
        # self.minimax(self.YOU,self.board,0)
        self.minimaxAlphaBeta(self.YOU,self.board,0)
        
        
        return self.choice

    def minimax(self,turn,tempTable,depth):
        self.turnsPlayed+=1
        if(depth<self.depth):
            if(turn==self.YOU):
                maxVal=float("-inf")
                for x in range(self.columns):
                    isPassed=False
                    for y in range(self.rows-1,-1,-1):
                        if tempTable[y][x]==self.EMPTY:
                            currTable=copy.deepcopy(tempTable)
                            currTable[y][x]=self.YOU
                            isPassed=True
                            break
                    if(isPassed):
                        eval=self.minimax(self.CPU,currTable,depth+1)
                        maxVal=max(maxVal,eval)
                        if((self.depth%2==0 or self.depth==1) and maxVal==eval):
                            self.choice=x+1
                
                return maxVal
            
            elif(turn==self.CPU):
                minVal=float("inf")
                for x in range(self.columns):
                    isPassed=False
                    for y in range(self.rows-1,-1,-1):
                        if tempTable[y][x]==self.EMPTY:
                            currTable=copy.deepcopy(tempTable)
                            currTable[y][x]=self.CPU
                            isPassed=True
                            break
                    if(isPassed):
                        eval=self.minimax(self.YOU,currTable,depth+1)
                        minVal=min(minVal,eval)
                        if(self.depth%2==1 and minVal==eval):
                            self.choice=x+1
                return minVal
        
        else:
            scores=list()
            scores.append(self.__countDiagonalDanger1(countinousCellsNum=2,table=tempTable))
            scores.append([4*x for x in self.__countDiagonalDanger1(countinousCellsNum=3,table=tempTable)])
            
            scores.append(self.__countHorizontalDanger(countinousCellsNum=2,table=tempTable))
            scores.append([4*x for x in self.__countHorizontalDanger(countinousCellsNum=3,table=tempTable)])
            
            scores.append(self.__countVerticalDanger(countinousCellsNum=2,table=tempTable))
            scores.append([4*x for x in self.__countVerticalDanger(countinousCellsNum=3,table=tempTable)])
            
            scores.append(self.__countDiagonalDanger2(countinousCellsNum=2,table=tempTable))
            scores.append([4*x for x in self.__countDiagonalDanger2(countinousCellsNum=3,table=tempTable)])
            
            boardCopy=copy.deepcopy(self.board)
            self.board=tempTable
            hasPlayerWon=self.check_if_player_has_won(turn)
            self.board=copy.deepcopy(boardCopy)
            
            score=0
            if(hasPlayerWon):
                if(turn==self.YOU):score= 1000
                if(turn==self.CPU):score= -1000

            for x in scores:score+= x[0]-x[1]

            return score

    def minimaxAlphaBeta(self,turn,tempTable,depth):
        if(depth<self.depth):
            if(turn==self.YOU):
                maxVal=float("-inf")
                for x in range(self.columns):
                    isPassed=False
                    for y in range(self.rows-1,-1,-1):
                        if tempTable[y][x]==self.EMPTY:
                            currTable=copy.deepcopy(tempTable)
                            currTable[y][x]=self.YOU
                            isPassed=True
                            break
                    if(isPassed):
                        eval=self.minimax(self.CPU,currTable,depth+1)
                        maxVal=max(maxVal,eval)
                        if((self.depth%2==0 or self.depth==1) and maxVal==eval):
                            self.choice=x+1
                            self.minimaxTempValue=maxVal
                        if(eval>self.minimaxTempValue):
                            break
                return maxVal
            
            elif(turn==self.CPU):
                minVal=float("inf")
                for x in range(self.columns):
                    isPassed=False
                    for y in range(self.rows-1,-1,-1):
                        if tempTable[y][x]==self.EMPTY:
                            currTable=copy.deepcopy(tempTable)
                            currTable[y][x]=self.CPU
                            isPassed=True
                            break
                    if(isPassed):
                        eval=self.minimax(self.YOU,currTable,depth+1)
                        minVal=min(minVal,eval)
                        if(self.depth%2==1 and minVal==eval):
                            self.choice=x+1
                        if(eval<self.minimaxTempValue):
                            break
                return minVal
        
        elif(depth==self.depth):
            scores=list()
            scores.append(self.__countDiagonalDanger1(countinousCellsNum=2,table=tempTable))
            scores.append([2*x for x in self.__countDiagonalDanger1(countinousCellsNum=3,table=tempTable)])
            
            scores.append(self.__countHorizontalDanger(countinousCellsNum=2,table=tempTable))
            scores.append([2*x for x in self.__countHorizontalDanger(countinousCellsNum=3,table=tempTable)])
            
            scores.append(self.__countVerticalDanger(countinousCellsNum=2,table=tempTable))
            scores.append([2*x for x in self.__countVerticalDanger(countinousCellsNum=3,table=tempTable)])
            
            scores.append(self.__countDiagonalDanger2(countinousCellsNum=2,table=tempTable))
            scores.append([2*x for x in self.__countDiagonalDanger2(countinousCellsNum=3,table=tempTable)])
            
            boardCopy=copy.deepcopy(self.board)
            self.board=tempTable
            hasPlayerWon=self.check_if_player_has_won(turn)
            self.board=copy.deepcopy(boardCopy)
            
            score=0
            if(hasPlayerWon):
                if(turn==self.YOU):score= 1000
                if(turn==self.CPU):score= -1000
            for x in scores:score+= x[0]-x[1]

            return score

        
    def __countHorizontalDanger(self,table,countinousCellsNum=3):
        numYouDangers=0
        numCPUDangers=0
        for i in range(self.rows-1,-1,-1):
            for j in range(0,self.columns-countinousCellsNum+1):
                currCells=table[i][j:j+countinousCellsNum]
                if (currCells==[self.YOU]*countinousCellsNum or 
                currCells==[self.CPU]*countinousCellsNum):
                    if(j==0):
                        if(table[i][countinousCellsNum] ==self.EMPTY):
                            if(table[i][j]==self.YOU):
                                numYouDangers+=1
                            else:
                                numCPUDangers+=1
                    elif(j==self.columns-countinousCellsNum):
                        if(table[i][j-1] ==self.EMPTY):
                            if(table[i][j]==self.YOU):
                                numYouDangers+=1
                            else:
                                numCPUDangers+=1
                    else:
                        if(table[i][j-1] ==self.EMPTY or table[i][j+countinousCellsNum]==self.EMPTY):
                            if(table[i][j]==self.YOU):
                                numYouDangers+=1
                            else:
                                numCPUDangers+=1
        return [numYouDangers,numCPUDangers]
    
    def __countVerticalDanger(self,table,countinousCellsNum=3):
        numYouDangers=0
        numCPUDangers=0
        for j in range(self.columns):
            for i in range(self.rows-1,countinousCellsNum,-1):
                if(countinousCellsNum==3):currCells=[table[i][j],table[i-1][j],table[i-2][j]]
                else:currCells=[table[i][j],table[i-1][j]]
                
                if (currCells==[self.YOU]*countinousCellsNum or 
                currCells==[self.CPU]*countinousCellsNum):
                    if(i==countinousCellsNum-1):
                        if(table[countinousCellsNum][j] ==self.EMPTY):
                            if(table[i][j]==self.YOU):numYouDangers+=1
                            else:numCPUDangers+=1
                    elif(i==self.rows-1):
                        if(table[i-countinousCellsNum][j] ==self.EMPTY):
                            if(table[i][j]==self.YOU):numYouDangers+=1
                            else:numCPUDangers+=1
                    else:
                        if(table[i+1][j] ==self.EMPTY or table[i-countinousCellsNum][j]==self.EMPTY):
                            if(table[i][j]==self.YOU):numYouDangers+=1
                            else:numCPUDangers+=1
        return [numYouDangers,numCPUDangers]
        
    def __countDiagonalDanger1(self,table,countinousCellsNum=3):
        numYouDangers=0
        numCPUDangers=0
        for i in range(self.rows-countinousCellsNum):
            for j in range(self.columns-countinousCellsNum):
                if(countinousCellsNum==2):currCells=[table[i][j],table[i+1][j+1]]
                else:currCells=[table[i][j],table[i+1][j+1],table[i+2][j+2]]
                if (currCells==[self.YOU]*countinousCellsNum or 
                currCells==[self.CPU]*countinousCellsNum):
                    if(i==0):
                        if(table[i+countinousCellsNum][j+countinousCellsNum] ==self.EMPTY):
                            if(table[i][j]==self.YOU):numYouDangers+=1
                            else:numCPUDangers+=1
                    elif(i+countinousCellsNum==self.rows):
                        if(table[i-1][j-1] ==self.EMPTY):
                            if(table[i][j]==self.YOU):numYouDangers+=1
                            else:numCPUDangers+=1
                    else:
                        if(table[i-1][j-1] ==self.EMPTY or table[i+countinousCellsNum][j+countinousCellsNum]==self.EMPTY):
                            if(table[i][j]==self.YOU):numYouDangers+=1
                            else:numCPUDangers+=1
        return [numYouDangers,numCPUDangers]
    
    def __countDiagonalDanger2(self,table,countinousCellsNum=3):
        numYouDangers=0
        numCPUDangers=0
        for i in range(self.rows-countinousCellsNum+1):
            for j in range(self.columns-1,countinousCellsNum-2,-1):
                if(countinousCellsNum==2):currCells=[table[i][j],table[i+1][j-1]]
                else:currCells=[table[i][j],table[i+1][j-1],table[i+2][j-2]]
                if (currCells==[self.YOU]*countinousCellsNum or 
                currCells==[self.CPU]*countinousCellsNum):
                    if((i==0 and j-countinousCellsNum<self.columns) or (j==self.columns-1 and i+countinousCellsNum<self.rows)):
                        if(table[i+countinousCellsNum][j-countinousCellsNum] ==self.EMPTY):
                            if(table[i][j]==self.YOU):
                                numYouDangers+=1
                            else:
                                numCPUDangers+=1
                    elif(i+countinousCellsNum==self.rows and j+1<self.columns):
                        if(table[i-1][j+1] ==self.EMPTY):
                            if(table[i][j]==self.YOU):
                                numYouDangers+=1
                            else:
                                numCPUDangers+=1
                    else:
                        if(j+1<self.columns and i+countinousCellsNum<self.rows and (table[i-1][j+1] ==self.EMPTY or table[i+countinousCellsNum][j-countinousCellsNum]==self.EMPTY)):
                            if(table[i][j]==self.YOU):
                                numYouDangers+=1
                            else:
                                numCPUDangers+=1
        return [numYouDangers,numCPUDangers]
    
    def check_for_winners(self):
        have_you_won = self.check_if_player_has_won(self.YOU)
        if have_you_won:
            return self.YOU
        has_cpu_won = self.check_if_player_has_won(self.CPU)
        if has_cpu_won:
            return self.CPU
        return self.EMPTY

    def check_if_player_has_won(self, player_id):
        return (
            self.__has_player_won_diagonally(player_id)
            or self.__has_player_won_horizentally(player_id)
            or self.__has_player_won_vertically(player_id)
        )
    
    def is_move_valid(self, move):
        if (move < 1 or move > self.columns):
            return False
        column_index = move - 1
        return self.board[0][column_index] == 0
    
    def get_possible_moves(self):
        possible_moves = []
        for i in range(self.columns):
            move = i + 1
            if (self.is_move_valid(move)):
                possible_moves.append(move)
        return possible_moves
    
    def register_input(self, player_input, current_player):
        if (not self.is_move_valid(player_input)):
            return False
        self.__drop_piece_in_column(player_input, current_player)
        return True

    def __init_board(self):
        self.board = []
        for i in range(self.rows):
            self.board.append([self.EMPTY] * self.columns)

    def __print(self, message: str):
        if not self.silent:
            print(message)

    def __has_player_won_horizentally(self, player_id):
        for i in range(self.rows):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_vertically(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_diagonally(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + self.__CONNECT_NUMBER - 1 - x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __get_random_starter(self):
        players = [self.YOU, self.CPU]
        return players[int(random() * len(players))]
    
    def __get_cpu_input(self):
        bb = copy.deepcopy(self.board)
        pm = self.get_possible_moves()
        for m in pm:
            self.register_input(m, self.CPU)
            if (self.check_if_player_has_won(self.CPU)):
                self.board = bb
                return m
            self.board = copy.deepcopy(bb)
        if (self.is_move_valid((self.columns // 2) + 1)):
            c = 0
            cl = (self.columns // 2) + 1
            for x in range(self.rows):
                if (self.board[x][cl] == self.CPU):
                    c += 1
            if (random() < 0.65):
                return cl
        return pm[int(random() * len(pm))]
    
    def __drop_piece_in_column(self, move, current_player):
        last_empty_space = 0
        column_index = move - 1
        for i in range(self.rows):
            if (self.board[i][column_index] == 0):
                last_empty_space = i
        self.board[last_empty_space][column_index] = current_player
        return True
        
    def __print_winner_message(self, winner):
        if (winner == self.YOU):
            self.__print("congrats! you have won!")
        else:
            self.__print("gg. CPU has won!")
    
    def __change_turn(self, turn):
        if (turn == self.YOU): 
            return self.CPU
        else:
            return self.YOU

    def __print_board(self):
        if (self.silent): return
        print("Y: you, C: CPU")
        for i in range(self.rows):
            for j in range(self.columns):
                house_char = "O"
                if (self.board[i][j] == self.YOU):
                    house_char = "Y"
                elif (self.board[i][j] == self.CPU):
                    house_char = "C"
                    
                print(f"{house_char}", end=" ")
            print()



visitedNodesNum=int()
winNum=0
losenum=0
def startGame(boardSize,depth_):
    global winNum,losenum,visitedNodesNum
    game = ConnectSin(board_size=boardSize,silent=True,depth=depth_)
    winner=game.run()
    if(winner==1):winNum+=1
    elif(winner==-1):losenum+=1
    visitedNodesNum=game.turnsPlayed
    del game
    
def runNtime(boardSize,depth):
    startTime=time.time()
    global winNum,losenum,visitedNodesNum
    for i in range(playCount):
        startGame(boardSize,depth)
    
    endTime=time.time()
    print("boardSize:",boardSize)
    print("depth:",depth)
    print("Number of wins:",winNum)
    print("Number of loses:",losenum)
    print("winRate:",100*winNum/playCount)
    print("EXE time for 20 times execution:",endTime-startTime)
    print("average EXE time:",(endTime-startTime)/playCount)
    
    
    visitedNodesNum=0
    winNum=0
    losenum=0
    
def runForAllBoards():
    for board in [(6,8),(7,8),(7,10)]:
        for depth in [1,3]:
            runNtime(board,depth)
    
runForAllBoards()