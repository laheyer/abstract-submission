// dynamicInput.js
//
// Allow html forms to include text input fields which can optionally
// provide additional input fields.
// The result is stored in an array from the form.
//
// Author: S.T. Castle
// Created: 07 May 2015
// From: Allen Liu, www.randomsnippets.com

// Track the current number of fields added.
var counter = 1;
// Place a limit on the total number of fields allowed.
var limit = 9;
// Main function.
function addInput(divName){
    if (counter == limit)  {
        alert("You have reached the limit of adding " + (counter+1) +
                " authors.");
    }
    else {
        var newdiv = document.createElement('div');
        newdiv.innerHTML = "Author " + (counter + 2) +
                        " <br><input type='text' name='second_authors'>";
        document.getElementById(divName).appendChild(newdiv);
        counter++;
    }
}
