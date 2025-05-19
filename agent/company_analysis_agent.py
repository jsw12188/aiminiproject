from prompt_templates import COMPANY_SWOT_PROMPT

class CompanyAnalysisAgent:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search = search_tool

    def run(self, company):
        web_data = self.search.invoke(f"{company} 회사 소개 및 AI 관련 사업")
        prompt = COMPANY_SWOT_PROMPT.format(company=company, web_data=web_data)
        return self.llm.invoke(prompt).content