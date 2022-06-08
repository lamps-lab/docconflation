import os
import csv

def main():
    
    with open("GT.csv", "r") as gt, open("groundTruth.csv", "w") as out:

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
                colValues.append(col)
            writer.writerow(colValues)

    gt.close()
    out.close()



if __name__ == "__main__":
    main()
