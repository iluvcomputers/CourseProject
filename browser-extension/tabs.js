function pasteQuery() {
  navigator.clipboard
    .readText()
    .then(
      (clipText) => (document.getElementById('query-area').innerText = clipText)
    );
}

document.addEventListener('DOMContentLoaded', pasteQuery);

console.log('made it to tabs');
// test hitting our local server
fetch('http://localhost:5000/test')
  .then(function (response) {
    return response.json();
  })
  .then(function (jsonResponse) {
    console.log(jsonResponse);
  })
  .catch(function (error) {
    console.log('Error: ' + error);
  });
