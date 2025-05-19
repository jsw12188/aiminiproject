from prompt_templates import REPORT_WRITING_PROMPT

class ReportWritingAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, company, market, selection, competitors, partners):
        prompt = REPORT_WRITING_PROMPT.format(
            company=company,
            market=market,
            selection=selection,
            competitors=competitors,
            partners=partners
        )
        return self.llm.invoke(prompt).content