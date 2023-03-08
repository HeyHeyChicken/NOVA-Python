class ProcessorResult:
    def __init__(self, utterance: str):
        self.intent: str = None
        self.utterance: str = utterance
        self.variables: list[str] = []
        self.answers: list[str] = []
        self.answer: str = None