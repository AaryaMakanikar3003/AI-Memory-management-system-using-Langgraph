import os
import json
import re
from datetime import datetime
from graph.state import CopilotState


MEMORY_DIR = "memory/user_data"


def memory_write_node(state: CopilotState) -> CopilotState:

    user_id = state.get("user_id", "student_001")
    user_input_raw = state.get("user_input", "")
    user_input = user_input_raw.lower()

    file_path = os.path.join(MEMORY_DIR, f"{user_id}.json")

    # ----------------------------
    # Load Memory
    # ----------------------------
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            memory_data = json.load(f)
    else:
        memory_data = {
            "user_id": user_id,
            "long_term_memory": {
                "goals": {
                    "primary_goal": None,
                    "exam_date": None
                },
                "weak_topics": [],
                "learning_preferences": {
                    "explanation_style": None,
                    "likes_examples": False
                },
                "history_summary": None
            },
            "metadata": {}
        }

    long_term = memory_data["long_term_memory"]

    # =====================================================
    # 1️⃣ EXAM + DATE EXTRACTION (ROBUST)
    # =====================================================

    if "exam" in user_input:

        # Date patterns supported:
        # 20 june 2026
        # june 20 2026
        # 20/06/2026
        # 20-06-2026
        date_patterns = [
            r"\d{1,2}\s+(jan|feb|march|april|may|june|july|aug|sep|oct|nov|dec)[a-z]*\s*\d{0,4}",
            r"(jan|feb|march|april|may|june|july|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}\s*\d{0,4}",
            r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        ]

        extracted_date = None

        for pattern in date_patterns:
            match = re.search(pattern, user_input)
            if match:
                extracted_date = match.group(0)
                break

        if extracted_date:
            long_term["goals"]["exam_date"] = extracted_date
            goal_text = user_input.replace(extracted_date, "")
        else:
            goal_text = user_input

        # Clean goal text intelligently
        goal_text = re.sub(r"i have|i am preparing for|my|an|a", "", goal_text)
        goal_text = re.sub(r"\s+", " ", goal_text).strip()

        long_term["goals"]["primary_goal"] = goal_text

    # =====================================================
    # 2️⃣ WEAK TOPIC EXTRACTION (ROBUST PATTERNS)
    # =====================================================

    weak_patterns = [

        # I struggle with X
        r"struggle with (.*)",

        # I am weak in X
        r"weak in (.*)",

        # I don't understand X
        r"don't understand (.*)",
        r"dont understand (.*)",

        # I find X difficult
        r"find (.*?) (very )?difficult",

        # X is difficult
        r"(.*?) is (very )?difficult"
    ]

    for pattern in weak_patterns:
        matches = re.findall(pattern, user_input)

        for match in matches:

            # Some regex return tuples
            if isinstance(match, tuple):
                topic_part = match[0]
            else:
                topic_part = match

            topic_part = topic_part.strip()

            # Remove trailing phrases
            topic_part = re.sub(r"to understand.*", "", topic_part)
            topic_part = topic_part.strip()

            # Split multiple topics
            topics = re.split(r",|and", topic_part)

            for topic in topics:
                topic = topic.strip()

                if topic and topic not in long_term["weak_topics"]:
                    long_term["weak_topics"].append(topic)

    # =====================================================
    # 3️⃣ UPDATE METADATA
    # =====================================================

    memory_data["metadata"]["last_updated"] = datetime.utcnow().isoformat()

    with open(file_path, "w") as f:
        json.dump(memory_data, f, indent=4)

    print("\n=== MEMORY WRITE NODE ===")
    print("Updated Memory:", long_term)

    return state
