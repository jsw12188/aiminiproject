import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_core.messages import AIMessage

from agent.market_analysis_agent import MarketAnalysisAgent
from agent.company_analysis_agent import CompanyAnalysisAgent
from agent.region_selection_agent import RegionSelectionAgent
from agent.competition_analysis_agent import CompetitionAnalysisAgent
from agent.partner_analysis_agent import PartnerAnalysisAgent
from agent.report_writing_agent import ReportWritingAgent

from langgraph.graph import StateGraph, START, END
from state import WorkflowState
from prompt_templates import REPORT_WRITING_PROMPT

import markdown
import pdfkit

load_dotenv()
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")
search = TavilySearchResults()

company_name = input("분석할 기업명을 입력하세요: ").strip()
countries = ["United States", "China"]

market_agent = MarketAnalysisAgent(llm, search)
company_agent = CompanyAnalysisAgent(llm, search)
region_agent = RegionSelectionAgent(llm)
competition_agent = CompetitionAnalysisAgent(llm, search)
partner_agent = PartnerAnalysisAgent(llm, search)
report_agent = ReportWritingAgent(llm)

def market_node(state):
    market_results = {}
    market_sources = []
    for country in countries:
        out = market_agent.run(country)
        market_results[country] = out["summary"]
        for t, url in out["sources"]:
            market_sources.append((country, t, url))
    return {
        "market": [AIMessage(content=json.dumps(market_results))],
        "market_sources": [AIMessage(content=json.dumps(market_sources))]
    }

def company_node(state):
    out = company_agent.run(company_name)
    return {
        "company": [AIMessage(content=out["summary"])],
        "company_sources": [AIMessage(content=json.dumps(out["sources"]))]
    }

def selection_node(state):
    import re
    market_results = json.loads(state["market"][0].content)
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
    return {
        "selected_country": [AIMessage(content=top_country)],
        "selection_results": [AIMessage(content=json.dumps(selection_results))]
    }

def competition_node(state):
    country = state["selected_country"][0].content
    out = competition_agent.run(country)
    return {
        "competitors": [AIMessage(content=out["summary"])],
        "competitors_sources": [AIMessage(content=json.dumps(out["sources"]))]
    }

def partner_node(state):
    country = state["selected_country"][0].content
    out = partner_agent.run(country)
    return {
        "partners": [AIMessage(content=out["summary"])],
        "partners_sources": [AIMessage(content=json.dumps(out["sources"]))]
    }

def report_node(state):
    market_result = json.loads(state["market"][0].content)
    market_sources = json.loads(state["market_sources"][0].content)
    company_result = state["company"][0].content
    company_sources = json.loads(state["company_sources"][0].content)
    selection_results_raw = state.get("selection_results", [AIMessage(content="{}")])[0].content
    selection_results = json.loads(selection_results_raw)
    country = state["selected_country"][0].content
    competitors = state["competitors"][0].content
    competitors_sources = json.loads(state["competitors_sources"][0].content)
    partners = state["partners"][0].content
    partners_sources = json.loads(state["partners_sources"][0].content)

    if country not in selection_results:
        for k in selection_results.keys():
            if country in k:
                country_key = k
                break
        else:
            raise KeyError(f"{country} not found in selection_results: {selection_results.keys()}")
    else:
        country_key = country

    # 출처 모으기 (market/company/competitors/partners)
    ref_md = ""
    for c, t, url in market_sources:
        ref_md += f"- [시장][{c}] {t}: <{url}>\n"
    for t, url in company_sources:
        ref_md += f"- [기업] {t}: <{url}>\n"
    for t, url in competitors_sources:
        ref_md += f"- [경쟁사] {t}: <{url}>\n"
    for t, url in partners_sources:
        ref_md += f"- [파트너] {t}: <{url}>\n"
    if not ref_md:
        ref_md = "- (자료 및 출처는 현재 제공된 링크의 정보를 활용합니다. 보다 구체적인 자료는 최신 데이터와 보고서를 참고하십시오.)"

    market_compare = ""  # PESTEL 비교 등 원하는 내용 구현
    report = llm.invoke(REPORT_WRITING_PROMPT.format(
        company=company_result,
        market=market_compare,
        selection=selection_results[country_key],
        competitors=competitors,
        partners=partners,
        references=ref_md
    )).content

    with open("final_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    style = """
            <style>
            body {
                font-family: "Malgun Gothic", "Nanum Gothic", "Apple SD Gothic Neo", sans-serif;
                line-height: 1.6;
                font-size: 14px;
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            table, th, td {
                border: 1px solid black;
                padding: 6px;
                text-align: left;
            }
            </style>
            """
    html = style + markdown.markdown(report, extensions=["tables"])

    pdfkit.from_string(html, "final_report.pdf", options={"encoding": "utf-8"})
    print("\n✅ 전략 보고서가 'final_report.pdf'에도 저장되었습니다.")
    return {"report": [AIMessage(content=report)]}

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
