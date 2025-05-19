from prompt_templates import PARTNER_PROMPT

class PartnerAnalysisAgent:
    def __init__(self, llm, search_tool):
        self.llm = llm
        self.search = search_tool

    def run(self, country):
        web_data = self.search.invoke(f"{country} AI 분야 파트너사, VC, 현지 협력 네트워크")
        prompt = PARTNER_PROMPT.format(country=country, web_data=web_data)
        return self.llm.invoke(prompt).content
