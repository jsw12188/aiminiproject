from prompt_templates import COMPANY_SWOT_PROMPT

class CompanyAnalysisAgent:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search = search_tool

    def run(self, company):
        web_result = self.search.invoke(f"{company}의 강점과 약점 분석")
        web_data = "\n".join([r.get("snippet", "") for r in web_result])
        sources = [(r.get("title", ""), r.get("url", "")) for r in web_result]
        prompt = COMPANY_SWOT_PROMPT.format(company=company, web_data=web_data)
        out = self.llm.invoke(prompt)
        return {
            "summary": out.content,
            "sources": sources,
        }
