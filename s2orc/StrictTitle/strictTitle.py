import mysql.connector
import sys
import re
import csv
import numpy as np
import pandas as pd
import time
import config
import MySQLdb as sql

db=sql.connect(host = config.host, user = config.user, passwd = config.passwd, db = config.db, charset = "utf8")

def get_time():
    x = datetime.datetime.now()
    print(x) 

def main():
    csv_header()
    r = db.cursor()
    
    file1 = '../testFiles/known.txt'
    df = pd.read_csv('../testFiles/NEWyearTrial.csv')
    df_i = df.set_index('corpus_id')

    start = time.time()
    with open(file1) as f1:
        for x in f1:
            
            matches = []
            paperid = x.replace('\n','')
            original = f"SELECT title, year, field FROM s2orcDATA WHERE corpus_id = {paperid}"
            print(original)
            r.execute(original)
            
            
            Ori =  r.fetchone()
            oTitle = re.sub(r'[^A-Za-z0-9 ]+', '', Ori[0])

            oYear = Ori[1]
            oField = Ori[2]

            df1 = df_i['title'].str.match(oTitle)
            data = df1.to_frame()
            data.columns = ['bool']
            #print(data)
            for index, z in data.loc[data['bool'] == True].iterrows():
                matches.append(index)

            # if the cluster has more than one unique id's it is a near duplicate
            if len(matches) > 1:
                # if the paperid is in duplicate list, then remove it
                if paperid in matches:
                    index = [x for x in range(len(matches)) if matches[x] == paperid] 
                    matches.pop(index[0])
                csv_w(paperid, matches)

            del df1

    end = time.time()
    total = float(start - end)
    print(total)
    r.close()
    db.close()
            

            
def csv_w(Ocorpus, Dcourpus):
    oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/TrueDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(oringinal_corpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(oringinal_corpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        print(row)
        
def csv_header():
    with open('Results/TrueDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()