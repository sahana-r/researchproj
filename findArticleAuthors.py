import os
import glob
import re
import csv
import argparse
import shutil
import sys
import tensorflow as tf

path = '/Users/sahanarangarajan/researchproj/articles/'
author_labels = {}
author_labels[path + '1stamend.txt'] = 'Brooks Boliek'
author_labels[path + '092793.txt'] = 'David Zizzo'

def findAuthors():
    authors = {}
    path = '/Users/sahanarangarajan/researchproj/articles/'
    ind = 0
    for infile in glob.glob(os.path.join(path, '*.txt')):
        currFile = open(infile, 'r')
        currTxt = currFile.read()
        m = re.search(r'author:(.*)', currTxt, re.I)
        if m:
            authors[infile[len(path):]] = m.group(1).strip()
        else:
            m = re.search(r'by:(.*)', currTxt, re.I)
            if m:
                authors[infile[len(path):]] = m.group(1).strip()
            else:
                m = re.search(r'by(.*)', currTxt, re.I)
                if m:
                    authors[infile[len(path):]] = m.group(1).strip()
    return authors

def authorsToCSV(authorDict):
    csvList = [['Article', 'Title(regex)']]
    for entry in authorDict:
        csvList.append([entry, authorDict[entry]])
    csvFile = open('/Users/sahanarangarajan/researchproj/authors.csv', 'w')
    with csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvList)

def parseIntoLines(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    lines = [line.rstrip('\r') for line in lines]
    lines = [line.rstrip('\x1a') for line in lines]
    lines = [line for line in lines if line != '']
    lines = [line for line in lines if line != ' ']
    return lines

def containsAuthorOrBy(line):
    if "author" in line.lower() or " by" in line.lower():
        return True
    return False

def distFromTop(line, lines):
    return int(lines.index(line))

def containsPunctuation(line):
    if '.' in line or ';' in line or '?' in line or '!' in line:
        return True
    return False

def labeler(line, filename):
    authorName = author_labels[filename]
    if authorName in line:
        return True
    return False

def authorAlgo():
    path = '/Users/sahanarangarajan/researchproj/articles/'
    files = []
    for infile in glob.glob(os.path.join(path, '*.txt')):
        files.append(infile)
    dataset = tf.data.TextLineDataset(files)

def linesCSV(filename):
    lines = parseIntoLines(filename)
    csvList = []
    for line in lines:
        currLineCSV = [line]
        currLineCSV.append(distFromTop(line, lines))
        currLineCSV.append(containsPunctuation(line))
        currLineCSV.append(containsAuthorOrBy(line))
        currLineCSV.append(labeler(line, filename))
        csvList.append(currLineCSV)
    csvFile = open('/Users/sahanarangarajan/researchproj/classifier_data.csv', 'w')
    with csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvList)

def testCSV(filename):
    lines = parseIntoLines(filename)
    csvList = [] 
    for line in lines:
        currLineCSV = [line]
        currLineCSV.append(distFromTop(line, lines))
        currLineCSV.append(containsPunctuation(line))
        currLineCSV.append(containsAuthorOrBy(line))
        currLineCSV.append(labeler(line, filename))
        csvList.append(currLineCSV)
    csvFile = open('/Users/sahanarangarajan/researchproj/classifier_test.csv', 'w')
    with csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvList)

if __name__ == '__main__':
  filenames = author_labels.keys()
  for filename in filenames:
    linesCSV(filename)
  testCSV(path + '092793.txt')  


