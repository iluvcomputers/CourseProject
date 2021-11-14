# Browser Extension

### Requirements

- Firefox (Tested on v94.0.1)

### Installation Instructions

First, import the add-on:

1. In Firefox, go to about:debugging
2. Click "This Firefox"
3. Click "Load Temporary Add-On"
4. Navigate to your saved `manifest.json` file and click on it

### Using the Extension

1. Navigate to https://www.coursera.org/learn/cs-410/home/welcome
2. Highlight a term you'd like to fuzzy search for
3. Right-click and select "Send to Fuzzy Search"

### Required JS files

- background.js: This script is required for the "Send to fuzzy search" context menu option
- query-copy.js: This script is required to copy from the clipboard
- tabs.js: This script is required to paste query data into the results.html page

---
