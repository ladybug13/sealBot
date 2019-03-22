from random import randint as random

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __str__(self):
        return "Point(" + str(self.x) + "," + str(self.y) + ")"

    def compareTo(self, anotherPoint):
        if(anotherPoint.x == self.x and anotherPoint.y == self.y):
            return True
        else:
            return False

class Box():

    def __init__(self, column, row, id):
        #Points
        self.bL = Point(column-1, row-1)
        self.bR = Point(column, row-1)
        self.tL = Point(column-1, row)
        self.tR = Point(column, row)

        self.id = id
        #Lines
        self.b = Line(self.bL, self.bR)
        self.t = Line(self.tL, self.tR)
        self.l = Line(self.bL, self.tL)
        self.r = Line(self.bR, self.tR)

        self.col = column
        self.row = row

        self.fill = 0


    def compareTo(self, anotherBox):
        if(self.bL.compareTo(anotherBox.bL) and self.bR.compareTo(anotherBox.bR) and self.tL.compareTo(anotherBox.tL) and self.tR.compareTo(anotherBox.tR)):
            return True
        else:
            return False

    def toList(self):
        coordinates = {"column":self.col , "row":self.row , }
        return self.id
        #return {"Box": coordinates }

    def isBoxFilledByTwo(self):
        linesFilled =0
        returningLines = []

        if self.b.isFill():
            linesFilled = linesFilled+1
            returningLines.append(self.b)

        if self.t.isFill():
            linesFilled = linesFilled+1
            returningLines.append(self.t)

        if self.l.isFill():
            linesFilled = linesFilled+1
            returningLines.append(self.l)

        if self.r.isFill():
            linesFilled = linesFilled+1
            returningLines.append(self.r)

        if linesFilled == 2:
            return returningLines

        else:
            return None


    def isBoxFilledByThree(self):
        linesNotFilled =0
        returningLines = None

        if not self.b.isFill():
            linesNotFilled = linesNotFilled+1
            returningLines = self.b

        if not self.t.isFill():
            linesNotFilled = linesNotFilled+1
            returningLines = self.t

        if not self.l.isFill():
            linesNotFilled = linesNotFilled+1
            returningLines = self.l

        if not self.r.isFill():
            linesNotFilled = linesNotFilled+1
            returningLines = self.r

        if linesNotFilled == 1:
            return returningLines

        else:
            return None

    def updateBoxStatus(self, whoseMove):
        #print(str(self) + " trying to be updated...")
        if(self.fill == 0):

            if(self.b.isFill() and self.l.isFill() and self.r.isFill() and self.t.isFill()):
                # print(str(self.b))
                # print(str(self.l))
                # print(str(self.r))
                # print(str(self.t))
                self.fill = whoseMove

                # print(str(self) + " just got updated")


    def __str__(self):
        return "Box " + str(self.id) + ": (" + str(self.bL) + "," + str(self.bR) + "," +str(self.tL) + "," + str(self.tR) + ") is filled with " + str(self.fill)

class Line():
    def __init__(self, pFrom, pTo):
        self.pFrom = pFrom
        self.pTo = pTo
        self.fill = 0

    def compareTo(self, anotherLine):
        if( self.pFrom.compareTo(anotherLine.pFrom) and self.pTo.compareTo(anotherLine.pTo)):
            return True
        else:
            return False

    def paint(self):
        self.fill = 1

    def isFill(self):

        if self.fill == 1:
            return True


    def toList(self):
        coordinates = {"point_from_x":self.pFrom.x , "point_from_y":self.pFrom.y , "point_to_x":self.pTo.x , "point_to_y":self.pTo.y }
        return coordinates

    def __str__(self):
        return "Line from " + str(self.pFrom) + " to " + str(self.pTo) + " filled with " + str(self.fill)

