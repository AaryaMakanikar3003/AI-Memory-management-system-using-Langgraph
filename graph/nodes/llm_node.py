import os
from openai import OpenAI
from graph.state import CopilotState
from dotenv import load_dotenv
load_dotenv()


# Choose provider: "groq" or "openai"
LLM_PROVIDER = "groq"

def llm_node(state: CopilotState) -> CopilotState:
    """
    Node 4: LLM Response Generation

    Supports:
    - Groq (OpenAI-compatible)
    - OpenAI
    """

    prompt = state.get("constructed_prompt", "")

    if LLM_PROVIDER == "groq":
        # client = OpenAI(
        #     api_key=os.getenv("GROQ_API_KEY"),
        #     base_url="https://api.groq.com/openai/v1"
        # )
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        model_name = "openai/gpt-oss-120b"

    elif LLM_PROVIDER == "openai":
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        model_name = "gpt-4o-mini"

    else:
        raise ValueError("Invalid LLM_PROVIDER")

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    state["llm_response"] = response.choices[0].message.content

    print("\n=== LLM NODE ===")
    print("Model Used:", model_name)
    print("Response:\n", state["llm_response"])

    return state
