var helpful     = 1;
var SHelpful    = "Helpful";
var helpfulBut  = 2;
var SHelpfulBut = "Helpful, but";
var unhelpful   = 3;
var SUnhelpful  = "Unhelpful";
var myDialog;

var areasToImproveFieldId = "00N30000001mN1v";
var feedbackTypeFieldId   = "00N30000001mN1l";

// This array is used to populate the Areas to Improve checkbox descriptions, since they vary across
// different types of feedback.
var cbSpanText = Array();
// cbSpanText[x][0] is for the Yes, except... page, cbSpanText[x][1] for the No page
cbSpanText.push(new Array("Some information was incorrect", "It contains inaccurate information"));
cbSpanText.push(new Array("Some information is difficult to understand", "It's difficult to understand"));
cbSpanText.push(new Array("There's missing information", "There's missing information"));
cbSpanText.push(new Array("Code samples or images are incorrect", "Code samples or images are incorrect"));
cbSpanText.push(new Array("It has one or more broken links", "It has one or more broken links"));
cbSpanText.push(new Array("There's a typo", "There's a typo"));
cbSpanText.push(new Array("It needs more code samples", "It needs more code samples"));
cbSpanText.push(new Array("Misleading title", "Based on the title, I thought it would help, but it doesn't provide the information I expected"));
cbSpanText.push(new Array("Incorrectly found in search results", "Search referred me to this document, but it has nothing to do with what I'm looking for"));


function $(id) {
	return document.getElementById(id);
}
function hide(el) {
	el.style.display = "none";
}
function show(el) {
	el.style.display = "";
}

function init() {
	myDialog = new YAHOO.widget.Dialog("feedback", 
		{ close: false, fixedcenter : true, visible : false, constraintoviewport : false, underlay: "none", 
			buttons : [ { text:"Send Feedback", handler:submitForm },
						{ text:"Cancel", handler:cancel } ],
			postmethod : "form"
		});
	myDialog.render();
}

// set the name, email, and address of the user into a cookie
function setCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";

	document.cookie = name+"="+value+expires+"; path=/";
}                
                
// get the cookie
function getCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return escape(c.substring(nameEQ.length,c.length));
	}
	return " ";
}

// if this is the user's first time, establish the cookies
function checkCookie() {
	if (getCookie('formName') == "undefined" || getCookie('formName') == null) setCookie('formName', ' ', 30);
	if (getCookie('formEmail') == "undefined" || getCookie('formEmail') == null) setCookie('formEmail', ' ', 30);
	if (getCookie('formCompany') == "undefined" || getCookie('formCompany') == null) setCookie('formCompany', ' ', 30);	
}

// erase the cookie (currently not in use)
function eraseCookie(name) {
	createCookie(name,"",-1);
}
   

function openFeedback(type) {
	/* Clear all the checkboxes that may have been left over
	 * from a previous type, so that they don't get submitted. 
	 */
	da = document.getElementsByName(areasToImproveFieldId);
	for (n=0; n < da.length; n++) {
		da[n].checked = false;
	}
	
	if (type == helpful || type == SHelpful) {
		// Set the value of the dropdown box with the type of feedback
		$(feedbackTypeFieldId).value = SHelpful;
		// Set the text in the header
		$("header").innerHTML = "Yes, It Was Helpful";
		// Hide the Areas to Improve section
		hide($("improve"));
	} else if (type == helpfulBut || type == SHelpfulBut) {
		// Set the value of the dropdown box with the type of feedback
		$(feedbackTypeFieldId).value = SHelpfulBut;
		// Set the text in the header
		$("header").innerHTML = "It Was Good, But...";
		// Show the Areas to Improve section
		show($("improve"));
		// Hide the two last rows, which were not wanted in the "Yes, except" section
		hide($("tr7"));
		hide($("tr8"));
		// Set the text for the checkboxes based on the array defined above
		for (i=0; i<cbSpanText.length; i++) {
			$("cb" + i).innerHTML = cbSpanText[i][0];
		}
	} else if (type == unhelpful || type == SUnhelpful) {
		$(feedbackTypeFieldId).value = SUnhelpful;
		$("header").innerHTML = "No, It Wasn't Helpful";
		show($("improve"));
		show($("tr7"));
		show($("tr8"));
		for (i=0; i<cbSpanText.length; i++) {
			$("cb" + i).innerHTML = cbSpanText[i][1];
		}
	}
	// Set the height of the containing iframe on the parent page
	changeHeight(parent.document.getElementById("formiframe"));
	myDialog.hide(); // This recenters the form, so it doesn't slide off the page
	myDialog.show();
	$("description").focus();
}
				
function submitForm() {
	if (validateForm()) {
		this.submit();
		parent.document.getElementById("formiframe").style.height = $("feedbackmenu").style.height;

		changeSmallHeight(parent.document.getElementById("formiframe"));
		parent.document.getElementById("formiframe").src="feedback/thanks.htm";
		parent.document.getElementById("formiframe").focus;
		
	}
}

function cancel() {
	this.cancel();
	parent.document.getElementById("formiframe").style.height = $("feedbackmenu").style.height;
	changeSmallHeight(parent.document.getElementById("formiframe"));
	parent.document.getElementById("formiframe").focus;
}

function validateForm() {
	var valid = true;
	
	// Check that the comments field has at most 32,000 characters (limit of the description field in the Case object
	var length = $("description").value.length;
	var commentLength = (length <= 32000);
	if (!commentLength) {
		alert("Please enter a maximum of 32,000 characters in the comments field, or alternatively send an email to docfeedback@salesforce.com" +
			" if you need more space.\n\nThe comments field currently has " + length + " characters in it.");
	}
	valid = valid && commentLength;
	return valid;
}

function changeHeight(iframe)
      {
        try
        {
          var innerDoc = (iframe.contentDocument) ? iframe.contentDocument : iframe.contentWindow.document;
          if (innerDoc.body.offsetHeight) //ns6 syntax
          {
             iframe.height = 920; 
          }
          else if (iframe.Document && iframe.Document.body.scrollHeight) //ie5+ syntax
          {
             iframe.style.height = 920;
          }
        }
        catch(err)
        {
          alert(err.message);
        }
      }
      
      function changeSmallHeight(iframe)
      {
        try
        {
          var innerDoc = (iframe.contentDocument) ? iframe.contentDocument : iframe.contentWindow.document;
          if (innerDoc.body.offsetHeight) //ns6 syntax
          {
             iframe.height = 320; 
          }
          else if (iframe.Document && iframe.Document.body.scrollHeight) //ie5+ syntax
          {
             iframe.style.height = 320;
          }
        }
        catch(err)
        {
          alert(err.message);
        }
      }
