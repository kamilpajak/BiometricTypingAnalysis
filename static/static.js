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

const languageFlag = "polish"; // Change to "english" as needed

let currentPhrase = ""; // Stores the current phrase to be typed

const typingDataInput = document.getElementById('typingData');
const phraseToTypeElement = document.getElementById('phraseToType');

function recordKeyEvent(key, eventType, time) {
  keyEvents.push({ key, type: eventType, time });
}

function textMatchesPhrase() {
  // Checks if the current input text exactly matches the phrase
  return typingDataInput.value.trim() === phraseToTypeElement.textContent.trim();
}

function resetTyping() {
  typingDataInput.value = '';
  keyEvents = [];
}

function selectNewPhrase() {
  let newPhrase;
  const currentPhrases = phrases[languageFlag];
  do {
    newPhrase = currentPhrases[Math.floor(Math.random() * currentPhrases.length)];
  } while (newPhrase === currentPhrase);
  currentPhrase = newPhrase;
  phraseToTypeElement.textContent = newPhrase;
}

function sendKeystrokesToServer() {
  // Sends the keystrokes to the server if the text matches the phrase
  if (textMatchesPhrase()) {
    const data = JSON.stringify({ keyEvents });

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
  }
}

function checkTypingAccuracy() {
  if (!currentPhrase.startsWith(typingDataInput.value.trim())) {
    alert('The text does not match. Please try again.');
    resetTyping();
    selectNewPhrase();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  selectNewPhrase();
  typingDataInput.focus();

  typingDataInput.addEventListener('paste', (event) => {
    event.preventDefault();
    alert('Pasting text is not allowed.');
  });

  typingDataInput.addEventListener('input', (event) => {
    checkTypingAccuracy(); // Checks the typing accuracy on every input
  });

  typingDataInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      // Check if the phrase matches and then send the data
      if (textMatchesPhrase()) {
        sendKeystrokesToServer();
      } else {
        alert('The text does not match the phrase. Please try again.');
        resetTyping();
      }
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
