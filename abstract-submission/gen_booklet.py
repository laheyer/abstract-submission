#!/usr/bin/python

'''
gen_booklet.py

usage: python gen_booklet.py <path-to-parent-directory>

This script was created for the Davidson College Math and Science Research
Symposium.
It processes submitted abstracts to generate an abstract booklet
and list of authors.
It uses all files in the given directory and subdirectories.

Author: S.T. Castle
Created: 20 Apr 2015
'''

# Imports for html cgi docs.
import cgi
import cgitb
cgitb.enable()

import os
import sys

def main():
    # Get path to parent directory for files.
    if len(sys.argv) > 1: # If user specified directory as argument.
        parent = sys.argv[1]
    else:
        sys.exit('usage: python gen_booklet.py <path-to-parent-directory>')
        #print 'Enter the full or relative path to the parent'
        #print 'directory for all abstract files:'
        #parent = raw_input('> ')
    parent = os.path.abspath(parent) # Convert to absolute path.

    #print parent

    # Abort if parent directory path does not exist.
    if not os.path.exists(parent):
        sys.exit('ERROR: Directory '+parent+' does not exist. Process aborted.')

    # Dictionary of lists to store all data.
    # A top-level dictionary of departments maps to lists
    # containing data for each submission.
    data = {
            'MAT': [],
            'PHY': [],
            'BIO': [],
            'CHE': []
           }

    # Walk through every file in parent directory and any subdirectories.
    for root, dirs, files in os.walk(parent, topdown=False):
        for f in files:
            if f[-3:] == 'txt':  # Only process text files.
                f = os.path.join(root, f)    # Full path.
                get_data_from_file(f, data)  # Add data from current file.
                #print f
    
    # Finished extracting data from files.
    # Sort data within each department.
    custom_sort(data)
    #print data

def custom_sort(data):
    '''Sorts the dataset within each department, using alphabetical
    order based on the author list.
    Takes as a parameter the dataset to be sorted.
    ''' 
    # Loop through each department in the data dictionary.
    for dept in data.keys():
        # data[dept] is a list of 3-tuples.
        # Sort by the first element (author) in the 3-tuple.
        data[dept] = sorted(data[dept], key=lambda x: x[0])

def get_data_from_file(filename, data):
    '''Get the necessary data from the file and add it to the data set.
    The input file should have the following format:
    "
    department
    title
    primary author
    secondary authors, separated by semicolons
    abstract text
    "

    If file's first line is not a valid department code or the file
    does not contain at least 5 lines, an exception is thrown, an error
    message is printed to stdout, and no change is made to the dataset.

    Takes the following parameters:
    filename: the absolute path to the file containing data.
    data: the dataset to update.
    '''
    try:
        #print 'Opening '+filename
        # Open the file.
        with open(filename, 'r') as f:
            lines = f.readlines()
            # First, extract header data from file.
            dept = lines[0].strip() # Grab the next line and strip newline.
            # Skip this file if first line is not an expected department code.
            if dept not in data.keys():
                return
            title = lines[1].strip()
            author = lines[2].strip()
            # Get list of possible second authors.
            second_author = [s.strip() for s in lines[3].split(';')]
            second_author = filter(None, second_author)  # Remove empty strings.
            text = lines[4:]
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print 'Error reading '+filename
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print 'Error reading'+filename

    # Now store the data from this file as a 3-tuple
    # of (author, title, text).
    comb_author = combine_authors(author, second_author)
    data[dept].append((comb_author, title, text))

def combine_authors(first, second):
    '''Return a string containing the authors in format
    "Author 1, Author 2, ..., and Author n".
    Takes the following parameters:
    first: the name of the first author.
    second: a list of all remaining authors. May be size 0 to n-1,
            for n authors.
    '''
    if len(second) == 0:  # If no second authors.
        return first
    elif len(second) == 1:
        return first+' and '+second[0]
    else:
        s = first + ', ' + ','.join(second[:-1])
        s = s + ', and ' + second[-1]
        return s

if __name__ == '__main__':
    main()
