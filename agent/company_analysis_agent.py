from prompt_templates import COMPANY_SWOT_PROMPT

class CompanyAnalysisAgent:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search = search_tool

    def run(self, company):
        web_result = self.search.invoke(f"{company}의 투자자 관점 강점, 약점, 재무 위험, 시장 평가, 기술력, 브랜드 가치, 시장 적응성, 핵심 전략, 성장 전망")
        web_data = "\n".join([r.get("snippet", "") for r in web_result])
        sources = [(r.get("title", ""), r.get("url", "")) for r in web_result]
        prompt = COMPANY_SWOT_PROMPT.format(company=company, web_data=web_data)
        out = self.llm.invoke(prompt)
        return {
            "summary": out.content,
            "sources": sources,
        }
