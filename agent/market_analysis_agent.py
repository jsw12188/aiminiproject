from prompt_templates import MARKET_PESTEL_PROMPT

class MarketAnalysisAgent:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search = search_tool

    def run(self, country):
        web_data = self.search.invoke(f"{country} AI 산업 최신 동향 2024")
        prompt = MARKET_PESTEL_PROMPT.format(country=country, web_data=web_data)
        return self.llm.invoke(prompt).content
