def NJ(fileName):
    file = open(fileName,'r')
    lines = file.read().splitlines()
    rows = []
    for i in range(0,len(lines)):
        rows.append((lines[i].split(" ")))
    matrix = [["-" for x in range(len(rows[i])+1)] for y in range(len(rows))]
    fillMatrix(matrix,rows)
    calculateRowSums(matrix)
    qMatrix = calculateQMatrix(matrix)
    printMatrices(matrix,qMatrix)

    while(len(matrix)-1 > 2):
        smallestQ,smallestPos = findSmallestQ(qMatrix)
        print(smallestQ,smallestPos)
        newVals = generateNewVals(matrix,smallestPos)
        print(newVals)
        matrix = shrinkMatrix(matrix,smallestPos[0],smallestPos[1],False)
        printMatrices(matrix,qMatrix)
        qMatrix = shrinkMatrix(qMatrix,smallestPos[0],smallestPos[1],True)
        calculateQMatrix(matrix)
        printMatrices(matrix,qMatrix)



def printMatrices(matrix,qMatrix):
    print("Distance Matrix:")
    print('\n'.join(['\t'.join([str(num) for num in row]) for row in matrix]))
    print("\n")
    print("Q Matrix:")
    print('\n'.join(['\t'.join([str(num) for num in row]) for row in qMatrix]))

def fillMatrix(matrix,rows):
    matrix[0][len(rows[0])] = "Row Sums"
    for i in range(0,len(rows)):
        for j in range(0,len(rows[i])):
            if(j>0 and i>0):
                matrix[i][j] = float(rows[i][j])
            else:
                matrix[i][j] = rows[i][j]
    return matrix

def calculateRowSums(matrix):
    for i in range(1,len(matrix[0])-1):
        rSum = 0.0
        for j in range(1,len(matrix)):
            rSum += float(matrix[i][j])
        matrix[i][len(matrix)] = rSum
    return matrix

def calculateQMatrix(theMatrix):
    qMatrix = [["-" for x in range(len(theMatrix[0])-1)] for y in range(len(theMatrix))]
    for j in range(0,len(theMatrix)):
        qMatrix[j][0] = theMatrix[j][0]
    for i in range(1,len(theMatrix[0])-1):
        qMatrix[0][i] = theMatrix[0][i]
        
    r = len(theMatrix[0])-2
    for i in range(1,len(theMatrix[0])-1):
        for j in range(1,len(theMatrix)):
            qMatrix[i][j] = ( ((r-1)*(theMatrix[i][j]))
                             - (theMatrix[i][len(theMatrix)-1])
                                - (theMatrix[j][len(theMatrix)]) )
    qMatrix = removeDups(qMatrix)
    return qMatrix

def removeDups(matrix,q):
    for i in range(1,len(matrix[0])):
        for j in range(1,len(matrix)):
            if matrix[i][0] == matrix[0][j]:
                matrix[i][j] = 0.0
    return matrix

def findSmallestQ(qMatrix):
    smallestQ = 9999999
    smallestPos = []
    for i in range(1,len(qMatrix[0])):
        for j in range(1,len(qMatrix)):
            if((qMatrix[i][j]) < smallestQ):               
                smallestQ = (qMatrix[i][j])
                smallestPos = [i,j]
    return smallestQ,smallestPos

def shrinkMatrix(matrix,row,col,q):
    newName = matrix[row][0] + matrix[col][0]
    matrix[0][row] = newName
    matrix[col][0] = newName
    lenOfRow = len(matrix[0])
    lenOfCol = len(matrix)
    newMatrix = [["-" for x in range(lenOfRow-1)] for y in range(lenOfCol-1)]
    rows = []
    if q == False:
        for i in range(0,lenOfRow-1):
            if(i != row):
                rowContents = []
                for j in range(0,lenOfCol):
                    if j!= col:
                        rowContents.append(matrix[i][j])
                if(q == False):
                    rowContents.append("-")
                rows.append(rowContents)
    else:
        for i in range(0,lenOfRow):
            if(i != row):
                rowContents = []
                for j in range(0,lenOfCol):
                    if j!= col:
                        rowContents.append(matrix[i][j])
                if(q == False):
                    rowContents.append("-")
                rows.append(rowContents)
    for k in range(0,len(rows)):
        newMatrix[k] = rows[k]
    if(q == False):
        newVals = generateNewVals(newMatrix,[row,col])
        for m in range(1,len(newVals)+1):
            newMatrix[col-1][m] = newVals[m-1]
            newMatrix[m][row] = newVals[m-1]
        newMatrix = calculateRowSums(newMatrix)
    if(q == False):
        newMatrix[0][len(newMatrix[0])-1] = "Row Sums"
        newMatrix = removeDups(newMatrix,False)
    else:
        newMatrix = removeDups(newMatrix,True)
    
    return newMatrix

def generateNewVals(matrix,smallestPos):
    row = smallestPos[0]
    col = smallestPos[1]
    newVals = []
    for i in range(1, len(matrix[0])-1):
        if(i != row):
            newVals.append(((matrix[row][i])
                           + (matrix[col][i])
                           - (matrix[row][col]))/2)
    return newVals

def updateMatrix(matrix,newVals,row,col):
    
    matrix = shrinkMatrix(matrix,row,col,False)

    return matrix

NJ("matrix2.txt")
