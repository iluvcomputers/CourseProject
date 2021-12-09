const form = document.querySelector('form');

// this function accepts an {object} and returns the contents displayed to the page
function displayResults(jsonData) {
  // receiving array of objects here

  // results is an array of n items
  let results = jsonData;

  results.forEach((element) => {
    let item = JSON.stringify(element);
    // you can now access element.body, element.lecture, element.timestamp, element.week

    // create a new div area for each element
    // insert into that div, elements for each body/lecture/timestamp/week
    // create a DOM table
    var newTable = document.createElement('table');
    newTable.setAttribute('style', 'border-spacing:50px;');
    // add the DOM table to the landing-area
    document.getElementById('landing-area').appendChild(newTable);
    var headerRow =
      '<tr> <td> <b> Body </b> </td> <td> <b> Lecture </b> </td> <td> <b> Timestamp </b> </td> <td> <b> Week </b> </td></tr>';
    var tr = '<tr>';
    tr +=
      '<td> ' +
      element.body +
      '</td>' +
      '<td> ' +
      element.lecture +
      '</td>' +
      '<td>' +
      element.timestamp +
      '</td>' +
      '<td>' +
      element.week +
      '</td>';

    document.getElementById('landing-area').lastChild.innerHTML += headerRow;
    document.getElementById('landing-area').lastChild.innerHTML += tr;
  });
}

function clearResults() {
  document.getElementById('landing-area').innerText = '';
}

function sendQuery(formData) {
  // clear search results area before starting a new search
  clearResults();

  fetch('http://localhost:5000/search', {
    method: 'post',
    body: formData,
  })
    .then((response) => {
      // this returns a promise
      response.json().then((data) => {
        // this is an object containing an array of results, which are themselves objects
        var resultsData = data.results;
        console.log(resultsData);
        displayResults(data.results);
      });
    })
    .catch((error) => {
      console.log('Error: ' + error);
    });
}

function handleSubmit(event) {
  // Prevent the default submission
  event.preventDefault();

  // Log the serialized data
  console.log(serializeObject(this));

  // Alert the user
  alert('Check the console.');
}

// add event listener for Clear Results button
document
  .getElementById('clear-results')
  .addEventListener('click', clearResults);

// add event listener for query form
document.getElementById('form').addEventListener('submit', function (e) {
  e.preventDefault();

  // create formData object
  const formData = new FormData(this);

  // jsonify the query to send to the server
  var object = {};
  formData.forEach(function (value, key) {
    object[key] = value;
  });
  var json = JSON.stringify(object);

  sendQuery(json);
});
