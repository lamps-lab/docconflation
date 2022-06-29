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

# connect to the database
db=sql.connect(host = config.host, user = config.user, passwd = config.passwd, db = config.db, charset = "utf8")


def main():
    csv_header()
    r = db.cursor()

    start = time.time()

    df = pd.read_csv('../testFiles/NEWyearTrial.csv')

    df['year'] = df['year'].fillna(0.0).astype(int)
    df.set_index('year')
    df.set_index('field')

    file1 = '../testFiles/known.txt'

    with open(file1) as f1:
        for x in f1:
            paperid = x.replace('\n','')
            original = f"SELECT title, authors, year, field FROM s2orcDATA WHERE corpus_id = {paperid}"
            r.execute(original)

            Ori =  r.fetchone()
            oTitle = Ori[0]
            oAuthor = Ori[1]
            oYear = Ori[2]
            oField = Ori[3]
                
            oAuthor = re.sub(' +', ' ', oAuthor)
            oAuthorList = oAuthor.split(',')
               
            matches = []

            for index, z in df.iterrows():           
                dCorpus = z['corpus_id']
                dTitle = z['title']

                if fuzzy_score(oTitle, dTitle) > 95:
                    print (dCorpus)
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
    with open('Results/95TrueDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(oringinal_corpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(oringinal_corpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open('Results/95TrueDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()