#!/usr/bin/python
import time
import sys
import numpy as np

# YOUR FUNCTIONS GO HERE -------------------------------------
def scoring(seq1,seq2):
    score = 0
    firstSeq = seq1
    secondSeq = seq2
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
    highestScore = -99
    highestPos = []
    rows = len(seq1)
    cols = len(seq2)
    for i in range(1,rows+1):
        for j in range(1,cols+1):
            val1 = scoring(seq1[i-1],seq2[j-1])+matrix[i-1][j-1]
            val2 = matrix[i-1][j]-4
            val3 = matrix[i][j-1]-4
            matrix[i][j] = max(val1,val2,val3,0)
            btMatrix = btInsert(i,j,btMatrix,val1,val2,val3,matrix[i][j])
            if matrix[i][j] > highestScore:
                highestScore = matrix[i][j]
                highestPos = [i,j]
##    for m in range(1,rows+1):
##        val1 = scoring(seq1[m-1],seq2[cols-1])+matrix[m-1][cols-1]
##        val2 = matrix[m-1][cols]-4
##        val3 = matrix[m][cols-1]
##        matrix[m][cols] = max(val1,val2,val3,0)
##        btMatrix = btInsert(m,cols,btMatrix,val1,val2,val3,matrix[m][cols])
##        if matrix[m][cols] > highestScore:
##                highestScore = matrix[m][cols]
##                highestPos = [m,cols]
##                
##    for n in range(1,cols+1):
##        val1 = scoring(seq1[rows-1],seq2[n-1])+matrix[rows-1][n-1]
##        val2 = matrix[rows-1][n]
##        val3 = matrix[rows][n-1]-4
##        matrix[rows][n] = max(val1,val2,val3,0)
##        btMatrix = btInsert(rows,n,btMatrix,val1,val2,val3,matrix[rows][n])
##        if matrix[rows][n] > highestScore:
##                highestScore = matrix[rows][n]
##                highestPos = [rows,n]
    return highestScore,highestPos

def generateBTMatrix(seq1,seq2):
    rows = len(seq1)
    cols = len(seq2)
    btMatrix = [[0 for x in range(cols+1)] for y in range(rows+1)]
    btMatrix[0][0] = "E"
    for i in range(1,cols+1):
        btMatrix[0][i] = "E"
    for j in range(1,rows+1):
        btMatrix[j][0] = "E"
    return btMatrix

def btInsert(r,c,btMatrix,val1,val2,val3,maxi):
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
    cseq1 = seq1[:len(seq1)-(len(seq1)-bestPos[0])]
    cseq2 = seq2[:len(seq2)-(len(seq2)-bestPos[1])]
    alignedSeq1 = ""
    alignedSeq2 = ""
    currentPos = bestPos
    while(btMatrix[currentPos[0]][currentPos[1]] != "E"):
        if btMatrix[currentPos[0]][currentPos[1]] == "D":
            alignedSeq1 = cseq1[-1] + alignedSeq1
            alignedSeq2 = cseq2[-1] + alignedSeq2
            cseq1 = cseq1[:-1]
            cseq2 = cseq2[:-1]
            currentPos[0] -= 1
            currentPos[1] -= 1
        elif btMatrix[currentPos[0]][currentPos[1]] == "L":
            alignedSeq2 = cseq2[-1] + alignedSeq2
            alignedSeq1 = "-" + alignedSeq1
            cseq2 = cseq2[:-1]
            currentPos[1] -= 1
            
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
matrix = createMatrix(seq1,seq2)
btMatrix = generateBTMatrix(seq1,seq2)
best_score,highestPos = fillScores(matrix,seq1,seq2,btMatrix)
best_alignment = createAlignment(btMatrix, highestPos,seq1,seq2)
print(scoring(best_alignment[0],best_alignment[1]),"ALIGNMENT SCORE")
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

