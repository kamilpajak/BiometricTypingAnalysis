// static.js

// Initializes an array to store the key events data
let keyEvents = [];

// These phrases were chosen based on their ability to maximize the diversity of letter pairs, providing a wide range of combinations for analysis or application purposes.
const phrases = {
  // This array contains a carefully selected list of phrases optimized to include a total of 91 unique two-letter combinations.
  english: [
    "Pessimistic Hurricane",
    "Frozen Mountain",
    "Clumsy Waterfall",
    "Graceful Nightmare",
    "Polished Blizzard",
    "Glowing Tornado"
  ],
  // This array contains a carefully selected list of phrases optimized to include a total of 98 unique two-letter combinations.
  polish: [
    "Perfekcyjny Mikrofon",
    "Racjonalny Zasobnik",
    "Zdeprawowany Laptop",
    "Energetyczny Samolot",
    "Gadatliwy Telewizor",
    "Brzydki Poduszkowiec"
  ]
};

// Hardcoded language flag
const languageFlag = "polish"; // Use "english" or "polish" to set the language of phrases

let currentPhrase = ""; // Variable to store the current phrase

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

// Helper function to randomly select a new phrase different from the current one
function selectNewPhrase() {
  let newPhrase;
  const currentPhrases = phrases[languageFlag]; // Access phrases based on the current language flag
  do {
    newPhrase = currentPhrases[Math.floor(Math.random() * currentPhrases.length)];
  } while (newPhrase === currentPhrase);
  currentPhrase = newPhrase;
  phraseToTypeElement.textContent = newPhrase;
}

// Sends the keystrokes to the server if the text matches the phrase
function sendKeystrokesToServer() {
  if (textMatchesPhrase()) {
    const data = JSON.stringify({ keyEvents: keyEvents });

    fetch('/capture/process_keystrokes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: data
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      resetTyping();
      selectNewPhrase();
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
  selectNewPhrase(); // Initially select a random phrase when the page loads
  typingDataInput.focus(); // Automatically focus on the typing input field when the page loads

  typingDataInput.addEventListener('paste', (event) => {
    event.preventDefault(); // Disable paste into the input field
    alert('Pasting text is not allowed.');
  });

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