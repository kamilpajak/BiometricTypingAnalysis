let key_events = [];

document.addEventListener('DOMContentLoaded', (event) => {
  const typingDataTextarea = document.getElementById('typingData');

  typingDataTextarea.addEventListener('keydown', (event) => {
    const keydownTime = Date.now();
    key_events.push({
      key: event.key,
      type: 'press',
      time: keydownTime
    });
  });

  typingDataTextarea.addEventListener('keyup', (event) => {
    const keyupTime = Date.now();
    key_events.push({
      key: event.key,
      type: 'release',
      time: keyupTime
    });
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
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}
