import os
import csv

def main():
    
    with open("GT.csv", "r") as gt, open("groundTruth.csv", "w") as out:

        reader = csv.reader(gt)
        writer = csv.writer(out)
        
        header = next(reader)
        writer.writerow(header)

        for row in reader:
            #print("Corpus: ", row[0], "Amount: ", row[1], "Duplicates", row[2])
            duplicate_list = row[2].split(" ")
            if row[0] in duplicate_list:
                index = [x for x in range(len(duplicate_list)) if duplicate_list[x] == row[0]] 
                duplicate_list.pop(index[0])

            colValues = []

            # loop through the columns in the row
            for col in row:
                # if it is the amount column
                if col == row[1]:
                    col = len(duplicate_list)
                # if it is the duplicates column
                if col == row[2]:
                    toAdd = ""
                    duplicates = ""
                    for x in duplicate_list:
                        if duplicate_list[-1] == x:
                            toAdd = str(x)
                        else:
                            toAdd = str(x) + " "
                        duplicates += toAdd
                    col = duplicates
                    
                colValues.append(col)
            writer.writerow(colValues)

    gt.close()
    out.close()



if __name__ == "__main__":
    main()
