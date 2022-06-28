import os
import csv

def main():
    
    with open("groundTruth.csv", "r") as gt, open("groundTruthAfter.csv", "w") as out:

        reader = csv.reader(gt, delimiter = ',')
        writer = csv.writer(out, delimiter = ',')
        
        header = next(reader)
        writer.writerow(header)

        for row in reader:
            #print("Corpus: ", row[0], "Amount: ", row[1], "Duplicates", row[2])
            duplicate_list = row[2].split(" ")
            colValues = []
            for col in row:
                if col == row[2]:
                    col = duplicate_list
                    col.append(row[0])
                if col == row[1]:
                    col = str(int(row[1]) + 1)
                colValues.append(col)
            writer.writerow(colValues)

    gt.close()
    out.close()



if __name__ == "__main__":
    main()
