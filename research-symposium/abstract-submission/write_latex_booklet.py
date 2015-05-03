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

def write_booklet():

    output_file = 'master_output.tex'
    preamble_file = 'preamble.tex'

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
    with open(preamble_file, 'r') as f:
        output += f.readlines()
    output.append('\n')
    output.append('% ----------------- End of preamble file -----------------\n')
    output.append('\n')

    # Walk through every file in parent directory and any subdirectories.
    # !!!Important!!! Finding the department name in this loop relies heavily on
    # the specific file structure created during the abstract submission
    # process. For example, Sam Castle's math abstract will be located in 
    # /some_path/mat/castle_sam/castle_sam_abstract.tex
    currdept = ''  # The current department being processed.
    for root, dirs, files in os.walk(parent, topdown=False):
        for f in files:
            # Move on to the next file if current is not an abstract file.
            # First character '.' represents a hidden file.
            if f[0] == '.' or f[-13:] != '_abstract.tex':
                continue
            f = os.path.join(root, f)    # Full path.

            # This is the crucial step to get dept code based on arbitrary
            # but specified directory structure.
            deptcode = root.split('/')[-2].lower()
            if deptcode != currdept:  # Changed to next department.
                # Start next dept.
                output += get_dept_header(deptcode)
                currdept = deptcode

            # Now, get the abstract text from this file.
            output += get_text_from_file(f)

    # Conclude the master booklet file.
    output.append('\\end{document}')
    
    # Finished extracting data from files.
    # Write the output to the new file.
    with open (output_file, 'w') as f:
        f.writelines(output)

def get_text_from_file(path):
    '''
    Return a list of lines which are the desired text from the given file.
    This will collect the title, author, and abstract text from the abstract
    file. That is, everything between the LaTeX commands ``\begin{document}''
    and ``\end{document}''
    '''
    # Save the text as a list of lines.
    text = []
    # Initial part of file.
    text.append('% --------------------- New abstract ---------------------\n')
    text.append('\\begin{titleauthorabstract}\n')
    # Open the file and store every line with the LaTeX document environment.
    with open(path, 'r') as f:
        record = False  # Triggers when to record lines.
        for line in f:
            if record:
                # Check to see if reached end of file.
                if line.strip() == '\\end{document}':
                    break  # Finished retrieving text.
                # If not at end of file, record the line..
                text.append(line)
            # Set record to true when the beginning of the document is reached.
            elif line.strip() == '\\begin{document}':
                record = True

    # End the text.
    text.append('\\end{titleauthorabstract}\n')
    text.append('% --------------------------------------------------------\n')
    text.append('\n')
    return text

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
    text = []
    text.append('% -------------------- New department --------------------\n')
    text.append('\\begin{departmentheading}\n')
    text.append(deptname + '\n')
    text.append('\\end{departmentheading}\n')
    text.append('% --------------------------------------------------------\n')
    text.append('\n')
    return text

if __name__ == '__main__':
    write_booklet()
