def NJ(fileName):
    file = open(fileName,'r')
    lines = file.read().splitlines()
    rows = []
    for i in range(0,len(lines)):
        rows.append((lines[i].split(" ")))
    matrix = [[0 for x in range(len(rows[i])+1)] for y in range(len(rows))]
    qMatrix = [[0 for x in range(len(rows[i]))] for y in range(len(rows))]
    matrix = fillMatrix(matrix,rows)
    matrix = calculateRowSums(matrix)
    qMatrix = fillQMatrix(qMatrix,matrix)
    printMatrices(matrix,qMatrix)

    while(len(matrix)-1 > 2):
        smallestQ,smallestPos = findSmallestQ(qMatrix)
        print(smallestQ, smallestPos)
        newVals = generateNumVals(matrix,smallestPos)
        matrix = updateMatrix(matrix,newVals,smallestPos[0],smallestPos[1])
        qMatrix = shrinkMatrix(qMatrix,smallestPos[0],smallestPos[1],False)
        qMatrix = fillQMatrix(qMatrix,matrix)
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

def fillQMatrix(qMatrix,matrix):
    for j in range(0,len(matrix)):
        qMatrix[j][0] = matrix[j][0]
    for i in range(1,len(matrix[0])-1):
        qMatrix[0][i] = matrix[0][i]
    qMatrix = calculateQMatrix(qMatrix,matrix)
    return qMatrix


    
def calculateQMatrix(qMatrix,matrix):
    r = len(matrix[0])-2
    for i in range(1,len(matrix[0])-1):
        for j in range(1,len(matrix)):
            qMatrix[i][j] = ( ((r-1)*(matrix[i][j]))
                             - (matrix[i][len(matrix)])
                                - (matrix[j][len(matrix)]) )
    qMatrix = removeDups(qMatrix,True)
    return qMatrix

def findSmallestQ(qMatrix):
    smallestQ = 9999999
    smallestPos = []
    for i in range(1,len(qMatrix[0])):
        for j in range(1,len(qMatrix)):
            if((qMatrix[i][j]) < smallestQ):               
                smallestQ = (qMatrix[i][j])
                smallestPos = [i,j]
    return smallestQ,smallestPos

def generateNumVals(matrix,smallestPos):
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
    matrix = shrinkMatrix(matrix,row,col,True)
    for i in range(1,len(newVals)+1):
        matrix[row][i] = newVals[i-1]
        matrix[i][col-1] = newVals[i-1]
    matrix = removeDups(matrix,False)
    matrix = calculateRowSums(matrix)
    return matrix

def shrinkMatrix(matrix,row,col,q):
    newName = matrix[row][0] + matrix[col][0]
    matrix[0][row] = newName
    matrix[col][0] = newName
    lenOfRow = len(matrix[0])
    lenOfCol = len(matrix)
    if q == True:
        newMatrix = [[0 for x in range(lenOfRow)] for y in range(lenOfCol-1)]
    else:
        newMatrix = [[0 for x in range(lenOfRow-1)] for y in range(lenOfCol-1)]
    rows = []
    for i in range(0,lenOfRow-1):
        if(i != row):
            rowContents = []
            for j in range(0,lenOfCol):
                if j!= col:
                    rowContents.append(matrix[i][j])
            if(q == True):
                rowContents.append("-")
            rows.append(rowContents)
    for k in range(0,len(rows)):
        newMatrix[k] = rows[k] 

    if(q == True):
        newMatrix[0][len(newMatrix[0])-1] = "Row Sums"

    return newMatrix

def removeDups(matrix,q):
    if(q):
        for i in range(1,len(matrix[0])):
            for j in range(1,len(matrix)):
                if matrix[i][0] == matrix[0][j]:
                    matrix[i][j] = 0.0
    else:
        for i in range(1,len(matrix[0])-1):
            for j in range(1,len(matrix)):
                if matrix[i][0] == matrix[0][j]:
                    matrix[i][j] = 0.0
    return matrix
    
NJ("matrix2.txt")
