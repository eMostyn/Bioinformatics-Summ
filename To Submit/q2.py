#!/usr/bin/python
import time
import sys

# YOUR FUNCTIONS GO HERE -------------------------------------
def scoring(seq1,seq2):
    #Scoring algorith, takes 2 sequences and returns their alignment score 
    score = 0
    firstSeq = seq1
    secondSeq = seq2
    #For each item in the alignment, add to the score
    for i in range(0,len(firstSeq)):
        if(firstSeq[i] == secondSeq[i]):
            if firstSeq[i] == "A":
                score += 3
            elif firstSeq[i] == "C":
                score += 2
            elif firstSeq[i] == "G":
                score += 1
            else:
                score += 2
        elif(firstSeq[i] == "-" or secondSeq[i] == "-"):
            score -= 4
        else:
            score -= 3
    return score

def createMatrix(seq1,seq2):
    #Generate the matrix, setting the upper row and left column to 0
    rows = len(seq1)
    cols = len(seq2)
    matrix = [[0 for x in range(cols+1)] for y in range(rows+1)]
    matrix[0][0] = 0
    for i in range(0,cols+1):
        matrix[0][i] = 0
    for j in range(0,rows+1):
        matrix[j][0] = 0
    return matrix

def fillScores(matrix,seq1,seq2,btMatrix):
    #Fill the scores into the matrix
    highestScore = -99
    highestPos = []
    rows = len(seq1)
    cols = len(seq2)
    for i in range(1,rows+1):
        for j in range(1,cols+1):
            #Generate the vals 
            val1 = scoring(seq1[i-1],seq2[j-1])+matrix[i-1][j-1]
            val2 = matrix[i-1][j]-4
            val3 = matrix[i][j-1]-4
            #Insert the maximum into the array
            matrix[i][j] = max(val1,val2,val3,0)
            #Update the backtrack matrix 
            btMatrix = btInsert(i,j,btMatrix,val1,val2,val3,matrix[i][j])
            #Update highest score and position if applicable
            if matrix[i][j] > highestScore:
                highestScore = matrix[i][j]
                highestPos = [i,j]

    return highestScore,highestPos

def generateBTMatrix(seq1,seq2):
    rows = len(seq1)
    cols = len(seq2)
    #Create the backtrack matrix
    btMatrix = [[0 for x in range(cols+1)] for y in range(rows+1)]
    #Set the top row and left column to E 
    btMatrix[0][0] = "E"
    for i in range(1,cols+1):
        btMatrix[0][i] = "E"
    for j in range(1,rows+1):
        btMatrix[j][0] = "E"
    return btMatrix

def btInsert(r,c,btMatrix,val1,val2,val3,maxi):
    #Insert the correct letter depending on which score is maximum 
    if maxi == 0:
        btMatrix[r][c] = "E"
    elif maxi == val1:
        btMatrix[r][c] = "D"
    elif maxi == val2:
        btMatrix[r][c] = "U"
    elif maxi == val3:
        btMatrix[r][c] = "L"
    return btMatrix

def createAlignment(btMatrix,bestPos,seq1,seq2):
    #Create the sequences to be used, depending on where the bestPos is
    cseq1 = seq1[:len(seq1)-(len(seq1)-bestPos[0])]
    cseq2 = seq2[:len(seq2)-(len(seq2)-bestPos[1])]
    alignedSeq1 = ""
    alignedSeq2 = ""
    currentPos = bestPos
    #While the currentPos isnt E
    while(btMatrix[currentPos[0]][currentPos[1]] != "E"):
        #If D then use both letters and move to the diagonal spot
        if btMatrix[currentPos[0]][currentPos[1]] == "D":
            alignedSeq1 = cseq1[-1] + alignedSeq1
            alignedSeq2 = cseq2[-1] + alignedSeq2
            cseq1 = cseq1[:-1]
            cseq2 = cseq2[:-1]
            currentPos[0] -= 1
            currentPos[1] -= 1
        #If l use 1 letter 1 - 
        elif btMatrix[currentPos[0]][currentPos[1]] == "L":
            alignedSeq2 = cseq2[-1] + alignedSeq2
            alignedSeq1 = "-" + alignedSeq1
            cseq2 = cseq2[:-1]
            currentPos[1] -= 1
        #Else use other letter and "-"
        else:
            alignedSeq1 = cseq1[-1] + alignedSeq1
            alignedSeq2 = "-" + alignedSeq2
            cseq1 = cseq1[:-1]
            currentPos[0] -= 1
    return [alignedSeq1,alignedSeq2]

# ------------------------------------------------------------



# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# To work with the printing functions below the best local alignment should be called best_alignment and its score should be called best_score. 
#Create the matrixes
matrix = createMatrix(seq1,seq2)
btMatrix = generateBTMatrix(seq1,seq2)
best_score,highestPos = fillScores(matrix,seq1,seq2,btMatrix)
best_alignment = createAlignment(btMatrix, highestPos,seq1,seq2)
#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------

