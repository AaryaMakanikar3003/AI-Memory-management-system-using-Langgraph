AI Memory Management System using LangGraph

An intelligent memory-enabled conversational system built using a LangGraph-style node orchestration architecture. The system maintains persistent per-user memory, supports structured information extraction, and enables adaptive multi-turn LLM responses.

🚀 Overview
This project implements a modular graph-based conversational architecture where:
Each node performs a defined responsibility (LLM call, memory read/write, state update).
User memory is stored persistently in JSON format.
Structured information (e.g., goals, exam dates, weak topics) is extracted and retained.
Responses are dynamically generated using Groq/OpenAI models.
Multi-turn conversations are supported with contextual continuity.

🧠 Key Features
Persistent per-user memory storage
Explicit memory read and write nodes
Structured information extraction pipeline
Modular graph-based orchestration
Scalable architecture for advanced workflows
Clean separation of state, memory, and LLM layers

📂 Project structure
AI-Memory-management-system-using-Langgraph/
|
|-- app.py
|-- workflow.py
|-- state.py
|-- llm_node.py
|
|-- graph/
|   |-- __init__.py
|   |-- (graph node modules)
|
|-- memory/
|   |-- long_term_store.py
|   |-- user_data/
|       |-- student_001.json
|
|-- evaluation/
|
|-- .gitignore
`-- README.md


⚙️ Architecture
The system follows a graph-based orchestration model:
User Input
Memory Read Node
Structured Extraction Node
LLM Response Node
Memory Write Node
Final Output
Each node operates on a shared state object, enabling controlled data flow and modular extensibility.

🛠️ Technologies Used
Python 3.10+
LangGraph-style orchestration
OpenAI / Groq LLM APIs
JSON-based persistent storage]

▶️ How to Run
Clone the repository:
git clone https://github.com/your-username/AI-Memory-management-using-Langgraph.git

Navigate into the project directory:
cd AI-Memory-management-using-Langgraph

Install dependencies:
pip install -r requirements.txt

Add your API key in a .env file:
OPENAI_API_KEY=your_key_here

Run the application:
python app.py

📌 Use Cases
Personalized AI study assistant
Long-term conversational agents
Context-aware tutoring systems
Memory-enabled chatbot frameworks
Structured knowledge tracking






