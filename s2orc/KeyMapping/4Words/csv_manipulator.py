import os
import csv
import re

def main():
    
    with open("Results/o4WordsTrueDuplicates.csv", "r") as input, open("TrueDuplicates.csv", "w") as out:

        reader = csv.reader(input, delimiter = ',')
        writer = csv.writer(out, delimiter = ',')
        
        header = next(reader)
        writer.writerow(header)

        for row in reader:
            #print("Corpus: ", row[0], "Amount: ", row[1], "Duplicates", row[2])
            duplicate_list = row[2].split(",")
            colValues = []

            for col in row:
                # if it is the duplicate column
                if col == row[2]:
                    pattern = [r'\w+']
                    for p in pattern:
                        match = re.findall(p, col)
                        duplicate_list = match
                    toAdd = ""
                    duplicates = ""
                    for x in duplicate_list:
                        if duplicate_list[-1] == x:
                            toAdd = x
                        else:
                            toAdd = x + " "
                        duplicates += toAdd
                    col = duplicates
                    #print(col)

                # Amount column
                if col == row[1]:
                    col = str(int(row[1]))
                colValues.append(col)
            print(colValues)
            writer.writerow(colValues)


        
        
        #print("duplicates", duplicates)
        colValues.append(duplicates)
        writer.writerow(colValues)
    input.close()
    out.close()



if __name__ == "__main__":
    main()
