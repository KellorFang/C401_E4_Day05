"""
Main Module for LangGraph Agent
Quản lý luồng hội thoại, định nghĩa State và các Node làm việc (Reasoning, Routing).
"""

from typing import TypedDict, Annotated, List, Any
import operator

# 1. State Schema:
# Định nghĩa State và logic reducer (operator.add) cho history để ngăn vấn đề State Inconsistency
class AgentState(TypedDict):
    conversation_history: Annotated[List[str], operator.add]
    current_intent: str
    retrieved_context: str
    iteration_count: int

# 2. Nodes:
def intent_classifier_node(state: AgentState) -> AgentState:
    """Phân loại ý định của sinh viên để chuyển hướng (Routing)."""
    # TODO: Dùng LLM và Pydantic để xuất ra Intent chuẩn
    pass

def reasoning_node(state: AgentState) -> AgentState:
    """Đưa ra câu trả lời cuối cùng hoặc gợi ý (Augmentation)."""
    # TODO: Bọc LLM lấy context + history tạo câu trả lời
    pass

def retrieve_slide_node(state: AgentState) -> AgentState:
    """Lấy kiến thức từ RAG Tool."""
    pass

def web_search_node(state: AgentState) -> AgentState:
    """Lấy thông tin từ Web Search Tool."""
    pass

def github_tool_node(state: AgentState) -> AgentState:
    """Đọc assignment từ Github repo."""
    pass

# 3. Routing Edges:
def route_intent(state: AgentState) -> str:
    """Dựa vào current_intent trả về string tên node tiếp theo."""
    # TODO: Trả về "retrieve_slide_node", "web_search_node", v.v.
    # TODO: Khống chế (Recursion limit) chặn lặp vô tận bằng state.iteration_count
    pass

# 4. Graph Construction (Pseudocode)
# graph = StateGraph(AgentState)
# graph.add_node("intent", intent_classifier_node)
# graph.add_node("reasoning", reasoning_node)
# ... setting up conditional edges
# app = graph.compile()
