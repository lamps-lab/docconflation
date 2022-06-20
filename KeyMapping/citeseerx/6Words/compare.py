# Program to 

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

    for paper in dup_list:
        paper = re.sub('[^0-9.]', '', paper)
        # regular expression to get only alphanumerical and dots ('.')  array of words of authors and title
        dictionary[id].append(paper)
    return dictionary


def main():
    ground_truth_df = pd.read_csv('../GT.csv')
    compare_df = pd.read_csv('./Results/6WordsDuplicates.csv')

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
        
        #print(reported_dict)
    #print (allRC)

    print(len(reportedIDs))
    falseNegative = open("./falseNegatives.txt", "w")
    for index2, j in ground_truth_df.iterrows():
        GT_corpus = j[0]
        trueIDs.append(j[0])
        
        GT_NearDuplicates = j[2]

        TrueNearDuplicates = GT_NearDuplicates.split(" ")

        true_dict = list_cleaner(TrueNearDuplicates, GT_corpus)

        if GT_corpus not in reportedIDs:
            fn += 1
            falseNegative.write(str(GT_corpus) + "\n")
        trueDuplicateList.append(true_dict)
    # end for ground_truth
    falseNegative.close()

    print("how many trueduplicates? ", len(trueDuplicateList))
    print("how many reporteduplicates? ", len(reportedDuplicateList))
    for reportedict in reportedDuplicateList:
        x = list(reportedict.keys())[0]

        tpfound = 0
        for truedict in trueDuplicateList:
            y = list(truedict.keys())[0]
            if reportedict[x] == truedict[y]:
                tp += 1
                tpfound = 1
                break
        if tpfound == 0:
            fp += 1

    # Calculations  
    precision = tp /(tp + fp)
    recall = tp/(tp + fn)
    f1 = (2 * precision * recall) / (precision + recall)

    print (f"File: True Positives: {tp}   False Positives: {fp}   \n True Negative: {tn}     False Negatives: {fn}")
    print("\nPrecision: ", round(precision, 4), "\nRecall: ", round(recall,4), "\nF1 score: ", round(f1, 4))
    print()
    print()

if __name__ == "__main__":

    main()