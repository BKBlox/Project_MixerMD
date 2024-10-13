# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from config import Config
from extensions import mongo  # Import mongo from extensions.py

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize PyMongo with the app
mongo.init_app(app)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No input data provided'}), 400  # Bad Request

        # Extract the user's name and responses
        name = data.get('name')
        responses = data.get('responses')

        # Validate the data
        if not name:
            return jsonify({'message': 'User name is required.'}), 400

        if not responses or not isinstance(responses, list) or len(responses) != 10:
            return jsonify({'message': 'Exactly 10 responses are required.'}), 400

        # Further validation: Ensure none of the responses are empty
        if not all(responses):
            return jsonify({'message': 'All responses must be provided and non-empty.'}), 400

        # Process the data (e.g., save to database)
        # For example:
        # save_user_responses(name, responses)

        # Return a success response
        return jsonify({'message': 'Data received successfully!', 'name': name, 'responses': responses}), 200

    except Exception as e:
        app.logger.error(f'Error in /submit route: {e}')
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# Register Blueprints
from routes import user_bp, test_bp, game_bp
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(test_bp, url_prefix='/api/test')
app.register_blueprint(game_bp, url_prefix='/api/game')

# Define a simple home route
@app.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the Local Parties App API"}, 200

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
