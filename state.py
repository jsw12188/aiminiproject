from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class WorkflowState(TypedDict, total=False):
    
    # 1. 시장 분석 에이전트 (국가별 PESTEL 분석)
    market: Annotated[Sequence[BaseMessage], add_messages]
    
    # 2. 기업 분석 에이전트 (대상 기업 SWOT 분석)
    company: Annotated[Sequence[BaseMessage], add_messages]
    
    # 3. 진출 지역 선정 에이전트 (최종 진출 지역 선별)
    selected_country: Annotated[Sequence[BaseMessage], add_messages]
    
    # 4. 경쟁 분석 에이전트 (진출 지역 경쟁 환경 분석)
    competitors: Annotated[Sequence[BaseMessage], add_messages]
    
    # 5. 파트너 에이전트 (진출 지역 내 파트너 분석)
    partners: Annotated[Sequence[BaseMessage], add_messages]
    
    # 6. 최종 보고서 에이전트 (전략 수립 및 보고서 작성)
    report: Annotated[Sequence[BaseMessage], add_messages]