"""
KeyGeneration for Research paper

@authors: Ryan Hiltabrand, Dominik Soos
"""

import sys, csv, xlrd, re
import MySQLdb as sql

import config


def main():

    # Add the proper connection information depending on the server you are on
    db = sql.connect(
        host = config.hawkingh,
        user = config.hawkingu,
        passwd = config.hawkingp,
        db = config.hawkingdb,
        charset = "utf8"
    )
    hawking = db.cursor()

    db = sql.connect(
        host = config.chandrah,
        user = config.chandrau,
        passwd = config.chandrap,
        db = config.chandradb,
        charset = "utf8"
    )
    chandra = db.cursor()

    # init
    first = ''
    second = ''
    third = ''
    forth = ''
    fifth = ''
    sixth = ''

    # Getting the input file from Trial.csv that we retrieved from citeseerx database
    # In: Trial.csv has the format id, title, year
    data = csv.reader(open("./Trial.csv"))#, index_col=0)

    # skip the header of the csv file
    next(data)

    # loop through each row of input file
    for row in data:

        #print("id", row[0], "title", row[1], "year", row[2])
        print("\n\nid:", row[0] ,"original title: ", row[1])
        
        paperid = row[0]
        title = row[1].lower()
        year = row[2]

        # get all the authors as a tuple
        auth = ("SELECT name FROM authors WHERE paperid = '%s'" % (paperid))
        hawking.execute(auth)
        authors = hawking.fetchall()


        # if there are greater than zero authors, get the first author
        if len(authors) > 0:
            # get the first order author for the paper and turn it in to a string
            query = ("SELECT name FROM authors WHERE paperid = '%s' AND ord = 1" % (paperid))
            hawking.execute(query)
            firstAuthor = str(hawking.fetchone())
            print(firstAuthor)

            # if there are more than one authors, get the second one
            if len(authors) > 1:
                query = ("SELECT name FROM authors WHERE paperid = '%s' AND ord = 2" % (paperid))
                hawking.execute(query)
                secondAuthor = str(hawking.fetchone())
                print(secondAuthor)
            else:
                secondAuthor = None
        else:
            firstAuthor = None
            secondAuthor = None


        # could make it to a function?
        # regular expression to get only alphanumerical array of words of authors and title
        # if any of the str is alphanumerical, its returned as list
        pattern = [r'\w+']
        for p in pattern:
            match = re.findall(p, title)
            titleList = match

            # get the last name of the first author if exist
            if firstAuthor:
                match = re.findall(p, firstAuthor)
                firstAuthor = str(match[-1]).lower()

            # get the last name of the second author if exist
            if secondAuthor:
                match = re.findall(p, secondAuthor)
                secondAuthor = str(match[-1]).lower()

        #print(firstAuthor, secondAuthor)

        
        if len(titleList) > 5:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = longestString(titleList)
            titleList.remove(forth)
            fifth = longestString(titleList)
            titleList.remove(fifth)
            sixth = longestString(titleList)
            titleList.remove(sixth)

        elif len(titleList) > 4:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = longestString(titleList)
            titleList.remove(forth)
            fifth = longestString(titleList)
            titleList.remove(fifth)
            sixth = ''
            
        elif len(titleList) > 3:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = longestString(titleList)
            titleList.remove(forth)
            fifth = ''
            sixth = ''

        elif len(titleList) > 2:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = longestString(titleList)
            titleList.remove(third)
            forth = ''
            fifth = ''
            sixth = ''

        elif len(titleList) > 1:
            first = longestString(titleList)
            titleList.remove(first)
            second = longestString(titleList)
            titleList.remove(second)
            third = ''
            forth = ''

        elif len(titleList) == 1:
            first = longestString(titleList)
            titleList.remove(first)
            second = ''
            third = ''
            forth = ''
            fifth = ''
            sixth = ''

        else:
            first = ''
            second = ''
            third = ''
            forth = ''
            fifth = ''
            sixth = ''

        three_firstKey = ThreekeyString(first, second, third, firstAuthor)
        three_secondKey = ThreekeyString(second, third, forth, firstAuthor)
        three_thirdKey = ThreekeyString(first, second, third, secondAuthor)
        three_forthKey = ThreekeyString(second, third, forth, secondAuthor)

        print()
        print("Three\nfirst: ", three_firstKey, "\nsecond:", three_secondKey, "\nthird:", three_thirdKey, "\nfourth:", three_forthKey)

        four_firstKey = FourkeyString(first, second, third, forth, firstAuthor)
        four_secondKey = FourkeyString(second, third, forth, fifth, firstAuthor)
        four_thirdKey = FourkeyString(first, second, third, forth, secondAuthor)
        four_forthKey = FourkeyString(second, third, forth, fifth, secondAuthor)

        print()
        print("Four\n first:", four_firstKey, "\nsecond:", four_secondKey, "\nthird:", four_thirdKey, "\nfourth:", four_forthKey)
        

        five_firstKey = FivekeyString(first, second, third, forth, fifth, firstAuthor)
        five_secondKey = FivekeyString(second, third, forth, fifth, sixth, firstAuthor)
        five_thirdKey = FivekeyString(first, second, third, forth, fifth, secondAuthor)
        five_forthKey = FivekeyString(second, third, forth, fifth, sixth, secondAuthor)


        print("\nFive\n first:", five_firstKey, "\nsecond:", five_secondKey, "\nthird:", five_thirdKey, "\nfourth:", five_forthKey)
        print()
        print()

        if year:
            chandra.execute("INSERT INTO LongWordsKey (corpus_id, key1, key2, key3, key4, year) VALUES(%s, %s, %s, %s, %s, %s)", (paperid, three_firstKey, three_secondKey, three_thirdKey, three_forthKey, year))
            #db.commit()
            chandra.execute("INSERT INTO FourWordsKey (corpus_id, key1, key2, key3, key4, year) VALUES(%s, %s, %s, %s, %s,%s)", (paperid, four_firstKey, four_secondKey, four_thirdKey, four_forthKey, year))
            #db.commit()
            chandra.execute("INSERT INTO FiveWordsKey (corpus_id, key1, key2, key3, key4, year) VALUES(%s, %s, %s, %s, %s,%s)", (paperid, five_firstKey, five_secondKey, five_thirdKey, five_forthKey, year))
            #db.commit()
        else:
            chandra.execute("INSERT INTO LongWordsKey (corpus_id, key1, key2, key3, key4) VALUES(%s, %s, %s, %s, %s)", (paperid, three_firstKey, three_secondKey, three_thirdKey, three_forthKey))
            #db.commit()
            chandra.execute("INSERT INTO FourWordsKey (corpus_id, key1, key2, key3, key4) VALUES(%s, %s, %s, %s, %s)", (paperid, four_firstKey, four_secondKey, four_thirdKey, four_forthKey))
            #db.commit()
            chandra.execute("INSERT INTO FiveWordsKey (corpus_id, key1, key2, key3, key4) VALUES(%s, %s, %s, %s, %s)", (paperid, five_firstKey, five_secondKey, five_thirdKey, five_forthKey))
            #db.commit()
    # end for row in data
    
    # Reports
    chandra.execute("SELECT count(*) FROM LongWordsKey")
    totalThree = int(chandra.fetchone())
    print("Total number in LongWordsKey: ", totalThree)

    chandra.execute("SELECT count(*) FROM FourWordsKey")
    totalFour = int(chandra.fetchone())
    print("Total number in FourWordsKey: ", totalFour)

    chandra.execute("SELECT count(*) FROM FiveWordsKey")
    totalFive = int(chandra.fetchone())
    print("Total number in LongWordsKey: ", totalFive)

    hawking.close()
    chandra.close()
    db.close()
