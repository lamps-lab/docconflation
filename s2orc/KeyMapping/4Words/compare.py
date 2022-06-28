import sys
import csv
import numpy as np
import pandas as pd
import re


# Function to create dicitonary from duplicate list and paperid
# and to remove everything but alphanumerical characters
def list_cleaner(dup_list, id):
    dictionary = {}
    dictionary[id] = []
    pattern = [r'\w+']

    
    dup_list.pop(-1)

    for paper in dup_list:

        # regular expression to get only alphanumerical array of words of authors and title
        for p in pattern:
            match = re.findall(p, paper)
            dictionary[id].append(match)
    return dictionary


def main():
    ground_truth_df = pd.read_csv('../DC2.csv')
    compare_df = pd.read_csv('./Results/4WordsDuplicates.csv')

    tp = 0
    fp = 0 
    tn = 0
    fn = 0

    trueDuplicateList = []
    reportedDuplicateList = []
    reportedIDs =[]
    trueIDs = []
    duplicate_list = []

    for index, i in compare_df.iterrows():
        reportedIDs.append(i[0])

        duplicate_list = i[2].split(" ")

        reported_dict = list_cleaner(duplicate_list, i[0])
        reportedDuplicateList.append(reported_dict)
        
        #sprint(reported_dict)
    #print (allRC)

    print(len(reportedIDs))
    testFile = open("./test.txt", "w")
    for index2, j in ground_truth_df.iterrows():
        GT_corpus = j[0]
        trueIDs.append(j[0])
        #if GT_corpus not in allRC:
        #    fn += 1

        testFile.write(str(GT_corpus) + "\n")
        GT_NearDuplicates = j[2]
        row = compare_df.loc[compare_df['Corpus'] == GT_corpus]
        if row.dropna(how='all').empty:
            continue

        #compared_NearDuplicates = row['Duplicates'].values[0]

        TrueNearDuplicates = GT_NearDuplicates.split(",")

        true_dict = list_cleaner(TrueNearDuplicates, GT_corpus)
        trueDuplicateList.append(true_dict)

    # end for ground_truth
    testFile.close()

    print("truelist: ",trueDuplicateList)
    print("prediction list: ", reportedDuplicateList)
    for truedict in trueDuplicateList:
        for x in truedict:
            if x not in reportedIDs:
                fn += 1
    
    for reportedict in reportedDuplicateList:
        for x in reportedict:
            #print("x: ",x, "reported[x]: ",reportedict[x])
            if x in trueIDs:
                #if reportedict[x] in tr
                tp += 1
            else:
                fp += 1
    '''           
    for paper in trueIDs:
        #print(paper)
        if paper in reportedIDs:
            tp += 1
        else:
            fn += 1
    for paper in reportedIDs:
        if paper not in trueIDs:
            fp += 1'''

        #print("true: ", trueIDs)
        #print("reported: ", reportedIDs)
    print (f"File: True Positives: {tp}   False Positives: {fp}   True Negative: {tn}     False Negatives: {fn}")
    precision = tp /(tp + fp)
    recall = tp/(tp + fn)

    print("Precision: ", precision, "\nRecall: ", recall)
    print()

if __name__ == "__main__":

    main()