#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------
def scoring(seqs):
    #Scoring algorith which takes two sequences and returns the alignment score
    global best_score
    global best_alignment
    global num_alignments
    num_alignments += 1
    score = 0
    firstSeq = seqs[0]
    secondSeq = seqs[1]
    #For each item in the sequence
    for i in range(0,len(firstSeq)):
        if(firstSeq[i] == secondSeq[i]):
            #Score depending on alignment 
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
    if score > best_score:
        best_score = score
        best_alignment = [firstSeq,secondSeq]


def generateAlignments(seq1,seq2,cseq1, cseq2):
#If either of the sequences are blank
    if(seq1 != "" or seq2 != ""):
        if seq1 == "":
            seq1 = "-"
            scoring(sameLength(seq1+cseq1,seq2+cseq2))
        elif seq2 == "":
            seq2 = "-"
            scoring(sameLength(seq1+cseq1,seq2+cseq2))
        #Use both letters
        else:
            if(len(seq1)!= 1):
                generateAlignments(seq1[:-1],seq2[:-1],seq1[-1]+cseq1,seq2[-1]+cseq2)
            else:
                scoring(sameLength(seq1+cseq1,seq2+cseq2))
            #Seq1 letter, seq2 -
            generateAlignments(seq1[:-1],seq2,seq1[-1]+cseq1,"-"+cseq2)
            #Seq2 letter, seq1 "-"
            generateAlignments(seq1,seq2[:-1],"-"+cseq1,seq2[-1]+cseq2)
    else:
        scoring(sameLength(seq1+cseq1,seq2+cseq2))


def sameLength(seq1,seq2):
    #If one alignment is greater than the other, append a "-" where applicable 
    while(len(seq1)> len(seq2)):
        seq2 = "-" + seq2
    while(len(seq2)> len(seq1)):
        seq1 = "-" + seq1
    return [seq1,seq2]
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
best_aligment = ""
best_score = -99


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Call any functions you need here, you can define them above.
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score. 
# The number of alignments you have checked should be stored in a variable called num_alignments.
num_alignments = 0

generateAlignments(seq1,seq2,"","")

##for i in range(0,num_alignments):


    
#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Alignments generated: '+str(num_alignments))
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------
