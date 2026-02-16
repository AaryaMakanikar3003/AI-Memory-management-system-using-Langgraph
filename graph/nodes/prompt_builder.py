from graph.state import CopilotState


def prompt_builder_node(state: CopilotState) -> CopilotState:
    """
    Node 3: Prompt Construction

    Responsibilities:
    - Build structured prompt
    - Inject filtered memory explicitly
    - Keep memory influence transparent
    """

    user_input = state.get("user_input", "")
    memory = state.get("filtered_memory", {})

    prompt_sections = []
    prompt_sections.append("You are an educational AI assistant helping a student.\n")

    # Inject Goal Context
    if "goal_context" in memory:
        goal = memory["goal_context"].get("primary_goal")
        exam_date = memory["goal_context"].get("exam_date")

        prompt_sections.append("Student Goal Context:")
        if goal:
            prompt_sections.append(f"- Primary Goal: {goal}")
        if exam_date:
            prompt_sections.append(f"- Exam Date: {exam_date}")
        prompt_sections.append("")

    # Inject Weak Topics
    if "weak_topics" in memory:
        prompt_sections.append("Student Weak Topics:")
        for topic in memory["weak_topics"]:
            prompt_sections.append(f"- {topic}")
        prompt_sections.append("")

    # Inject Learning Preferences
    if "learning_preferences" in memory:
        prefs = memory["learning_preferences"]
        prompt_sections.append("Learning Preferences:")
        for key, value in prefs.items():
            if value:
                prompt_sections.append(f"- {key}: {value}")
        prompt_sections.append("")

    # Inject Session Memory (if any)
    if "session_memory" in memory:
        prompt_sections.append("Session Context:")
        for key, value in memory["session_memory"].items():
            prompt_sections.append(f"- {key}: {value}")
        prompt_sections.append("")

    # Add Current User Question
    prompt_sections.append("Current Question:")
    prompt_sections.append(user_input)
    prompt_sections.append("\nProvide a clear, helpful, and adaptive explanation.")

    final_prompt = "\n".join(prompt_sections)

    state["constructed_prompt"] = final_prompt

    # Debug visibility
    print("\n=== PROMPT BUILDER NODE ===")
    print("Constructed Prompt:\n", final_prompt)

    return state
