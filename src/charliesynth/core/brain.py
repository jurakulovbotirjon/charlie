class CharlieSynth:

    def __init__(self):
        self.name = "CharlieSynth"
        self.version = "0.1.0"
        self.knowledge_sources = 0

    def status(self):
        return {
            "name": self.name,
            "version": self.version,
            "knowledge_sources": self.knowledge_sources,
            "state": "NEWBORN",
        }

    def answer(self, question: str) -> str:

        if not question.strip():
            return "Please ask me something."

        return (
            "I don't know yet. My personal knowledge library "
            "has not been initialized with any information."
        )