#end main


def longestString(List):
    longest_string = max(List, key=len)
    return longest_string

def ThreekeyString(one, two, three, author):
    if author == None:
        key = one+'_'+two+'_'+three
        return key
    else:
        key = one+'_'+two+'_'+three+'_'+author
        return key
    
def FourkeyString(one, two, three, four, author):
    if author == None:
        key = one+'_'+two+'_'+three+'_'+four
        return key
    else:
        key = one+'_'+two+'_'+three+'_'+four+'_'+author
        return key

def FivekeyString(one, two, three, four, five, author):
    if author == None:
        key = one+'_'+two+'_'+three+'_'+four+'_'+five
        return key
    else:
        key = one+'_'+two+'_'+three+'_'+four+'_'+five+'_'+author
        return key

def firstA(authors):
    author = authors.strip()
    author = author.lower()
    if ',' in author:
        author = author.replace(',', " , ")
        aList = author.split()
        pos = aList.index(',')
        return aList[pos-1]
    elif author == '':
        return None
    else:
        aList = authors.split()
        return aList[-1]
            
def last(authors):
    authors = authors.strip()
    authors = authors.lower()
    if authors == '':
        return None
    else:
        author = authors.split()
        return author[-1]

def keyCreator(title1, title2, title3, author):
    key = [title1, title2, title3, author]
    return key

if __name__ == "__main__":

    main()
