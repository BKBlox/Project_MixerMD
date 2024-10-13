from extensions import mongo  # Changed from 'from app import mongo'
from bson.objectid import ObjectId
from datetime import datetime

class GameSession:
    @staticmethod
    def create_session(user_id, story):
        """
        Creates a new game session with a single user and their story.
        """
        session = {
            "user1_id": ObjectId(user_id),
            "user2_id": None,
            "story1": story,
            "story2": None,
            "emoji_story1": None,  # Emoji version of story1 by user2
            "emoji_story2": None,  # Emoji version of story2 by user1
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "waiting"  # 'waiting', 'matched', 'completed'
        }
        result = mongo.db.game_sessions.insert_one(session)
        return result.inserted_id

    @staticmethod
    def find_waiting_session(exclude_user_id):
        """
        Finds a session that's waiting for a second user, excluding the current user.
        """
        return mongo.db.game_sessions.find_one({
            "status": "waiting",
            "user1_id": {"$ne": ObjectId(exclude_user_id)}
        })

    @staticmethod
    def join_session(session_id, user_id, story):
        """
        Adds the second user and their story to an existing session.
        """
        result = mongo.db.game_sessions.update_one(
            {"_id": ObjectId(session_id), "status": "waiting"},
            {
                "$set": {
                    "user2_id": ObjectId(user_id),
                    "story2": story,
                    "status": "matched",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    @staticmethod
    def get_session_by_user(user_id):
        """
        Retrieves a session involving the specified user.
        """
        return mongo.db.game_sessions.find_one({
            "$or": [
                {"user1_id": ObjectId(user_id)},
                {"user2_id": ObjectId(user_id)}
            ]
        })

    @staticmethod
    def submit_emoji_story(session_id, user_id, emoji_story):
        """
        Submits the emoji version of the partner's story.
        """
        session = mongo.db.game_sessions.find_one({"_id": ObjectId(session_id)})
        if not session:
            return False

        updates = {"updated_at": datetime.utcnow()}

        if session['user1_id'] == ObjectId(user_id) and not session.get('emoji_story2'):
            updates['emoji_story2'] = emoji_story
        elif session['user2_id'] == ObjectId(user_id) and not session.get('emoji_story1'):
            updates['emoji_story1'] = emoji_story
        else:
            return False  # Invalid user or emoji story already submitted

        # Check if both emoji stories are submitted
        if session.get('emoji_story1') and session.get('emoji_story2'):
            updates['status'] = 'completed'

        result = mongo.db.game_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": updates}
        )
        return result.modified_count > 0

    @staticmethod
    def get_partner_story(session_id, user_id):
        """
        Retrieves the partner's original story.
        """
        session = mongo.db.game_sessions.find_one({"_id": ObjectId(session_id)})
        if not session:
            return None

        if session['user1_id'] == ObjectId(user_id):
            return session.get('story2')
        elif session['user2_id'] == ObjectId(user_id):
            return session.get('story1')
        else:
            return None

    @staticmethod
    def get_emoji_story(session_id, user_id):
        """
        Retrieves the emoji version of the user's own story created by the partner.
        """
        session = mongo.db.game_sessions.find_one({"_id": ObjectId(session_id)})
        if not session:
            return None

        if session['user1_id'] == ObjectId(user_id):
            return session.get('emoji_story1')
        elif session['user2_id'] == ObjectId(user_id):
            return session.get('emoji_story2')
        else:
            return None