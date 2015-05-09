#!/usr/bin/python

'''
gen_booklet.cgi

This script was created for the Davidson College Math and Science Research
Symposium.
It is the cgi code for a web form used to generate and download the
abstract booklet for a specified year of the research symposium.
It uses all files in the directory specified by the chosen year.

Author: S.T. Castle
Created: 20 Apr 2015
Updated: 08 May 2015

Suggestions:
Allow the user to specify a single department or all departments.
It would be fairly easy to generate the booklet only for a
single department---just call the department's subdirectory as
the parent directory in the call to write_booklet().
'''

# Imports for html cgi docs.
import cgi
import cgitb
cgitb.enable()

import os
import sys

# Local imports
from write_latex_booklet import write_booklet

def generate_booklet():

    # Required header that tells the browser how to render the text.
    # First line, *first character*, must have header 
    # "Content-Type: text/html" followed by blank line
    print "Content-Type: text/html"
    print

    # Print html code.
    print '''
        <TITLE>Davidson College Math and Science Research Symposium</TITLE>
        <h1>Davidson College Math and Science Research Symposium</h1>
        <h2>Download abstract booklet.</h2>
    '''

    # Obtain data from the html form, indexed like a dictionary.
    form = cgi.FieldStorage()  # Get dictionary from form.
    passwd = form['password'].value
    year = form['year'].value
    date = form['department'].value
    date = date.strip()  # Remove whitespace on ends.

    # Check that the password is correct.
    if passwd != '#CatsAreWild':
        print '''
            <h2>Sorry, you entered an incorrect password.</h2>
            <br>
            <p>Use the following link to return to the original form.</p>
            <p>
            <a href=
            "get_abstract_booklet.html">
            Original form.</a></br>
            </p>
            '''
        return

    # Write the date into the title page for the booklet.
    title_page = 'customtitle.tex'             # New tex file to be written.
    old_title_page = 'customtitle_nodate.tex'  # Title page template, sans date.
    # Get all lines from template file.
    with open(old_title_page, 'r') as f:
        title_page_output = list(f)
    # Insert the date command at the beginning of the lines.
    title_page_output.insert(0,'\\newcommand*{\\customdate}{' + date + '}')
    # Write the lines to the new file.
    with open (title_page, 'w') as f:
        f.writelines(title_page_output)

    # Generate the booklet using LaTeX and the directory corresponding to the
    # specified year.
    abstract_dir = year + '/'                   # Parent directory of abstracts.
    preamble = 'preamble.tex'                    # LaTeX preamble file.
    booklet_tex = year + '_abstract_booklet.tex' # Final booklet tex file.
    booklet_pdf = year + '_abstract_booklet.pdf' # Final booklet pdf file.
    write_booklet(abstract_dir, preamble, booklet_tex)

    # Create the pdf booklet using pdflatex.
    # !!!

    # Display a link to download the newly-created file.
    print '''
        <br>
        <H2>Abstract booklet for the ''' + year + ''' research symposium.</H2>
        <p>
        <a href='''+booklet_pdf+''' download>
        Click here to download the booklet.</a></br>
        </p>
        '''
    print '''
        <br>
        <H2>Return to original form:</H2>
        <p>
        <a href=
        "get_abstract_booklet.html">
        Click here to return to the original form and
        generate a different booklet.</a></br>
        </p>
        '''

if __name__ == '__main__':
    generate_booklet()
