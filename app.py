# app.py
from utils.csv_handler import write_to_csv
from flask import Flask, request, jsonify
from flask_cors import CORS
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
        responses = request.get_json() # data
        print(responses)
        if not responses:
            return jsonify({'message': 'No input data provided'}), 400  # Bad Request
        # Validate the data
        if not responses or not isinstance(responses, list) or len(responses) != 11:
            return jsonify({'message': 'Username + exactly 10 responses are required.'}), 400
        # Further validation: Ensure none of the responses are empty
        print("Making json_dict")
        json_dict = {"name" : responses[0]}
        i = 1
        while i < len(responses):
            key = "ans" + str(i)
            json_dict.update({key : responses[i]})
            i += 1
        write_to_csv(json_dict)
        return "0" # return the row the user was written to (UUID) to be passed back to user script?
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
