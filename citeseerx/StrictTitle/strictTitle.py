import mysql.connector
import sys
import datetime
import re
import csv
import numpy as np
import pandas as pd
import time
import MySQLdb as sql
import config

db=sql.connect(host = config.hawkingh, user = config.hawkingu, passwd = config.hawkingp, db = config.hawkingdb, charset = "utf8")


def main():
    csv_header()
    r = db.cursor()
    
    file1 = '../testFiles/known.txt'
    df = pd.read_csv('../testFiles/Trial.csv')
    df_i = df.set_index('id')

    start = time.time()

    with open(file1) as f1:
        for x in f1:
            matches = []
            paperid = x.replace('\n','')
            original = f"SELECT title, year FROM papers WHERE id = '{paperid}'"
            r.execute(original)
            
            Ori =  r.fetchone()
            oTitle = re.sub(r'[^A-Za-z0-9 ]+', '', Ori[0])

            df1 = df_i['title'].str.match(oTitle)
            data = df1.to_frame()
            data.columns = ['bool']

            for index, z in data.loc[data['bool'] == True].iterrows():
                print (index)
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
        fieldNames = ['id', 'Amount' , 'Duplicates']

        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(oringinal_corpus)}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'id': f'{str(oringinal_corpus)}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        
        print(row)
        
def csv_header():
    with open('Results/TrueDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['id' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

if __name__ == "__main__":

    main()