// Initializes an array to store the key events data.
let key_events = [];

// Listens for the DOMContentLoaded event to ensure the DOM is fully loaded before executing the script.
document.addEventListener('DOMContentLoaded', (event) => {
  // Retrieves the input element by its ID.
  const typingDataInput = document.getElementById('typingData');

  // Listens for keydown events on the input field.
  typingDataInput.addEventListener('keydown', (event) => {
    // Checks if the Enter key is pressed.
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevents the default form submission.
      sendKeystrokesToServer(); // Calls the function to send the key events to the server.
    } else {
      // Records the time of the keydown event.
      const keydownTime = Date.now();
      // Adds the keydown event data to the key_events array.
      key_events.push({
        key: event.key,
        type: 'press',
        time: keydownTime
      });
    }
  });

  // Listens for keyup events on the input field.
  typingDataInput.addEventListener('keyup', (event) => {
    // Ignores the keyup event for Enter if it's already handled in keydown.
    if (event.key === 'Enter') {
      return;
    } else {
      // Records the time of the keyup event.
      const keyupTime = Date.now();
      // Adds the keyup event data to the key_events array.
      key_events.push({
        key: event.key,
        type: 'release',
        time: keyupTime
      });
    }
  });
});

// Defines the function to send the keystrokes to the server.
function sendKeystrokesToServer() {
    // Converts the key_events array to a JSON string.
    const data = JSON.stringify({ key_events: key_events });

    // Sends the data to the server using the fetch API.
    fetch('/analyze_keystrokes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data); // Logs the success message and data.
        key_events = []; // Resets the key_events array after successful submission.
        // Fetches a new phrase from the server.
        return fetch('/get_new_phrase');
    })
    .then(response => response.json())
    .then(data => {
        // Updates the displayed phrase with the new phrase received from the server.
        const phraseToType = document.getElementById('phraseToType');
        phraseToType.textContent = data.newPhrase;
    })
    .catch((error) => {
        console.error('Error:', error); // Logs any errors that occur during the fetch operation.
    });
}
