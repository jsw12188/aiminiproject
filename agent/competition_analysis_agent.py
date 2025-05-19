from prompt_templates import COMPETITION_PROMPT

class CompetitionAnalysisAgent:
    def __init__(self, llm, search):
        self.llm = llm
        self.search = search

    def run(self, country):
        web_result = self.search.invoke(f"{country} AI 산업 주요 경쟁사, 시장 구조")
        web_data = "\n".join([r.get("snippet", "") for r in web_result])
        sources = [(r.get("title", ""), r.get("url", "")) for r in web_result]
        prompt = COMPETITION_PROMPT.format(country=country, web_data=web_data)
        out = self.llm.invoke(prompt)
        return {
            "summary": out.content,
            "sources": sources,
        }
