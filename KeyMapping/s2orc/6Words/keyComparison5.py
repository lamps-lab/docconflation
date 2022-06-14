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
        #ct = datetime.datetime.now()

        cur = f"SELECT database_id, corpus_id, key1, key2, key3, key4, year FROM  FiveWordsKey WHERE corpus_id = {i}"
        r.execute(cur)
        
        current =  r.fetchone()
        #print(current)
        #databaseid = current[0]
        paperid = current[1]
        key1 = current[2]
        key2 = current[3]
        key3 = current[4]
        key4 = current[5]
        year = current[6]

        #print("Key1",key1, "Key2", key2, "Key3", key3, "Key4", key4)

        #print("current time:-", ct)
        
        first_key = keyString(key1, year)
        #print(first_key)   
        second_key = keyString(key2, year) 
        #print(second_key)
        third_key = keyString(key3, year)
        #print(third_key)
        forth_key = keyString(key4, year)
        #print(forth_key)

        merged = list(set(first_key + second_key + third_key + forth_key))
        #print("unique ids", merged,"\n\n")
        
        # if the cluster has more than one unique id's it is a near duplicate
        if len(merged) > 1:
            csv_w(paperid, merged)
    print("Papers completed")

    end = time.time()
    total = float(end - start)
    
    print("total time: ", total)
    file2 = open("time3.txt","w")
    file2.write(f'{total}')
    file2.close()
    r.close()
    db.close()


               
def csv_w(Ocorpus, Dcourpus):
    #oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/6WordsDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        #row = f'[{str(int(Ocorpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(Ocorpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        
def csv_header():
    with open('Results/6WordsDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()       
       
def keyString(key, year):
    keymatches = []
    mycursor = db.cursor()
    key_string = f'SELECT corpus_id FROM  FiveWordsKey WHERE year = "{year}" AND (key1 = "{key}" OR key2 = "{key}" OR key3 = "{key}" OR key4 = "{key}")'

    mycursor.execute(key_string)
    result = mycursor.fetchall()
    for x in result:
        for y in range(len(x)):
            keymatches.append(x[y])
    
    #print(keymatches)

    return keymatches


if __name__ == "__main__":
    main()
