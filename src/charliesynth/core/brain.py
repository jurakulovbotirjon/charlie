
from charliesynth.reasoning.evidence import EvidenceAnswerEngine


class CharlieSynth:
    def __init__(self):
        self.name = "CharlieSynth"
        self.version = "0.1.0"
        self.knowledge_sources = 0
        self.state = "LEARNING"
        self.evidence_engine = EvidenceAnswerEngine()

    def status(self):
        return {
            "name": self.name,
            "version": self.version,
            "state": self.state,
        }

    def answer(self, question: str) -> str:
        if not question or not question.strip():
            return "Please ask me something."

        result = self.evidence_engine.answer(question)

        if result["status"] == "unknown":
            return result["answer"]

        output = [result["answer"]]

        for source in result["sources"]:
            page = source["page_number"] or "Unknown"
            output.append(
                f"\nSource: {source['filename']} | Page: {page}"
            )

            for sentence in source["evidence"]:
                output.append(f"  - {sentence}")

        return "\n".join(output)
