# routes/user_routes.py

from flask import Blueprint, request, jsonify
from models.user import User
from bson.objectid import ObjectId
from utils.helpers import match_users
from utils.csv_handler import write_to_csv, read_from_csv

user_bp = Blueprint('users', __name__)

@user_bp.route('/submit-questionnaire', methods=['POST'])
def submit_questionnaire():
    """
    User submits their information through a questionnaire.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Validate that the required fields are present
    required_fields = ['user_id', 'username', 'email', 'story']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "All fields are required"}), 400

    # Optional: Validate user existence if needed
    user_id = data.get('user_id')
    if not User.get_user_by_id(user_id):  # Assuming you have a method to validate user
        return jsonify({"message": "User not found"}), 404

    # Write the data to the CSV file
    write_to_csv(data)
    return jsonify({"message": "Data saved successfully"}), 200

@user_bp.route('/get-users', methods=['GET'])
def get_users():
    """Retrieve all user data from the CSV file."""
    users = read_from_csv()
    return jsonify(users), 200

@user_bp.route('/create', methods=['POST'])
def create_user():
    """
    Endpoint to create a new user.
    Expects JSON data with 'full_name' and 'questions'.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided."}), 400

    full_name = data.get('full_name')
    questions = data.get('questions')  # Should be a dict with 10 questions

    if not full_name or not questions:
        return jsonify({"message": "Full name and questions are required."}), 400

    # Validate that there are exactly ten questions
    if not isinstance(questions, dict) or len(questions) != 10:
        return jsonify({"message": "Exactly ten questions must be provided in a dictionary."}), 400

    user_id = User.create_user(full_name, questions)

    return jsonify({"message": "User created successfully.", "user_id": str(user_id.inserted_id)}), 201


@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Endpoint to retrieve a user's information by their ID.
    """
    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    # Convert ObjectId to string for JSON serialization
    user_data = {
        "user_id": str(user["_id"]),
        "full_name": user["full_name"],
        "questions": user["questions"],
        "created_at": user["created_at"].isoformat() + 'Z',
        "updated_at": user["updated_at"].isoformat() + 'Z'
    }

    return jsonify({"user": user_data}), 200


@user_bp.route('/<user_id>/update', methods=['PUT'])
def update_user(user_id):
    """
    Endpoint to update a user's answers to the questions.
    Expects JSON data with 'questions'.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided."}), 400

    updated_questions = data.get('questions')  # Should be a dict with 10 questions

    if not updated_questions:
        return jsonify({"message": "Questions data is required for update."}), 400

    # Validate that there are exactly ten questions
    if not isinstance(updated_questions, dict) or len(updated_questions) != 10:
        return jsonify({"message": "Exactly ten questions must be provided in a dictionary."}), 400

    success = User.update_user_questions(user_id, updated_questions)
    if not success:
        return jsonify({"message": "User not found or update failed."}), 404

    return jsonify({"message": "User questions updated successfully."}), 200


@user_bp.route('/<user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
    """
    Endpoint to delete a user by their ID.
    """
    success = User.delete_user(user_id)
    if not success:
        return jsonify({"message": "User not found or deletion failed."}), 404

    return jsonify({"message": "User deleted successfully."}), 200


@user_bp.route('/', methods=['GET'])
def list_users():
    """
    Endpoint to list all users.
    """
    users = User.get_all_users()
    users_data = []
    for user in users:
        users_data.append({
            "user_id": str(user["_id"]),
            "full_name": user["full_name"],
            "questions": user["questions"],
            "created_at": user["created_at"].isoformat() + 'Z',
            "updated_at": user["updated_at"].isoformat() + 'Z'
        })

    return jsonify({"users": users_data}), 200


@user_bp.route('/<user_id>/matches', methods=['GET'])
def get_matches(user_id):
    """
    Endpoint to retrieve matched users for a given user.
    """
    matches = match_users(user_id)
    if matches is None:
        return jsonify({"message": "User not found."}), 404

    return jsonify({"matches": matches}), 200
