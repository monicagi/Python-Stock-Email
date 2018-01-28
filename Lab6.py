"""Name: Monica Guevara
    Class: CSC 4800
    Assignment: Lab #4
    Date: 2/15/17
"""
import re
import urllib.request
import sys

def get_file():
    """The get_file function asks the user to enter a file name for reading and checks if it exists
       Then it calls the read_file function passing the file as an argument"""

    file_name = input("Enter filename: ")

    #Checks to see if the file exists
    try:
        file = open(file_name, 'r')
    except IOError:
        print("Unable to open file")
    else:
        print("Reading from file '%s'" %(file_name))

        read_file(file)

def read_file(file):
    """The read_file function accepts a file as a parameter and then reads in the stock symbols from the
        file and stores them in the stock list"""
    i = 0
    j = 0
    stocks = []
    sym = '&s='

    for line in file:
        line = line.strip()
        stocks.append(line)

    file.close()

    while i < len(stocks):
        sym = '&s='

        if (i == len(stocks)-1):
            sym = sym + stocks[i]
            i = i + 1

        else:
            while(j < 5):
                if(j == 0):
                    sym = sym + stocks[i]
                else:
                    sym = sym + '+' + stocks[i]

                j = j + 1

                i = i + 1
        j = 0
        Process_Quotes(sym)

def Process_Quotes(strSyms):
    """The Process_Quotes accepts the stock symbol as a parameter and then appends it to the URL and then sends it
        to Yahoo Finance and it recevies a line with information on the stock. Then it calls the Find_Info
        function passing the line as an argument"""

    strUrl = 'http://finance.yahoo.com/d/quotes.csv?f=sd1t1l1bawmc1vj2&e=.csv'
    strUrl = strUrl + strSyms

    try:
        f = urllib.request.urlopen(strUrl)

    except:
        print("URL Access Failed:\n" + strUrl + "\n")
        return

    for line in f.readlines():
        line = line.decode().strip()
        Find_Info(line)

#info is a global variable that will store the information returned by Yahoo Finance
info = ""
def Find_Info(line):
    """The Find_Info Function accepts the line as a parameter and then it looks for information such as the symbol,
        time, and date and numbers related to the stock using regular expressions. It also creates a file to store
        the stock information. The output is directed to the file instead of the console"""

    global info

    info = info + line + "\n"

    filex = '2017-02-15 stockquotes.xml'
    sys.stdout = open(filex, "a")

    #Looks for the stock symbol
    symb = re.match(r'"(.*?)"', line)

    # If it did not find a symb then it returns No Match because the stock may not exist
    if symb is None:
        return print("Unknown Symbol: No Match\n\n")

    #Looks for the date
    date = re.match(r'".+?(\d+/\d+/\d+)"', line)

    #If it did not find a date then it returns No Match because the stock may not exist
    if date is None:
        return print("Unknown Symbol: No Match\n\n")

    #Looks for the time
    time = re.match(r'".+?(\d+:\d+[a-z]{2})"', line)

    #If there any N/A in the line they are replaced or substituted with -0.00
    l = re.sub('N/A', '-0.00', line)

    #This looks for all the numbers in the modified line ignoring the date and time using findall which stores them in
    # a list
    nums = re.findall(r'["|,|\- ]([+-]?\d+(?!/|:)[\.]?[\d+]*)', l)

    titles = ['LastSalePrice', 'BidPrice', 'AskPrice', '52WeekLow', '52WeekHigh', 'TodaysLow', 'TodaysHigh',
                'NetChangePrice', 'ShareVolumeQty', 'TotalOutstandingSharesQty']

    i = 0
    j = 0

    print("<stockquote>")
    print("\t<qSymbol>%s</qSymbol>" %(symb.group(1)))
    print("\t<qDate>%s</qDate>" %(date.group(1)))
    print("\t<qTime>%s</qTime>" %(time.group(1)))

    #This while loop prints the information from the stock ignoring the (-0.00) that was used to replace N/A
    while (i < len(nums)):

        if(i == 3):
            if(nums[i] == '-0.00'):
                i = i +1
                j = j + 2

        if(i == 5):
            if (nums[i] == '-0.00'):
                i = i + 1
                j = j + 2

        if(nums[i] != '-0.00'):
            print("\t<q%s>%s</q%s>" %(titles[j], nums[i], titles[j]))

        i = i+1
        j = j+1

    print("</stockQuote>")

    sys.stdout.close()
    sys.stdout = sys.__stdout__
