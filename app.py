# app.py
from utils.csv_handler import write_to_csv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize PyMongo with the app

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

@app.route('/')
def home():
    return render_template('index.html')  # This will serve the 'index.html' file

@app.route('/submit', methods=['POST'])
def submit():
    try:
        responses = request.get_json() # data
        if not responses:
            return jsonify({'message': 'No input data provided'}), 400  # Bad Request
        # Validate the data
        if not responses or not isinstance(responses, list) or len(responses) != 11:
            return jsonify({'message': 'Username + exactly 10 responses are required.'}), 400
        # Further validation: Ensure none of the responses are empty
        json_dict = {"name" : responses[0]}
        i = 1
        while i < len(responses):
            key = "ans" + str(i)
            json_dict.update({key : responses[i]})
            i += 1
        user_uuid = write_to_csv(json_dict)
        return jsonify({"status": "success", "uuid": user_uuid}), 200
    except Exception as e:
        app.logger.error(f'Error in /submit route: {e}')
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

if __name__ == '__main__': # DO NOT HAVE MULTIPLE OF THESE IN THIS FILE
    app.run(port=5000)

# Register Blueprints
from routes import user_bp, test_bp, game_bp
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(test_bp, url_prefix='/api/test')
app.register_blueprint(game_bp, url_prefix='/api/game')