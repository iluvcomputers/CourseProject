function pasteQuery() {
  navigator.clipboard
    .readText()
    .then(
      (clipText) => (document.getElementById('query-area').innerText = clipText)
    );
}

document.addEventListener('DOMContentLoaded', pasteQuery);

// this function accepts an {object} and returns the contents displayed to the page
function displayResults(jsonData) {
  // results is an array of n items
  let results = jsonData['results'];

  results.forEach((element) => {
    let item = JSON.stringify(element);
    // you can now access element.body, element.lecture, element.timestamp, element.week
    document.getElementById('results-area').innerText = element.body;

    // create a new div area for each element
    // insert into that div, elements for each body/lecture/timestamp/week
  });
}

console.log('made it to tabs');
// test hitting our local server
fetch('http://localhost:5000/test')
  .then(function (response) {
    return response.json();
  })
  .then(function (jsonResponse) {
    console.log(jsonResponse);
    // document.getElementById('results-area').innerText = JSON.stringify(
    //   jsonResponse['results'][0]
    // );

    // document.getElementById('results-area').innerText =
    //   JSON.stringify(jsonResponse);
    displayResults(jsonResponse);
  })
  .catch(function (error) {
    console.log('Error: ' + error);
  });
