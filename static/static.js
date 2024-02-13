// static.js

// Initializes an array to store the key events data
let keyEvents = [];

// Retrieves the input element and phrase display by their IDs
const typingDataInput = document.getElementById('typingData');
const phraseToTypeElement = document.getElementById('phraseToType');

// Helper function to record a key event
function recordKeyEvent(key, eventType, time) {
  keyEvents.push({ key, type: eventType, time });
}

// Helper function to check if entered text matches the phrase
function textMatchesPhrase() {
  return typingDataInput.value.trim() === phraseToTypeElement.textContent.trim();
}

// Helper function to clear input and key events data
function resetTyping() {
  typingDataInput.value = '';
  keyEvents = [];
}

// Sends the keystrokes to the server if the text matches the phrase
function sendKeystrokesToServer() {
  if (textMatchesPhrase()) {
    const data = JSON.stringify({ keyEvents: keyEvents });

    fetch('/capture/analyze_keystrokes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: data
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      resetTyping();
      return fetch('/capture/get_new_phrase');
    })
    .then(response => response.json())
    .then(data => {
      phraseToTypeElement.textContent = data.newPhrase;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  } else {
    alert('The text does not match. Please try again.');
    resetTyping();
  }
}

// Set up event listeners after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  // Listen for keydown and keyup events on the input field
  typingDataInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendKeystrokesToServer();
    } else {
      recordKeyEvent(event.key, 'press', Date.now());
    }
  });

  typingDataInput.addEventListener('keyup', (event) => {
    if (event.key !== 'Enter') {
      recordKeyEvent(event.key, 'release', Date.now());
    }
  });
});
