// Initialize an array to store key events data
let key_events = [];

// Listen for the DOMContentLoaded event to ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', (event) => {
  // Get the textarea element by its ID
  const typingDataTextarea = document.getElementById('typingData');

  // Listen for keydown events on the textarea
  typingDataTextarea.addEventListener('keydown', (event) => {
    // Check if the Enter key is pressed without the Shift key
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevent the default form submission
      sendKeystrokesToServer(); // Call the function to send the key events to the server
    } else {
      // Record the time of the keydown event
      const keydownTime = Date.now();
      // Add the keydown event data to the key_events array
      key_events.push({
        key: event.key,
        type: 'press',
        time: keydownTime
      });
    }
  });

  // Listen for keyup events on the textarea
  typingDataTextarea.addEventListener('keyup', (event) => {
    // Ignore the keyup event for Enter if it's already handled in keydown
    if (event.key === 'Enter' && !event.shiftKey) {
      return;
    } else {
      // Record the time of the keyup event
      const keyupTime = Date.now();
      // Add the keyup event data to the key_events array
      key_events.push({
        key: event.key,
        type: 'release',
        time: keyupTime
      });
    }
  });
});

function sendKeystrokesToServer() {
    const data = JSON.stringify({ key_events: key_events });

    fetch('/analyze_keystrokes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        key_events = [];
        return fetch('/get_new_phrase');
    })
    .then(response => response.json())
    .then(data => {
        const phraseToType = document.getElementById('phraseToType');
        phraseToType.textContent = data.newPhrase;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

