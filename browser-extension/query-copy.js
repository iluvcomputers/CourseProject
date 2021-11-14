/*
copy the selected text to clipboard
*/
function copySelection() {
  var selectedText = window.getSelection().toString().trim();

  if (selectedText) {
    navigator.clipboard.writeText(selectedText);
    console.log(selectedText);
  } // end if selectedText
} // end copySelection

let url = window.location.href;

/*
Add copySelection() as a listener to mouseup events.
*/
document.addEventListener('mouseup', copySelection);
