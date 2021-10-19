from Player import Player
import random

class ComputerPlayer(Player):

    def __init__(self):
        super().__init__()
        self.firstHit = False
    def findFirstX(self):
        while True and self.firstHit:
            col = random.randint(0, 9)
            row = random.randint(0, 9)
            if(self.gridShots.returnLocation(row, col) == "X"):
                return [row, col]
        return [-1, -1]

    def checkOverlapping(self, size, vOrH, rowStart, colStart):
        if vOrH == 0:
            for i in range(size):
                if not self.gridShips.isSpaceWater(i, colStart - 1):
                    return False
        elif vOrH == 1:
            for k in range(size):
                if not self.gridShips.isSpaceWater(rowStart-1, k):
                    return False
        return True

    def takeTurn(self, otherPlayer):
        direction = random.randint(1, 4)
        startx = -1
        starty = -1

        smartShotInvalid = False

        if not self.firstHit:
            startx = random.randrange(0, 10)
            starty = random.randrange(0, 10)
        else:
            target = self.findFirstX()

            try:
                self.gridShots.isSpaceWater(target[0], target[1] - 1)
                self.gridShots.isSpaceWater(target[0], target[1] + 1)
                self.gridShots.isSpaceWater(target[0] - 1, target[1])
                self.gridShots.isSpaceWater(target[0] + 1, target[1])
            except:
                smartShotInvalid = True

            if smartShotInvalid or (self.gridShots.isSpaceWater(target[0], target[1] - 1) == False) and (self.gridShots.isSpaceWater(target[0], target[1] + 1) == False) and (self.gridShots.isSpaceWater(target[0] - 1, target[1]) == False) and (self.gridShots.isSpaceWater(target[0] + 1, target[1])  == False):
                startx = random.randrange(0, 10)
                starty = random.randrange(0, 10)
            elif(direction == 1): #up
                startx = target[0]
                starty = target[1] - 1
            elif (direction == 2):  # down
                startx = target[0]
                starty = target[1] + 1
            elif (direction == 3):  # left
                startx = target[0] - 1
                starty = target[1]
            elif (direction == 4):  # right
                startx = target[0] + 1
                starty = target[1]

        if (not self.gridShots.isSpaceWater(startx, starty)) or (0 > startx > 9 or 0 > starty > 9):
            self.takeTurn(otherPlayer)
        if not otherPlayer.gridShips.isSpaceWater(startx, starty) and not otherPlayer.gridShips.returnLocation(startx, starty) == "O":
            self.gridShots.changeSingleSpace(startx, starty, "X")
            otherPlayer.gridShips.changeSingleSpace(startx, starty, "X")
            self.firstHit = True
        else:
            self.gridShots.changeSingleSpace(startx, starty, "O")
            otherPlayer.gridShips.changeSingleSpace(startx, starty, "O")

    def createShipGrid(self):
        self.placeShip("A", 5)
        self.placeShip("B", 4)
        self.placeShip("C", 3)
        self.placeShip("S", 3)
        self.placeShip("D", 2)

    def placeShip(self, ship, size):
        count = 1
        while count > 0:
            vOrH = random.randint(0, 1)
            colStart = random.randint(1, 10)
            rowStart = random.randint(1, 10)

            if 10 >= colStart >= 1 and 10 >= rowStart >= 1 and self.gridShips.isSpaceWater(rowStart - 1, colStart - 1):
                if vOrH == 0:
                    if rowStart - 1 + size <= 9 and self.checkOverlapping(size, vOrH, rowStart, colStart):
                        self.gridShips.changeCol(colStart - 1, ship, rowStart - 1, size)
                        self.printGrids()
                    else:
                        count += 1
                elif vOrH == 1:
                    if colStart - 1 + size <= 9 and self.checkOverlapping(size, vOrH, rowStart, colStart):
                        self.gridShips.changeRow(rowStart - 1, ship, colStart - 1, size)
                        self.printGrids()
                    else:
                        count += 1
                else:
                    count += 1
            else:
                count += 1
            count -= 1

        # this method will determine if the Player's ship grid still
        # has ships or not
        # If they have no ships left, the other player wins
        # This method returns true if they still have ships
        # This method returns false if they don't have ships

    def stillHasShips(self):
        for j in range(10):
            for k in range(10):
                if not self.gridShips.returnLocation(j, k) == "~" or not self.gridShips.returnLocation(j,k) == "X" or not self.gridShips.returnLocation(j, k) == "O":
                    return True
        return False


cpu = ComputerPlayer()
cpu.printGrids()
cpu.createShipGrid()
cpu.printGrids()

for i in range(100):
    cpu.takeTurn(cpu)
    cpu.printGrids()