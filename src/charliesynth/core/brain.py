
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

    def answer_structured(self, question: str) -> dict:
        if not question or not question.strip():
            return {
                "status": "unknown",
                "answer": "Please ask me something.",
                "results": [],
            }

        result = self.evidence_engine.answer(question)

        return {
            "status": result["status"],
            "answer": result["answer"],
            "results": [
                {
                    "filename": source["filename"],
                    "page_number": source["page_number"],
                    "content": "\n".join(source["evidence"]),
                    "score": source["score"],
                }
                for source in result["sources"]
            ],
        }

    def answer(self, question: str) -> str:
        result = self.answer_structured(question)

        if not result["results"]:
            return result["answer"]

        output = [result["answer"]]

        for source in result["results"]:
            page = source["page_number"] or "Unknown"
            output.append(
                f"\nSource: {source['filename']} | Page: {page}"
            )
            output.append(source["content"])

        return "\n".join(output)
