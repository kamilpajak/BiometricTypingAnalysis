from flask import Flask, render_template, request, jsonify

from keystroke_processor import KeystrokeProcessor

app = Flask(__name__)

keystroke_processor = KeystrokeProcessor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/capture_keystrokes', methods=['POST'])
def capture_keystrokes():
    key_events = request.json
    processor = KeystrokeProcessor()
    keystrokes = processor.process_key_events(key_events)
    return jsonify({'message': 'Keystrokes processed successfully', 'data': keystrokes})


@app.before_request
def before_request():
    app.logger.debug('Incoming request: %s %s', request.method, request.url)
    if request.method == 'POST':
        app.logger.debug('Request data: %s', request.get_data(as_text=True))


@app.after_request
def after_request(response):
    app.logger.debug('Response status: %s', response.status)
    if not response.direct_passthrough:
        app.logger.debug('Response data:\n%s', response.get_data(as_text=True))
    else:
        app.logger.debug('Response data: not available (passthrough mode)')
    return response


if __name__ == '__main__':
    app.run(debug=True)
