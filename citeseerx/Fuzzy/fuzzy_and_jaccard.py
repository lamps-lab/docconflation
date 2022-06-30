import mysql.connector
import sys
import datetime
import re
import csv
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import MySQLdb as sql
import time
import config

db=sql.connect(host = config.hawkingh, user = config.hawkingu, passwd = config.hawkingp, db = config.hawkingdb, charset = "utf8")

def get_time():
    x = datetime.datetime.now()
    print(x) 

def main():
    csv_header()
    r = db.cursor()
    start = time.time()
    
    df = pd.read_csv('../testFiles/Trial.csv')
    
    df['year'] = df['year'].fillna(0.0).astype(int)
    df.set_index('year')

    file1 = '../testFiles/known.txt'

    with open(file1) as f1:
        for x in f1:
            paperid = x.replace('\n','')
            original = f"SELECT title, year FROM papers WHERE id = '{paperid}'"
            r.execute(original)
            t = time.process_time()
            Ori =  r.fetchone()
            oTitle = Ori[0]
            oYear = Ori[1]

            matches = []
            
            for index, z in df.iterrows():           
                dCorpus = z['id']
                dTitle = z['title']

                if fuzzy_score(oTitle, dTitle) > 80:
                    matches.append(dCorpus)
                    
            # if the cluster has more than one unique id's it is a near duplicate
            if len(matches) > 1:
                # if the paperid is in duplicate list, then remove it
                if paperid in matches:
                    index = [x for x in range(len(matches)) if matches[x] == paperid] 
                    matches.pop(index[0])
                csv_w(paperid, matches)
    end = time.time()
    total = float(end - start)
    print(total)

    r.close()
    db.close()

                
def fuzzy_score(Otitle, Dtitle):
    score = fuzz.partial_ratio(Otitle, Dtitle)
    print(score)
    return score

def jaccard_score(Oauthors, Dauthors):
    intersection = len(list(set(Oauthors).intersection(Dauthors)))
    union = (len(Oauthors) + len(Dauthors)) - intersection
    return float(intersection) / union

def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/80TrueDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['id', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(oringinal_corpus)}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'id': f'{str(oringinal_corpus)}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open('Results/80TrueDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['id' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()