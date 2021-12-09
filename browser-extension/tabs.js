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

function clearResults() {
  document.getElementById('results-area').innerText = '';
}

function sendQuery() {
  fetch('http://localhost:5000/test')
    .then((response) => {
      return response.json();
    })
    .then((jsonResponse) => {
      displayResults(jsonResponse).catch((error) => {
        console.log('Error: ' + error);
      });
    });
}

console.log('made it to tabs');
// test hitting our local server
fetch('http://localhost:5000/test')
  .then(function (response) {
    return response.json();
  })
  .then(function (jsonResponse) {
    // displayResults(jsonResponse);
    console.log('do nothing');
  })
  .catch(function (error) {
    console.log('Error: ' + error);
  });

// add event listener for Search button
document.getElementById('search-button').addEventListener('click', sendQuery);
document
  .getElementById('clear-results')
  .addEventListener('click', clearResults);
