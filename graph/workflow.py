from langgraph.graph import StateGraph, END
from graph.state import CopilotState

from graph.nodes.memory_read import memory_read_node
from graph.nodes.memory_filter import memory_filter_node
from graph.nodes.prompt_builder import prompt_builder_node
from graph.nodes.llm_node import llm_node
from graph.nodes.memory_write import memory_write_node


def build_graph():
    workflow = StateGraph(CopilotState)

    workflow.add_node("memory_read", memory_read_node)
    workflow.add_node("memory_filter", memory_filter_node)
    workflow.add_node("prompt_builder", prompt_builder_node)
    workflow.add_node("llm", llm_node)
    workflow.add_node("memory_write", memory_write_node)

    workflow.set_entry_point("memory_read")

    workflow.add_edge("memory_read", "memory_filter")
    workflow.add_edge("memory_filter", "prompt_builder")
    workflow.add_edge("prompt_builder", "llm")
    workflow.add_edge("llm", "memory_write")
    workflow.add_edge("memory_write", END)

    return workflow.compile()
