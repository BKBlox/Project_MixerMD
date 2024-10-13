# utils/helpers.py

from models.user import User


def match_users(target_user_id):
    """
    Matches the target user with other users based on their answers.
    Returns a list of matched users with their matching scores.
    If the target user does not exist, returns None.
    """
    target_user = User.get_user_by_id(target_user_id)
    if not target_user:
        return None

    all_users = User.get_all_users()
    matches = []

    target_questions = target_user.get("questions", {})

    for user in all_users:
        if str(user["_id"]) == target_user_id:
            continue  # Skip matching with self

        user_questions = user.get("questions", {})
        score = 0

        # Simple matching logic: increment score for each matching answer
        for q_num in range(1, 11):
            q_key = f"question_{q_num}"
            if target_questions.get(q_key) and target_questions.get(q_key) == user_questions.get(q_key):
                score += 1

        # Define a threshold for matching (e.g., at least 5 matching answers)
        if score >= 5:
            matches.append({
                "user_id": str(user["_id"]),
                "full_name": user.get("full_name", "N/A"),
                "score": score
            })

    return matches
