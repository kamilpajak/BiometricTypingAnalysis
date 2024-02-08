from flask import Flask, render_template, request, jsonify

from feature_calculator import FeatureCalculator
from keystroke_processor import KeystrokeProcessor

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze_keystrokes', methods=['POST'])
def analyze_keystrokes():
    key_events = request.json
    processor = KeystrokeProcessor()
    keystrokes = processor.process_key_events(key_events)
    feature_calculator = FeatureCalculator()
    features = feature_calculator.calculate_features(keystrokes)
    return jsonify({'message': 'Keystrokes analyzed successfully', 'data': features})


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
