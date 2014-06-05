#!/usr/bin/python2.7

# Unittest run if file is run without any cmd line input
# Result  displayed in case of a valid file is supplied as in input
# Required files 'test_share_data.csv' and 'badcsvfile' must be located in the same directory


# In case of any missing value for any column, the available values are considered and result is formed
# based on available values

# Last relevant Month/Year is considered in case of multiple highest share price

import csv
import sys

class BadInputFile(Exception):
    """Exception class for bad file type"""
    
    def __init__(self,filename):
        self.filename = filename

    def __str__(self):
        return "Bad input file: '{}'".format(self.filename)



def ParseData(filename):
    '''
        Funtion responsible for:
         1) Exception handle while opening the file
         2) Printing the required output
    '''
    actualResult = {}
    try:
        fh = open(filename,'r')
        reader = csv.DictReader(fh) #Try and open the file with csv dictreader

        #Get the field names in the file: Will help verify if fields needed are there or not
        fields = set(reader.fieldnames)
        if not fields or ('Year' not in fields and 
                'Month' not in fields):
            raise BadInputFile(filename)
        companies = fields - {'Year', 'Month'}
        for name in companies:
            #sorting the csv file data based on column data with Company Name as Key
            result = sorted(reader, key=lambda d: float(d[name]), reverse=True)
            result = result[0]
            tup = (result[name],result['Year'],result['Month'])
            actualResult.update({str(name): tup})
            fh.seek(0) #rewinding the file to initial position
            fh.next()  #Moving to the 1st row
    except (IOError, BadInputFile) as e:
        print "Error: ", str(e) # Invalid input file
        raise


    return actualResult


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print "No input file given. Run unit test\n"
        unittest.main()
    else:
        print "Parsing the CSV file"
        result = ParseData(filename)
        print result

# Since the exact environment of the script testing is unknown, testing
# code has been included within the same file so as to provide seamless
# testing

# Tests run incase of no file is provided as input

import unittest

class TestPraseData(unittest.TestCase):

    def setUp(self):
    # Expected output for the declared file
        expectedData ={
                        'Company-E': ('997', '2008', 'Oct'),
                        'Company-D': ('999', '2002', 'Apr'),
                        'Company-C': ('995', '1993', 'Jun'),
                        'Company-B': ('986', '2007', 'Mar'),
                        'Company-A': ('1000', '2000', 'Mar')
                      }

    def Check_Output(self):
        '''Check the output'''
        Data = ParseData('test_share_data.csv')
        self.assertEqual(self.exectedData, Data)


    def Check_IoError(self):
        '''check for IoError'''
        with self.assertRaises(IOError):
            ParseData('Non-ExistingFile')

    def Check_If_BadInputFile(self):
        '''Check for BadInputFile -- File with not poper fields'''
        with self.assertRaise(BadInputFile):
            ParseData('BadCsvFile')


if __name__ == '__main__':
    main()
