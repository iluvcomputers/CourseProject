browser.contextMenus.create({
  id: 'send-to-fuzzy-search',
  title: 'Send to fuzzy search',
  contexts: ['selection'],
});

browser.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'send-to-fuzzy-search') {
    // pass to content script

    browser.tabs.executeScript(tab.id, {
      file: 'background-script.js',
    });

    const customUrl = browser.runtime.getURL('/results.html');
    var creating = browser.tabs.create({
      url: customUrl,
    });
    creating.then(onCreated, onError);
  }
});
