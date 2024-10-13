# app.py
from utils.csv_handler import write_to_csv
from flask import Flask, request, jsonify, render_template
import csv
import os
from datetime import datetime
from flask_cors import CORS
from config import Config
from extensions import mongo # Import mongo from extensions.py


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize PyMongo with the app
mongo.init_app(app)

# Enable CORS
CORS(app) # , resources={r"/*": {"origins": "*"}}, supports_credentials=True    

@app.route('/')
def home():
    return render_template('index.html')  # This will serve the 'index.html' file

if __name__ == "__main__":
    app.run(debug=True)

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

# Route to save emoji data
@app.route('/save-emoji', methods=['POST'])
def save_emoji():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        # Extract data from the request
        user_id = data.get('user_id')  # Required
        emotion = data.get('emotion')
        emoji = data.get('emoji')

        # Validate data
        if not user_id or not emotion or not emoji:
            return jsonify({'message': 'User ID, emotion, and emoji are required'}), 400

        # Prepare the data row
        row = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'emotion': emotion,
            'emoji': emoji
        }

        # Define the CSV file path
        csv_file_path = 'emoji_data.csv'

        # Check if file exists to determine if headers are needed
        file_exists = os.path.isfile(csv_file_path)

        # Write to CSV file
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'user_id', 'emotion', 'emoji']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)

        return jsonify({'message': 'Emoji data saved successfully'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# Route to calculate affinity scores
@app.route('/calculate-affinity', methods=['GET'])
def calculate_affinity_scores():
    try:
        # Define the CSV file paths
        emoji_csv_path = 'emoji_data.csv'
        answers_csv_path = 'answers_data.csv'  # Assume you have another CSV for questionnaire answers

        # Check if the CSV files exist
        if not os.path.isfile(emoji_csv_path) or not os.path.isfile(answers_csv_path):
            return jsonify({'message': 'CSV file(s) not found'}), 404

        # Read user emoji data
        emoji_data = {}
        with open(emoji_csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                user_id = row['user_id']
                emoji_data[user_id] = row['emoji']

        # Read user answers data
        user_data = []
        with open(answers_csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                user_id = row['user_id']
                user_data.append({
                    'username': row['username'],
                    'answers': [row[f'question{i+1}'][0] for i in range(10)],  # First letter of each answer
                    'emoji': emoji_data.get(user_id, ''),  # Get emoji from emoji_data
                    'user_id': user_id
                })

        # Calculate affinity scores
        affinity_scores = {}
        for i, user1 in enumerate(user_data):
            for j, user2 in enumerate(user_data):
                if i != j:
                    user1_id = user1['user_id']
                    user2_id = user2['user_id']
                    if (user1_id, user2_id) not in affinity_scores:
                        affinity_scores[(user1_id, user2_id)] = 0

                    # Compare their answers for questions 1 to 10
                    score = sum(1 for a1, a2 in zip(user1['answers'], user2['answers']) if a1 == a2) * 0.5

                    # Compare emoji selection
                    if user1['emoji'] == user2['emoji'] and user1['emoji'] != '':
                        score += 1

                    # Add the score for both users in the affinity table
                    affinity_scores[(user1_id, user2_id)] += score
                    affinity_scores[(user2_id, user1_id)] += score  # Symmetric

        # Find the top 3 matches for each user
        top_3_matches = {}
        for user in user_data:
            user_id = user['user_id']
            # Collect all affinity scores for this user
            user_affinities = [(other_user_id, affinity_scores[(user_id, other_user_id)])
                               for other_user_id in [u['user_id'] for u in user_data if u['user_id'] != user_id]]

            # Sort affinities by score in descending order
            user_affinities.sort(key=lambda x: x[1], reverse=True)

            # Get the top 3 matches
            top_3 = user_affinities[:3]

            # Store the top 3 matches for this user
            top_3_matches[user_id] = [
                {"match_user_id": match[0], "affinity_score": match[1]} for match in top_3
            ]

        # Return the top 3 matches as JSON
        return jsonify({
            'status': 'success',
            'top_3_matches': top_3_matches
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# Register Blueprints
from routes import user_bp, test_bp, game_bp
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(test_bp, url_prefix='/api/test')
app.register_blueprint(game_bp, url_prefix='/api/game')

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
