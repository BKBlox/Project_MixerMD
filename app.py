# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import csv
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes and methods
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# Define paths for CSV files
DATA_DIR = 'data'
ANSWERS_CSV = os.path.join(DATA_DIR, 'answers_data.csv')
EMOJI_CSV = os.path.join(DATA_DIR, 'emoji_data.csv')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Function to write questionnaire responses to CSV
def write_answers_to_csv(data):
    file_exists = os.path.isfile(ANSWERS_CSV)
    fieldnames = ['user_id'] + [f'question{i}' for i in range(1, 11)]

    with open(ANSWERS_CSV, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

# Function to write emoji data to CSV
def write_emoji_to_csv(data):
    file_exists = os.path.isfile(EMOJI_CSV)
    fieldnames = ['timestamp', 'user_id', 'emotion', 'emoji']

    with open(EMOJI_CSV, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure 'index.html' is in the 'templates/' directory

# Route to submit questionnaire responses
@app.route('/submit', methods=['POST'])
def submit():
    try:
        responses = request.get_json()
        if not responses:
            return jsonify({'message': 'No input data provided'}), 400  # Bad Request

        # Validate the data
        if not isinstance(responses, list) or len(responses) != 11:
            return jsonify({'message': 'User ID + exactly 10 responses are required.'}), 400

        # Build the data dictionary
        json_dict = {"user_id": responses[0]}  # Assuming the first element is user_id
        for i in range(1, len(responses)):
            key = f"question{i}"
            json_dict[key] = responses[i]

        # Write to CSV
        write_answers_to_csv(json_dict)

        return jsonify({"status": "success", "user_id": responses[0]}), 200
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

        # Write to CSV file
        write_emoji_to_csv(row)

        return jsonify({'message': 'Emoji data saved successfully'}), 200

    except Exception as e:
        app.logger.error(f'Error in /save-emoji route: {e}')
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# Route to calculate affinity scores
@app.route('/calculate-affinity', methods=['GET'])
def calculate_affinity_scores():
    try:
        # Check if the CSV files exist
        if not os.path.isfile(EMOJI_CSV) or not os.path.isfile(ANSWERS_CSV):
            return jsonify({'message': 'CSV file(s) not found'}), 404

        # Read user emoji data
        emoji_data = {}
        with open(EMOJI_CSV, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                user_id = row['user_id']
                emoji_data[user_id] = row['emoji']

        # Read user answers data
        user_data = []
        with open(ANSWERS_CSV, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                user_id = row['user_id']
                # Ensure that each question answer is not empty
                answers = []
                for i in range(1, 11):
                    answer = row.get(f'question{i}', '')
                    if answer:
                        answers.append(answer[0])  # Take the first character
                    else:
                        answers.append('')  # Placeholder for missing answer

                user_data.append({
                    'username': row.get('username', ''),
                    'answers': answers,
                    'emoji': emoji_data.get(user_id, ''),
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
                        # Initialize the score
                        affinity_scores[(user1_id, user2_id)] = 0

                    # Compare their answers for questions 1 to 10
                    score = sum(
                        1 for a1, a2 in zip(user1['answers'], user2['answers']) if a1 == a2 and a1 != ''
                    ) * 0.5

                    # Compare emoji selection
                    if user1['emoji'] and user1['emoji'] == user2['emoji']:
                        score += 1

                    # Set the score
                    affinity_scores[(user1_id, user2_id)] = score

        # Find the top 3 matches for each user
        top_3_matches = {}
        for user in user_data:
            user_id = user['user_id']
            # Collect all affinity scores for this user
            user_affinities = [
                (other_user_id, affinity_scores.get((user_id, other_user_id), 0))
                for other_user_id in [u['user_id'] for u in user_data if u['user_id'] != user_id]
            ]

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
        app.logger.error(f'Error in /calculate-affinity route: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':  # Ensure only one instance of this block exists
    app.run(port=5000, debug=True)
