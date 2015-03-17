/* This file is the compliment to clippy.swf. Clippy.swf accepts two variables on MOUSE_UP--a function to call,
and a parameter to pass to that function.

The function is set to getText(), and the parameter is the ID of the div which clippy.swf is in. clippy.swf
copies all the text in the div to a user's clipboard, and also highlights the div  */

function getText(codeID) {
	var hasInnerText = (document.getElementsByTagName("body")[0].innerText != undefined) ? true : false;
	var elem = document.getElementById(codeID);	
	var content;

	// strip out all html tags and just get the text
	if (!hasInnerText) { 
		content = elem.textContent;			
    }
    else { // ie check
		content =  elem.innerText;
    }
	content = content.replace(/\xA0/g,' ');

    borderOff(codeID);
    borderOn(codeID);
    borderOff(codeID);
    
    // returns the plain text, and clippy.swf sets that to your clipboard
    return content;
}

function borderOn(codeID) {
    var elem = document.getElementById(codeID);	
    
    elem.className += " clipboardBorder";
}

function borderDash(codeID) {
    var elem = document.getElementById(codeID);	
    
    elem.className += " clipboardDashed";
}

function borderOff(codeID) {
    var elem = document.getElementById(codeID);	
    
    elem.className = elem.className.replace(/clipboardBorder/,'');
    elem.className = elem.className.replace(/clipboardDashed/,'');
}