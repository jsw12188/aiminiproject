from prompt_templates import MARKET_PESTEL_PROMPT

class MarketAnalysisAgent:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search = search_tool

    def run(self, country):
        web_result = self.search.invoke(f"{country} AI 산업 관련 정치, 경제, 사회, 기술, 법, 환경 이슈")
        web_data = "\n".join([r.get("snippet", "") for r in web_result])
        sources = [(r.get("title", ""), r.get("url", "")) for r in web_result]
        prompt = MARKET_PESTEL_PROMPT.format(country=country, web_data=web_data)
        out = self.llm.invoke(prompt)
        return {
            "summary": out.content,
            "sources": sources,   
        }
