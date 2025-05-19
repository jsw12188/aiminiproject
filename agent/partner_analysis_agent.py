from prompt_templates import PARTNER_PROMPT

class PartnerAnalysisAgent:
    def __init__(self, llm, search):
        self.llm = llm
        self.search = search

    def run(self, country):
        web_result = self.search.invoke(f"{country} AI 시장 주요 파트너/투자사/컨설팅사")
        web_data = "\n".join([r.get("snippet", "") for r in web_result])
        sources = [(r.get("title", ""), r.get("url", "")) for r in web_result]
        prompt = PARTNER_PROMPT.format(country=country, web_data=web_data)
        out = self.llm.invoke(prompt)
        return {
            "summary": out.content,
            "sources": sources,
        }
