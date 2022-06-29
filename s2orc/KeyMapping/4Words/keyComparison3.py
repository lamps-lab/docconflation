import sys
import datetime
import re
import MySQLdb as sql
import csv
import time

import config

db=sql.connect(host = config.chandrah, user = config.chandrau, passwd = config.chandrap, db = config.chandradb, charset = "utf8")


def main():
    csv_header()

    r = db.cursor()
    start = time.time()

    File = open(f'./known.txt', 'r')
    
    cases = []
    for row in File:
        nrow = row.replace('\n','')
        cases.append(nrow)
    File.close()
    
    # cases holds the id numbers
    print("all of cases: ", len(cases))
    for i in cases:


        cur = f"SELECT database_id, corpus_id, key1, key2, key3, key4, year FROM  LongWordsKeys WHERE corpus_id = {i}"
        r.execute(cur)
        
        current =  r.fetchone()

        paperid = current[1]
        key1 = current[2]
        key2 = current[3]
        key3 = current[4]
        key4 = current[5]
        year = current[6]
        
        first_key = keyString(key1, year) 
        second_key = keyString(key2, year) 
        third_key = keyString(key3, year)
        forth_key = keyString(key4, year)

        merged = list(set(first_key + second_key + third_key + forth_key))
        
        # if the cluster has more than one unique id's it is a near duplicate
        if len(merged) > 1:
            # if the paperid is in duplicate list, then remove it
            if paperid in merged:
                index = [x for x in range(len(merged)) if merged[x] == paperid] 
                merged.pop(index[0])
            csv_w(paperid, merged)
    print("Papers completed")

    end = time.time()
    total = float(end - start)
    
    print("total time: ", total)
    file2 = open("time.txt","w")
    file2.write(f'{total}')

    file2.close()
    r.close()
    db.close()

def csv_w(Ocorpus, Dcourpus):
    #oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/4WordsDuplicates.csv', mode='a') as csv_file:
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(csv_file)
        #print(Ocorpus, Dcourpus)
        colValues = []
        colValues.append(Ocorpus)
        colValues.append(len(Dcourpus))
        toAdd = ""
        duplicates = ""
        for x in Dcourpus:
            toAdd = str(x) + " "
            duplicates += toAdd
        #print("duplicates", duplicates)
        colValues.append(duplicates)
        writer.writerow(colValues)


def csv_header():
    with open('Results/4WordsDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()       
       
def keyString(key, year):
    keymatches = []
    mycursor = db.cursor()
    key_string = f'SELECT corpus_id FROM  LongWordsKeys WHERE year = "{year}" AND (key1 = "{key}" OR key2 = "{key}" OR key3 = "{key}" OR key4 = "{key}")'

    mycursor.execute(key_string)
    result = mycursor.fetchall()
    for x in result:
        for y in range(len(x)):
            keymatches.append(x[y])
    
    #print(keymatches)

    return keymatches


if __name__ == "__main__":
    main()
