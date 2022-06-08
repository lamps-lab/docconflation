import sys
import datetime
import re
import MySQLdb as sql
import csv
import time

import config

conn=sql.connect(host = config.chandrah, user = config.chandrau, passwd = config.chandrap, db = config.chandradb, charset = "utf8")

def main():
    csv_header()

    chandra = conn.cursor()
    start = time.process_time()

    infile = csv.reader(open("../Trial.csv"))
    next(infile)
    
    cases = []
    for row in infile:
        cases.append(row[0])
    
    # cases holds the id numbers to test
    print("all of cases: ", len(cases))
    for i in cases:
        print(i)
        query = f"SELECT corpus_id, key1, key2, key3, key4, year FROM  LongWordsKey WHERE corpus_id = \"{i}\""
        chandra.execute(query)
        
        current =  chandra.fetchone()
        print(current)
        paperid = current[0]
        key1 = current[1]
        key2 = current[2]
        key3 = current[3]
        key4 = current[4]
        year = current[5]

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
        print("unique ids", merged,"\n\n")
        
        # if the cluster has more than one unique id's it is a near duplicate
        if len(merged) > 1:
            csv_w(paperid, merged)

    chandra.close()
    conn.close()
    end = time.process_time()
    total = float(start) - end
    print("total time: ", total)
    file2 = open("time3.txt","w")
    file2.write(f'{total}')
    file2.close()


               
def csv_w(Ocorpus, Dcourpus):
    #oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/4WordsDuplicates.csv', mode='a') as csv_file:
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(csv_file)
        print(Ocorpus, Dcourpus)
        colValues = []
        colValues.append(Ocorpus)
        colValues.append(len(Dcourpus))
        colValues.append(str(Dcourpus))
        writer.writerow(colValues)
        
def csv_header():
    with open('Results/4WordsDuplicates.csv', mode='w') as csv_file:
        fieldNames = ['Corpus' , 'Amount' , 'Duplicates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()       
       
def keyString(key, year):
    keymatches = []
    mycursor = conn.cursor()
    key_string = f'SELECT corpus_id FROM  LongWordsKey WHERE year = "{year}" AND (key1 = "{key}" OR key2 = "{key}" OR key3 = "{key}" OR key4 = "{key}")'

    mycursor.execute(key_string)
    result = mycursor.fetchall()
    for x in result:
        for y in range(len(x)):
            keymatches.append(x[y])
    
    print(keymatches)

    return keymatches


if __name__ == "__main__":
    main()
