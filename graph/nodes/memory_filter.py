from graph.state import CopilotState


def memory_filter_node(state: CopilotState) -> CopilotState:
    """
    Node 2: Memory Filter

    Responsibilities:
    - Apply relevance filtering
    - Avoid injecting unnecessary memory
    - Prepare clean filtered_memory for prompt construction
    """

    user_input = state.get("user_input", "").lower()
    retrieved = state.get("retrieved_memory", {})

    filtered = {}

    # 1️⃣ Include goal only if exam/prepare context appears
    goals = retrieved.get("goals", {})
    if goals.get("primary_goal"):
        if "exam" in user_input or "prepare" in user_input:
            filtered["goal_context"] = goals

    # 2️⃣ Include weak topics only if relevant to current query
    weak_topics = retrieved.get("weak_topics", [])
    relevant_weak_topics = []

    for topic in weak_topics:
        if topic.lower() in user_input:
            relevant_weak_topics.append(topic)

    if relevant_weak_topics:
        filtered["weak_topics"] = relevant_weak_topics

    # 3️⃣ Always include learning preferences (low risk memory)
    preferences = retrieved.get("learning_preferences", {})
    if preferences:
        filtered["learning_preferences"] = preferences

    # 4️⃣ Include session memory if exists
    session_memory = retrieved.get("session_memory", {})
    if session_memory:
        filtered["session_memory"] = session_memory

    state["filtered_memory"] = filtered

    # Debug visibility
    print("\n=== MEMORY FILTER NODE ===")
    print("Filtered Memory:", filtered)

    return state
