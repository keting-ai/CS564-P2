
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Bulk-Loading Data into SQLite Databases

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

"""
Returns true if a file ends in .json
"""


def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


"""
Converts month to a number, e.g. 'Dec' to '12'
"""


def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""


def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""


def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""


def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']  # creates a Python dictionary
        # open files, if not exist, create them
        i = open('items.dat', 'a')
        c = open('categories.dat', 'a')
        b = open('bids.dat', 'a')
        u = open('users.dat', 'a')
        for item in items:
            # get Users tabel
            # get seller's id
            # UserID|Location|Country|Rating
            sellers = item['Seller']
            data = ''
            if sellers['UserID'] != None:
                data += "\"" + sub(r'\"', '\"\"', sellers["UserID"]) + "\""
            else:
                data += "NULL"
            if item['Location'] != None:
                data += columnSeparator + "\"" + \
                    sub(r'\"', '\"\"', item["Location"]) + "\""
            else:
                data += columnSeparator + "NULL"
            if item['Country'] != None:
                data += columnSeparator + "\"" + \
                    sub(r'\"', '\"\"', item["Country"]) + "\""
            else:
                data += columnSeparator + "NULL"
            if sellers['Rating'] != None:
                data += columnSeparator + sellers['Rating'] + '\n'
            else:
                data += columnSeparator + "NULL" + '\n'
            u.write(data)

            bids = item['Bids']
            data = ''
            if bids != None:
                for x in range(len(bids)):
                    bidder = bids[x]['Bid']['Bidder']
                    if bidder['UserID'] != None:
                        data += "\"" + sub(r'\"', '\"\"',
                                           bidder["UserID"]) + "\""
                    else:
                        data = '' + "NULL"
                    if 'Location' not in bidder.keys() or bidder['Location'] == None:
                        data += columnSeparator + "NULL"
                    else:
                        data += columnSeparator + "\"" + \
                            sub(r'\"', '\"\"', bidder["Location"]) + "\""
                    if 'Country' not in bidder.keys() or bidder['Country'] == None:
                        data += columnSeparator + "NULL"
                    else:
                        data += columnSeparator + "\"" + \
                            sub(r'\"', '\"\"', bidder["Country"]) + "\""
                    if bidder['Rating'] != None:
                        data += columnSeparator + bidder['Rating'] + '\n'
                    else:
                        data += columnSeparator + "NULL" + '\n'
                u.write(data)

            # get categories table
            # ItemID|Category
            data = ''
            categories = item['Category']
            items_id = item['ItemID']
            if items_id == None:
                items_id = "NULL"
            for category in categories:
                data += items_id + columnSeparator + "\"" + category + "\"" + '\n'
            c.write(data)

            # get bids table
            # ItemID|UserID|Time|Amount
            bids = item['Bids']
            data = ''
            if bids != None:
                for x in range(len(bids)):
                    if item['ItemID'] != None:
                        data += '' + item['ItemID']
                    else:
                        data = '' + "NULL"
                    bid = bids[x]['Bid']
                    if bid['Bidder']['UserID'] != None:
                        data += columnSeparator + "\"" + \
                            sub(r'\"', '\"\"', bid["Bidder"]["UserID"]) + "\""
                    else:
                        data += columnSeparator + "NULL"
                    if bid['Time'] != None:
                        data += columnSeparator + transformDttm(bid['Time'])
                    else:
                        data += columnSeparator + "NULL"
                    if bid['Amount'] != None:
                        data += columnSeparator + \
                            transformDollar(bid['Amount']) + '\n'
                    else:
                        data += columnSeparator + "NULL" + '\n'
                b.write(data)

            # get items table
            data = '' + items_id + columnSeparator + sellers['UserID']
            if item['Name'] != None:
                data += columnSeparator + "\"" + \
                    sub(r'\"', '\"\"', item["Name"]) + "\""
            else:
                data += columnSeparator + "NULL"
            if item['Currently'] != None:
                data += columnSeparator + transformDollar(item['Currently'])
            else:
                data += columnSeparator + "NULL"
            if item['First_Bid'] != None:
                data += columnSeparator + transformDollar(item['First_Bid'])
            else:
                data += columnSeparator + "NULL"
            if item['Number_of_Bids'] != None:
                data += columnSeparator + item['Number_of_Bids']
            else:
                data += columnSeparator + "NULL"
            if item['Started'] != None:
                data += columnSeparator + transformDttm(item['Started'])
            else:
                data += columnSeparator + "NULL"
            if item['Ends'] != None:
                data += columnSeparator + transformDttm(item['Ends'])
            else:
                data += columnSeparator + "NULL"
            if 'Buy_Price' not in item.keys():
                data += columnSeparator + "NULL"
            else:
                data += columnSeparator + transformDollar(item['Buy_Price'])
            if item['Description'] != None:
                data += columnSeparator + \
                    "\"" + sub(r'\"', '\"\"',
                               item["Description"]) + "\"" + '\n'
            else:
                data += columnSeparator + "NULL" + '\n'
            i.write(data)
        i.close()
        u.close()
        c.close()
        b.close()


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""


def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)


if __name__ == '__main__':
    main(sys.argv)
