from prompt_templates import SUITABILITY_SCORING_PROMPT

class RegionSelectionAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, country, strengths, weaknesses, pestel_summary):
        prompt = SUITABILITY_SCORING_PROMPT.format(
            country=country,
            strengths=strengths,
            weaknesses=weaknesses,
            pestel=pestel_summary
        )
        return self.llm.invoke(prompt).content