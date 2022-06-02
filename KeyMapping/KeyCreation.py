"""
Program to generate based on paper 

@author: Ryan Hiltabrand, Dominik Soos
"""


# Imports
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
    # The input file has the format id, title, year
    data = csv.reader(open("./Trial.csv"))#, index_col=0)

    # skip the header of the csv file
    next(data)

    i = 0
    # loop through each row of input file
    for row in data:
        i += 1

        #print("id", row[0], "title", row[1], "year", row[2])
        print("\n\nid:", row[0] ,"original title: ", row[1])
        
        paperid = row[0]
        title = row[1].lower()
        year = row[2]

        # get all the authors as a tuple
        auth = ("SELECT name FROM authors WHERE paperid = '%s'" % (paperid))
        hawking.execute(auth)
        authors = hawking.fetchall()

        if len(authors) > 0:
            firstAuthor = str(authors[0])
        else:
            firstAuthor = None
        
        if len(authors) > 1:
            secondAuthor = str(authors[1])
        else:
            secondAuthor = None


        # could make it to a function?
        # regular expression to get only alphanumerical array of words of authors and title
        # if any of the str is alphanumerical, its returned as list
        pattern = [r'\w+']
        for p in pattern:
            match = re.findall(p, title)
            titleList = match

            if firstAuthor:
                match = re.findall(p, firstAuthor)
                # get the last name of the first author
                firstAuthor = str(match[-1])
            if secondAuthor:
                match = re.findall(p, secondAuthor)
                # get the last name of the second author
                secondAuthor = str(match[-1])

        print(firstAuthor, secondAuthor)

        
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
            chandra.execute("INSERT INTO FourWordsKey (corpus_id, key1, key2, key3, key4, year) VALUES(%s, %s, %s, %s, %s,%s)", (paperid, four_firstKey, four_secondKey, four_thirdKey, four_forthKey, year))
        else:
            chandra.execute("INSERT INTO FourWordsKey (corpus_id, key1, key2, key3, key4) VALUES(%s, %s, %s, %s, %s)", (paperid, four_firstKey, four_secondKey, four_thirdKey, four_forthKey))
        db.commit()

        if year:
            chandra.execute("INSERT INTO FiveWordsKey (corpus_id, key1, key2, key3, key4, year) VALUES(%s, %s, %s, %s, %s,%s)", (paperid, five_firstKey, five_secondKey, five_thirdKey, five_forthKey, year))
        else:
            chandra.execute("INSERT INTO FiveWordsKey (corpus_id, key1, key2, key3, key4) VALUES(%s, %s, %s, %s, %s)", (paperid, five_firstKey, five_secondKey, five_thirdKey, five_forthKey))
        db.commit()
        
    print(i)
        


def longestString(List):
    longest_string = max(List, key=len)
    return longest_string


def keyString(one, two, three,four):
    if four == None:
        key = one+'_'+two+'_'+three
        return key
    else:
        key = one+'_'+two+'_'+three+'_'+four.lower()
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
