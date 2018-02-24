import os
import glob
import re
import csv
import argparse
import shutil
import sys
import tensorflow as tf

path = '/Users/sahanarangarajan/researchproj/articles/'


def findAuthors():
    authors = {}
    path = '/Users/sahanarangarajan/researchproj/articles/'
    ind = 0
    for infile in glob.glob(os.path.join(path, '*.txt')):
        lines = parseIntoLines(filename)
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

def findBylines():
    bylines = {}
    for infile in glob.glob(os.path.join(path, '*.txt')):
        lines = [line.rstrip('\n') for line in open(infile)]
        bylineFound = False
        for line in lines:
            if not bylineFound:
                if "author:" in line.lower() or "by:" in line.lower() or "by " in line.lower():
                    bylines[infile[len(path):]] = line
                    bylineFound = True
    return bylines

def authorsToCSV(authorDict):
    csvList = [['Article', 'Title(regex)']]
    for entry in authorDict:
        csvList.append([entry, authorDict[entry]])
    csvFile = open('/Users/sahanarangarajan/researchproj/authors.csv', 'w')
    with csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvList)

def bylinesToCSV(bylineDict):
    csvList = [['Article', 'Byline(script)']]
    for entry in bylineDict:
        csvList.append([entry, bylineDict[entry]])
    csvFile = open('/Users/sahanarangarajan/researchproj/bylines.csv', 'w')
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

def getBylineCSV():
    csvList = []
    with open('bylines.csv', 'rb') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            csvList.append(row)
    return csvList


if __name__ == '__main__':
  byline_dict = findBylines()
  bylinesToCSV(byline_dict)
  print getBylineCSV()  


