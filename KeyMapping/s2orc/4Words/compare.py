import sys
import csv
import numpy as np
import pandas as pd

def main():
    #compared_file = sys.argv[1]
    ground_truth_df = pd.read_csv('../groundTruth.csv')
    compare_df = pd.read_csv('Results/4WordsDuplicates.csv')
    #print(ground_truth_df)
    #print(compare_df)

    tp = 0
    fp = 0 
    tn = 0
    fn = 0
    allRC =[]
    for index2, h in compare_df.iterrows():
        allRC.append(h[0])
    #print (allRC)

    for index, j in ground_truth_df.iterrows():
        GT_corpus = j[0]
        if GT_corpus not in allRC:
            fn += 1

        GT_NearDuplicates = j[2]
        row = compare_df.loc[compare_df['Corpus'] == GT_corpus]
        if row.dropna(how='all').empty:
            continue
        #print(row['Duplicates'])
        #print(row)
        #print(GT_corpus)
        compared_NearDuplicates = row['Duplicates'].values[0]
        #print(GT_NearDuplicates)
        #print(compared_NearDuplicates)
        TrueNearDuplicates = GT_NearDuplicates.split(' ')
        ReportedNearDuplicates = str(compared_NearDuplicates).split(' ')
        #print(TrueNearDuplicates)
        #print(ReportedNearDuplicates)
        #print(index)
        for x in TrueNearDuplicates:
            if x in ReportedNearDuplicates:
                tp += 1
            elif x not in ReportedNearDuplicates:
                fn += 1
        for x in ReportedNearDuplicates:
            if x not in TrueNearDuplicates:
                fp += 1
    print (f"File: True Positives: {tp}   False Positives: {fp}   True Negative: {tn}     False Negatives: {fn}")
    precision = tp /(tp + fp)
    recall = tp/(tp + fn)

    print("Precision: ", precision, "\nRecall: ", recall)

if __name__ == "__main__":

    main()