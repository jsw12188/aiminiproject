from prompt_templates import COMPETITION_PROMPT

class CompetitionAnalysisAgent:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search = search_tool

    def run(self, country):
        web_data = self.search.invoke(f"{country} AI 분야 주요 경쟁사 및 시장 점유율")
        prompt = COMPETITION_PROMPT.format(country=country, web_data=web_data)
        return self.llm.invoke(prompt).content