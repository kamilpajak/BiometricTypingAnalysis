let keystrokes = [];

document.addEventListener('DOMContentLoaded', (event) => {
  const typingDataTextarea = document.getElementById('typingData');

  typingDataTextarea.addEventListener('keydown', (event) => {
    const keydownTime = Date.now();
    keystrokes.push({
      key: event.key,
      type: 'press',
      time: keydownTime
    });
  });

  typingDataTextarea.addEventListener('keyup', (event) => {
    const keyupTime = Date.now();
    keystrokes.push({
      key: event.key,
      type: 'release',
      time: keyupTime
    });
  });
});

function sendKeystrokesToServer() {
  const data = JSON.stringify(keystrokes);

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
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}
