class Corpus:
    def __init__(self, intent: str, utterances: list[str], answers: list[str], errors: dict[str, list[str]] = {}):
        self.intent: str = intent
        self.utterances: list[str] = utterances
        self.answers: list[str] = answers
        self.errors: list[str] = errors