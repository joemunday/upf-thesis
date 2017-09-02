"""
Joe Munday
Master Thesis: Interfaces for Improvising with a Jazz Melody Generation System
Melody Generation Module

Master in Sound and Music Computing
Universitat Pompeu Fabra 2016-2017
"""

import csv
import os
import random
import random
import numpy as np
from scipy import stats
import copy


def chordSimplify(complexChord):
    """
    Takes strings represnting chords, and returns a major or minor version of that chord

    """
    if complexChord == 'silence':
        return 'silence'
    if complexChord[1] == 'b' or complexChord[1] == '#':
        noteName = complexChord[:2]
    else:
        noteName = complexChord[0]
    
    if 'min' in complexChord:
        return noteName+'min'
    else:
        return noteName+'maj'

rootdir = '' #path to source csv files

majorFiles = {}
minorFiles = {}

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if "csv" in os.path.join(subdir, file):
            newFile = csv.DictReader(open(os.path.join(subdir, file)))
            newNotes = []
            longDuration = 0
            shortDuration = 100000
            major = False
            totalDuration = 0.0
            counter = 0
            for row in newFile:
                if float(row['duration']) > longDuration:
                    longDuration = float(row['duration'])
                if float(row['duration']) < shortDuration:
                    shortDuration = float(row['duration'])
                totalDuration += float(row['duration'])
                counter +=1
                
            averageDuration = totalDuration/counter
            newFile = csv.DictReader(open(os.path.join(subdir, file)))
            for row in newFile:
                note = {}
                note['midiValue'] = row['pitch']

                note['chord'] = row['chord']
                note['simpleChord'] = chordSimplify(row['chord']) #run definition below before this line
                note['duration'] = row['duration']
                note['durationWeight'] = float(row['duration'])/averageDuration
                note['shortDuration'] = shortDuration
                note['longDuration'] = longDuration

                newNotes.append(note)
                if row['newKey'] == 'C':
                    major=True

            if major:
                majorFiles[file] = newNotes
            else:
                minorFiles[file] = newNotes

