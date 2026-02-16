import os
import json
from datetime import datetime

# Base directory for storing user JSON files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_DIR = os.path.join(BASE_DIR, "user_data")

# Ensure directory exists
os.makedirs(USER_DATA_DIR, exist_ok=True)


def _get_user_file_path(user_id: str) -> str:
    """Return file path for a specific user."""
    return os.path.join(USER_DATA_DIR, f"{user_id}.json")


def _default_memory_schema(user_id: str) -> dict:
    """Return default long-term memory structure for new users."""
    return {
        "user_id": user_id,
        "long_term_memory": {
            "goals": {
                "primary_goal": None,
                "exam_date": None,
            },
            "weak_topics": [],
            "learning_preferences": {
                "explanation_style": None,
                "likes_examples": False,
            },
            "history_summary": None,
        },
        "metadata": {
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat(),
        }
    }

def load_long_term_memory(user_id: str) -> dict:
    """
    Load user long-term memory from JSON.
    If not exists, create default schema.
    """
    file_path = _get_user_file_path(user_id)

    if not os.path.exists(file_path):
        memory = _default_memory_schema(user_id)
        save_long_term_memory(user_id, memory)
        return memory

    with open(file_path, "r") as f:
        return json.load(f)

def save_long_term_memory(user_id: str, memory: dict) -> None:
    """
    Save user long-term memory to JSON.
    """
    file_path = _get_user_file_path(user_id)

    memory["metadata"]["last_updated"] = datetime.utcnow().isoformat()

    with open(file_path, "w") as f:
        json.dump(memory, f, indent=4)
