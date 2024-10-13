# models/user.py

from app import mongo
from bson.objectid import ObjectId
from datetime import datetime


class User:
    @staticmethod
    def create_user(full_name, questions):
        """
        Creates a new user with the provided full name and questions.
        """
        user = {
            "full_name": full_name,
            "questions": questions,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return mongo.db.users.insert_one(user)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user by their unique ID.
        """
        try:
            return mongo.db.users.find_one({"_id": ObjectId(user_id)})
        except:
            return None

    @staticmethod
    def get_all_users():
        """
        Retrieves all users from the database.
        """
        return list(mongo.db.users.find())

    @staticmethod
    def update_user_questions(user_id, updated_questions):
        """
        Updates the answers to the questions for a specific user.
        """
        try:
            result = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "questions": updated_questions,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except:
            return False

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user from the database.
        """
        try:
            result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False