rawPairs = []
noteChordPairs = []
noteChordPairsSimple = []
for key in majorFiles.keys():
    for index in range (1, len(majorFiles[key])):
        noteChordPairs.append([[int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['chord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['chord']]])
        noteChordPairsSimple.append([[int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['simpleChord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['simpleChord']]])
        rawPairs.append([majorFiles[key][index-1],majorFiles[key][index]])

firstOrderComplexDict = {}
firstOrderChordDict = {}
firstOrderNoteDict = {}
currentChords= []

for pair in noteChordPairs:
    if pair[1][1] not in currentChords:
        currentChords.append(pair[1][1])
        firstOrderComplexDict[pair[1][1]] = {}
        firstOrderChordDict[pair[1][1]] = {}
    if str(pair[0]) not in firstOrderComplexDict[pair[1][1]].keys():
        firstOrderComplexDict[pair[1][1]][str(pair[0])] = []
    if str(pair[0][0]) not in firstOrderChordDict[pair[1][1]].keys():
        firstOrderChordDict[pair[1][1]][str(pair[0][0])] = []
    if str(pair[0][0]) not in firstOrderNoteDict.keys():
        firstOrderNoteDict[str(pair[0][0])] = []
    firstOrderComplexDict[pair[1][1]][str(pair[0])].append(pair[1][0])
    firstOrderChordDict[pair[1][1]][str(pair[0][0])].append(pair[1][0])
    firstOrderNoteDict[str(pair[0][0])].append(pair[1][0])

firstOrderSimpleDict = {}
firstOrderSimpleChordDict = {}
currentChords = []
for pair in noteChordPairsSimple:
    if pair[1][1] not in currentChords:
        currentChords.append(pair[1][1])
        firstOrderSimpleDict[pair[1][1]] = {}
        firstOrderSimpleChordDict[pair[1][1]] = {}
    if str(pair[0]) not in firstOrderSimpleDict[pair[1][1]].keys():
        firstOrderSimpleDict[pair[1][1]][str(pair[0])] = []
    if str(pair[0][0]) not in firstOrderSimpleChordDict[pair[1][1]].keys():
        firstOrderSimpleChordDict[pair[1][1]][str(pair[0][0])] = []
    firstOrderSimpleDict[pair[1][1]][str(pair[0])].append(pair[1][0])
    firstOrderSimpleChordDict[pair[1][1]][str(pair[0][0])].append(pair[1][0])
    
print 'firstOrderDict Complete'


rawTriples = [] #all information for three consecutive notes
noteChordTriples = [] #two chroma and an interval with relevant chord information
noteChordTriplesSimple = [] #two chroma and an interval with relevant simplified chord information
for key in majorFiles.keys():
    for index in range (2, len(majorFiles[key])):
        noteChordTriples.append([[int(majorFiles[key][index-2]['midiValue'])%12,majorFiles[key][index-2]['chord']],
                                 [int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['chord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['chord']]])
        noteChordTriplesSimple.append([[int(majorFiles[key][index-2]['midiValue'])%12,majorFiles[key][index-2]['simpleChord']],
                                 [int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['simpleChord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['simpleChord']]])


        rawTriples.append([majorFiles[key][index-2],majorFiles[key][index-1],majorFiles[key][index]])


secondOrderComplexDict = {}
secondOrderChordDict = {}
secondOrderNoteDict = {}
currentChords= []

for triple in noteChordTriples:
    if triple[2][1] not in currentChords:
        currentChords.append(triple[2][1])
        secondOrderComplexDict[triple[2][1]] = {}
        secondOrderChordDict[triple[2][1]] = {}
    if str(triple[:2]) not in secondOrderComplexDict[triple[2][1]].keys():
        secondOrderComplexDict[triple[2][1]][str(triple[:2])] = []
    if str([triple[0][0],triple[1][0]]) not in secondOrderChordDict[triple[2][1]].keys():
        secondOrderChordDict[triple[2][1]][str([triple[0][0],triple[1][0]])] = []
    if str([triple[0][0],triple[1][0]]) not in secondOrderNoteDict.keys():
        secondOrderNoteDict[str([triple[0][0],triple[1][0]])] = []
    secondOrderComplexDict[triple[2][1]][str(triple[:2])].append(triple[2][0])
    secondOrderChordDict[triple[2][1]][str([triple[0][0],triple[1][0]])].append(triple[2][0])
    secondOrderNoteDict[str([triple[0][0],triple[1][0]])].append(triple[2][0])
    
    
secondOrderSimpleDict = {}
secondOrderSimpleChordDict = {}
currentChords= []

for triple in noteChordTriplesSimple:
    if triple[2][1] not in currentChords:
        currentChords.append(triple[2][1])
        secondOrderSimpleDict[triple[2][1]] = {}
        secondOrderSimpleChordDict[triple[2][1]] = {}
    if str(triple[:2]) not in secondOrderSimpleDict[triple[2][1]].keys():
        secondOrderSimpleDict[triple[2][1]][str(triple[:2])] = []
    if str([triple[0][0],triple[1][0]]) not in secondOrderSimpleChordDict[triple[2][1]].keys():
        secondOrderSimpleChordDict[triple[2][1]][str([triple[0][0],triple[1][0]])] = []
    secondOrderSimpleDict[triple[2][1]][str(triple[:2])].append(triple[2][0])
    secondOrderSimpleChordDict[triple[2][1]][str([triple[0][0],triple[1][0]])].append(triple[2][0])

print 'secondOrderDict Complete'


rawQuads = []
noteChordQuads = []
noteChordQuadsSimple = []
for key in majorFiles.keys():
    for index in range (3, len(majorFiles[key])):
        noteChordQuads.append([[int(majorFiles[key][index-3]['midiValue'])%12,majorFiles[key][index-3]['chord']],
                               [int(majorFiles[key][index-2]['midiValue'])%12,majorFiles[key][index-2]['chord']],
                               [int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['chord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['chord']]])
        noteChordQuadsSimple.append([[int(majorFiles[key][index-3]['midiValue'])%12,majorFiles[key][index-3]['simpleChord']],
                               [int(majorFiles[key][index-2]['midiValue'])%12,majorFiles[key][index-2]['simpleChord']],
                               [int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['simpleChord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['simpleChord']]])
        rawQuads.append([majorFiles[key][index-3],majorFiles[key][index-2],majorFiles[key][index-1],majorFiles[key][index]])


thirdOrderComplexDict = {}
thirdOrderChordDict = {}
thirdOrderNoteDict = {}
currentChords= []

for quad in noteChordQuads:
    if quad[3][1] not in currentChords:
        currentChords.append(quad[3][1])
        thirdOrderComplexDict[quad[3][1]] = {}
        thirdOrderChordDict[quad[3][1]] = {}
    if str(quad[:3]) not in thirdOrderComplexDict[quad[3][1]].keys():
        thirdOrderComplexDict[quad[3][1]][str(quad[:3])] = []
    if str([quad[0][0],quad[1][0],quad[2][0]]) not in thirdOrderChordDict[quad[3][1]].keys():
        thirdOrderChordDict[quad[3][1]][str([quad[0][0],quad[1][0],quad[2][0]])] = []
    if str([quad[0][0],quad[1][0],quad[2][0]]) not in thirdOrderNoteDict.keys():
        thirdOrderNoteDict[str([quad[0][0],quad[1][0],quad[2][0]])] = []
    thirdOrderComplexDict[quad[3][1]][str(quad[:3])].append(quad[3][0])
    thirdOrderChordDict[quad[3][1]][str([quad[0][0],quad[1][0],quad[2][0]])].append(quad[3][0])
    thirdOrderNoteDict[str([quad[0][0],quad[1][0],quad[2][0]])].append(quad[3][0])

thirdOrderSimpleDict = {}
thirdOrderSimpleChordDict = {}
currentChords= []

for quad in noteChordQuadsSimple:
    if quad[3][1] not in currentChords:
        currentChords.append(quad[3][1])
        thirdOrderSimpleDict[quad[3][1]] = {}
        thirdOrderSimpleChordDict[quad[3][1]] = {}
    if str(quad[:3]) not in thirdOrderSimpleDict[quad[3][1]].keys():
        thirdOrderSimpleDict[quad[3][1]][str(quad[:3])] = []
    if str([quad[0][0],quad[1][0],quad[2][0]]) not in thirdOrderSimpleChordDict[quad[3][1]].keys():
        thirdOrderSimpleChordDict[quad[3][1]][str([quad[0][0],quad[1][0],quad[2][0]])] = []
    thirdOrderSimpleDict[quad[3][1]][str(quad[:3])].append(quad[3][0])
    thirdOrderSimpleChordDict[quad[3][1]][str([quad[0][0],quad[1][0],quad[2][0]])].append(quad[3][0])
    
print 'thirdOrderDict Complete'


rawFives = []
noteChordFives = []
noteChordFivesSimple = []
for key in majorFiles.keys():
    for index in range (4, len(majorFiles[key])):
        noteChordFives.append([[int(majorFiles[key][index-4]['midiValue'])%12,majorFiles[key][index-4]['chord']],
                               [int(majorFiles[key][index-3]['midiValue'])%12,majorFiles[key][index-3]['chord']],
                               [int(majorFiles[key][index-2]['midiValue'])%12,majorFiles[key][index-2]['chord']],
                               [int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['chord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['chord']]])
        noteChordFivesSimple.append([[int(majorFiles[key][index-3]['midiValue'])%12,majorFiles[key][index-4]['simpleChord']],
                                     [int(majorFiles[key][index-3]['midiValue'])%12,majorFiles[key][index-3]['simpleChord']],
                               [int(majorFiles[key][index-2]['midiValue'])%12,majorFiles[key][index-2]['simpleChord']],
                               [int(majorFiles[key][index-1]['midiValue'])%12,majorFiles[key][index-1]['simpleChord']],
                               [int(majorFiles[key][index]['midiValue'])-int(majorFiles[key][index-1]['midiValue']),majorFiles[key][index]['simpleChord']]])
        rawFives.append([majorFiles[key][index-4],majorFiles[key][index-3],majorFiles[key][index-2],majorFiles[key][index-1],majorFiles[key][index]])


fourthOrderComplexDict = {}
fourthOrderChordDict = {}
fourthOrderNoteDict = {}
currentChords= []

for five in noteChordFives:
    if five[4][1] not in currentChords:
        currentChords.append(five[4][1])
        fourthOrderComplexDict[five[4][1]] = {}
        fourthOrderChordDict[five[4][1]] = {}
    if str(five[:4]) not in fourthOrderComplexDict[five[4][1]].keys():
        fourthOrderComplexDict[five[4][1]][str(five[:4])] = []
    if str([five[0][0],five[1][0],five[2][0],five[3][0]]) not in fourthOrderChordDict[five[4][1]].keys():
        fourthOrderChordDict[five[4][1]][str([five[0][0],five[1][0],five[2][0],five[3][0]])] = []
    if str([five[0][0],five[1][0],five[2][0],five[3][0]]) not in fourthOrderNoteDict.keys():
        fourthOrderNoteDict[str([five[0][0],five[1][0],five[2][0],five[3][0]])] = []
    fourthOrderComplexDict[five[4][1]][str(five[:4])].append(five[4][0])
    fourthOrderChordDict[five[4][1]][str([five[0][0],five[1][0],five[2][0],five[3][0]])].append(five[4][0])
    fourthOrderNoteDict[str([five[0][0],five[1][0],five[2][0],five[3][0]])].append(five[4][0])
    
fourthOrderSimpleDict = {}
fourthOrderSimpleChordDict = {}
currentChords= []

for five in noteChordFivesSimple:
    if five[4][1] not in currentChords:
        currentChords.append(five[4][1])
        fourthOrderSimpleDict[five[4][1]] = {}
        fourthOrderSimpleChordDict[five[4][1]] = {}
    if str(five[:4]) not in fourthOrderSimpleDict[five[4][1]].keys():
        fourthOrderSimpleDict[five[4][1]][str(five[:4])] = []
    if str([five[0][0],five[1][0],five[2][0],five[3][0]]) not in fourthOrderSimpleChordDict[five[4][1]].keys():
        fourthOrderSimpleChordDict[five[4][1]][str([five[0][0],five[1][0],five[2][0],five[3][0]])] = []
    fourthOrderSimpleDict[five[4][1]][str(five[:4])].append(five[4][0])
    fourthOrderSimpleChordDict[five[4][1]][str([five[0][0],five[1][0],five[2][0],five[3][0]])].append(five[4][0])



def noteSuggestion(noteChordSequence,currentChord):
    """
    Parameters
    ----------
    noteChordSequence: list
    An array of midinote and chord pairs which represent a melody string. Must consist of a four note sequence.
    
    currentChord: str
    A string which represents the current harmonic context.

    """
    currentChordSimple = chordSimplify(currentChord)
    octave = noteChordSequence[3][0] - noteChordSequence[3][0]%12
    if noteChordSequence[3][0]<45:
        octave+=12
    if noteChordSequence[3][0]>95:
        octave-=12
    noteSequence = []

    for index in range(0,len(noteChordSequence)):
        noteSequence.append(noteChordSequence[index][0]%12)
        noteChordSequence[index][0] = noteChordSequence[index][0]%12
    
    if currentChord in fourthOrderComplexDict.keys() and str(noteChordSequence) in fourthOrderComplexDict[currentChord].keys():  
        return random.choice(fourthOrderComplexDict[currentChord][str(noteChordSequence)])+noteChordSequence[3][0]+octave
    if currentChord in thirdOrderComplexDict.keys() and str(noteChordSequence[1:]) in thirdOrderComplexDict[currentChord].keys():  
        return random.choice(thirdOrderComplexDict[currentChord][str(noteChordSequence[1:])])+noteChordSequence[3][0]+octave
    if currentChord in secondOrderComplexDict.keys() and str(noteChordSequence[2:]) in secondOrderComplexDict[currentChord].keys():  
        return random.choice(secondOrderComplexDict[currentChord][str(noteChordSequence[2:])])+noteChordSequence[3][0]+octave
    if currentChord in firstOrderComplexDict.keys() and str(noteChordSequence[3:]) in firstOrderComplexDict[currentChord].keys():  
        return random.choice(firstOrderComplexDict[currentChord][str(noteChordSequence[3:])])+noteChordSequence[3][0]+octave

    
    if currentChordSimple in fourthOrderSimpleDict.keys() and str(noteChordSequence) in fourthOrderSimpleDict[currentChordSimple].keys():  
        return random.choice(fourthOrderSimpleDict[currentChordSimple][str(noteChordSequence)])+noteChordSequence[3][0]+octave
    if currentChordSimple in thirdOrderSimpleDict.keys() and str(noteChordSequence[1:]) in thirdOrderSimpleDict[currentChordSimple].keys():  
        return random.choice(thirdOrderSimpleDict[currentChordSimple][str(noteChordSequence[1:])])+noteChordSequence[3][0]+octave
    if currentChordSimple in secondOrderSimpleDict.keys() and str(noteChordSequence[2:]) in secondOrderSimpleDict[currentChordSimple].keys():  
        return random.choice(secondOrderSimpleDict[currentChordSimple][str(noteChordSequence[2:])])+noteChordSequence[3][0]+octave
    if currentChordSimple in firstOrderSimpleDict.keys() and str(noteChordSequence[3:]) in firstOrderSimpleDict[currentChordSimple].keys():  
        return random.choice(firstOrderSimpleDict[currentChordSimple][str(noteChordSequence[3:])])+noteChordSequence[3][0]+octave


    if currentChord in fourthOrderChordDict.keys() and str(noteSequence) in fourthOrderChordDict[currentChord].keys():
        return random.choice(fourthOrderChordDict[currentChord][str(noteSequence)])+noteChordSequence[3][0]+octave
    if currentChord in thirdOrderChordDict.keys() and str(noteSequence[1:]) in thirdOrderChordDict[currentChord].keys():
        return random.choice(thirdOrderChordDict[currentChord][str(noteSequence[1:])])+noteChordSequence[3][0]+octave
    if currentChord in secondOrderChordDict.keys() and str(noteSequence[2:]) in secondOrderChordDict[currentChord].keys():
        return random.choice(secondOrderChordDict[currentChord][str(noteSequence[2:])])+noteChordSequence[3][0]+octave
    if currentChord in firstOrderChordDict.keys() and str(noteSequence[3:]) in firstOrderChordDict[currentChord].keys():
        return random.choice(firstOrderChordDict[currentChord][str(noteSequence[3:])])+noteChordSequence[3][0]+octave

    if str(noteSequence) in fourthOrderNoteDict.keys():
        return random.choice(fourthOrderNoteDict[str(noteSequence)])+noteChordSequence[3][0]+octave
    if str(noteSequence[1:]) in thirdOrderNoteDict.keys():
        return random.choice(thirdOrderNoteDict[str(noteSequence[1:])])+noteChordSequence[3][0]+octave
    if str(noteSequence[2:]) in secondOrderNoteDict.keys():
        return random.choice(secondOrderNoteDict[str(noteSequence[2:])])+noteChordSequence[3][0]+octave
    if str(noteSequence[3:]) in firstOrderNoteDict.keys():
        return random.choice(firstOrderNoteDict[str(noteSequence[3:])])+noteChordSequence[3][0]+octave


def noteTransitions(noteChordSequence,currentChord):
    """
    Parameters
    ----------
    noteChordSequence: list
    An array of midinote and chord pairs which represent a melody string. Must consist of a four note sequence.
    
    currentChord: str
    A string which represents the current harmonic context.

    """
    currentChordSimple = chordSimplify(currentChord)
    noteSequence = []
    #convert pitches to chroma
    for index in range(0,len(noteChordSequence)):
        noteSequence.append(noteChordSequence[index][0]%12)
        noteChordSequence[index][0] = noteChordSequence[index][0]%12
    
    if currentChord in fourthOrderComplexDict.keys() and str(noteChordSequence) in fourthOrderComplexDict[currentChord].keys():  
        return fourthOrderComplexDict[currentChord][str(noteChordSequence)]
    if currentChord in thirdOrderComplexDict.keys() and str(noteChordSequence[1:]) in thirdOrderComplexDict[currentChord].keys():  
        return thirdOrderComplexDict[currentChord][str(noteChordSequence[1:])]
    if currentChord in secondOrderComplexDict.keys() and str(noteChordSequence[2:]) in secondOrderComplexDict[currentChord].keys():  
        return secondOrderComplexDict[currentChord][str(noteChordSequence[2:])]
    if currentChord in firstOrderComplexDict.keys() and str(noteChordSequence[3:]) in firstOrderComplexDict[currentChord].keys():  
        return firstOrderComplexDict[currentChord][str(noteChordSequence[3:])]

    
    if currentChordSimple in fourthOrderSimpleDict.keys() and str(noteChordSequence) in fourthOrderSimpleDict[currentChordSimple].keys():  
        return fourthOrderSimpleDict[currentChordSimple][str(noteChordSequence)]
    if currentChordSimple in thirdOrderSimpleDict.keys() and str(noteChordSequence[1:]) in thirdOrderSimpleDict[currentChordSimple].keys():  
        return thirdOrderSimpleDict[currentChordSimple][str(noteChordSequence[1:])]
    if currentChordSimple in secondOrderSimpleDict.keys() and str(noteChordSequence[2:]) in secondOrderSimpleDict[currentChordSimple].keys():  
        return secondOrderSimpleDict[currentChordSimple][str(noteChordSequence[2:])]
    if currentChordSimple in firstOrderSimpleDict.keys() and str(noteChordSequence[3:]) in firstOrderSimpleDict[currentChordSimple].keys():  
        return firstOrderSimpleDict[currentChordSimple][str(noteChordSequence[3:])]


    if currentChord in fourthOrderChordDict.keys() and str(noteSequence) in fourthOrderChordDict[currentChord].keys():
        return fourthOrderChordDict[currentChord][str(noteSequence)]
    if currentChord in thirdOrderChordDict.keys() and str(noteSequence[1:]) in thirdOrderChordDict[currentChord].keys():
        return thirdOrderChordDict[currentChord][str(noteSequence[1:])]
    if currentChord in secondOrderChordDict.keys() and str(noteSequence[2:]) in secondOrderChordDict[currentChord].keys():
        return secondOrderChordDict[currentChord][str(noteSequence[2:])]
    if currentChord in firstOrderChordDict.keys() and str(noteSequence[3:]) in firstOrderChordDict[currentChord].keys():
        return firstOrderChordDict[currentChord][str(noteSequence[3:])]

    if str(noteSequence) in fourthOrderNoteDict.keys():
        return fourthOrderNoteDict[str(noteSequence)]
    if str(noteSequence[1:]) in thirdOrderNoteDict.keys():
        return thirdOrderNoteDict[str(noteSequence[1:])]
    if str(noteSequence[2:]) in secondOrderNoteDict.keys():
        return secondOrderNoteDict[str(noteSequence[2:])]
    if str(noteSequence[3:]) in firstOrderNoteDict.keys():
        return firstOrderNoteDict[str(noteSequence[3:])]

def noteTransitionsComplex(noteChordSequence,currentChord):
    """
    Parameters
    ----------
    noteChordSequence: list
    An array of midinote and chord pairs which represent a melody string. Must consist of a four note sequence.
    
    currentChord: str
    A string which represents the current harmonic context.

    """
    currentChordSimple = chordSimplify(currentChord)
    noteSequence = []
    #convert pitches to chroma
    for index in range(0,len(noteChordSequence)):
        noteSequence.append(noteChordSequence[index][0]%12)
        noteChordSequence[index][0] = noteChordSequence[index][0]%12
    
    if currentChord in fourthOrderComplexDict.keys() and str(noteChordSequence) in fourthOrderComplexDict[currentChord].keys():  
        return fourthOrderComplexDict[currentChord][str(noteChordSequence)]
    if currentChord in thirdOrderComplexDict.keys() and str(noteChordSequence[1:]) in thirdOrderComplexDict[currentChord].keys():  
        return thirdOrderComplexDict[currentChord][str(noteChordSequence[1:])]
    if currentChord in secondOrderComplexDict.keys() and str(noteChordSequence[2:]) in secondOrderComplexDict[currentChord].keys():  
        return secondOrderComplexDict[currentChord][str(noteChordSequence[2:])]
    if currentChord in firstOrderComplexDict.keys() and str(noteChordSequence[3:]) in firstOrderComplexDict[currentChord].keys():  
        return firstOrderComplexDict[currentChord][str(noteChordSequence[3:])]
    else:
        return []

def noteTransitionsSimpleChord(noteChordSequence,currentChord):
    """
    Parameters
    ----------
    noteChordSequence: list
    An array of midinote and chord pairs which represent a melody string. Must consist of a four note sequence.
    
    currentChord: str
    A string which represents the current harmonic context.

    """
    currentChordSimple = chordSimplify(currentChord)
    noteSequence = []
    #convert pitches to chroma
    for index in range(0,len(noteChordSequence)):
        noteSequence.append(noteChordSequence[index][0]%12)
        noteChordSequence[index][0] = noteChordSequence[index][0]%12

    
    if currentChordSimple in fourthOrderSimpleDict.keys() and str(noteChordSequence) in fourthOrderSimpleDict[currentChordSimple].keys():  
        return fourthOrderSimpleDict[currentChordSimple][str(noteChordSequence)]
    if currentChordSimple in thirdOrderSimpleDict.keys() and str(noteChordSequence[1:]) in thirdOrderSimpleDict[currentChordSimple].keys():  
        return thirdOrderSimpleDict[currentChordSimple][str(noteChordSequence[1:])]
    if currentChordSimple in secondOrderSimpleDict.keys() and str(noteChordSequence[2:]) in secondOrderSimpleDict[currentChordSimple].keys():  
        return secondOrderSimpleDict[currentChordSimple][str(noteChordSequence[2:])]
    if currentChordSimple in firstOrderSimpleDict.keys() and str(noteChordSequence[3:]) in firstOrderSimpleDict[currentChordSimple].keys():  
        return firstOrderSimpleDict[currentChordSimple][str(noteChordSequence[3:])]
    else:
        return []


def noteTransitionsSingleChord(noteChordSequence,currentChord):
    """
    Parameters
    ----------
    noteChordSequence: list
    An array of midinote and chord pairs which represent a melody string. Must consist of a four note sequence.
    
    currentChord: str
    A string which represents the current harmonic context.

    """
    currentChordSimple = chordSimplify(currentChord)
    noteSequence = []
    #convert pitches to chroma
    for index in range(0,len(noteChordSequence)):
        noteSequence.append(noteChordSequence[index][0]%12)
        noteChordSequence[index][0] = noteChordSequence[index][0]%12


    if currentChord in fourthOrderChordDict.keys() and str(noteSequence) in fourthOrderChordDict[currentChord].keys():
        return fourthOrderChordDict[currentChord][str(noteSequence)]
    if currentChord in thirdOrderChordDict.keys() and str(noteSequence[1:]) in thirdOrderChordDict[currentChord].keys():
        return thirdOrderChordDict[currentChord][str(noteSequence[1:])]
    if currentChord in secondOrderChordDict.keys() and str(noteSequence[2:]) in secondOrderChordDict[currentChord].keys():
        return secondOrderChordDict[currentChord][str(noteSequence[2:])]
    if currentChord in firstOrderChordDict.keys() and str(noteSequence[3:]) in firstOrderChordDict[currentChord].keys():
        return firstOrderChordDict[currentChord][str(noteSequence[3:])]
    else:
        return []

def noteTransitionsBasic(noteChordSequence,currentChord):
    """
    Parameters
    ----------
    noteChordSequence: list
    An array of midinote and chord pairs which represent a melody string. Must consist of a four note sequence.
    
    currentChord: str
    A string which represents the current harmonic context.

    """
    currentChordSimple = chordSimplify(currentChord)
    noteSequence = []
    for index in range(0,len(noteChordSequence)):
        noteSequence.append(noteChordSequence[index][0]%12)
        noteChordSequence[index][0] = noteChordSequence[index][0]%12

    if str(noteSequence) in fourthOrderNoteDict.keys():
        return fourthOrderNoteDict[str(noteSequence)]
    if str(noteSequence[1:]) in thirdOrderNoteDict.keys():
        return thirdOrderNoteDict[str(noteSequence[1:])]
    if str(noteSequence[2:]) in secondOrderNoteDict.keys():
        return secondOrderNoteDict[str(noteSequence[2:])]
    if str(noteSequence[3:]) in firstOrderNoteDict.keys():
        return firstOrderNoteDict[str(noteSequence[3:])]


def updateSuggestions(finalUpperSuggestions, finalLowerSuggestions, suggestions,model,order):
    upperSuggestions = []
    lowerSuggestions = []

    finalUpperSuggestionsMIDI = []
    finalLowerSuggestionsMIDI = []

    for index in range(0,len(finalUpperSuggestions)):
        finalUpperSuggestionsMIDI.append(finalUpperSuggestions[index][0])

    for index in range(0,len(finalLowerSuggestions)):
        finalLowerSuggestionsMIDI.append(finalLowerSuggestions[index][0])

    for suggestion in suggestions:
        if suggestion>0 and suggestion not in finalUpperSuggestionsMIDI:
            upperSuggestions.append(suggestion)
        if suggestion<0 and suggestion not in finalLowerSuggestionsMIDI:
            lowerSuggestions.append(suggestion)

    # print 'final upper suggestions midi'
    # print finalUpperSuggestionsMIDI
    # print 'final upper suggestions'
    # print finalUpperSuggestions
    # print 'upper suggestions'
    # print upperSuggestions

    if len(finalUpperSuggestions) != 2 and len(upperSuggestions) > 0:
        firstSuggestion = random.choice(upperSuggestions)
        if len(upperSuggestions) >=2 and len(finalUpperSuggestions)==0:
            random.shuffle(upperSuggestions)
            secondSuggestion = -1
            for suggestion in upperSuggestions:
                if suggestion != firstSuggestion:
                    secondSuggestion = suggestion
            finalUpperSuggestions.append([firstSuggestion,[model,order]])
            if secondSuggestion >0:
                finalUpperSuggestions.append([secondSuggestion,[model,order]])
        else:
            if firstSuggestion not in finalUpperSuggestions:
                finalUpperSuggestions.append([firstSuggestion,[model,order]])

    if len(finalLowerSuggestions) != 2 and len(lowerSuggestions) > 0:
        firstSuggestion = random.choice(lowerSuggestions)
        if len(lowerSuggestions) >=2 and len(finalLowerSuggestions) == 0:
            random.shuffle(lowerSuggestions)
            secondSuggestion = 1
            for suggestion in lowerSuggestions:
                if suggestion != firstSuggestion:
                    secondSuggestion = suggestion
            finalLowerSuggestions.append([firstSuggestion,[model,order]])
            if secondSuggestion <0:
                finalLowerSuggestions.append([secondSuggestion,[model,order]])
        else:
            if firstSuggestion not in finalLowerSuggestions:
                finalLowerSuggestions.append([firstSuggestion,[model,order]])

    return finalUpperSuggestions,finalLowerSuggestions


def fiveSuggestions(noteChordSequenceCurrent, currentChord):
    """
    Parameters
    ----------
    noteChordSequence: list
    An array of midinote and chord pairs which represent a melody string. Must consist of a four note sequence.
    
    currentChord: str
    A string which represents the current harmonic context.

    """
    noteSequence = []
    noteChordSequence = copy.deepcopy(noteChordSequenceCurrent)
    noteChordSequenceSimple = copy.deepcopy(noteChordSequenceCurrent)
    currentChordSimple = chordSimplify(currentChord)
    finalSuggestions = []
    finalSuggestions.append(noteChordSequence[3][0])
    finalUpperSuggestions = []
    finalLowerSuggestions = []
    
    for index in range(0,len(noteChordSequence)):
        noteSequence.append(noteChordSequence[index][0]%12)
        noteChordSequence[index][0] = noteChordSequence[index][0]%12
        noteChordSequenceSimple[index][0] = noteChordSequenceSimple[index][0]%12
        noteChordSequenceSimple[index][1] = chordSimplify(noteChordSequenceSimple[index][1])

    #complex suggestions
    if currentChord in fourthOrderComplexDict.keys() and str(noteChordSequence) in fourthOrderComplexDict[currentChord].keys():
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,fourthOrderComplexDict[currentChord][str(noteChordSequence)],1,4)

    if currentChord in thirdOrderComplexDict.keys() and str(noteChordSequence[1:]) in thirdOrderComplexDict[currentChord].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,thirdOrderComplexDict[currentChord][str(noteChordSequence[1:])],1,3)

    if currentChord in secondOrderComplexDict.keys() and str(noteChordSequence[2:]) in secondOrderComplexDict[currentChord].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,secondOrderComplexDict[currentChord][str(noteChordSequence[2:])],1,2)
        

    if currentChord in firstOrderComplexDict.keys() and str(noteChordSequence[3:][0]) in firstOrderComplexDict[currentChord].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,firstOrderComplexDict[currentChord][str(noteChordSequence[3:][0])],1,1)


    # print "simple chord suggestions"
    if currentChordSimple in fourthOrderSimpleDict.keys() and str(noteChordSequenceSimple) in fourthOrderSimpleDict[currentChordSimple].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,fourthOrderSimpleDict[currentChordSimple][str(noteChordSequenceSimple)],2,4)

    if currentChordSimple in thirdOrderSimpleDict.keys() and str(noteChordSequenceSimple[1:]) in thirdOrderSimpleDict[currentChordSimple].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,thirdOrderSimpleDict[currentChordSimple][str(noteChordSequenceSimple[1:])],2,3)

    if currentChordSimple in secondOrderSimpleDict.keys() and str(noteChordSequenceSimple[2:]) in secondOrderSimpleDict[currentChordSimple].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,secondOrderSimpleDict[currentChordSimple][str(noteChordSequenceSimple[2:])],2,2)

    if currentChordSimple in firstOrderSimpleDict.keys() and str(noteChordSequenceSimple[3:][0]) in firstOrderSimpleDict[currentChordSimple].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,firstOrderSimpleDict[currentChordSimple][str(noteChordSequenceSimple[3:][0])],2,1)


    # print "single chord suggestions"
    if currentChord in fourthOrderChordDict.keys() and str(noteSequence) in fourthOrderChordDict[currentChord].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,fourthOrderChordDict[currentChord][str(noteSequence)],3,4)
        

    if currentChord in thirdOrderChordDict.keys() and str(noteSequence[1:]) in thirdOrderChordDict[currentChord].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,thirdOrderChordDict[currentChord][str(noteSequence[1:])],3,3)
        

    if currentChord in secondOrderChordDict.keys() and str(noteSequence[2:]) in secondOrderChordDict[currentChord].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,secondOrderChordDict[currentChord][str(noteSequence[2:])],3,2)
        

    if currentChord in firstOrderChordDict.keys() and str(noteSequence[3:][0]) in firstOrderChordDict[currentChord].keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,firstOrderChordDict[currentChord][str(noteSequence[3:][0])],3,1)



    # print "simple suggestions"
    if str(noteSequence) in fourthOrderNoteDict.keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,fourthOrderNoteDict[str(noteSequence)],4,4)
        

    if str(noteSequence[1:]) in thirdOrderNoteDict.keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,thirdOrderNoteDict[str(noteSequence[1:])],4,3)
        

    if str(noteSequence[2:]) in secondOrderNoteDict.keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  
        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,secondOrderNoteDict[str(noteSequence[2:])],4,2)

    if str(noteSequence[3:]) in secondOrderNoteDict.keys() and len(finalUpperSuggestions)+len(finalLowerSuggestions) < 4:  

        finalUpperSuggestions,finalLowerSuggestions = updateSuggestions(finalUpperSuggestions,finalLowerSuggestions,firstOrderNoteDict[str(noteSequence[3:][0])],4,1)


    modelDict = {}
    for index in range(0,2):
        # print 'HERRERER'
        # print finalUpperSuggestions[index][1]
        # print finalUpperSuggestions[index][0]
        modelDict[str(finalUpperSuggestions[index][0])] = finalUpperSuggestions[index][1]
        modelDict[str(finalLowerSuggestions[index][0])] = finalLowerSuggestions[index][1]

    print 'final upper suggestions:'
    print finalUpperSuggestions
    print 'final lower suggestions:'
    print finalLowerSuggestions

    finalSuggestions.append(finalSuggestions[0]+finalUpperSuggestions[0][0])
    finalSuggestions.append(finalSuggestions[0]+finalUpperSuggestions[1][0])
    finalSuggestions.append(finalSuggestions[0]+finalLowerSuggestions[0][0])
    finalSuggestions.append(finalSuggestions[0]+finalLowerSuggestions[1][0])
    finalSuggestions.sort()


    finalModels = []
    for suggestion in finalSuggestions:
        originalSuggestion = suggestion-finalSuggestions[2]
        if str(originalSuggestion) in modelDict.keys():
            finalModels.append((modelDict[str(originalSuggestion)][0]*10)+(modelDict[str(originalSuggestion)][1]))
        else:
            finalModels.append(0)
    # print modelDict
    print "finalSuggestions"
    print finalSuggestions
    return finalSuggestions,finalModels


print 'Models Ready'


### OSC SERVER ###

#!/usr/bin/env python3
from OSC import OSCServer
import OSC
import sys
from time import sleep
server = OSCServer( ("localhost", 57125) )
processing = OSC.OSCClient()
processing.connect(('127.0.0.1', 12000))   # connect to Processing


currentChain = [[62,'G9'],[60,'G9'],[62,'G9'],[60,'G9']]
currentChord = 'Cmaj9'
run = True

def handle_timeout(self):
    self.timed_out = True
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

def quit_callback(path, tags, args, source):
    global run
    run = False
    server.close()

def newNote(path, tags, args, source):
    global currentChain
    currentChain = currentChain[1:]+currentChain[:1]
    currentChain[3] = [args[0],args[1]]
    # sendNotes()
    global currentChord
    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/newSuggestions")
    fiveNewSuggestions,fiveNewModels = fiveSuggestions(currentChain,currentChord)
    oscmsg.append(fiveNewSuggestions)
    oscmsg.append(fiveNewModels)
    processing.send(oscmsg)

def sendnotes():
    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/newSuggestions")
    oscmsg.append(fiveSuggestions(currentChain,currentChord))
    processing.send(oscmsg)

def newChord(path, tags, args, source):
    global currentChord
    currentChord = args[0]
    global currentChain
    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/newSuggestions")
    oscmsg.append(fiveSuggestions(currentChain,currentChord))
    processing.send(oscmsg)

server.addMsgHandler( "/newNote", newNote )
server.addMsgHandler( "/newChord", newChord )
server.addMsgHandler( "/quit", quit_callback )