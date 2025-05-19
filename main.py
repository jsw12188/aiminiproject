import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_core.messages import AIMessage
import ast

from agent.market_analysis_agent import MarketAnalysisAgent
from agent.company_analysis_agent import CompanyAnalysisAgent
from agent.region_selection_agent import RegionSelectionAgent
from agent.competition_analysis_agent import CompetitionAnalysisAgent
from agent.partner_analysis_agent import PartnerAnalysisAgent
from agent.report_writing_agent import ReportWritingAgent

from langgraph.graph import StateGraph, START, END
from state import WorkflowState

load_dotenv()
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")
search = TavilySearchResults()

company_name = input("분석할 기업명을 입력하세요: ").strip()
countries = ["United States", "China"]

# 에이전트 초기화
market_agent = MarketAnalysisAgent(llm, search)
company_agent = CompanyAnalysisAgent(llm, search)
region_agent = RegionSelectionAgent(llm)
competition_agent = CompetitionAnalysisAgent(llm, search)
partner_agent = PartnerAnalysisAgent(llm, search)
report_agent = ReportWritingAgent(llm)

# LangGraph 노드 함수 정의
def market_node(state):
    market_results = {}
    for country in countries:
        market_results[country] = market_agent.run(country)
    # dict를 string으로 감싸서 메시지에 저장
    return {"market": [AIMessage(content=str(market_results))]}

def company_node(state):
    company_result = company_agent.run(company_name)
    return {"company": [AIMessage(content=company_result)]}

def selection_node(state):
    import re
    import ast
    market_results = ast.literal_eval(state["market"][0].content)
    company_result = state["company"][0].content
    try:
        strength_block = company_result.split("- 약점:")[0].replace("- 강점:", "").strip()
        weakness_block = company_result.split("- 약점:")[1].strip()
    except:
        strength_block = company_result
        weakness_block = ""
    selection_results = {}
    scores = []
    for country in countries:
        pestel = market_results[country]
        suitability = region_agent.run(country, strength_block, weakness_block, pestel)
        selection_results[country] = suitability
        m = re.search(r'총합[^\d]*(\d+)[^\d]*점', suitability)
        score = int(m.group(1)) if m else 0
        scores.append((country, score, suitability))
    top_country = max(scores, key=lambda x: x[1])[0]
    print("DEBUG selection_results (in node):", selection_results)
    return {
        "selected_country": [AIMessage(content=top_country)],
        "selection_results": [AIMessage(content=str(selection_results))]
    }

def competition_node(state):
    country = state["selected_country"][0].content
    result = competition_agent.run(country)
    return {"competitors": [AIMessage(content=result)]}

def partner_node(state):
    country = state["selected_country"][0].content
    result = partner_agent.run(country)
    return {"partners": [AIMessage(content=result)]}

def report_node(state):
    company_result = state["company"][0].content
    market_result = ast.literal_eval(state["market"][0].content)
    selection_results_raw = state.get("selection_results", [AIMessage(content="{}")])[0].content
    selection_results = ast.literal_eval(selection_results_raw)
    country = state["selected_country"][0].content

    # 키 보정
    if country not in selection_results:
        for k in selection_results.keys():
            if country in k:
                country_key = k
                break
        else:
            raise KeyError(f"{country} not found in selection_results: {selection_results.keys()}")
    else:
        country_key = country

    competitors = state["competitors"][0].content
    partners = state["partners"][0].content
    report = report_agent.run(
        company=company_result,
        market=f"## {country}\n{market_result[country]}",
        selection=selection_results[country_key],  # ★ 반드시 country_key로!
        competitors=f"## {country}\n{competitors}",
        partners=f"## {country}\n{partners}"
    )
    with open("final_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("\n✅ 전략 보고서가 'final_report.md'에 저장되었습니다.")
    print("DEBUG selection_results_raw (in report):", selection_results_raw)
    print("DEBUG selection_results (in report):", selection_results)
    print("DEBUG country:", country)
    return {"report": [AIMessage(content=report)]}


# LangGraph 워크플로우 정의
g = StateGraph(WorkflowState)
g.add_node("market_node", market_node)
g.add_node("company_node", company_node)
g.add_node("selection_node", selection_node)
g.add_node("competition_node", competition_node)
g.add_node("partner_node", partner_node)
g.add_node("report_node", report_node)

g.add_edge(START, "market_node")
g.add_edge("market_node", "company_node")
g.add_edge("company_node", "selection_node")
g.add_edge("selection_node", "competition_node")
g.add_edge("competition_node", "partner_node")
g.add_edge("partner_node", "report_node")
g.add_edge("report_node", END)

workflow = g.compile()

if __name__ == "__main__":
    workflow.invoke({})
