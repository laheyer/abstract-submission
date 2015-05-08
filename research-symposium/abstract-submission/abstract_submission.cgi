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
import subprocess

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
    year = form['year'].value
    dept = form['department'].value
    dept = dept.lower()  # Get lowercase.
    author1 = form['first_author'].value
    author2 = form.getlist('second_authors') # List of additional authors.
    author2 = [s.strip() for s in author2] # Strip unnecessary whitespace.
    title = form['title'].value

    # Generate filename from the name of the first author.
    # Make first author lowercase, remove '.', split on whitespace,
    # move the last name to front, and re-concatenate with underscores.
    author_compressed = author1.lower().replace('.','').split()
    author_compressed.insert(0, author_compressed.pop())
    author_compressed = '_'.join(author_compressed)

    # Sort into directory based on the department.
    dirname = year + '/' + dept + '/' + author_compressed
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
    
    # Convert the rtf file to a LaTeX file.
    tex_filepath = convert_rtf_to_tex(filepath)

    # Add title and author information to the LaTeX file.
    add_title_and_author(tex_filepath, title, author1, author2)

    # Generate pdf from the LaTeX file using pdflatex subprocess.
    #subprocess.check_call(['pdflatex', tex_filepath])
    # Remove auxiliary files from pdflatex compilation.

def add_title_and_author(path, title, author1, author2): 
    '''
    Add the title and author information to the specified tex file.
    params:
      path: The relative path to the tex file.
      title: The title of the abstract, which may contain LaTeX markup.
      author1: The primary author.
      author2: List of zero, one, or more secondary authors.
    '''
    # Get string of authors.
    authors = combine_authors(author1, author2)

    # Store a list of lines to overwrite existing lines in the file.
    output = []

    # Open file for reading.
    # Insert title and author immediately following ``\begin{document}'' line.
    with open(path, 'r') as f:
        wait_abstract = False  # True if the abstract is the next text.
        for line in f:
            line_strip = line.strip()
            # Start by recording each line unless waiting through blank lines
            # for the abstract.
            if not wait_abstract:
                output.append(line)
            # Take every line except the LaTeX ``\newpage'' command.
            if line_strip == '\\newpage':
                output.pop()
            # Check for ``\begin{document}''. Add title and author here.
            if line_strip == '\\begin{document}':
                output.append('\n')
                output.append('\\begin{customtitle}\n')
                output.append(title + '\n')
                output.append('\\end{customtitle}\n')
                output.append('\n')
                output.append('\\begin{customauthor}\n')
                output.append(authors + '\n')
                output.append('\\end{customauthor}\n')
                output.append('\n')
                wait_abstract = True  # Now waiting for the abstract text.
                continue              # Continue to next line in file.
            # Check for the first line with text when waiting for the abstract.
            # This, of course, will be the start of the abstract.
            if wait_abstract and line_strip != '':
                output.append('\\begin{customabstract}\n')
                output.append(line)
                wait_abstract = False
            # Check for ``\end{document}'' to signify the end of the abstract.
            if line_strip == '\\end{document}':
                output.pop()  # Remove the ``\end{document}'' line temporarily.
                # Remove excess blank lines.
                while output[-1] == '\n':
                    output.pop()
                # Signal end of abstract and replace ``\end{document}''
                output.append('\\end{customabstract}\n')
                output.append('\n')
                output.append(line)

            # Remove additional unnecessary and unwanted formatting.
            if line_strip == '\\begin{center}' or line_strip == '\\end{center}':
                output.pop()

    # Now open the file for writing to overwrite the original.
    with open(path, 'w') as f:
        f.writelines(output)

    # Make sure file permissions are as desired.
    os.chmod(path, 0666)

def combine_authors(first, second):
    '''
    Return a string containing the authors in format
    "Author 1, Author 2, ..., and Author n".
    params:
      first: The name of the first author.
      second: List of zero, one, or more secondary authors.
    '''
    # Remove whitespace or newlines at ends of string.
    first = first.strip()

    # Get a list of second authors.
    second = filter(None, second)  # Remove empty strings. 

    # Combine the list of authors and return the result.
    if len(second) == 0:  # If no second authors.
        return first
    elif len(second) == 1:
        return (first + ' and ' + second[0])
    else:
        s = first + ', ' + ', '.join(second[:-1])
        s = s + ', and ' + second[-1]
        return s

def convert_rtf_to_tex(filepath):
    '''
    Convert the specified rtf file to a LaTeX file using rtf2latex2e.
    Return the path to the newly created tex file.
    '''
    # Run rtf2latex2e to convert the new rtf file to a LaTeX file.
    rtf2latex2e = '/DATA/Documents/csc209/STC/bin/rtf2latex2e'
    params = '-n'  # Natural mode.
    subprocess.check_call([rtf2latex2e, params, filepath])

    # Change file permissions.
    tex_filepath = filepath[:-4] + '.tex'  # Remove '.rtf' from end.
    os.chmod(tex_filepath, 0666)

    return tex_filepath
    
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
        f.write(';'.join(author2)+'\n')

    # Change file permissions.
    os.chmod(filepath, 0664)

def make_directory(name):
    '''
    Check whether a directory with the given name exists.
    If so, create a new name.
    Make a directory with this name and return the directory name.
    '''
    name = name.lower() # Make lowercase.
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
