from charliesynth.core.brain import CharlieSynth


def test_charlie_initializes():
    charlie = CharlieSynth()

    assert charlie.name == "CharlieSynth"
    assert charlie.knowledge_sources == 0


def test_charlie_does_not_invent_knowledge():
    charlie = CharlieSynth()

    answer = charlie.answer("What is quantum physics?")

    assert "don't know" in answer.lower()


def test_empty_question():
    charlie = CharlieSynth()

    assert charlie.answer("") == "Please ask me something."