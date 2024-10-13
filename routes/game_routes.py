from flask import Blueprint, request, jsonify
from models.game_session import GameSession
from models.user import User
from bson.objectid import ObjectId

game_bp = Blueprint('game', __name__)

@game_bp.route('/submit-story', methods=['POST'])
def submit_story():
    """
    User submits a story and gets matched with another user.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    user_id = data.get('user_id')
    story = data.get('story')

    if not user_id or not story:
        return jsonify({"message": "User ID and story are required"}), 400

    # Validate user existence
    if not User.get_user_by_id(user_id):
        return jsonify({"message": "User not found"}), 404

    # Check if user is already in a session
    existing_session = GameSession.get_session_by_user(user_id)
    if existing_session:
        return jsonify({"message": "User is already in a game session"}), 400

    # Try to find a waiting session
    waiting_session = GameSession.find_waiting_session(user_id)
    if waiting_session:
        # Join the session
        success = GameSession.join_session(waiting_session['_id'], user_id, story)
        if success:
            session_id = str(waiting_session['_id'])
            return jsonify({"message": "Matched with another user", "session_id": session_id}), 200
        else:
            return jsonify({"message": "Failed to join session"}), 500
    else:
        # Create a new session
        session_id = GameSession.create_session(user_id, story)
        return jsonify({"message": "Waiting for another user", "session_id": str(session_id)}), 200

@game_bp.route('/<session_id>/partner-story', methods=['GET'])
def get_partner_story(session_id):
    """
    Retrieves the partner's original story.
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    story = GameSession.get_partner_story(session_id, user_id)
    if story:
        return jsonify({"partner_story": story}), 200
    else:
        return jsonify({"message": "Partner's story not available yet"}), 404

@game_bp.route('/<session_id>/submit-emoji', methods=['POST'])
def submit_emoji(session_id):
    """
    User submits the emoji version of the partner's story.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    user_id = data.get('user_id')
    emoji_story = data.get('emoji_story')

    if not user_id or not emoji_story:
        return jsonify({"message": "User ID and emoji story are required"}), 400

    success = GameSession.submit_emoji_story(session_id, user_id, emoji_story)
    if success:
        return jsonify({"message": "Emoji story submitted"}), 200
    else:
        return jsonify({"message": "Failed to submit emoji story"}), 500

@game_bp.route('/<session_id>/emoji-story', methods=['GET'])
def get_emoji_story(session_id):
    """
    Retrieves the emoji version of the user's own story.
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    emoji_story = GameSession.get_emoji_story(session_id, user_id)
    if emoji_story:
        return jsonify({"emoji_story": emoji_story}), 200
    else:
        return jsonify({"message": "Emoji story not available yet"}), 404


@game_bp.route('/<session_id>/guess', methods=['POST'])
def guess_emoji_story(session_id):
    """
    User guesses which emoji story matches their original story.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    user_id = data.get('user_id')
    guessed_user_id = data.get('guessed_user_id')

    if not user_id or not guessed_user_id:
        return jsonify({"message": "User ID and guessed user ID are required"}), 400

    # Check if the guessed emoji story matches the user's original story
    correct = GameSession.check_guess(session_id, user_id, guessed_user_id)

    if correct:
        return jsonify({"message": "Correct guess!", "result": "win"}), 200
    else:
        return jsonify({"message": "Incorrect guess", "result": "lose"}), 200