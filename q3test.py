def splitTest(fileName):
    file = open(fileName,'r')
    rows = file.read().splitlines()
    for i in range(0,len(rows)):
        rows[i]= rows[i].replace(" ","")
    matrix = [[0 for x in range(len(rows[i])+1)] for y in range(len(rows))]
    matrix = fillMatrix(matrix,rows)
    printMatrices(matrix)
    matrix = shrinkMatrix(matrix,2,5)
    printMatrices(matrix)

def fillMatrix(matrix,rows):
    matrix[0][len(rows[0])] = "Row Sums"
    for i in range(0,len(rows)):
        for j in range(0,len(rows[i])):
            if(j>0 and i>0):
                matrix[i][j] = float(rows[i][j])
            else:
                matrix[i][j] = rows[i][j]
    return matrix


def printMatrices(matrix):
    print("Distance Matrix:")
    print('\n'.join(['\t'.join([str(num) for num in row]) for row in matrix]))


def shrinkMatrix(matrix,row,col):
    newName = matrix[row][0] + matrix[col][0]
    matrix[0][row] = newName
    matrix[col][0] = newName
    lenOfRow = len(matrix[0])
    lenOfCol = len(matrix)
    newMatrix = [[0 for x in range(lenOfRow-1)] for y in range(lenOfCol-1)]
    rows = []
    for i in range(0,lenOfRow-1):
        if(i != row):
            rowContents = []
            for j in range(0,lenOfCol):
                if j!= col:
                    rowContents.append(matrix[i][j])

            rows.append(rowContents)
    for k in range(0,len(rows)):
        newMatrix[k] = rows[k]

    return newMatrix
splitTest("matrix2.txt")
