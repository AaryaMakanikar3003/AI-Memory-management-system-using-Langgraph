from graph.state import CopilotState
from memory.long_term_store import load_long_term_memory


def memory_read_node(state: CopilotState) -> CopilotState:
    """
    Node 1: Memory Read

    Responsibilities:
    - Load persistent user memory (full JSON structure)
    - Attach full object for safe future writes
    - Prepare structured retrieved_memory
    """

    user_id = state.get("user_id")
    user_input = state.get("user_input", "")

    # 1️⃣ Load full persistent object
    persistent_data = load_long_term_memory(user_id)

    # Store full object separately (for safe writing later)
    state["persistent_memory"] = persistent_data

    # Extract only long_term_memory section for runtime use
    long_term_memory = persistent_data.get("long_term_memory", {})

    state["long_term_memory"] = long_term_memory

    # 2️⃣ Prepare retrieved memory (raw, unfiltered)
    state["retrieved_memory"] = {
        "user_input": user_input,
        "goals": long_term_memory.get("goals", {}),
        "weak_topics": long_term_memory.get("weak_topics", []),
        "learning_preferences": long_term_memory.get("learning_preferences", {}),
        "history_summary": long_term_memory.get("history_summary"),
        "session_memory": state.get("session_memory", {})
    }

    # Debug visibility
    print("\n=== MEMORY READ NODE ===")
    print("Persistent Metadata:", persistent_data.get("metadata", {}))
    print("Retrieved Memory:", state["retrieved_memory"])

    return state
