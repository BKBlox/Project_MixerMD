# routes/test_routes.py

from flask import Blueprint, jsonify
from extensions import mongo

test_bp = Blueprint('test', __name__)


@test_bp.route('/test-db', methods=['GET'])
def test_db():
    """
    Test route to verify MongoDB connection.
    Inserts a test document and retrieves it.
    """
    # Insert a test document
    test_data = {"test_key": "test_value"}
    try:
        insert_result = mongo.db.test_collection.insert_one(test_data)
    except Exception as e:
        return jsonify({"message": "Insertion failed.", "error": str(e)}), 500

    # Retrieve the test document
    try:
        retrieved_data = mongo.db.test_collection.find_one({"_id": insert_result.inserted_id})
    except Exception as e:
        return jsonify({"message": "Retrieval failed.", "error": str(e)}), 500

    # Clean up by deleting the test document
    try:
        mongo.db.test_collection.delete_one({"_id": insert_result.inserted_id})
    except Exception as e:
        return jsonify({"message": "Cleanup failed.", "error": str(e)}), 500

    # Prepare the response
    response = {
        "inserted_id": str(insert_result.inserted_id),
        "retrieved_data": {
            "_id": str(retrieved_data["_id"]),
            "test_key": retrieved_data["test_key"]
        }
    }

    return jsonify(response), 200