#############################################################################
class bot(object):

    def __init__(self,in_dimensions=5):
        self.dimensions = in_dimensions

    def belongsTo(self,move, arrayOfMoves):
        for onemove in arrayOfMoves:
            if(onemove['point_from_x']==move['point_from_x'] and onemove['point_from_y']==move['point_from_y'] and onemove['point_to_x']==move['point_to_x'] and onemove['point_from_y']==move['point_from_y']):
                return True
        return False

    def makeTheMove(self,all_the_moves):
        mapBox = None
        movesIShouldntMake = []
        movesICantMake = []
        moveIwillMake = {}
        aRange = range(1, self.dimensions+1)
        dimensions = self.dimensions+1
        #Create the mapBox wgich will be a abstract representaion
        #of the boxes in the field and init each cell to 0
        #Its an array dimesnions by dimensions
        mapBox = [[0] * dimensions for i in range(dimensions)]
        noFilledBoxes = 0
        id = 0  #this will be the box feature that will be returned to front end
        for r in aRange:
            for c in aRange:
                mapBox[c][r] = Box(c, r, id)
                id = id + 1

        if(all_the_moves != []):
            for move in all_the_moves:
                p1 = Point(move['point_from_x'], move['point_from_y'])
                p2 = Point(move['point_to_x'], move['point_to_y'])
                line = Line(p1, p2)

                for j in aRange: #for all the rows
                        for i in aRange: #for all the columns

                            if(mapBox[i][j].b.compareTo(line)):
                                mapBox[i][j].b.paint()
                                movesICantMake.append(move)
                            elif(mapBox[i][j].t.compareTo(line)):
                                mapBox[i][j].t.paint()
                                movesICantMake.append(move)
                            elif(mapBox[i][j].l.compareTo(line)):
                                mapBox[i][j].l.paint()
                                movesICantMake.append(move)
                            elif(mapBox[i][j].r.compareTo(line)):
                                mapBox[i][j].r.paint()
                                movesICantMake.append(move)

            for r in aRange:
                for c in aRange:

                    if(mapBox[r][c].isBoxFilledByThree() != None):
                        line = mapBox[r][c].isBoxFilledByThree()
                        moveIwillMake={'point_from_x':line.pFrom.x, 'point_from_y':line.pFrom.y, 'point_to_x':line.pTo.x, 'point_to_y':line.pTo.y}
                        print("FILLED BY THREE")
                    elif(mapBox[r][c].isBoxFilledByTwo() != None):
                        print("FILLED BY Two")
                        lines = mapBox[r][c].isBoxFilledByTwo()
                        line1 = lines[0]
                        line2 = lines[1]
                        move1 = {'point_from_x':line1.pFrom.x, 'point_from_y':line1.pFrom.y, 'point_to_x':line1.pTo.x, 'point_to_y':line1.pTo.y}
                        move2 = {'point_from_x':line2.pFrom.x, 'point_from_y':line2.pFrom.y, 'point_to_x':line2.pTo.x, 'point_to_y':line2.pTo.y}
                        movesIShouldntMake.append(move1)
                        movesIShouldntMake.append(move2)


        print(movesIShouldntMake)
        print(movesICantMake)
        if(moveIwillMake == {}):
            print("move is {}")
            isValid = False
            noOfIterations = 0
            while(not isValid):
                #1 corresponds to vertical, 2 to horizontal direction
                direction =0
                point_from_x=5
                point_from_y=5

                while(point_from_x==5 and point_from_y==5):
                    point_from_x = random(0, self.dimensions )
                    point_from_y = random(0, self.dimensions )

                if(point_from_x == 5):
                    direction = 1
                elif(point_from_y == 5):
                    direction = 2
                else:
                    direction = random(1, 2)

                if(direction == 1):
                    point_to_x = point_from_x
                    point_to_y = point_from_y + 1
                else:
                    point_to_x = point_from_x + 1
                    point_to_y = point_from_y

                    print("no Of iterations is less than 100")

                if (movesICantMake != []):
                    print("Check if what we calculated is a move we cant make")
                    moveValidSoFar = True
                    for move in movesICantMake:
                        if(moveValidSoFar):
                            if (move['point_from_x']==point_from_x) and (move['point_from_y']==point_from_y) and (move['point_to_x']==point_to_x) and (move['point_to_y']==point_to_y):
                                moveValidSoFar = False

                    if(moveValidSoFar and noOfIterations<=100):
                        for move in movesIShouldntMake:
                            if(moveValidSoFar):
                                if (move['point_from_x']==point_from_x) and (move['point_from_y']==point_from_y) and (move['point_to_x']==point_to_x) and (move['point_to_y']==point_to_y):
                                    moveValidSoFar = False

                    if(moveValidSoFar): isValid = True

                else:
                    isValid=True


                noOfIterations=noOfIterations+1
                print(noOfIterations)
                moveIwillMake={'point_from_x':point_from_x, 'point_from_y':point_from_y, 'point_to_x':point_to_x, 'point_to_y':point_to_y}
                print(moveIwillMake)

        return moveIwillMake
