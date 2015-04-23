#!/usr/bin/python
import cgi
import cgitb
cgitb.enable()

'''
request_abstract_permission.cgi

The code receives the name and department specified by a user.
The code adds the user's name to a list of names for the specified department.
These lists can be downloaded from original page or after submission.

Author: S.T. Castle
Created: 21 Apr 2015
'''

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
    student = form['student_name'].value
    advisor = form['advisor_name'].value
    dept = form['department'].value

    # Add the names to the appropriate text file.
    filename = dept.lower() + '_students_pending.txt'
    # Open the file for appending.
    with open(filename, 'a') as f:
        f.write('Student: {0:23s} --- Advisor: {1}\n'.format(student,advisor))

    # Write message on new page.
    print '''
        <h2>Congrats! You were successfully added to your
        department's list of pending entrants.</h2>
        <br>
        <p>
        Do not use your browser's refresh button, as this will submit a
        duplicate form.
        </p>
        '''
    print '''
        <br>
        <p>You can safely leave this page,
        or use the following link to return to the original form.</p>
        <p>
        <a href=
        "request_abstract_permission.html">
        Original form.</a></br>
        </p>
        '''

if __name__ == '__main__':
    main()
