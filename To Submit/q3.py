def NJ(fileName):
    #Open file, split the file into seperate lines
    file = open(fileName,'r')
    lines = file.read().splitlines()
    rows = []
    #For each of the lines, split the items by whitespace 
    for i in range(0,len(lines)):
        rows.append((lines[i].split(" ")))
    #Create the main matrix and row some array 
    matrix = [["-" for x in range(len(rows[i]))] for y in range(len(rows))]
    rowSums = [[0.0 for x in range(0)] for y in range(len(rows))]
    #Fill the matrix and calculate the row sums
    fillMatrix(matrix,rows)
    calculateRowSums(matrix,rowSums)
    printMatrix(matrix,rowSums)
    #Print the qMatrix after calculating it
    qMatrix = calculateQMatrix(matrix,rowSums)
    printQMatrix(qMatrix)
    
    while(len(matrix)-1 > 2):
        smallestQ,smallestPos = findSmallestQ(qMatrix)
        newVals = generateNewVals(matrix,smallestPos)
        matrix = shrinkMatrix(matrix,smallestPos[0],smallestPos[1],newVals)
        rowSums= calculateRowSums(matrix,rowSums)
        printMatrix(matrix,rowSums)
        qMatrix = calculateQMatrix(matrix,rowSums)
        printQMatrix(qMatrix)
        


def printMatrix(matrix,rowSums):
    print("Distance Matrix:")
    #For each row in the matrix
    for i in range(0,len(matrix[0])):
        toPrint = ""
        #For each item in the row
        for j in range(0,len(matrix)):
            #Convert it to string and a tab and concatenate it.
            toPrint += str(matrix[i][j]) + "\t"
        #Also print the row sums for that row
        toPrint += str(rowSums[i])
        print(toPrint)
    print("\n")

def printQMatrix(qMatrix):
    print("Q Matrix")
    #Same as function that print normal matrix except it doesn't print row sums
    for i in range(0,len(qMatrix[0])):
        toPrint = ""
        for j in range(0,len(qMatrix)):
            toPrint += str(qMatrix[i][j]) + "\t"
        print(toPrint)
    print("\n")
            
def fillMatrix(matrix,rows):
    #For each item in the matrix
    for i in range(0,len(rows)):
        for j in range(0,len(rows[i])):
            #Either add it as a float (if greater a number)
            if(j>0 and i>0):
                matrix[i][j] = float(rows[i][j])
            #Add as string if a letter
            else:
                matrix[i][j] = rows[i][j]
    return matrix

def calculateRowSums(matrix,rowSums):
    #Add row sum title
    rowSums[0]= "Row Sums"
    #For each row
    for i in range(1,len(matrix[0])):
        rSum = 0.0
        #For each column
        for j in range(1,len(matrix)):
            #Add that number to the total
            rSum += float(matrix[i][j])
        #Add that total to row sum
        rowSums[i] = rSum
    return rowSums

def shrinkMatrix(matrix,row,col,newVals):
    #Pick the row/column to be deleted out of the two
    toBeDeleted = max(row,col)
    saved = min(row,col)
    #Set value of new row/col
    newName = matrix[row][0] + matrix[col][0]
    matrix[saved][0] = newName
    matrix[0][saved] = newName

    lenOfRow = len(matrix[0])
    lenOfCol = len(matrix)
    #Generate the new smaller matrix
    newMatrix = [["-" for x in range(lenOfRow-1)] for y in range(lenOfCol-1)]
    rows = []

    #For each row 
    for i in range(0,lenOfRow):
            #If the row is not the one to be deleted
            if(i != toBeDeleted):
                rowContents = []
                #For each column
                for j in range(0,lenOfCol):
                    #If the col is not to be deleted
                    if j!= toBeDeleted:
                        #Add that item to the new rows contents 
                        rowContents.append(matrix[i][j])
                #Append the contents to rows
                rows.append(rowContents)

    #Add the rows to the new matrix
    for k in range(0,len(rows)):
        newMatrix[k] = rows[k]

    newRow = 0
    newCol = 0
    #Find new column by searching through columns and seeing where newName is
    for p in range(0, len(newMatrix)):
        if newMatrix[0][p] == newName:
            newCol = p
    #Find new row by seraching through the rows and seeing where newName is
    for o in range(0,len(newMatrix[0])):
        if newMatrix[o][0] == newName:
            newRow = o
    #Update the values on that row and col
    newMatrix = updateVals(newMatrix,newRow,newCol,newVals)
    return newMatrix

def calculateQMatrix(theMatrix,rowSums):
    #Create the new, smaller q matrix which is the same size of the matrix
    qMatrix = [["-" for x in range(len(theMatrix[0]))]
               for y in range(len(theMatrix))]

    #Update the letters on the side
    for j in range(0,len(theMatrix)):
        qMatrix[j][0] = theMatrix[j][0]
    for i in range(1,len(theMatrix[0])):
        qMatrix[0][i] = theMatrix[0][i]

    #Generate r - the amount of species in the matrix
    r = len(theMatrix[0])-1
    #FOr each item in the qMatrix
    for i in range(1,len(theMatrix[0])):
        for j in range(1,len(theMatrix)):
            #Generate the q value at this position
            qMatrix[i][j] = ( ((r-1)*(theMatrix[i][j]))
                             - (rowSums[i])
                                - (rowSums[j]) )
    #Remove the dups, setting the dups to 0.0
    qMatrix = removeDups(qMatrix)
    return qMatrix

def removeDups(matrix):
    #For each item in the matrix
    for i in range(1,len(matrix[0])):
        for j in range(1,len(matrix)):
            #If the species name is the same on row and col
            if matrix[i][0] == matrix[0][j]:
                #Set it to 0
                matrix[i][j] = 0.0
    return matrix

def findSmallestQ(qMatrix):
    smallestQ = 9999999
    smallestPos = []
    #For each item in the qMatrix
    for i in range(1,len(qMatrix[0])):
        for j in range(1,len(qMatrix)):
            #If the item is smaller than the current smaller
            if((qMatrix[i][j]) < smallestQ):
                #Set the smallest value and position 
                smallestQ = (qMatrix[i][j])
                smallestPos = [i,j]
    return smallestQ,smallestPos

def generateNewVals(matrix,smallestPos):
    row = smallestPos[0]
    col = smallestPos[1]
    newVals = []
    #For each of the cols 
    for i in range(1, len(matrix)):
        #If it isnt the col thats being deleted generate the new vals
        if(i != col):
            newVals.append(((matrix[row][i])
                           + (matrix[col][i])
                           - (matrix[row][col]))/2)
    return newVals

def updateVals(matrix,row,col,newVals):
    #Update the values in the new matrix and the set row and col
    for i in range(1,len(newVals)+1):
        if(matrix[row][0] != matrix[i][0]):
            matrix[row][i] = newVals[i-1]
    for j in range(1,len(newVals)+1):
        if(matrix[j][col] != matrix[0][j]):
            matrix[j][col] = newVals[j-1]
    matrix = removeDups(matrix)
    return matrix
