from graph.workflow import build_graph

def main():
    graph = build_graph()

    user_id = "student_001"

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        initial_state = {
            "user_id": user_id,
            "user_input": user_input,
            "session_memory": {}
        }

        result = graph.invoke(initial_state)

        print("\nAssistant:", result.get("llm_response"))


if __name__ == "__main__":
    main()
