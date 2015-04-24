#!/usr/bin/python

'''
abstract_submisison.cgi

This script was created for the Davidson College Math and Science Research
Symposium.
It works with an html form to save uploaded abstracts on the server and
generate LaTeX documents from the original .rtf or .tex abstracts.

Author: S.T. Castle
Created: 24 Apr 2015
'''
#-------------------------------------------------------------------------------

# Imports for html cgi docs.
import cgi
import cgitb
cgitb.enable()

import os
import sys

def main():

    # Required header that tells the browser how to render the text.
    # First line, *first character*, must have header 
    # "Content-Type: text/html" followed by blank line
    print "Content-Type: text/html"
    print

    # Print html code.
    print '''
        <TITLE>Davidson College Math and Science Research Symposium</TITLE>
        <h1>Davidson College Math and Science Research Symposium</h1>
    '''

    # Obtain data from the html form, indexed like a dictionary.
    form = cgi.FieldStorage()  # Get dictionary from form.
    dept = form['department'].value
    author1 = form['first_author'].value
    author2 = form['second_author'].value
    title = form['title'].value

    # Get the uploaded file and generate filename.
    # Split first author name on whitespace and re-concatenate.
    author_compressed = ''.join(author1.split())

    # Sort into directory based on the department.
    dirname = dept + '/' + author_compressed
    # And check whether departmental directory exists.
    if not os.path.exists(dept):
        os.makedirs(dept)
        os.chmod(dept, 0777)

    # Build a directory with the name of the author. 
    dirname = make_directory(dirname)

    # Get last part of directory path for the filename.
    filename = dirname.split('/')[-1]
    filepath = dirname + '/' + filename + '_abstract.rtf'

    # Write the uploaded file.
    write_uploaded_file(form['abstract_file'], filepath)

    # Write the metadata file to the directory.
    metadata_filepath = dirname + '/' + filename + '_metadata.txt'
    write_metadata(metadata_filepath, dept, author1, author2, title)
    
def write_metadata(filepath, dept, author1, author2, title):
    '''
    Write a file to the new directory containing department, author,
    and title information for this abstract.
    '''
    if os.path.exists(filepath):
        print 'Error writing metadata file: already exists!'
        return

    with open(filepath, 'w') as f:
        f.write(dept+'\n')
        f.write(title+'\n')
        f.write(author1+'\n')
        f.write(author2+'\n')

    # Change file permissions.
    os.chmod(filepath, 0664)

def make_directory(name):
    '''
    Check whether a directory with the given name exists.
    If so, create a new name.
    Make a directory with this name and return the directory name.
    '''
    size = len(name)  # Length of original name.
    counter = 1 # Number of directories with this name, including this one.

    # Add to the end of the name if directory already exists.
    while os.path.exists(name):
        counter += 1
        name = name[:size] + str(counter)

    # Now directory name is unique. Make directory.
    os.makedirs(name)
    os.chmod(name, 0777)  # Give all permissions so directory can be removed.
    
    # Return the filename within the new directory, to be created later.
    return name

def write_uploaded_file(fileitem, filename):
    '''Write the uploaded file to the specified name and path.'''
    try: # Windows needs stdio set for binary mode.
        import msvcrt
        msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
        msvcrt.setmode (1, os.O_BINARY) # stdout = 1
    except ImportError:
        pass
    
    #form = cgi.FieldStorage()
    
    # A nested FieldStorage instance holds the file
    #fileitem = form['file']
    
    # Test if the file was uploaded
    #if fileitem.filename:
    try:
       
        # Get original filename.
        fn = os.path.basename(fileitem.filename)
        #open(fn, 'wb').write(fileitem.file.read())
        open(filename, 'wb').write(fileitem.file.read())
        # Make the file writeable by group.
        os.chmod(filename, 0664)
        message = 'The file "' + fn + '" was uploaded successfully'
       
    #else:
    except:
        message = 'Error: ' + str(sys.exc_info()[0])
        message += '\n\nNo file was uploaded'
       
    print '''
    <p>%s</p>
    ''' % (message)

if __name__ == '__main__':
    main()
