from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class WorkflowState(TypedDict, total=False):
    market: Annotated[Sequence[BaseMessage], add_messages]
    market_sources: Annotated[Sequence[BaseMessage], add_messages]
    company: Annotated[Sequence[BaseMessage], add_messages]
    company_sources: Annotated[Sequence[BaseMessage], add_messages]        
    selected_country: Annotated[Sequence[BaseMessage], add_messages]
    selection_results: Annotated[Sequence[BaseMessage], add_messages]
    competitors: Annotated[Sequence[BaseMessage], add_messages]
    competitors_sources: Annotated[Sequence[BaseMessage], add_messages]     
    partners: Annotated[Sequence[BaseMessage], add_messages]
    partners_sources: Annotated[Sequence[BaseMessage], add_messages]     
    report: Annotated[Sequence[BaseMessage], add_messages]