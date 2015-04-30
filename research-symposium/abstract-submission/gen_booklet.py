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

    # Create a list of lines, output, that will store all lines to be written to
    # the final LaTeX file used to generate the booklet.
    # Initialize the output first with the contents of the LaTeX preamble.
    output = []
    preamble = 'test-booklet/preamble.tex'
    with open(preamble, 'r') as f:
        output.append(f.readlines())

    # Walk through every file in parent directory and any subdirectories.
    # !!!Important!!! Finding the department name in this loop relies heavily on
    # the specific file structure created during the abstract submission
    # process. For example, Sam Castle's math abstract will be located in 
    # /some_path/mat/castle_sam/castle_sam_abstract.tex
    for root, dirs, files in os.walk(parent, topdown=False):
        currdept = ''  # The current department being processed.
        for f in files:
            if f[-3:] == 'tex':  # Only process tex files.
                print 'Orig path:',
                print f
                f = os.path.join(root, f)    # Full path.
                # This is the crucial step to get dept code based on arbitrary
                # but specified directory structure.
                deptcode = root.split('/')[-2].lower()
                if deptcode != currdept:  # Changed to next department.
                    # End previous department.

                    # Start next dept.
                    output.append(get_dept_header(deptcode))
                    currdept = deptcode
                #get_data_from_file(f, data)  # Add data from current file.
                #print f
                print 'Full path:',
                print f
                print 'root:',
                print root
                print 'dirs:',
                print dirs
                print
                print '------'
                print
    
    # Finished extracting data from files.
    # Sort data within each department.
    #custom_sort(data)
    #print data

def get_dept_header(code):
    '''
    Given the three-letter department code, return the LaTeX code as a string
    that will write the department name as a section header and set up the new
    department's section in the master LaTeX document.
    '''
    # Map the department codes used in directory names to their full names.
    dept = {
            'bio': 'Biology',
            'che': 'Chemistry',
            'env': 'Environmental Studies',
            'mat': 'Mathematics and Computer Science',
            'phy': 'Physics',
            'psy': 'Psychology'
           }

    # Get department name, and make sure department code is valid.
    try:
        deptname = dept[code]
    except KeyError e:
        print 'Error: Incorrect department code or incorrect file structure.',
        print 'Files should be in a directory as follows:'
        print '/some_path/mat/castle_sam/castle_sam_abstract.tex'
        print 'for Sam Castle\'s abstract in the Math department.'
        print "Key error({0}): {1}".format(e.errno, e.strerror)

    # Return the LaTeX code to write the section header for the new department.
    return ('''
    %---- new dept
    %\\begin{department}  % ''' + deptname + '''
    ''')
   

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
        s = first + ', ' + ', '.join(second[:-1])
        s = s + ', and ' + second[-1]
        return s

if __name__ == '__main__':
    main()
