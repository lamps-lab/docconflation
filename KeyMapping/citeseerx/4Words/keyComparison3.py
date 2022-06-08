import sys
import datetime
import re
import MySQLdb as sql
import csv
import time

db=sql.connect(host = "chandra.cs.odu.edu", user = "domsoos", passwd = "FriMay64:01:22PM", db = "s2orc_2020", charset = "utf8")

def main(count):
    csv_header()
    r = db.cursor()
    start = time.process_time()

    cases = []
    #File = open(f'../../test.txt', 'r')
    File = open(f'../../known.txt', 'r')
    
    for row in File:
        nrow = row.replace('\n','')
        cases.append(nrow)
    
    # cases holds the id numbers

    for i in cases:
        cur = f"SELECT database_id, corpus_id, key1, key2, key3, key4, year FROM  LongWordsKeys WHERE corpus_id = {i}"
        r.execute(cur)
        ct = datetime.datetime.now()
        current =  r.fetchone()
        print(current)
        databaseid = current[0]
        paperid = current[1]
        key1 = current[2]
        key2 = current[3]
        key3 = current[4]
        key4 = current[5]
        year = current[6]

        print("Key1",key1, "Key2", key2, "Key3", key3, "Key4", key4)

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
        if len(merged) > 1:
            csv_w(paperid, merged)
        #print("i", i)
        end = time.process_time()
        
        file2 = open("time3.txt","a")
        file2.write(f'{start-end}')


        """
        Algorithm for precision and recall
        # init
        tp = 0
        tn = 0
        fp = 0
        fn = 0

        # algorithm to calculate recall and precision based on ground truth
        prediction = open(f'', 'r')
        truth = open(f'', 'r')

        # loop through each paper in predictions
        for paper in prediction:
            # true positive if paper both in prediction and truth
            if paper in truth:
                tp += 1
            # if the paper is not in truth but in prediction it is a false positive
            else:
                fp += 1

        for paper in truth:
            # if the paper is in the groundt truth but not in prediction then it is a false negative
            if paper not in prediction:
                fn += 1

        recall = tp / (tp + fn)
        precision = tp / (tp + fp)
        f1 = (2 * precision * recall) / (precision + recall)
        """

               
def csv_w(Ocorpus, Dcourpus):
    #oringinal_corpus = Ocorpus.replace('/n', '')
    with open('Results/4WordsTrueDuplicates.csv', mode='a') as csv_file:
        fieldNames = ['Corpus', 'Amount' , 'Duplicates']
        #writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        row = f'[{str(int(Ocorpus))}], [{str(len(Dcourpus))}], [{str(Dcourpus)}]'
        writer.writerow({'Corpus': f'{str(int(Ocorpus))}', 'Amount': f'{str(len(Dcourpus))}', 'Duplicates': f'{str(Dcourpus)}'})
        #writer.writerow(f'{row}')
        #print("row", row)
        
def csv_header():
    with open('Results/TrueDuplicates.csv', mode='w') as csv_file:
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
    
    print(keymatches)

    ct = datetime.datetime.now()
    print(ct)

    return keymatches
    

'''def insert(item_list, key, value): 
    item_list.append((key, value))
 
def search(item_list, key):
    for item in item_list:
        if item[0] == key:
            return item[1]'''



if __name__ == "__main__":
    for count in range(20):
        print("new main\n\n")
        main(count)