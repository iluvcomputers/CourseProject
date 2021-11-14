function pasteQuery() {
  navigator.clipboard
    .readText()
    .then(
      (clipText) => (document.getElementById('query-area').innerText = clipText)
    );
}

document.addEventListener('DOMContentLoaded', pasteQuery);
