
import re

from charliesynth.memory.repository import MemoryRepository


STOP_WORDS = {
    "what", "when", "where", "which", "who", "whom", "whose",
    "why", "how", "does", "did", "was", "were", "are", "is",
    "the", "and", "for", "from", "with", "about", "that",
    "this", "these", "those", "have", "has", "had", "can",
    "could", "would", "should", "tell", "me", "explain"
}


class EvidenceAnswerEngine:
    def __init__(self):
        self.repository = MemoryRepository()

    def tokenize(self, text: str) -> set[str]:
        words = re.findall(r"[a-zA-Z0-9]+", text.lower())
        return {
            word for word in words
            if len(word) > 2 and word not in STOP_WORDS
        }

    def answer(self, question: str) -> dict:
        question_terms = self.tokenize(question)

        if not question_terms:
            return {
                "status": "unknown",
                "answer": "I don't have enough information to answer.",
                "sources": [],
            }

        results = self.repository.search_chunks(question, limit=5)
        evidence = []

        for result in results:
            content = result["content"]
            content_terms = self.tokenize(content)

            matched = question_terms.intersection(content_terms)
            score = len(matched) / len(question_terms)

            if score < 0.35:
                continue

            sentences = re.split(r"(?<=[.!?])\s+", content)

            relevant_sentences = [
                sentence.strip()
                for sentence in sentences
                if question_terms.intersection(
                    self.tokenize(sentence)
                )
            ]

            if relevant_sentences:
                evidence.append({
                    "filename": result["filename"],
                    "page_number": result["page_number"],
                    "evidence": relevant_sentences,
                    "score": round(score, 2),
                })

        if not evidence:
            return {
                "status": "unknown",
                "answer": "I don't know. I couldn't find sufficient supporting evidence in my memory.",
                "sources": [],
            }

        evidence.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return {
            "status": "supported",
            "answer": "I found the following supporting information:",
            "sources": evidence,
        }
