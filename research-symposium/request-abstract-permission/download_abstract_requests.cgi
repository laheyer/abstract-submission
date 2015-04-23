#!/usr/bin/python

'''
download_abstract_requests.cgi

The code receives a password and department specified by a web user.
If the password is correct for the specified department, the
file, containing a list of students requesting permission to submit
an abstract, will be downloaded.

Author: S.T. Castle
Created: 22 Apr 2015
'''

import cgi
import cgitb
cgitb.enable()

def main():

    # Passwords used for each of the departments.
    codes = {
            'BIO': 'bio',
            'CHE': 'che',
            'MAT': 'mat',
            'PHY': 'phy'
            }

    # Required header that tells the browser how to render the text.
    # First line, *first character*, must have header 
    # "Content-Type: text/html" followed by blank line
    print "Content-Type: text/html"
    print

    # Print html code.
    print '''
        <TITLE>Davidson College Math and Science Research Symposium</TITLE>
        <H3>Davidson College Math and Science Research Symposium</H3>
        <p>Download permission request forms.</p>
        '''

    # Obtain data from the html form, indexed like a dictionary.
    form = cgi.FieldStorage()
    dept = form['department'].value
    password = form['password'].value

    # Stop if password is incorrect.
    if password != codes[dept]:
        print '''
            <br>
            <H1>Incorrect Password. Permission Denied.</H1>
            <p>
            <a href=
            "request_abstract_permission.html">
            Click here to return to the original form.</a></br>
            </p>
            '''
        return

    # Otherwise, password was correct, so download the appropriate file.
    filename = dept.lower() + '_students_pending.txt'
    print '''
        <br>
        <H2>Download file:</H2>
        <p>
        <a href='''+filename+''' download>
        Click here to download the current list of '''+dept+'''
        students.</a></br>
        </p>
        '''
    print '''
        <br>
        <H2>Return to original form:</H2>
        <p>
        <a href=
        "request_abstract_permission.html">
        Click here to return to the original form and try again.</a></br>
        </p>
        '''
 
if __name__ == '__main__':
    main()
