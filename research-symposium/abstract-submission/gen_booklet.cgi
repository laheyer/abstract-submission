#!/usr/bin/python

'''
write_latex_booklet.py

usage: python write_latex_booklet.py <path-to-parent-directory>

This script was created for the Davidson College Math and Science Research
Symposium.
It processes submitted abstracts to generate an abstract booklet
and list of authors.
It uses all files in the given directory and subdirectories.

Author: S.T. Castle
Created: 20 Apr 2015
'''

# Imports for html cgi docs.
#import cgi
#import cgitb
#cgitb.enable()

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
            # Move on to the next file if current is not an abstract file.
            if f[-13:] != '_abstract.tex':
                continue
            f = os.path.join(root, f)    # Full path.

            # This is the crucial step to get dept code based on arbitrary
            # but specified directory structure.
            deptcode = root.split('/')[-2].lower()
            if deptcode != currdept:  # Changed to next department.
                # Start next dept.
                output.append(get_dept_header(deptcode))
                currdept = deptcode

            # Now, get the abstract text from this file.
            output.append(get_text_from_file(f))
    
    # Finished extracting data from files.
    # Write the output to the new file.
    with open (output_file, 'w'):
        output_file.writelines(output)

def get_text_from_file(path):
    '''
    Return a list of lines which are the desired text from the given file.
    This will collect the title, author, and abstract text from the abstract
    file. That is, everything between the LaTeX commands ``\begin{document}''
    and ``\end{document}''
    '''
    # Save the text as a list of lines.
    text = []
    # Open the file and store every line with the LaTeX document environment.
    with open(path, 'r') as f:

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
    except KeyError as e:
        print 'Error: Incorrect department code or incorrect file structure.',
        print 'Files should be in a directory as follows:'
        print '/some_path/mat/castle_sam/castle_sam_abstract.tex'
        print 'for Sam Castle\'s abstract in the Math department.'

    # Return the LaTeX code to write the section header for the new department.
    return ('''
    % ------------------------- New department. -------------------------\n
    \\begin{departmentheading}\n''' +
    deptname +
    '''
    \end{departmentheading}\n
    % -------------------------------------------------------------------\n
    ''')

if __name__ == '__main__':
    main()
